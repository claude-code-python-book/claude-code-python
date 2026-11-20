"""Application wiring: the only module that knows every adapter."""

from __future__ import annotations

from fastapi import FastAPI, Response, status
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from . import settings
from .api import router
from .repository import SqlUnitOfWork
from .service import ReviewService
from .tasks import CeleryQueue

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

app = FastAPI(title="bookshop")
app.state.review_service = ReviewService(lambda: SqlUnitOfWork(SessionLocal),
                                         CeleryQueue())
app.include_router(router)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz(response: Response) -> dict[str, str]:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:  # any database failure means "not ready"
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "database unavailable"}
    return {"status": "ok"}
