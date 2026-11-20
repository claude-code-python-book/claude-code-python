# loyalty-service

Customer loyalty points for the shop: earning on orders, tiers, redemption
and expiry. Python 3.12+, SQLAlchemy 2.1 (async, asyncpg), Alembic 1.20,
PostgreSQL 16 or later.

## Commands

- Tests, no database: `uv run pytest tests --ignore=tests/db`
- Tests, with database: `docker compose up -d db && uv run pytest`
- Lint and types: `uv run ruff check . && uv run ruff format --check . && uv run mypy`
- New migration: `uv run alembic revision --autogenerate --rev-id NNNN -m "..."`
- Models and migrations agree: `uv run alembic check`
- Read a migration's SQL: `uv run alembic upgrade <prev>:<rev> --sql`
- Check a migration's safety: `uv run python tools/check_migrations.py <file>`

## Where things go

- Business rules: `loyalty/rules.py`, plain Python, no SQLAlchemy imports.
- Models: `loyalty/models.py`. Database work: `loyalty/service.py`.
- Engine and sessions: `loyalty/db.py`. Migrations: `migrations/versions/`.

## SQLAlchemy conventions

- 2.0 style only: `select()`, `session.scalars()`, `session.get()`. Never
  `session.query()`; it is the legacy API.
- Models use `Mapped[]` and `mapped_column()`. Nullability comes from the
  annotation: `Mapped[str | None]` is NULL, `Mapped[str]` is NOT NULL.
- Relationships are `lazy="raise"`. Load what you need in the query:
  `selectinload()` for collections, `joinedload()` for many-to-one.
- Service functions take an `AsyncSession` already in a transaction and
  never commit. Callers use `async with Session.begin() as session:`.
- One `AsyncSession` per request or task; never share one between tasks.
- Lock before read-modify-write on a balance: `locked_account()`.
- Money is `Decimal` and `Numeric(12, 2)`. Times are timezone-aware.
- No string-built SQL. Use bound parameters, even in `text()`.

## Migrations

- One migration per change, generated with `--autogenerate`, then read
  line by line: autogenerate sees a rename as a drop plus an add.
- Never edit a migration that has been merged; write a new one.
- Big tables: indexes `postgresql_concurrently=True` inside
  `autocommit_block()`; NOT NULL via a validated `CHECK ... NOT VALID`.
- Removing or renaming a column takes two releases: expand, then contract.
- Data migrations copy the values they need. Never import from `loyalty`.
- Every migration has a working `downgrade()`, or says why it can't.

## Testing

- Rules: plain pytest, `tests/test_rules.py`.
- Database tests in `tests/db/` run against PostgreSQL, each in a
  transaction that is rolled back. Never SQLite: the SQL differs.
- A new query that returns a list gets a test that counts its statements.

## Don't

- Don't run `alembic upgrade` or `downgrade` against anything but the local
  database; deploys run migrations.
- Don't read `.env`.
