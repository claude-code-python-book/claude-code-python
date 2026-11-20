---
description: Add logging to a module (stdlib logging or structlog).
argument-hint: <module.py>
disable-model-invocation: true
allowed-tools: Bash(uv run pytest *)
---

Add logging to $ARGUMENTS.

1. Check `pyproject.toml`. If `structlog` is a dependency, use
   `log = structlog.get_logger()`. Otherwise use the standard library:
   `logger = logging.getLogger(__name__)` at module level.
2. Never configure logging in library code: no `basicConfig()`, no
   handlers or levels outside the application's entry point.
3. Log at boundaries and decisions, not inside tight loops:
   - DEBUG: detail that helps when debugging this module.
   - INFO: one line per business event ("invoice totalled").
   - WARNING: a recoverable surprise, such as a fallback being used.
   - ERROR: `logger.exception(...)` in an `except` block that handles
     the error. Don't log an exception you re-raise.
4. Pass values as arguments, not f-strings:
   `logger.info("Totalled invoice %s: %s", invoice_id, total)`, or with
   structlog `log.info("invoice_totalled", invoice_id=..., total=...)`.
5. Never log secrets, tokens, card numbers or personal data. Log IDs.
6. Replace `print()` calls used for diagnostics.
7. Run the tests: adding logging must not change behaviour.
