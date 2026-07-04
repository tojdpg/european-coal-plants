#!/usr/bin/env python3
"""Guard the stable Berlin Fusion report shell.

This check is intentionally narrow. It protects only
reports/berlin-fusion/index.html from being replaced by an older generated
artifact while still allowing Paul or another content agent to update the
values, embedded images, and interpretation text.
"""

from __future__ import annotations

import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "berlin-fusion" / "index.html"
PREVIEW = ROOT / "reports" / "berlin-fusion" / "berlin-deep-weather-preview.jpg"


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._heading_tag: str | None = None
        self._heading_text: list[str] = []
        self.headings: list[str] = []
        self._in_figure = False
        self.figure_images = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"h1", "h2"}:
            self._heading_tag = tag
            self._heading_text = []
        if tag == "figure":
            self._in_figure = True
        if tag == "img" and self._in_figure:
            self.figure_images += 1

    def handle_data(self, data: str) -> None:
        if self._heading_tag:
            self._heading_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._heading_tag == tag:
            heading = " ".join("".join(self._heading_text).split())
            self.headings.append(heading)
            self._heading_tag = None
            self._heading_text = []
        if tag == "figure":
            self._in_figure = False


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def appears_in_order(items: list[str], required: list[str]) -> bool:
    pos = -1
    for item in required:
        try:
            pos = items.index(item, pos + 1)
        except ValueError:
            return False
    return True


def raster_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return None
    if data.startswith(b"\x89PNG\r\n\x1a\n") and data[12:16] == b"IHDR":
        return struct.unpack(">II", data[16:24])
    if data.startswith(b"\xff\xd8"):
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            i += 2
            if marker in {0xD8, 0xD9}:
                continue
            length = int.from_bytes(data[i : i + 2], "big")
            if marker in range(0xC0, 0xC4):
                height = int.from_bytes(data[i + 3 : i + 5], "big")
                width = int.from_bytes(data[i + 5 : i + 7], "big")
                return (width, height)
            i += length
    return None


def main() -> int:
    html = REPORT.read_text(encoding="utf-8")
    parser = ReportParser()
    parser.feed(html)

    errors: list[str] = []
    required_order = [
        "Berlin Deep Weather",
        "Clay / NDVI Context",
        "Interpretation",
        "Spectral Evidence",
        "Nearest GFS Weather",
        "Pollution Context",
        "How To Read The Numbers",
        "Caveats",
    ]

    require(
        "BERLIN_FUSION_SHELL_CONTRACT" in html,
        "Missing Berlin Fusion shell contract comment.",
        errors,
    )
    require(
        "Wetter, Luftqualität und Satellitenbild-Evidence für Berlin Mitte / Tiergarten." in html,
        "Missing intuitive social preview description.",
        errors,
    )
    require(
        appears_in_order(parser.headings, required_order),
        "Required Berlin Fusion heading order changed.",
        errors,
    )
    require(
        parser.figure_images >= 4,
        f"Expected at least 4 figure images, found {parser.figure_images}.",
        errors,
    )
    require("Evidence Hub" in html, "Missing Evidence Hub link.", errors)
    require("<title>Berlin Deep Weather</title>" in html, "Missing short Berlin Deep Weather title.", errors)
    require(
        'property="og:image" content="https://tojdpg.github.io/european-coal-plants/reports/berlin-fusion/berlin-deep-weather-preview.jpg"' in html
        and 'property="og:image:type" content="image/jpeg"' in html
        and 'name="twitter:card" content="summary_large_image"' in html,
        "Missing social sharing preview metadata.",
        errors,
    )
    require(
        raster_size(PREVIEW) == (1200, 630),
        "Social preview image must exist and be 1200 x 630.",
        errors,
    )
    require('id="lightbox"' in html, "Missing click-to-enlarge lightbox.", errors)
    require(
        "PAUL_INTERPRETATION_START" in html and "PAUL_INTERPRETATION_END" in html,
        "Missing Paul interpretation edit markers.",
        errors,
    )
    require(
        "Draft interpretation" not in html,
        "Interpretation must not be labelled as draft.",
        errors,
    )
    require(
        re.search(
            r"Pollution:</strong>.*?"
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\s*/\s*"
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}",
            html,
            re.S,
        )
        is not None,
        "Top context must include pollution UTC and local valid times.",
        errors,
    )
    require(
        "NDVI uses near-infrared and red light" in html
        and "ranges from -1 to 1" in html
        and "NDVI above 0.3" in html,
        "NDVI explanation is missing or unclear.",
        errors,
    )
    require(
        "BERLIN_FUSION_EXPLAINER_LOCK_START" in html
        and "BERLIN_FUSION_EXPLAINER_LOCK_END" in html,
        "Missing protected reader explainer markers.",
        errors,
    )
    explainer_match = re.search(
        r"BERLIN_FUSION_EXPLAINER_LOCK_START(?P<body>.*?)BERLIN_FUSION_EXPLAINER_LOCK_END",
        html,
        re.S,
    )
    explainer_body = explainer_match.group("body") if explainer_match else ""
    require(
        "How To Read The Numbers" in html
        and "Benchmarks here are orientation bands" in html
        and "O3 100-130" in html
        and "NDVI benchmark" in html
        and ("NDWI benchmark" in html or "not available" in explainer_body)
        and "p05 / p95 / valid pixels" in html
        and "Source / kind / timestamp" in html
        and "Weather / Earth2Studio GFS" in html,
        "Reader explainer definitions or benchmarks are missing.",
        errors,
    )
    require(
        "Here " not in explainer_body and "sits in" not in explainer_body,
        "Protected reader explainer should be value-neutral, not tied to refreshed table values.",
        errors,
    )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Berlin Fusion shell guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
