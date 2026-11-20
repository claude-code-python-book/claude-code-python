# tests

- `test_*.py`: the tests, mostly one file per module in `src/invoicer/`.
- `conftest.py`: shared fixtures. `make_row` builds a valid billing row and
  `rates_server` runs a local exchange-rate service; reuse them.
- `test_billing_characterization.py` compares the billing run with the files
  in `golden/`. When a change to the output is intended, regenerate them with
  `uv run python scripts/regen_golden.py` and explain the diff in the pull
  request. Never edit them by hand.
- `hooks/`: tests for the Claude Code hooks in `.claude/hooks/`.
- `data/`: input files. `billing_sample.csv` contains invalid rows on purpose.
