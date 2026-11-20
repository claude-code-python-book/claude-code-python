---
description: Add or fix Google-style docstrings in one Python file.
argument-hint: <file.py>
disable-model-invocation: true
allowed-tools: Bash(uv run ruff check *) Bash(uv run pytest *)
---

Add Google-style docstrings to $ARGUMENTS.

- Give every public module, class, function and method a docstring.
  Skip names that start with `_` unless the logic is not obvious.
- Summary line: one sentence in the imperative mood ("Return...",
  not "Returns..."), ending with a period, under 80 characters.
- Then, only as needed, these sections in this order: `Args:`,
  `Returns:` (or `Yields:`), `Raises:`, `Example:`. Don't repeat types
  the signature already annotates.
- Document what a caller needs to know: units, rounding, valid ranges,
  and every exception the function raises on purpose.
- Keep docstrings that are already correct. Fix wrong ones.
- Change docstrings only: no code, comment or import changes.

Then check the result:

    uv run ruff check --select D $ARGUMENTS
    uv run pytest --doctest-modules $ARGUMENTS

Fix what it reports and show me the final docstrings.
