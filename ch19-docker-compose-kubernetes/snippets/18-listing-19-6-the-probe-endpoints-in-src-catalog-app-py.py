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
