# invoicer

Invoice totals, tax and the monthly billing run for our billing service.
`invoicer` reads the CSV export from the billing system, validates every row,
adds tax by region, charges late fees on overdue invoices, and reports totals
per customer. Totals end up on legal documents, so money is always `Decimal`
and rounding is half-up, to the cent, once.

## Quick start

You need Python 3.11 or later and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/example/invoicer.git
cd invoicer
uv sync
uv run invoicer-billing docs/example-export.csv --today 2026-11-15
```

```text
Acme Ltd: billed 341.96, outstanding 350.06
Brandt GmbH: billed 610.47, outstanding 0
Grand total: 960.53
```

Rows that fail validation are listed on standard error, and the command then
exits with status 1. Run `uv run invoicer-billing --help` for the options.

## Use it from Python

```python
>>> from decimal import Decimal
>>> from invoicer import Line, total_with_tax
>>> lines = [Line("Widget", 3, Decimal("9.99"))]
>>> total_with_tax(lines, Decimal("0.20"))
Decimal('35.96')

```

The examples in this file are tested: `uv run pytest` runs them as doctests.

## Development

| Task | Command |
| --- | --- |
| Run the tests | `uv run pytest` |
| Lint and format | `uv run ruff check --fix .` and `uv run ruff format .` |
| Type-check | `uv run mypy src tests` and `uv run pyright` |
| Install the Git hooks | `pre-commit install` |

`CLAUDE.md` holds the project rules for Claude Code and for people; read it
before your first change.

## Documentation

- API reference: generated from the docstrings, see `docs/reference.md`.
- Decisions: `docs/adr/` records why the code is the way it is.
- Open question: whether a late fee at exactly day 60 is one period or two
  (ADR 0003).
