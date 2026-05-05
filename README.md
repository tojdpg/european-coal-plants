# european-coal-plants
Interactive map of European coal plants — climate transition risk

## Project Boundary

This repository is only for the European coal asset tracker and related Clay evidence reports.

Clay-generated public reports belong under:

```text
reports/<slug>/
```

Do not mix unrelated OpenClaw, personal, research-workbench, Framer, Tally, Calendly, or other project content into this repository. Use this repo as the evidence/publication layer for coal asset analysis only.

## Saved Report Workbench

Use `scripts/report_workbench.py` for report generation when the task is too large for one LLM pass.

The workbench stores every stage locally under:

```text
workbench/<slug>/
  00-intake.json
  01-imagery.json
  02-clay-results.json
  03-report.draft.md
  04-page-build.json
  05-verify.json
  final/
```

Only after `verify` passes should a report be promoted into:

```text
reports/<slug>/
```

Example:

```bash
./scripts/report_workbench.py init --slug janschwalde-refresh --title "Janschwalde Power Station" --lat 51.835666 --lon 14.457808 --date-a 2024-06 --date-b 2026-05
./scripts/report_workbench.py all --slug janschwalde-refresh
./scripts/report_workbench.py promote --slug janschwalde-refresh --confirm yes
```

Do not claim a report is finished until `05-verify.json` says `"ok": true`, the report index has been rebuilt, and the published page has been checked.
