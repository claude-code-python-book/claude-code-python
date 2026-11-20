# Chapter 10 sample: code review, linting and type checking

`invoicer/` is the project after Chapter 10. Its history tells the chapter's story:

    git log --graph --oneline

- `Widen Ruff's rules, add pyright; fix what they found` (Sections 4-5)
- branch `reminders`: `Add payment reminders` is the pull request as submitted
  (Listing 10-1); `Address review findings in reminders` is the fix (Section 6)
- `Add a pre-commit quality gate` (Section 11)

See the bugs for yourself:

    git switch --detach $(git log --all --format=%h --grep="Add payment reminders")
    uv run ruff check src/invoicer/reminders.py
    uv run mypy src/invoicer/reminders.py
    uv run pyright src/invoicer/reminders.py
    git switch main

Setup: `cd invoicer && uv lock && uv sync && uv run pytest`, then
`uv tool install pre-commit` (4.4.0 or later) and `pre-commit install`.
