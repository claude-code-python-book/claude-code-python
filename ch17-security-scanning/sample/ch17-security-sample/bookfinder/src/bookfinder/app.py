"""HTTP API: GET /search returns JSON, GET /search.html returns a page."""

import os
from contextlib import closing

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route

from bookfinder.db import connect
from bookfinder.render import render_results
from bookfinder.search import search_books

DB_PATH = os.environ.get("BOOKFINDER_DB", ":memory:")


def _params(request: Request) -> tuple[str, str]:
    return request.query_params.get("q", ""), request.query_params.get("sort", "title")


async def search(request: Request) -> JSONResponse:
    """Search books; a bad ``sort`` value is a 400, not a 500."""
    query, sort = _params(request)
    try:
        with closing(connect(DB_PATH)) as conn:
            books = search_books(conn, query, sort)
    except ValueError as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    return JSONResponse({"query": query, "results": books})


async def search_page(request: Request) -> HTMLResponse:
    """Render the same search as HTML."""
    query, sort = _params(request)
    try:
        with closing(connect(DB_PATH)) as conn:
            books = search_books(conn, query, sort)
    except ValueError as error:
        return HTMLResponse(str(error), status_code=400)
    return HTMLResponse(render_results(query, books))


app = Starlette(routes=[Route("/search", search), Route("/search.html", search_page)])
