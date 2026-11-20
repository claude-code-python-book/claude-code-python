"""The exception handlers, on a bare Starlette app (FastAPI uses the same hooks)."""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette.testclient import TestClient

from orders.domain import OrderStatus
from orders.errors import InvalidTransition, OrderNotFound
from orders.handlers import EXCEPTION_HANDLERS


def missing(request: Request) -> Response:
    raise OrderNotFound(42)


def shipped(request: Request) -> Response:
    raise InvalidTransition(7, OrderStatus.SHIPPED, OrderStatus.CANCELLED)


app = Starlette(
    routes=[
        Route("/orders/42", missing),
        Route("/orders/7/cancel", shipped, methods=["POST"]),
    ],
    exception_handlers=EXCEPTION_HANDLERS,
)
client = TestClient(app)


def test_order_not_found_is_a_404_problem() -> None:
    response = client.get("/orders/42")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json() == {
        "type": "about:blank",
        "title": "Order not found",
        "status": 404,
        "detail": "Order 42 does not exist.",
        "instance": "/orders/42",
    }


def test_invalid_transition_is_a_409_problem() -> None:
    response = client.post("/orders/7/cancel")
    assert response.status_code == 409
    assert (
        response.json()["detail"] == "Order 7 is shipped and cannot become cancelled."
    )
