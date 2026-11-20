# bookshop

Sample project for Chapter 21 of *Claude Code for Python Developers*: one
feature (star ratings, `docs/features/ratings.md`) taken from code through
tests, review and a CI/CD pipeline.

```bash
uv sync --all-groups
uv run pytest -q -m "not integration"         # fast tests, no services
DATABASE_URL=postgresql+psycopg://... uv run pytest --cov   # with PostgreSQL
uv run ruff check . && uv run mypy
uv run --group security bandit -c pyproject.toml -r src
uv run alembic upgrade head
uv run fastapi dev                            # API on http://127.0.0.1:8000
uv run celery -A bookshop.tasks worker        # alert worker (needs Redis)
```

Claude Code setup: `CLAUDE.md`, `.claude/settings.json` (permissions and a
Stop hook that runs the fast tests), `.claude/agents/` (test-writer,
reviewer) and `.claude/skills/ship-feature/` (`/ship-feature docs/features/ratings.md`).

Run `uv lock` once before the first Docker build or CI run: the Dockerfile
and workflow use `uv sync --locked`, and this sample ships without a lock file.
