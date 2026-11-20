"""Configuration from environment variables, the way containers pass it."""

import os
from dataclasses import dataclass
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Settings:
    database_url: str
    redis_url: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            database_url=os.environ.get(
                "DATABASE_URL", "postgresql+psycopg://catalog@localhost:5432/catalog"
            ),
            redis_url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        )


def host_port(url: str, default_port: int) -> tuple[str, int]:
    """Return the host and port of a URL such as postgresql://user@db:5432/x."""
    parts = urlsplit(url)
    return parts.hostname or "localhost", parts.port or default_port
