# rowbatch

Small library and CLI that splits CSV rows into fixed-size batches.

## Commands

- Install: `uv sync`
- Lint: `uv run ruff check .` and `uv run ruff format --check .`
- Types: `uv run mypy` (checks against Python 3.12, the oldest we support)
- Tests: `uv run pytest`; on another Python: `uv run --python 3.12 pytest`

## Rules

- Supported Python: 3.12 and later (`requires-python`). Don't use standard
  library features added after 3.12 without a fallback.
- No runtime dependencies.

## CI

- `.github/workflows/ci.yml`: lint, then tests on 3.12-3.14 and three OSes.
- `.github/workflows/release.yml`: on a `vX.Y.Z` tag, build and publish to
  PyPI with trusted publishing. The tag must match `version` in
  pyproject.toml.
- To debug a failed run, use `/fix-ci <run-id>`. Never make CI pass by
  weakening it (skipping tests, removing matrix entries, continue-on-error).
