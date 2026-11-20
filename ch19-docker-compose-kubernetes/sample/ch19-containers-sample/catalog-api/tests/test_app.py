import socket
from collections.abc import Iterator

import pytest
from starlette.testclient import TestClient

from catalog.app import app
from catalog.settings import host_port


@pytest.fixture
def free_port() -> Iterator[int]:
    """A local port with nothing listening on it."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    yield port


@pytest.fixture
def listener() -> Iterator[int]:
    """A local port with a listening socket, standing in for a database."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        s.listen()
        yield s.getsockname()[1]


def client(
    monkeypatch: pytest.MonkeyPatch, db_port: int, redis_port: int
) -> TestClient:
    monkeypatch.setenv(
        "DATABASE_URL", f"postgresql+psycopg://u@127.0.0.1:{db_port}/catalog"
    )
    monkeypatch.setenv("REDIS_URL", f"redis://127.0.0.1:{redis_port}/0")
    return TestClient(app)


def test_liveness_ignores_dependencies(
    monkeypatch: pytest.MonkeyPatch, free_port: int
) -> None:
    with client(monkeypatch, free_port, free_port) as c:
        assert c.get("/healthz").json() == {"status": "ok"}


def test_ready_when_dependencies_answer(
    monkeypatch: pytest.MonkeyPatch, listener: int
) -> None:
    with client(monkeypatch, listener, listener) as c:
        r = c.get("/readyz")
    assert r.status_code == 200
    assert r.json() == {"ready": True, "checks": {"database": True, "redis": True}}


def test_not_ready_when_database_is_down(
    monkeypatch: pytest.MonkeyPatch, listener: int, free_port: int
) -> None:
    with client(monkeypatch, free_port, listener) as c:
        r = c.get("/readyz")
    assert r.status_code == 503
    assert r.json()["checks"] == {"database": False, "redis": True}


def test_index_names_the_process(
    monkeypatch: pytest.MonkeyPatch, free_port: int
) -> None:
    with client(monkeypatch, free_port, free_port) as c:
        body = c.get("/").json()
    assert body["service"] == "catalog" and body["host"] == socket.gethostname()


@pytest.mark.parametrize(
    ("url", "default", "expected"),
    [
        ("postgresql+psycopg://u:p@db:5433/catalog", 5432, ("db", 5433)),
        ("redis://redis/0", 6379, ("redis", 6379)),
    ],
)
def test_host_port(url: str, default: int, expected: tuple[str, int]) -> None:
    assert host_port(url, default) == expected
