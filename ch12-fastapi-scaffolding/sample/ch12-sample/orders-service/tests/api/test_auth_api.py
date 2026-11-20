import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from orders.passwords import hash_password
from orders.users import User


@pytest.fixture
def alice(app: FastAPI) -> User:
    user = User("alice", "C-1001", hash_password("correct horse"))
    app.state.users.add(user)
    return user


def login(client: TestClient, password: str) -> tuple[int, dict[str, str]]:
    response = client.post(
        "/auth/token", data={"username": "alice", "password": password}
    )
    return response.status_code, response.json()


@pytest.mark.usefixtures("alice")
def test_a_token_from_login_opens_the_orders_api(client: TestClient) -> None:
    status, token = login(client, "correct horse")
    assert (status, token["token_type"]) == (200, "bearer")
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    assert client.get("/orders", headers=headers).status_code == 200


@pytest.mark.usefixtures("alice")
def test_a_wrong_password_is_a_401(client: TestClient) -> None:
    status, _ = login(client, "battery staple")
    assert status == 401


def test_a_missing_token_is_a_401(client: TestClient) -> None:
    assert client.get("/orders").status_code == 401


def test_a_garbage_token_is_a_401_with_a_challenge(client: TestClient) -> None:
    response = client.get("/orders", headers={"Authorization": "Bearer not-a-jwt"})
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
