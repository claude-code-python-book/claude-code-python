# orders-service

The orders API for the shop: place, list, pay for and cancel orders.
FastAPI and Pydantic v2 on Python 3.12 or later. The sample project for
Chapter 12 of *Claude Code for Python Developers*.

## Run it

```bash
uv sync
export ORDERS_JWT_SECRET="$(openssl rand -hex 32)"
export ORDERS_DEMO_PASSWORD="change-me"   # creates the user "demo" (not in prod)
uv run fastapi dev
```

Open http://127.0.0.1:8000/docs, click **Authorize**, sign in as `demo`,
and try the endpoints.

## Work on it

| Task | Command |
| --- | --- |
| Tests | `uv run pytest -q` |
| Lint and format | `uv run ruff check --fix .` and `uv run ruff format .` |
| Types | `uv run mypy src tests` |
| Export the API contract | `uv run python scripts/export_openapi.py` |

Read `CLAUDE.md` before your first change.
