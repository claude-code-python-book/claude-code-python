# bookshop

FastAPI API, SQLAlchemy 2 models with Alembic migrations, Celery worker.

## Commands

- Fast tests: `uv run pytest -q -m "not integration"`
- All tests (needs DATABASE_URL): `uv run pytest --cov`
- Lint and types: `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy`
- Security: `uv run --group security bandit -c pyproject.toml -r src`
- Image: `docker build -t bookshop:dev .`

## Architecture

- `ratings.py` holds the rules and does no I/O. `service.py` holds use cases and
  talks to storage and Celery only through the protocols it defines.
- `repository.py`, `api.py`, `tasks.py` and `main.py` are thin adapters. New
  logic goes in `ratings.py` or `service.py`, with unit tests that use
  `tests/fakes.py`, never a real database.

## Rules

- Money and averages use `Decimal`, rounded `ROUND_HALF_UP`, never `float`.
- Counters change with one atomic `UPDATE ... SET n = n + 1`, never read,
  modify, write in Python.
- Enqueue Celery tasks only after the transaction commits. Pass IDs, not objects.
- Validate input with Pydantic at the edge and again in the service; no `assert`
  for validation.
- Every migration has a working `downgrade()`.
- Never edit `.github/workflows/` or `Dockerfile` without saying so in the
  summary. Never push, merge or deploy yourself.
