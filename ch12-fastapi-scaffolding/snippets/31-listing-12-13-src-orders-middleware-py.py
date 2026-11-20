"""Request logging as pure ASGI middleware."""

import logging
import re
import time
import uuid

from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger("orders.requests")
SAFE_ID = re.compile(r"[A-Za-z0-9-]{1,64}")


class RequestLogMiddleware:
    """Give every request an id and log one line when it finishes."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Handle one ASGI connection."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        incoming = Headers(scope=scope).get("x-request-id", "")
        request_id = incoming if SAFE_ID.fullmatch(incoming) else uuid.uuid4().hex
        status = 500  # what the client gets if the app raises before responding
        start = time.perf_counter()

        async def send_with_id(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                MutableHeaders(scope=message).append("X-Request-ID", request_id)
            await send(message)

        try:
            await self.app(scope, receive, send_with_id)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info(
                "%s %s %d %.1fms id=%s",
                scope["method"],
                scope["path"],
                status,
                elapsed_ms,
                request_id,
            )
