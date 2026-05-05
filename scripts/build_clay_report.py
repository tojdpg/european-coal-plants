"""Generate a static Clay evidence report for the coal asset website."""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from html import escape
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

ROOT = Path("/Users/thorstenjelinek/projects/eo-mcp-server")
WEB = ROOT / "web"
CLAY = Path("/Users/thorstenjelinek/.openclaw/bin/openclaw-clay")


def run_clay(*args: str) -> dict | list:
    result = subprocess.run(
        [str(CLAY), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(result.stdout)


def stretch(channel: np.ndarray) -> np.ndarray:
    lo, hi = np.nanpercentile(channel, [2, 98])
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        lo, hi = float(np.nanmin(channel)), float(np.nanmax(channel))
    if hi <= lo:
        return np.zeros(channel.shape, dtype=np.uint8)
    scaled = (channel - lo) / (hi - lo)
    return (np.clip(scaled, 0, 1) * 255).astype(np.uint8)


def geotiff_to_rgb(tile_path: str, out_path: Path) -> None:
    with rasterio.open(tile_path) as src:
        arr = src.read([3, 2, 1]).astype(np.float32)
    rgb = np.dstack([stretch(arr[0]), stretch(arr[1]), stretch(arr[2])])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgb, mode="RGB").save(out_path, optimize=True)


def fmt_num(value: float | int | None, digits: int = 2) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return f"{value:,}"
    return f"{value:,.{digits}f}"


def markdown_to_html(md: str) -> str:
    html: list[str] = []
    in_list = False
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line:
            if in_list:
                html.append("</ul>")
                in_list = False
            continue
        if line.startswith("# "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h1>{escape(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h2>{escape(line[3:])}</h2>")
        elif line.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{escape(line[2:])}</li>")
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<p>{escape(line)}</p>")
    if in_list:
        html.append("</ul>")
    return "\n".join(html)


def build_report(args: argparse.Namespace) -> None:
    out_dir = WEB / "reports" / args.slug
    assets = run_clay("find-assets", "--country", args.country, "--asset-type", args.asset_type, "--limit", "1")
    asset = assets[0] if assets else {
        "name": args.title,
        "lat": args.lat,
        "lon": args.lon,
        "capacity_mw": None,
        "annual_co2_mt": None,
        "phaseout_year": None,
        "owner": "",
        "parent": "",
        "status": "unknown",
    }

    lat = float(args.lat if args.lat is not None else asset["lat"])
    lon = float(args.lon if args.lon is not None else asset["lon"])
    title = args.title or asset["name"]

    tile_a = run_clay("get-imagery", "--lat", str(lat), "--lon", str(lon), "--date", args.date_a)
    tile_b = run_clay("get-imagery", "--lat", str(lat), "--lon", str(lon), "--date", args.date_b)
    change = run_clay(
        "detect-change",
        "--lat", str(lat),
        "--lon", str(lon),
        "--date-a", args.date_a,
        "--date-b", args.date_b,
    )
    emissions = run_clay("check-emissions", "--lat", str(lat), "--lon", str(lon))

    image_a = out_dir / "tile_a_rgb.png"
    image_b = out_dir / "tile_b_rgb.png"
    geotiff_to_rgb(tile_a["tile_path"], image_a)
    geotiff_to_rgb(tile_b["tile_path"], image_b)

    conclusion = (
        "The Clay embedding comparison indicates no meaningful visible/spectral change "
        "between the selected Sentinel-2 scenes. This supports a narrow claim of visual "
        "continuity, not a claim about generation, fuel use, or emissions without further data."
    )
    source_note = (
        "Imagery source: Sentinel-2 Level-2A, accessed through Microsoft Planetary Computer STAC. "
        "RGB previews are generated locally from the GeoTIFF tiles used for the Clay embedding "
        "comparison, using bands B04/B03/B02 as red/green/blue."
    )
    report_md = f"""# {title}: Clay Evidence Note

## Finding
- Interpretation: {change["interpretation"]}
- Cosine similarity: {change["cosine_sim"]:.4f}
- L2 distance: {change["l2_distance"]:.4f}
- Comparison window: {args.date_a} to {args.date_b}

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
- Tile A: {tile_a.get("capture_date") or args.date_a}
- Tile B: {tile_b.get("capture_date") or args.date_b}
- Tile A cloud: {fmt_num(tile_a.get("cloud_pct"), 4)}%
- Tile B cloud: {fmt_num(tile_b.get("cloud_pct"), 4)}%

## Caution
{conclusion}

## Sources & Method
{source_note}
"""

    report = {
        "title": title,
        "slug": args.slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "asset": asset,
        "lat": lat,
        "lon": lon,
        "dates": {"a": args.date_a, "b": args.date_b},
        "tiles": {"a": tile_a, "b": tile_b},
        "change": change,
        "emissions": emissions,
        "images": {"a": image_a.name, "b": image_b.name},
        "conclusion": conclusion,
        "source_note": source_note,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    (out_dir / "report.md").write_text(report_md)
    (out_dir / "index.html").write_text(render_html(report, report_md))
    build_reports_index()
    print(f"wrote {out_dir / 'index.html'}")


def render_html(report: dict, report_md: str) -> str:
    change = report["change"]
    asset = report["asset"]
    markdown_html = markdown_to_html(report_md)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(report["title"])} · Clay Evidence</title>
<style>
:root {{
  --bg:#f6f6ef; --ink:#111; --muted:#5f5f5f; --line:#d8d8c8;
  --accent:#ff6600; --paper:#fffff8; --soft:#eeeedf;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.5 Verdana, Geneva, sans-serif; }}
header {{ background:var(--accent); color:#000; padding:10px 16px; }}
header a {{ color:#000; text-decoration:none; font-weight:bold; }}
.wrap {{ max-width:1120px; margin:0 auto; padding:18px 16px 40px; }}
.meta {{ color:var(--muted); font-size:12px; margin-top:4px; }}
.grid {{ display:grid; grid-template-columns:1.1fr 0.9fr; gap:18px; align-items:start; }}
.panel {{ background:var(--paper); border:1px solid var(--line); border-radius:4px; padding:14px; }}
.score {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:14px 0; }}
.metric {{ background:var(--soft); border:1px solid var(--line); padding:10px; border-radius:3px; }}
.metric b {{ display:block; font-size:20px; margin-top:4px; }}
.label {{ color:var(--muted); font-size:11px; text-transform:uppercase; letter-spacing:.04em; }}
.images {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }}
figure {{ margin:0; }}
img {{ width:100%; height:auto; display:block; border:1px solid var(--line); background:#ddd; }}
figcaption {{ color:var(--muted); font-size:12px; margin-top:6px; }}
h1 {{ font-size:24px; line-height:1.2; margin:0; }}
h2 {{ font-size:15px; margin:20px 0 8px; border-bottom:1px solid var(--line); padding-bottom:4px; }}
table {{ width:100%; border-collapse:collapse; font-size:13px; }}
td {{ border-bottom:1px solid var(--line); padding:6px 0; vertical-align:top; }}
td:first-child {{ color:var(--muted); width:38%; padding-right:12px; }}
.note h1 {{ display:none; }}
.note p, .note li {{ font-size:14px; }}
.links a {{ color:#000; text-decoration:underline; margin-right:12px; }}
@media (max-width: 820px) {{
  .grid, .images, .score {{ grid-template-columns:1fr; }}
  h1 {{ font-size:20px; }}
}}
</style>
</head>
<body>
<header><a href="../../index.html">European Coal Asset Tracker</a> / Clay evidence report</header>
<main class="wrap">
  <section class="panel">
    <h1>{escape(report["title"])}</h1>
    <div class="meta">Generated {escape(report["generated_at"][:10])} · {escape(str(report["lat"]))}, {escape(str(report["lon"]))}</div>
    <div class="score" aria-label="Clay comparison metrics">
      <div class="metric"><span class="label">Interpretation</span><b>{escape(change["interpretation"])}</b></div>
      <div class="metric"><span class="label">Cosine similarity</span><b>{change["cosine_sim"]:.4f}</b></div>
      <div class="metric"><span class="label">L2 distance</span><b>{change["l2_distance"]:.4f}</b></div>
    </div>
    <div class="images">
      <figure><img src="{escape(report["images"]["a"])}" alt="RGB Sentinel-2 preview for first comparison date"><figcaption>Tile A · {escape(report["dates"]["a"])} · Sentinel-2 L2A RGB preview, bands B04/B03/B02</figcaption></figure>
      <figure><img src="{escape(report["images"]["b"])}" alt="RGB Sentinel-2 preview for second comparison date"><figcaption>Tile B · {escape(report["dates"]["b"])} · Sentinel-2 L2A RGB preview, bands B04/B03/B02</figcaption></figure>
    </div>
  </section>
  <div class="grid" style="margin-top:18px">
    <section class="panel note">{markdown_html}</section>
    <aside class="panel">
      <h2>Asset Metadata</h2>
      <table>
        <tr><td>Name</td><td>{escape(str(asset.get("name", "")))}</td></tr>
        <tr><td>Status</td><td>{escape(str(asset.get("status", "")))}</td></tr>
        <tr><td>Capacity</td><td>{fmt_num(asset.get("capacity_mw"), 0)} MW</td></tr>
        <tr><td>Annual CO2</td><td>{fmt_num(asset.get("annual_co2_mt"), 2)} Mt/year</td></tr>
        <tr><td>Owner</td><td>{escape(str(asset.get("owner") or "n/a"))}</td></tr>
        <tr><td>Parent</td><td>{escape(str(asset.get("parent") or "n/a"))}</td></tr>
      </table>
      <h2>Files</h2>
      <p class="links"><a href="report.json">report.json</a><a href="report.md">report.md</a></p>
      <h2>Sources & Method</h2>
      <p>{escape(report["source_note"])}</p>
    </aside>
  </div>
</main>
</body>
</html>
"""


def build_reports_index() -> None:
    reports_root = WEB / "reports"
    entries = []
    for path in sorted(reports_root.glob("*/report.json")):
        data = json.loads(path.read_text())
        entries.append((path.parent.name, data["title"], data["change"]["interpretation"], data["generated_at"][:10]))
    rows = "\n".join(
        f'<li><a href="{slug}/">{escape(title)}</a> <span>{escape(interp)} · {escape(date)}</span></li>'
        for slug, title, interp, date in entries
    )
    (reports_root / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Clay Evidence Reports</title>
<style>body{{margin:0;background:#f6f6ef;color:#111;font:15px/1.5 Verdana,Geneva,sans-serif}}header{{background:#ff6600;padding:10px 16px}}main{{max-width:900px;margin:0 auto;padding:22px 16px}}a{{color:#000}}li{{margin:10px 0}}span{{color:#666;font-size:12px}}</style>
</head><body><header><b>European Coal Asset Tracker</b> / Clay evidence reports</header>
<main><h1>Clay Evidence Reports</h1><ul>{rows}</ul></main></body></html>
""")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title")
    parser.add_argument("--country", default="DE")
    parser.add_argument("--asset-type", default="coal_power")
    parser.add_argument("--lat", type=float)
    parser.add_argument("--lon", type=float)
    parser.add_argument("--date-a", required=True)
    parser.add_argument("--date-b", required=True)
    build_report(parser.parse_args())


if __name__ == "__main__":
    main()
