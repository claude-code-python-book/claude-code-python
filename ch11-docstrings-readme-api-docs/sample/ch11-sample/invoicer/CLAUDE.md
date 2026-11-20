# invoicer

Invoice totals and tax for our billing service. Python 3.11+, src layout.
One runtime dependency: Pydantic, for validating input at the edges.
Totals end up on legal documents: correctness beats speed and cleverness.

<!-- Maintainers: keep this file under 80 lines. Review edits like code. -->

## Commands
- Setup: `uv sync` (installs the package in editable mode; tests need it)
- All tests: `uv run pytest -q`
- One test: `uv run pytest -q tests/test_tax.py::test_total_includes_tax`
- Fast loop: `uv run pytest -q -m "not slow"`
- Lint: `uv run ruff check --fix .` then `uv run ruff format .`
- Types: `uv run mypy src tests` (strict) and `uv run pyright`
- Billing run: `uv run invoicer-billing tests/data/billing_sample.csv --today 2026-11-15`
- Before you report a task as done, run tests, Ruff and mypy and show
  the output.

## Layout
- Code lives in `src/invoicer/`, tests in `tests/`. Tests import the
  installed package: on `ModuleNotFoundError: invoicer`, run `uv sync`.
  Never add `sys.path` hacks or a `pythonpath` setting.
- `tests/conftest.py` has the `make_line` factory fixture. Use it instead
  of building `Line` objects by hand.

## Conventions
- Money is `Decimal`, built from `str` or `int` with `invoicer.to_money`.
- Round once, at the end, with `quantize(CENT, rounding=ROUND_HALF_UP)`.
- No `Any` in public signatures. A `# type: ignore` needs an error code.
- Log with `logging.getLogger(__name__)`. No `print` in `src/`.
- Raise `ValueError` for bad input, with a message a user can read.

## Testing
- pytest functions and plain `assert`, not `unittest.TestCase` classes.
- A bug fix starts with a failing test that reproduces the bug.
- Use `@pytest.mark.parametrize` for input tables, not loops in a test.
- Mark tests slower than one second `@pytest.mark.slow`. Tests that need
  a database use `@pytest.mark.integration` and the `db_url` fixture.
- Markers are strict: register a new one in `pyproject.toml` first.
- Patch names where they are used (`invoicer.fx.urlopen`); never call the
  real rates service. Use the `rates_server` fixture or a stub.
- A known bug or open question is `xfail(strict=True)` with a reason.

## Don't
- Don't add runtime dependencies; ask first. Dev tools go in the `dev`
  group (`uv add --dev <tool>`).
- Don't edit `tests/golden/totals.json` by hand. Regenerate it with
  `uv run python scripts/regen_golden.py` and explain the diff.
- Don't change rounding or tax results in a refactor. That needs its own PR.

## Review
- Before a PR: Ruff, mypy, pyright and pytest green, then `/code-review`.
  Run `/security-review` for changes that touch SQL, files, HTTP or secrets.
- SQL takes values only through `?` placeholders. Secrets come from the
  environment. Never `pickle` data from outside the process.
- A `# noqa` or `# type: ignore` names its code and says why on the line above.

## Documentation
- Public modules, classes and functions get Google-style docstrings; Ruff's
  `D` rules check them. Say what a caller can't see in the signature.
- Change docstrings, `README.md` and `docs/` in the same commit as the code.
- A decision the code can't explain gets a record in `docs/adr/`.

## Gotchas
- `src/invoicer/legacy_export.py` looks unused, but the nightly finance
  job imports it. Keep its function signatures stable.
- Python's `round()` rounds half to even and floats are inexact:
  `round(2.675, 2)` is `2.67`. Never use `round()` or `float` for money.
- Integration tests skip unless `INVOICER_DB_URL` is set; see `.env.example`.
