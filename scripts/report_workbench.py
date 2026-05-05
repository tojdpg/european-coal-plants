#!/Users/thorstenjelinek/projects/.venv/bin/python
"""Stepwise, resumable Clay report workbench.

This script keeps large report jobs out of model context by writing every stage
to disk before moving to the next stage. Promotion into reports/<slug>/ is
blocked until verification passes.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from build_clay_report import build_reports_index, geotiff_to_rgb, render_html


SITE = Path(__file__).resolve().parents[1]
WORKBENCH = SITE / "workbench"
REPORTS = SITE / "reports"
CLAY = Path("/Users/thorstenjelinek/.openclaw/bin/openclaw-clay")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def step_path(slug: str, name: str) -> Path:
    return WORKBENCH / slug / name


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def write_state(slug: str, stage: str, ok: bool, message: str) -> None:
    write_json(step_path(slug, "state.json"), {
        "slug": slug,
        "stage": stage,
        "ok": ok,
        "message": message,
        "updated_at": now_iso(),
    })


def require_file(slug: str, filename: str) -> Path:
    path = step_path(slug, filename)
    if not path.exists():
        raise SystemExit(f"Missing {path}. Run the previous step first.")
    return path


def run_clay(*args: str) -> dict[str, Any] | list[Any]:
    result = subprocess.run(
        [str(CLAY), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(result.stdout)


def fmt_num(value: float | int | None, digits: int = 2) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return f"{value:,}"
    return f"{value:,.{digits}f}"


def intake(args: argparse.Namespace) -> None:
    if (args.lat is None) != (args.lon is None):
        raise SystemExit("Provide both --lat and --lon, or neither.")
    if args.lat is None and not args.title:
        raise SystemExit("Provide --title when coordinates are not supplied.")

    data = {
        "slug": args.slug,
        "title": args.title,
        "inquiry": args.inquiry,
        "country": args.country,
        "asset_type": args.asset_type,
        "lat": args.lat,
        "lon": args.lon,
        "date_a": args.date_a,
        "date_mid": args.date_mid,
        "date_b": args.date_b,
        "created_at": now_iso(),
        "notes": args.notes or "",
    }
    write_json(step_path(args.slug, "00-intake.json"), data)
    write_state(args.slug, "00-intake", True, "Intake saved.")
    print(step_path(args.slug, "00-intake.json"))


def imagery(args: argparse.Namespace) -> None:
    intake_data = read_json(require_file(args.slug, "00-intake.json"))
    lat, lon, asset = resolve_asset(intake_data)
    tiles = {
        "a": run_clay("get-imagery", "--lat", str(lat), "--lon", str(lon), "--date", intake_data["date_a"]),
        "b": run_clay("get-imagery", "--lat", str(lat), "--lon", str(lon), "--date", intake_data["date_b"]),
    }
    if intake_data.get("date_mid"):
        tiles["mid"] = run_clay("get-imagery", "--lat", str(lat), "--lon", str(lon), "--date", intake_data["date_mid"])

    write_json(step_path(args.slug, "01-imagery.json"), {
        "slug": args.slug,
        "generated_at": now_iso(),
        "lat": lat,
        "lon": lon,
        "asset": asset,
        "tiles": tiles,
    })
    write_state(args.slug, "01-imagery", True, "Imagery metadata saved.")
    print(step_path(args.slug, "01-imagery.json"))


def resolve_asset(intake_data: dict[str, Any]) -> tuple[float, float, dict[str, Any]]:
    if intake_data.get("lat") is not None and intake_data.get("lon") is not None:
        asset = {
            "name": intake_data.get("title"),
            "country": intake_data.get("country"),
            "lat": intake_data["lat"],
            "lon": intake_data["lon"],
            "capacity_mw": None,
            "annual_co2_mt": None,
            "phaseout_year": None,
            "owner": "",
            "parent": "",
            "status": "unknown",
        }
        return float(intake_data["lat"]), float(intake_data["lon"]), asset

    assets = run_clay(
        "find-assets",
        "--country", intake_data.get("country") or "DE",
        "--asset-type", intake_data.get("asset_type") or "coal_power",
        "--limit", "1",
    )
    if not assets:
        raise SystemExit("No asset returned by openclaw-clay find-assets.")
    asset = assets[0]
    return float(asset["lat"]), float(asset["lon"]), asset


def analyze(args: argparse.Namespace) -> None:
    intake_data = read_json(require_file(args.slug, "00-intake.json"))
    imagery_data = read_json(require_file(args.slug, "01-imagery.json"))
    lat = imagery_data["lat"]
    lon = imagery_data["lon"]
    change = run_clay(
        "detect-change",
        "--lat", str(lat),
        "--lon", str(lon),
        "--date-a", intake_data["date_a"],
        "--date-b", intake_data["date_b"],
    )
    change_mid_to_b = None
    if intake_data.get("date_mid"):
        change_mid_to_b = run_clay(
            "detect-change",
            "--lat", str(lat),
            "--lon", str(lon),
            "--date-a", intake_data["date_mid"],
            "--date-b", intake_data["date_b"],
        )
    emissions = run_clay("check-emissions", "--lat", str(lat), "--lon", str(lon))
    write_json(step_path(args.slug, "02-clay-results.json"), {
        "slug": args.slug,
        "generated_at": now_iso(),
        "change": change,
        "change_mid_to_b": change_mid_to_b,
        "emissions": emissions,
    })
    write_state(args.slug, "02-clay-results", True, "Clay results saved.")
    print(step_path(args.slug, "02-clay-results.json"))


def conclusion_for(change: dict[str, Any]) -> str:
    if float(change["cosine_sim"]) < 0.80:
        return (
            "The Clay embedding comparison indicates major visible/spectral change "
            "between the selected Sentinel-2 scenes. This supports a narrow claim "
            "of site-scale land-cover or structural transformation, not a claim "
            "about operations, output, employment, or financial status."
        )
    return (
        "The Clay embedding comparison indicates no meaningful visible/spectral "
        "change between the selected Sentinel-2 scenes. This supports a narrow "
        "claim of visual continuity, not a claim about operations, output, or "
        "emissions without further data."
    )


def draft(args: argparse.Namespace) -> None:
    intake_data = read_json(require_file(args.slug, "00-intake.json"))
    imagery_data = read_json(require_file(args.slug, "01-imagery.json"))
    results = read_json(require_file(args.slug, "02-clay-results.json"))
    asset = imagery_data["asset"]
    change = results["change"]
    tile_a = imagery_data["tiles"]["a"]
    tile_b = imagery_data["tiles"]["b"]
    change_mid = results.get("change_mid_to_b")
    title = intake_data.get("title") or asset.get("name") or args.slug
    inquiry = intake_data.get("inquiry") or (
        f"Did the area around {title} show meaningful visible or spectral change "
        f"between {intake_data['date_a']} and {intake_data['date_b']}?"
    )
    mid_line = ""
    if change_mid:
        mid_line = (
            f"- Recent stability: {intake_data['date_mid']} to {intake_data['date_b']}, "
            f"cosine {change_mid['cosine_sim']:.4f}, L2 {change_mid['l2_distance']:.4f}, "
            f"{change_mid['interpretation']}\n"
        )
    text = f"""# {title}: Clay Evidence Note

## Inquiry
{inquiry}

## Finding
- Interpretation: {change["interpretation"]}
- Cosine similarity: {change["cosine_sim"]:.4f}
- L2 distance: {change["l2_distance"]:.4f}
- Comparison window: {intake_data["date_a"]} to {intake_data["date_b"]}
{mid_line}
## Asset
- Name: {asset.get("name", title)}
- Country: {asset.get("country", "n/a")}
- Status: {asset.get("status", "n/a")}
- Capacity: {fmt_num(asset.get("capacity_mw"), 0)} MW
- Annual CO2 estimate: {fmt_num(asset.get("annual_co2_mt"), 2)} Mt/year
- Owner: {asset.get("owner") or "n/a"}
- Parent: {asset.get("parent") or "n/a"}

## Imagery
- Sensor: {tile_a.get("sensor", "sentinel-2-l2a")}
- Bands: {", ".join(tile_a.get("bands", []))}
- Tile A: {tile_a.get("capture_date") or intake_data["date_a"]}
- Tile B: {tile_b.get("capture_date") or intake_data["date_b"]}
- Tile A cloud: {fmt_num(tile_a.get("cloud_pct"), 4)}%
- Tile B cloud: {fmt_num(tile_b.get("cloud_pct"), 4)}%

## Caution
{conclusion_for(change)}

## Sources & Method
Imagery source: Sentinel-2 Level-2A, accessed through Microsoft Planetary Computer STAC. RGB previews are generated locally from the GeoTIFF tiles used for the Clay embedding comparison, using bands B04/B03/B02 as red/green/blue.
"""
    path = step_path(args.slug, "03-report.draft.md")
    path.write_text(text)
    write_state(args.slug, "03-report-draft", True, "Draft report saved.")
    print(path)


def build(args: argparse.Namespace) -> None:
    intake_data = read_json(require_file(args.slug, "00-intake.json"))
    imagery_data = read_json(require_file(args.slug, "01-imagery.json"))
    results = read_json(require_file(args.slug, "02-clay-results.json"))
    draft_text = require_file(args.slug, "03-report.draft.md").read_text()
    final_dir = step_path(args.slug, "final")
    final_dir.mkdir(parents=True, exist_ok=True)

    image_a = final_dir / "tile_a_rgb.png"
    image_b = final_dir / "tile_b_rgb.png"
    geotiff_to_rgb(imagery_data["tiles"]["a"]["tile_path"], image_a)
    geotiff_to_rgb(imagery_data["tiles"]["b"]["tile_path"], image_b)

    asset = imagery_data["asset"]
    title = intake_data.get("title") or asset.get("name") or args.slug
    inquiry = intake_data.get("inquiry") or (
        f"Did the area around {title} show meaningful visible or spectral change "
        f"between {intake_data['date_a']} and {intake_data['date_b']}?"
    )
    report = {
        "title": title,
        "inquiry": inquiry,
        "slug": args.slug,
        "generated_at": now_iso(),
        "asset": asset,
        "lat": imagery_data["lat"],
        "lon": imagery_data["lon"],
        "dates": {"a": intake_data["date_a"], "b": intake_data["date_b"]},
        "tiles": {"a": imagery_data["tiles"]["a"], "b": imagery_data["tiles"]["b"]},
        "change": results["change"],
        "change_mid_to_b": results.get("change_mid_to_b"),
        "emissions": results.get("emissions"),
        "images": {"a": image_a.name, "b": image_b.name},
        "conclusion": conclusion_for(results["change"]),
        "source_note": (
            "Imagery source: Sentinel-2 Level-2A, accessed through Microsoft Planetary "
            "Computer STAC. RGB previews are generated locally from the GeoTIFF tiles "
            "used for the Clay embedding comparison, using bands B04/B03/B02 as "
            "red/green/blue."
        ),
    }
    (final_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    (final_dir / "report.md").write_text(draft_text)
    (final_dir / "index.html").write_text(render_html(report, draft_text))
    write_json(step_path(args.slug, "04-page-build.json"), {
        "slug": args.slug,
        "generated_at": now_iso(),
        "final_dir": str(final_dir),
        "files": sorted(path.name for path in final_dir.iterdir() if path.is_file()),
    })
    write_state(args.slug, "04-page-build", True, "Final report page built in workbench.")
    print(final_dir)


def verify(args: argparse.Namespace) -> bool:
    final_dir = step_path(args.slug, "final")
    required_steps = [
        "00-intake.json",
        "01-imagery.json",
        "02-clay-results.json",
        "03-report.draft.md",
        "04-page-build.json",
    ]
    required_final = ["index.html", "report.md", "report.json", "tile_a_rgb.png", "tile_b_rgb.png"]
    missing = [name for name in required_steps if not step_path(args.slug, name).exists()]
    missing.extend(f"final/{name}" for name in required_final if not (final_dir / name).exists())
    report_ok = False
    report_title = None
    if (final_dir / "report.json").exists():
        try:
            report = read_json(final_dir / "report.json")
            report_title = report.get("title")
            report_ok = all(key in report for key in ["title", "inquiry", "change", "images", "tiles"])
        except json.JSONDecodeError:
            report_ok = False
    if not report_ok:
        missing.append("valid final/report.json")

    ok = not missing
    result = {
        "slug": args.slug,
        "generated_at": now_iso(),
        "ok": ok,
        "report_title": report_title,
        "missing": missing,
        "final_dir": str(final_dir),
    }
    write_json(step_path(args.slug, "05-verify.json"), result)
    write_state(args.slug, "05-verify", ok, "Verification passed." if ok else "Verification failed.")
    print(step_path(args.slug, "05-verify.json"))
    if missing:
        print("Missing or invalid:")
        for item in missing:
            print(f"- {item}")
    return ok


def promote(args: argparse.Namespace) -> None:
    verify_data = read_json(require_file(args.slug, "05-verify.json"))
    if not verify_data.get("ok"):
        raise SystemExit("Verification has not passed. Run verify and fix missing files first.")
    if args.confirm != "yes":
        raise SystemExit('Promotion requires --confirm yes.')

    final_dir = step_path(args.slug, "final")
    report_dir = REPORTS / args.slug
    report_dir.mkdir(parents=True, exist_ok=True)
    for source in final_dir.iterdir():
        if source.is_file():
            shutil.copy2(source, report_dir / source.name)
    build_reports_index()
    write_json(step_path(args.slug, "06-promote.json"), {
        "slug": args.slug,
        "generated_at": now_iso(),
        "report_dir": str(report_dir),
        "files": sorted(path.name for path in report_dir.iterdir() if path.is_file()),
    })
    write_state(args.slug, "06-promote", True, "Verified report promoted to public reports folder.")
    print(report_dir)


def status(args: argparse.Namespace) -> None:
    if args.slug:
        slugs = [args.slug]
    else:
        slugs = sorted(path.name for path in WORKBENCH.glob("*") if path.is_dir()) if WORKBENCH.exists() else []
    if not slugs:
        print("No report workbenches found.")
        return
    for slug in slugs:
        root = WORKBENCH / slug
        state_path = root / "state.json"
        state = read_json(state_path) if state_path.exists() else {}
        steps = sorted(path.name for path in root.iterdir() if path.is_file() or path.is_dir())
        print(f"{slug}: {state.get('stage', 'unknown')} - {state.get('message', 'no state')}")
        print("  " + ", ".join(steps))


def run_all(args: argparse.Namespace) -> None:
    imagery(args)
    analyze(args)
    draft(args)
    build(args)
    ok = verify(args)
    if not ok:
        raise SystemExit("Pipeline stopped: verification failed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Saved-step Clay report workbench")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Create 00-intake.json")
    p.add_argument("--slug", required=True)
    p.add_argument("--title")
    p.add_argument("--inquiry")
    p.add_argument("--country", default="DE")
    p.add_argument("--asset-type", default="coal_power")
    p.add_argument("--lat", type=float)
    p.add_argument("--lon", type=float)
    p.add_argument("--date-a", required=True)
    p.add_argument("--date-mid")
    p.add_argument("--date-b", required=True)
    p.add_argument("--notes")
    p.set_defaults(func=intake)

    for name, func, help_text in [
        ("imagery", imagery, "Create 01-imagery.json"),
        ("analyze", analyze, "Create 02-clay-results.json"),
        ("draft", draft, "Create 03-report.draft.md"),
        ("build", build, "Create final report files under workbench"),
        ("verify", verify, "Create 05-verify.json"),
        ("all", run_all, "Run imagery, analyze, draft, build, verify"),
    ]:
        step = sub.add_parser(name, help=help_text)
        step.add_argument("--slug", required=True)
        step.set_defaults(func=func)

    p = sub.add_parser("promote", help="Copy verified final files into reports/<slug>/")
    p.add_argument("--slug", required=True)
    p.add_argument("--confirm", required=True)
    p.set_defaults(func=promote)

    p = sub.add_parser("status", help="Show saved workbench state")
    p.add_argument("--slug")
    p.set_defaults(func=status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
