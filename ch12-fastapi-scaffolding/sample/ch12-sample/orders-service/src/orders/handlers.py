"""Turn service errors into RFC 9457 problem details responses."""

from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from orders.errors import InvalidTransition, OrderNotFound
from orders.schemas import Problem

PROBLEM_JSON = "application/problem+json"


def problem(request: Request, status: int, title: str, detail: str) -> JSONResponse:
    """Build a problem details response for the current request."""
    body = Problem(title=title, status=status, detail=detail, instance=request.url.path)
    return JSONResponse(body.model_dump(), status_code=status, media_type=PROBLEM_JSON)


async def order_not_found(request: Request, exc: Exception) -> Response:
    """Map OrderNotFound to 404 Not Found."""
    return problem(request, 404, "Order not found", str(exc))


async def invalid_transition(request: Request, exc: Exception) -> Response:
    """Map InvalidTransition to 409 Conflict."""
    return problem(request, 409, "Order status conflict", str(exc))


Handler = Callable[[Request, Exception], Awaitable[Response]]

EXCEPTION_HANDLERS: dict[type[Exception], Handler] = {
    OrderNotFound: order_not_found,
    InvalidTransition: invalid_transition,
}
