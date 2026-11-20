## pandas style

- pandas 3: no `inplace=True`, no chained assignment, no `.values`
  (use `.to_numpy()`). Functions return new frames and never mutate input.
- Vectorize. No `iterrows()` or `apply(axis=1)` for arithmetic.

## Notebooks

- Notebooks explore; `src/salesreport/` decides. When a cell grows into
  logic, move it to a function with a test and import it in the notebook.
- Before committing, clear outputs:
  `uv run --group notebooks jupyter nbconvert --clear-output --inplace notebooks/*.ipynb`
- A notebook must run top to bottom in a fresh kernel:
  `uv run --group notebooks jupyter nbconvert --to notebook --execute --output-dir tmp notebooks/*.ipynb`
