---
description: Review Python code for security problems. Read-only.
argument-hint: [path; default is the whole project]
disable-model-invocation: true
allowed-tools: Bash(uv run ruff check *)
---

Do a security review of: $ARGUMENTS
(If no path is given, review the whole project except `tests/`.)

Do not edit any file. Start with Ruff's `S` rules, its re-implementation
of the Bandit checks, as a quick scan:

    uv run ruff check --select S --no-fix --output-format concise <path>

Then read the code yourself; a scanner misses context. Look for:

- Injection: SQL built with f-strings, `%` or `+` instead of query
  parameters; `subprocess` with `shell=True` or untrusted arguments;
  `eval` and `exec`; file paths built from user input (traversal).
- Unsafe deserialization of untrusted data: `pickle`, `marshal`,
  `shelve`, `yaml.unsafe_load` or `yaml.load` with a non-safe loader.
- Secrets: hard-coded keys, tokens and passwords; secrets that reach
  logs, exceptions or error responses.
- Randomness and crypto: `random` for tokens (use `secrets`), MD5 or
  SHA-1 for passwords (use a password hash such as Argon2 or bcrypt).
- HTTP: `verify=False`, missing timeouts on outgoing requests, missing
  authorization checks on endpoints, CORS `*` with credentials.

Report a table with columns Severity, Location (`file:line`), Issue and
Fix, most severe first. Then remind me to audit dependencies with
`uvx pip-audit`, which this review does not cover.
