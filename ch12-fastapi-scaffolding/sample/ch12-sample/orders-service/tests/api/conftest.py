from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from orders.app import create_app
from orders.config import Settings
from orders.deps import get_current_user
from orders.users import User

SECRET = "test-secret-that-is-at-least-32-bytes-long"
ALICE = User("alice", "C-1001", hashed_password="not-used")


@pytest.fixture
def app() -> FastAPI:
    return create_app(Settings(environment="test", jwt_secret=SECRET))


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def as_alice(app: FastAPI, client: TestClient) -> Iterator[TestClient]:
    """A client whose requests run as Alice, without minting a token."""
    app.dependency_overrides[get_current_user] = lambda: ALICE
    yield client
    app.dependency_overrides.clear()
