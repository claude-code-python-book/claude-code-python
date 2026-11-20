uv run pytest -q tests/test_tax.py::test_total_includes_tax
uv run pytest -q -m "not slow" -rs
