---
description: Modernize a module to Python 3.12+ syntax and APIs.
argument-hint: <path>
disable-model-invocation: true
allowed-tools: Bash(uv run ruff check *) Bash(uv run pytest *)
---

Modernize $ARGUMENTS for Python 3.12 and later.

1. Read `requires-python` in `pyproject.toml`. If it allows a version
   older than 3.12, stop and tell me: the new syntax would break there.
2. Apply Ruff's pyupgrade rules and review the diff:

       uv run ruff check --select UP --target-version py312 \
           --fix $ARGUMENTS

3. Then, by hand, where it makes the code clearer:
   - `type` aliases and type-parameter syntax (PEP 695):
     `type Rows = list[Row]`, `def first[T](xs: list[T]) -> T`.
   - `@override` from `typing` on methods that override a parent's.
   - `itertools.batched()` instead of hand-written chunking.
   - `match` only where it replaces a long `isinstance`/`elif` chain.
4. Replace deprecated APIs: `datetime.utcnow()` and
   `datetime.utcfromtimestamp()` become `datetime.now(UTC)` and
   `datetime.fromtimestamp(ts, UTC)`. Note that the results are now
   timezone-aware and check that callers expect that.
5. Run the tests. Report each change you made by hand and why.
