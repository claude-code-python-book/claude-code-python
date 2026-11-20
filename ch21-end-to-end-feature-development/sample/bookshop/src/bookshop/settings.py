"""Configuration from the environment; no secrets in code."""

import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://bookshop@localhost/bookshop")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
