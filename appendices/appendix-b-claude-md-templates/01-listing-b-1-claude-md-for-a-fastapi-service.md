# <service-name>

<What the API does, in one line.> FastAPI, Pydantic v2, Python 3.12+,
src layout. <Who uses it and the main actions, in one line.>

<!-- Maintainers: keep this file under 80 lines. Review edits like code. -->

## Commands
- Setup: `uv sync`
- Run: `uv run fastapi dev` (the entrypoint is in `[tool.fastapi]`)
- Tests: `uv run pytest -q`
- Lint: `uv run ruff check --fix .` then `uv run ruff format .`
- Types: `uv run mypy src tests`
- Contract: `uv run python scripts/export_openapi.py`, then review the
  `openapi.json` diff and commit it with the change.
- Before you report a task as done, run tests, Ruff and mypy and show
  the output.

## Layout: api -> service -> repository, never the other way
- `api/<resource>.py`: one `APIRouter` per resource. Thin: take the
  request, call the service, return `<Resource>Read.model_validate(...)`.
- `schemas.py`: `<Resource>Create` (input) and `<Resource>Read` (output).
- `service.py`: business rules. Never imports `fastapi`.
- `repository.py`: storage behind a `Protocol`.
- `errors.py` and `handlers.py`: service errors and their HTTP mapping.
- `deps.py`: every dependency, as an `Annotated` alias.
- `config.py`: `Settings`. Read configuration only from there.

## API conventions
- Create returns 201 with a `Location` header. List endpoints take
  `limit` (1 to 100, default 20) and `offset`.
- The current user comes from the token, never from the request body
  or query.
- The service raises `<Project>Error` subclasses, never `HTTPException`.
  Map each new error in the exception handlers. Error bodies are
  RFC 9457 problem details.
- Request models set `extra="forbid"`. Money is `Decimal`, never float.
- Every path operation has a `summary`, a return type, and `responses`
  for each error status it can return.

## Testing
- Service and schema tests use no HTTP. API tests live in `tests/api/`,
  use `TestClient`, and override the current-user dependency instead of
  minting tokens (except the auth tests).
- One test for each status code an endpoint can return.

## Don't
- Don't use `@app.middleware("http")`; write pure ASGI middleware.
- Don't read `os.environ`; add a field to `Settings`.
- Don't change `openapi.json` by hand.
