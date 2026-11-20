---
description: Scaffold a FastAPI CRUD router with models and tests.
argument-hint: <resource> [field:type ...]
arguments: [resource]
disable-model-invocation: true
allowed-tools:
  - Bash(uv run pytest *)
  - Bash(uv run ruff *)
  - Bash(uv run mypy *)
---

Scaffold CRUD endpoints for the `$resource` resource.
Full request (resource, then field:type pairs): $ARGUMENTS

First read how this project builds its API: find the `FastAPI()` app
and any `APIRouter` modules, and copy their layout, naming and
dependency style. If FastAPI is not a dependency, stop and ask me.

Create:

1. Pydantic models: `<Resource>Create` for input, `<Resource>Update`
   with every field optional (for PATCH) and `<Resource>Read`, which
   adds `id`. Use `Decimal` for money and timezone-aware `datetime`.
2. An `APIRouter(prefix="/<resources>", tags=["<resources>"])` with
   `POST /` (201), `GET /` (list, with `limit` and `offset`),
   `GET /{id}`, `PATCH /{id}` and `DELETE /{id}` (204). Raise
   `HTTPException(status_code=404)` for an unknown id.
3. Storage behind a dependency (`Depends`) so tests can replace it.
   Reuse the project's repository or session dependency if one exists.
4. Register the router on the app with `include_router`.
5. Tests using `fastapi.testclient.TestClient`: one per endpoint and
   status code, including 404 for an unknown id and 422 for bad input.

Run the new tests, Ruff and mypy, then list the routes you added.
