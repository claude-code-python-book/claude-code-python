# salesreport

The sample project for Chapter 16 of *Claude Code for Python Developers*.
It turns a month of order exports into a short report:

```bash
uv sync
uv run python -m salesreport data/raw/orders-2026-10.csv --month 2026-10 --out out
uv run pytest -q
```

- `data/raw/` holds a generated, deliberately messy export
  (`scripts/make_fake_export.py`). Treat it as read-only.
- `data/sample/` holds a 1,000-row sample for notebooks.
- `extras/` shows the same steps with Polars, Pandera and Plotly; install
  them with `uv sync --group extras` to run `tests/extras`.
- `.gitattributes` expects the nbstripout filter: run
  `uv run --group notebooks nbstripout --install` once after cloning.
