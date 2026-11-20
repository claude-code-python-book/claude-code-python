"""The async engine and the session factory."""

import os

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def make_engine(url: str | None = None) -> AsyncEngine:
    """Create the app's engine, e.g. for postgresql+asyncpg://user:pw@host/db."""
    return create_async_engine(url or os.environ["DATABASE_URL"], pool_pre_ping=True)


def make_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Return a session factory.

    expire_on_commit=False keeps loaded attributes readable after commit;
    under asyncio a reload would be implicit I/O, which isn't allowed.
    """
    return async_sessionmaker(engine, expire_on_commit=False)
