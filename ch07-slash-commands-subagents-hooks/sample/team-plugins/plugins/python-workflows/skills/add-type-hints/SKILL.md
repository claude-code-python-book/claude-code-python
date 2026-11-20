---
description: Add type hints to one module and make it pass mypy --strict.
argument-hint: <module.py>
disable-model-invocation: true
allowed-tools: Bash(uv run mypy *) Bash(uv run pytest *)
---

Add type hints to $ARGUMENTS as one step of a gradual typing pass.

1. Run `uv run mypy --strict $ARGUMENTS` and read the errors first.
2. Annotate every function signature, parameters and return type.
   Then annotate module constants and class attributes whose type
   mypy cannot infer.
3. Use modern syntax: `list[int]`, `dict[str, Decimal]`, `X | None`,
   and `collections.abc` for `Iterable`, `Mapping` and `Callable`.
   Accept the broadest type that works (`Iterable[Line]`) and return
   the most specific one (`list[Line]`).
4. Prefer real types over `Any`. For truly dynamic values use `object`
   and narrow with `isinstance`. A `# type: ignore` needs an error
   code, such as `# type: ignore[import-untyped]`, and a reason.
5. Don't change runtime behaviour, and don't add `cast()` to silence
   an error you haven't understood. Fix the type or ask me.
6. Run mypy until the module is clean, then run the tests. Report any
   new errors in modules that import this one.
