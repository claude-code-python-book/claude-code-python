from collections.abc import Iterator
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from billing_api.app import app, get_fetch_rates

PARAMS = {"amount": "10.30", "base": "GBP", "target": "EUR"}


def fake_fetch_rates(base: str) -> dict[str, Decimal]:
    return {"EUR": Decimal("1.15")}


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides[get_fetch_rates] = lambda: fake_fetch_rates
    yield TestClient(app)
    app.dependency_overrides = {}


def test_convert_returns_the_rounded_amount(client: TestClient) -> None:
    response = client.get("/convert", params=PARAMS)
    assert response.status_code == 200
    assert response.json() == {"amount": "11.85", "currency": "EUR"}


def test_convert_unknown_currency_is_404(client: TestClient) -> None:
    response = client.get("/convert", params={**PARAMS, "target": "JPY"})
    assert response.status_code == 404
    assert response.json() == {"detail": "no rate from GBP to JPY"}


def test_convert_rejects_a_non_numeric_amount(client: TestClient) -> None:
    response = client.get("/convert", params={**PARAMS, "amount": "ten"})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_convert_over_asgi() -> None:
    app.dependency_overrides[get_fetch_rates] = lambda: fake_fetch_rates
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/convert", params=PARAMS)
    app.dependency_overrides = {}
    assert response.json()["amount"] == "11.85"
