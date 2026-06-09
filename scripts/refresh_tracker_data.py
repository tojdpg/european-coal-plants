#!/usr/bin/env python3
"""Refresh the European coal tracker data from GEM's public map GeoJSON.

The tracker displays plant-level rows, while GEM's Global Coal Plant Tracker
map data is unit-level. This script keeps the transformation reproducible.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ACTIVE_STATUSES = {"operating", "mothballed", "construction"}

COUNTRY_ISO2 = {
    "Bosnia and Herzegovina": "BA",
    "Bulgaria": "BG",
    "Croatia": "HR",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Finland": "FI",
    "France": "FR",
    "Germany": "DE",
    "Greece": "GR",
    "Hungary": "HU",
    "Italy": "IT",
    "Kosovo": "XK",
    "Moldova": "MD",
    "Montenegro": "ME",
    "Netherlands": "NL",
    "North Macedonia": "MK",
    "Poland": "PL",
    "Romania": "RO",
    "Serbia": "RS",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Spain": "ES",
    "Türkiye": "TR",
    "Ukraine": "UA",
}

INCLUDED_COUNTRIES = set(COUNTRY_ISO2)
EXCLUDED_COUNTRIES = {"Russia"}

SPAIN_OVERRIDES = {
    "Alcúdia power station": {
        "capacity_mw": 240.0,
        "status": "hibernating",
        "annual_co2_mt": None,
        "phaseout_year": 2026,
        "status_note": (
            "Spain 2026 update: only coal groups 3 and 4 remain open as "
            "security-reserve capacity; local reporting says Endesa is preparing "
            "final closure in 2026 subject to government authorization."
        ),
        "source_url": (
            "https://www.ultimahora.es/noticias/local/2025/12/07/2526783/"
            "endesa-ultima-cierre-central-murterar-alcudia-para-2026.html"
        ),
    },
    "Soto de Ribera power station": {
        "display_name": "Soto de Ribera 3 power station",
        "capacity_mw": 341.0,
        "status": "hibernating",
        "annual_co2_mt": None,
        "phaseout_year": None,
        "status_note": (
            "Spain 2026 update: kept available for security-of-supply / local "
            "grid-constraint reasons, with intermittent or minimal coal operation "
            "while the conversion-to-gas pathway is being assessed."
        ),
        "source_url": (
            "https://www.infolibre.es/medioambiente/espana-despide-medias-carbon-"
            "mantendra-seguridad-plantas-hibernacion-2026_1_2122158.html"
        ),
    },
}


def as_float(value: Any) -> float | None:
    if value in (None, "", "<NA>"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value: Any) -> int | None:
    number = as_float(value)
    if number is None:
        return None
    return int(number)


def country_from_areas(areas: str) -> str:
    return areas.strip().strip(";")


def eo_browser_url(lat: float, lon: float) -> str:
    return (
        "https://apps.sentinel-hub.com/eo-browser/"
        f"?zoom=14&lat={lat:.5f}&lng={lon:.5f}&themeId=DEFAULT-THEME&datasetId=S2L2A"
    )


def plant_status(statuses: Counter[str]) -> str:
    if statuses.get("operating"):
        return "operating"
    if statuses.get("construction"):
        return "construction"
    return "mothballed"


def first_present(values: list[Any]) -> Any:
    for value in values:
        if value not in (None, "", "<NA>"):
            return value
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gem-geojson", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--release",
        default="GEM Global Coal Plant Tracker map data 2026-02-02 / January 2026 release",
    )
    parser.add_argument("--generated-at", default=date.today().isoformat())
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = json.loads(args.gem_geojson.read_text())
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    for feature in source["features"]:
        props = feature["properties"]
        country = country_from_areas(props.get("areas", ""))
        status = props.get("status")
        if country in EXCLUDED_COUNTRIES or country not in INCLUDED_COUNTRIES:
            continue
        if status not in ACTIVE_STATUSES:
            continue
        grouped[(country, props["name"])].append(props)

    plants: list[dict[str, Any]] = []
    for (country, name), units in grouped.items():
        statuses = Counter(unit["status"] for unit in units)
        capacities = [as_float(unit.get("capacity-table")) or 0.0 for unit in units]
        annual_co2 = [as_float(unit.get("annual-co2-(million-tonnes-/-annum)")) or 0.0 for unit in units]
        lifetime_co2 = [as_float(unit.get("lifetime-co2-(million-tonnes)")) or 0.0 for unit in units]
        start_years = [as_int(unit.get("start-year")) for unit in units]
        phaseout_years = [as_int(unit.get("coal-phaseout-year")) for unit in units]
        lats = [as_float(unit.get("latitude")) for unit in units]
        lons = [as_float(unit.get("longitude")) for unit in units]
        lat = first_present(lats)
        lon = first_present(lons)
        if lat is None or lon is None:
            continue

        gem_url = first_present([unit.get("url") or unit.get("wiki-from-name") for unit in units])
        record = {
            "name": name,
            "country": country,
            "iso2": COUNTRY_ISO2[country],
            "lat": lat,
            "lon": lon,
            "capacity_mw": round(sum(capacities), 1),
            "status": plant_status(statuses),
            "annual_co2_mt": round(sum(annual_co2), 3),
            "lifetime_co2_mt": round(sum(lifetime_co2), 3),
            "owner": first_present([unit.get("owner") for unit in units]),
            "parent": first_present([unit.get("parent") for unit in units]),
            "earliest_start": min([year for year in start_years if year], default=None),
            "phaseout_year": max([year for year in phaseout_years if year], default=None),
            "n_units": len(units),
            "subnational": first_present([unit.get("subnat") for unit in units]),
            "source_dataset": "Global Coal Plant Tracker",
            "source_release": args.release,
            "source_statuses": dict(sorted(statuses.items())),
            "source_unit_ids": [unit.get("id") for unit in units if unit.get("id")],
            "source_unit_names": [
                unit.get("unit-name") for unit in units if unit.get("unit-name") not in (None, "", "<NA>")
            ],
            "gem_url": gem_url,
            "source_url": gem_url,
            "eo_browser": eo_browser_url(lat, lon),
        }

        if country == "Spain" and name in SPAIN_OVERRIDES:
            override = SPAIN_OVERRIDES[name]
            if override.get("display_name"):
                record["source_name"] = record["name"]
                record["name"] = override["display_name"]
            for key, value in override.items():
                if key != "display_name":
                    record[key] = value

        plants.append(record)

    plants.sort(key=lambda item: (item["country"], item["name"]))
    total_capacity = round(sum(plant["capacity_mw"] or 0 for plant in plants))
    total_co2 = round(sum(plant["annual_co2_mt"] or 0 for plant in plants), 1)
    total_lifetime = round(sum(plant["lifetime_co2_mt"] or 0 for plant in plants), 1)
    countries = sorted({plant["iso2"] for plant in plants})
    statuses = sorted({plant["status"] for plant in plants})

    output = {
        "totals": {
            "n_plants": len(plants),
            "total_capacity_mw": total_capacity,
            "total_annual_co2_mt": total_co2,
            "total_lifetime_co2_mt": total_lifetime,
            "countries": countries,
            "statuses": statuses,
            "data_source": args.release,
            "source_url": (
                "https://publicgemdata.nyc3.cdn.digitaloceanspaces.com/"
                "coal-plant/2026-02/coal-plant_map_2026-02-02.geojson"
            ),
            "scope_note": (
                "GEM active coal units in Europe plus Türkiye, excluding Russia; "
                "Spain has reviewed hibernating/security-reserve overrides."
            ),
            "generated_at": args.generated_at,
        },
        "plants": plants,
    }
    args.output.write_text(json.dumps(output, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
