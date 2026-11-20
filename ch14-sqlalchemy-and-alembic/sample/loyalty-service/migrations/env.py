"""Alembic environment.

The app talks to PostgreSQL through asyncpg. Migrations are a one-off
command, so they use psycopg, a synchronous driver, and Alembic's generic
environment. Each migration runs in its own transaction, and every
connection gives up waiting for a lock after five seconds.
"""

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from loyalty.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
# A literal % must be doubled for Alembic's config parser.
url = os.environ["MIGRATIONS_DATABASE_URL"]  # postgresql+psycopg://...
config.set_main_option("sqlalchemy.url", url.replace("%", "%%"))
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Print the SQL instead of running it: alembic upgrade head --sql."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        transaction_per_migration=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run the migrations against the database."""
    engine = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={"options": "-c lock_timeout=5s"},
    )
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transaction_per_migration=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
