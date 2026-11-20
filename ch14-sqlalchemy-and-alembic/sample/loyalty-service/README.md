# loyalty-service

Sample project for Chapter 14 of *Claude Code for Python Developers*:
customer loyalty points with SQLAlchemy 2.1 (async, asyncpg), Alembic 1.20
and PostgreSQL.

```bash
uv sync
uv run pytest tests --ignore=tests/db        # rules, migration checker, hook
docker compose up -d db
cp .env.example .env && export $(cat .env)   # or set the two URLs yourself
uv run alembic upgrade head
uv run pytest                                 # everything, against PostgreSQL
```

Migrations: `migrations/versions/0001` to `0005`. 0002 to 0005 add the `tier`
column with expand, migrate and contract steps. `tools/check_migrations.py`
flags risky operations; `.claude/hooks/check_migration.py` runs it on every
migration Claude Code writes.
