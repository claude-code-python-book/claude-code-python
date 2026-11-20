"""Serve the shop-db MCP server inside an existing FastAPI app.

Run it with:  uv run uvicorn fastapi_app:app --host 127.0.0.1 --port 8000
"""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from pg_server import mcp

mcp_app = mcp.streamable_http_app(streamable_http_path="/")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with mcp.session_manager.run():   # FastAPI must start it
        yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

app.mount("/mcp", mcp_app)               # MCP endpoint: /mcp
