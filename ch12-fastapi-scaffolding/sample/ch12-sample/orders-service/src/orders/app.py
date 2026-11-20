"""Build the FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from orders.api import auth, orders
from orders.config import Settings
from orders.handlers import EXCEPTION_HANDLERS
from orders.middleware import RequestLogMiddleware
from orders.passwords import hash_password
from orders.repository import InMemoryOrderRepository
from orders.users import InMemoryUserRepository, User

TAGS = [
    {"name": "orders", "description": "Place, list, pay for and cancel orders."},
    {"name": "auth", "description": "Get an access token."},
    {"name": "ops", "description": "Health checks for the platform."},
]


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the app. Tests pass settings; otherwise they come from the env."""
    settings = settings or Settings()  # reads the ORDERS_* variables
    app = FastAPI(
        title="Orders API",
        summary="Place and track orders for the shop.",
        version="1.0.0",
        openapi_tags=TAGS,
    )
    app.state.settings = settings
    app.state.orders = InMemoryOrderRepository()
    app.state.users = InMemoryUserRepository()
    if settings.demo_password is not None:
        hashed = hash_password(settings.demo_password.get_secret_value())
        app.state.users.add(User("demo", "C-0001", hashed))

    for exc_type, handler in EXCEPTION_HANDLERS.items():
        app.add_exception_handler(exc_type, handler)
    app.include_router(auth.router)
    app.include_router(orders.router)

    @app.get("/health", tags=["ops"], summary="Liveness check")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
        expose_headers=["Location", "X-Request-ID"],
    )
    app.add_middleware(RequestLogMiddleware)  # added last, so it runs first
    return app
