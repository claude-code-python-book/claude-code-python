## Data rules

- `data/raw/` is read-only evidence. Never edit, move, re-save or "fix" a raw
  file. Write results to `out/` or `tmp/`. `tests/test_raw_data.py` checks
  every raw file against `data/raw/MANIFEST.sha256`.
- Explore on `data/sample/orders-sample.csv` (1,000 rows). Don't print or
  paste more than 20 rows of any file into the conversation.
- Read CSVs with `salesreport.load.read_orders` (all columns as text). Parse
  types in `validate.py`, never with `read_csv` guessing.
- Dates: the East region's old till writes DD-MM-YYYY. Never parse dates
  with `format="mixed"` or `dayfirst`; convert known formats explicitly.
- Money is integer cents (`unit_price_cents`). No floats for money.
- Every rejected row goes to `rejected.csv` with a reason. Never drop rows
  silently, and never use `errors="coerce"` without counting what it lost.
