# bookfinder

Starlette API over SQLite: `src/bookfinder/`. Tests in `tests/`.

## Commands

- Tests: `uv run pytest -q`
- Lint, security lint, types: `uv run ruff check . && uv run mypy`
- Bandit: `uv run --group security bandit -c pyproject.toml -r src`
- Dependency audit: `uv run --group security pip-audit` (needs network)

## Security rules

- SQL: user input only through `?` placeholders. Identifiers such as sort
  columns come from an allowlist dict. Escape `%` and `_` for LIKE.
- Never `pickle`, `marshal`, `eval`, `exec` or `yaml.load` on data from outside
  the process. Use `json` or `yaml.safe_load`.
- `subprocess`: an argument list, never `shell=True`, always a `timeout`.
- Outbound HTTP to user-supplied URLs goes through `covers.check_url`:
  https only, host allowlist, public IPs only, no redirects, a timeout.
- Jinja2 environments use `select_autoescape()`. Never build templates from
  user input.
- A `# noqa: S...` needs a reason on the same line and a test that shows why
  the finding is safe.

## Security fixes

- Write a failing test that reproduces the exploit before changing code.
- Fix the class of bug, not the one payload. Don't filter "bad" characters.
- Don't add or upgrade dependencies without asking.
