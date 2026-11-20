# bookfinder

Sample project for Chapter 17 of *Claude Code for Python Developers*:
a Starlette search API whose first version had a SQL injection bug.

```bash
uv sync
uv run pytest -q
uv run ruff check .
```

`tests/test_search.py` keeps the injection payloads that worked against the
first version. `.github/workflows/security.yml` runs Ruff, Bandit, pip-audit
and gitleaks; `.github/dependabot.yml` keeps `uv.lock` current.
