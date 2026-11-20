# rowbatch

Split CSV rows into fixed-size batches for bulk inserts.

```console
$ rowbatch orders.csv --size 500
12034 rows in 25 batches of up to 500
```

```python
from rowbatch import batch_rows, read_rows

for batch in batch_rows(read_rows(path), 500):
    insert_many(batch)
```

## Development

```console
$ uv lock          # once, then commit uv.lock
$ uv sync
$ uv run ruff check . && uv run ruff format --check . && uv run mypy
$ uv run pytest
```

CI runs the same commands (`.github/workflows/ci.yml`). Releases are published to
PyPI by `.github/workflows/release.yml` when a `vX.Y.Z` tag is pushed.
