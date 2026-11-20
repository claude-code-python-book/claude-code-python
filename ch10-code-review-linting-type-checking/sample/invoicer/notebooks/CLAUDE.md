# Notebooks

Exploration notebooks for the finance team. Nothing in `src/` imports them.

- Start Jupyter with `uv run --group notebooks jupyter lab`.
- Work on `notebooks/data/sample.csv` (1,000 rows). Never open, copy or
  summarize files in `notebooks/data/raw/`: they hold customer data.
- Import logic from `invoicer`. When a cell grows into a function, move it
  to `src/invoicer/` with a test instead of copying it between notebooks.
- Clear outputs before committing:
  `uv run --group notebooks jupyter nbconvert --clear-output --inplace notebooks/*.ipynb`
