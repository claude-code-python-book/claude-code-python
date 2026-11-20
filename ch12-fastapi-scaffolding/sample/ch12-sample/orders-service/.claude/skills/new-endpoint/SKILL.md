---
description: Scaffold a new resource in orders-service, following its conventions.
argument-hint: <resource> [field:type ...]
arguments: [resource]
disable-model-invocation: true
allowed-tools:
  - Bash(uv run pytest *)
  - Bash(uv run ruff *)
  - Bash(uv run mypy *)
  - Bash(uv run python scripts/export_openapi.py)
---

Scaffold the `$resource` resource. Full request: $ARGUMENTS

Read CLAUDE.md first. The orders feature is the template: copy the shape
of `schemas.py`, `domain.py`, `repository.py`, `service.py`, `errors.py`,
`api/orders.py` and their tests. Don't introduce a new pattern; if the
request needs one, stop and ask me.

1. Schemas: `<Resource>Create` with `extra="forbid"`, and
   `<Resource>Read` with `from_attributes=True`.
2. A domain dataclass, a repository `Protocol` and an in-memory
   implementation with a lock.
3. A service class with no FastAPI imports. Errors subclass a base error
   in `errors.py` and get a handler in `EXCEPTION_HANDLERS`.
4. `api/<resources>.py`: `APIRouter(prefix="/<resources>",
   tags=["<resources>"])`, dependencies from `deps.py`, and a summary,
   return type and `responses` on every operation. Include the router in
   `create_app`, and add the tag to `TAGS`.
5. Tests: service tests without HTTP, and API tests in `tests/api/` with
   one test per status code.

Then run the tests, Ruff and mypy, run `scripts/export_openapi.py`, and
show me the new routes and `git diff --stat openapi.json`.
