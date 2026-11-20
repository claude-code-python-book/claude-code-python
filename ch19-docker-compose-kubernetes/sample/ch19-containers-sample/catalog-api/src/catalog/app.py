"""The catalog web service: one real endpoint and the probes containers need."""

import asyncio
import logging
import os
import socket
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from catalog.settings import Settings, host_port

log = logging.getLogger("uvicorn.error")


CHECK_TIMEOUT = 1.0  # seconds; keep below the readiness probe's timeoutSeconds


async def reachable(host: str, port: int) -> bool:
    """True if a TCP connection to host:port succeeds within CHECK_TIMEOUT."""
    try:
        async with asyncio.timeout(CHECK_TIMEOUT):
            _, writer = await asyncio.open_connection(host, port)
    except (OSError, TimeoutError):
        return False
    writer.close()
    await writer.wait_closed()
    return True


async def index(request: Request) -> JSONResponse:
    host, pid = socket.gethostname(), os.getpid()
    return JSONResponse({"service": "catalog", "host": host, "pid": pid})


async def healthz(request: Request) -> JSONResponse:
    """Liveness: the process can answer. Never check dependencies here."""
    return JSONResponse({"status": "ok"})


async def readyz(request: Request) -> JSONResponse:
    """Readiness: only send traffic here if the database and Redis answer."""
    settings: Settings = request.app.state.settings
    database, redis = await asyncio.gather(
        reachable(*host_port(settings.database_url, 5432)),
        reachable(*host_port(settings.redis_url, 6379)),
    )
    checks = {"database": database, "redis": redis}
    status = 200 if all(checks.values()) else 503
    return JSONResponse({"ready": status == 200, "checks": checks}, status_code=status)


async def slow(request: Request) -> JSONResponse:
    """A deliberately slow request, used to watch graceful shutdown."""
    seconds = min(float(request.query_params.get("seconds", "3")), 30.0)
    await asyncio.sleep(seconds)
    return JSONResponse({"slept": seconds})


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    app.state.settings = Settings.from_env()
    log.info("catalog starting in pid %s", os.getpid())
    yield
    log.info("catalog stopped cleanly in pid %s", os.getpid())


app = Starlette(
    routes=[
        Route("/", index),
        Route("/healthz", healthz),
        Route("/readyz", readyz),
        Route("/slow", slow),
    ],
    lifespan=lifespan,
)
