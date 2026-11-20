"""Fixtures for tests that need PostgreSQL.

The schema comes from `alembic upgrade head`, so every run also tests the
migrations. Each test runs in a transaction that is rolled back afterwards.
"""

import os
import subprocess
import sys
from collections.abc import AsyncIterator, Iterator

import pytest
from sqlalchemy import Engine, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

APP_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://loyalty:loyalty@localhost:5432/loyalty_test",
)
MIGRATIONS_URL = APP_URL.replace("+asyncpg", "+psycopg")


def alembic(*args: str) -> subprocess.CompletedProcess[str]:
    """Run an Alembic command against the test database."""
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        env={**os.environ, "MIGRATIONS_DATABASE_URL": MIGRATIONS_URL},
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.fixture(scope="session", autouse=True)
def migrated() -> Iterator[None]:
    """Build the schema once per test run, from the migrations."""
    alembic("downgrade", "base")
    alembic("upgrade", "head")
    yield


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    """Yield a session whose work is rolled back after the test."""
    engine = create_async_engine(APP_URL, poolclass=NullPool)
    async with engine.connect() as connection:
        transaction = await connection.begin()
        async with AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False,
        ) as session:
            yield session
        await transaction.rollback()
    await engine.dispose()


class StatementCounter:
    """Count the SQL statements a block of code sends."""

    def __init__(self) -> None:
        self.statements: list[str] = []

    def __call__(self, *args: object) -> None:
        self.statements.append(str(args[2]))  # (conn, cursor, statement, ...)


@pytest.fixture
def count_statements() -> Iterator[StatementCounter]:
    """Record every statement any engine executes during the test."""
    counter = StatementCounter()
    event.listen(Engine, "before_cursor_execute", counter)
    yield counter
    event.remove(Engine, "before_cursor_execute", counter)
