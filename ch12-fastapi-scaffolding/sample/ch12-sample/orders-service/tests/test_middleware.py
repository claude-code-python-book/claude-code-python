"""Request logging and CORS, on a bare Starlette app with the same middleware."""

import logging

import pytest
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.testclient import TestClient

from orders.middleware import RequestLogMiddleware

SHOP = "https://shop.example.com"
PREFLIGHT = {"Origin": SHOP, "Access-Control-Request-Method": "POST"}


def ok(request: Request) -> Response:
    return JSONResponse({"ok": True})


def boom(request: Request) -> Response:
    raise RuntimeError("bug")


def build(log_outermost: bool = True) -> Starlette:
    app = Starlette(
        routes=[Route("/orders", ok, methods=["GET", "POST"]), Route("/boom", boom)]
    )
    if log_outermost:  # the order create_app uses
        app.add_middleware(CORSMiddleware, allow_origins=[SHOP], allow_methods=["POST"])
        app.add_middleware(RequestLogMiddleware)
    else:
        app.add_middleware(RequestLogMiddleware)
        app.add_middleware(CORSMiddleware, allow_origins=[SHOP], allow_methods=["POST"])
    return app


def test_every_response_gets_a_request_id() -> None:
    response = TestClient(build()).get("/orders")
    assert len(response.headers["x-request-id"]) == 32


@pytest.mark.parametrize(
    ("sent", "kept"), [("abc-123", True), ("bad\r\nid", False), ("x" * 65, False)]
)
def test_only_safe_incoming_ids_are_reused(sent: str, kept: bool) -> None:
    response = TestClient(build()).get("/orders", headers={"X-Request-ID": sent})
    assert (response.headers["x-request-id"] == sent) is kept


def test_a_crash_is_logged_as_500(caplog: pytest.LogCaptureFixture) -> None:
    client = TestClient(build(), raise_server_exceptions=False)
    with caplog.at_level(logging.INFO, logger="orders.requests"):
        assert client.get("/boom").status_code == 500
    assert caplog.messages[-1].startswith("GET /boom 500 ")


def test_preflight_requests_are_logged_when_logging_is_outermost() -> None:
    response = TestClient(build()).options("/orders", headers=PREFLIGHT)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == SHOP
    assert "x-request-id" in response.headers


def test_cors_answers_preflights_itself_when_added_last() -> None:
    response = TestClient(build(log_outermost=False)).options(
        "/orders", headers=PREFLIGHT
    )
    assert response.status_code == 200
    assert "x-request-id" not in response.headers
