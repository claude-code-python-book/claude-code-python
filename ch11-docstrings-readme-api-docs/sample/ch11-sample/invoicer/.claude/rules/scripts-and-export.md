---
paths:
  - "src/invoicer/legacy_export.py"
  - "scripts/**/*.py"
---

# Scripts and the legacy export

- The nightly finance job calls `export_csv_row(line)` and splits on commas.
  Adding, removing or reordering fields breaks it.
- Scripts must run with `uv run python scripts/<name>.py` from the repo root
  and must not need network access.
