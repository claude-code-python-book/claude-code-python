# Chapter 9 sample: pytest and test coverage

- `invoicer/`: the project after Chapter 9. `git log` shows one commit per
  step of the chapter (late-fee tests, fixtures and fx, parametrize,
  boundaries, async and Hypothesis tests, gap tests, CI).
- `examples/billing_api/`: the FastAPI example (Section 6).
- `examples/billing_portal/`: the Django + pytest-django example (Section 7).
- `hand_mutants.py`: the 13 hand-made mutants behind Table 9-4. Run it as
  `python hand_mutants.py invoicer invoicer/.venv/bin/python` from this folder.

Setup:

    cd invoicer
    uv lock          # creates uv.lock; commit it, CI uses `uv sync --locked`
    uv sync
    uv run pytest

The test tools added in this chapter (pytest-cov, pytest-mock,
pytest-asyncio, Hypothesis) are in the `dev` dependency group.
The day-60 late-fee case is an intentional strict xfail (Section 10).
