# <project-name>

<What it builds, from which data, in one line:>
`data/raw/*.csv` -> `out/<report>`, `rejected.csv`.

## Commands
- Tests: `uv run pytest -q`
- Lint and types: `uv run ruff check . && uv run mypy src tests`
- Run: `uv run python -m <package> <input> --out out`
- Notebooks: `uv run --group notebooks jupyter lab`

## Data rules
- `data/raw/` is read-only evidence. Never edit, move, re-save or "fix" a
  raw file. Write results to `out/` or `tmp/`. A test checks every raw
  file against `data/raw/MANIFEST.sha256`.
- Explore on `data/sample/<sample>.csv`. Don't print or paste more than
  20 rows of any file into the conversation.
- Read CSVs with all columns as text. Parse types in `validate.py`,
  never with `read_csv` guessing.
- Dates: convert each known format explicitly. Never parse dates with
  `format="mixed"` or `dayfirst`.
- Money is integer cents. No floats for money.
- Every rejected row goes to `rejected.csv` with a reason. Never drop rows
  silently, and never use `errors="coerce"` without counting what it lost.

## pandas style
- pandas 3: no `inplace=True`, no chained assignment, no `.values`
  (use `.to_numpy()`). Functions return new frames and never mutate input.
- Vectorize. No `iterrows()` or `apply(axis=1)` for arithmetic.

## Notebooks
- Notebooks explore; `src/<package>/` decides. When a cell grows into
  logic, move it to a function with a test and import it in the notebook.
- Before committing, clear outputs:
  `uv run --group notebooks jupyter nbconvert --clear-output --inplace notebooks/*.ipynb`
- A notebook must run top to bottom in a fresh kernel:
  `uv run --group notebooks jupyter nbconvert --to notebook --execute --output-dir tmp notebooks/*.ipynb`
