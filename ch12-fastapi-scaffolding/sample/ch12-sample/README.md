# Chapter 12 sample: orders-service

A FastAPI orders API, with full git history:
  149b07e  Scaffold the orders domain: schemas, service and repository
  3a8b0ef  Add the HTTP layer: routers, dependencies, errors, auth, middleware
  2b13fb4  Add team conventions: CLAUDE.md, /new-endpoint, OpenAPI export, README

    cd orders-service
    uv sync
    uv run pytest -q          # 46 tests, including tests/api
    uv run ruff check .
    uv run mypy src tests
    uv run python scripts/export_openapi.py

Tests outside tests/api (34) were run while writing the chapter. The 12 tests
in tests/api need FastAPI 0.163, pydantic-settings and pwdlib; run them after
`uv sync`.
