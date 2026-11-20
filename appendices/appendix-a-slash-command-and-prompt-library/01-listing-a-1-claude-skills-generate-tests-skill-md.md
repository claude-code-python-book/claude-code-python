---
description: Write pytest tests for a module or function and run them.
argument-hint: <path-or-symbol> [what to focus on]
disable-model-invocation: true
allowed-tools: Bash(uv run pytest *)
---

Write pytest tests for: $ARGUMENTS

1. Read the code under test and the tests that already cover it. Read
   `tests/conftest.py` and reuse its fixtures instead of adding new ones.
2. Before writing code, list the behaviours worth testing: the normal
   path, boundaries (empty, zero, negative, very large), invalid input
   and the exceptions it raises, and any rounding or ordering rules.
3. Put the tests in `tests/test_<module>.py`, extending the file if it
   exists. Use plain test functions, plain `assert`,
   `pytest.raises(..., match=...)`, and `@pytest.mark.parametrize` for
   input tables. One behaviour per test, named `test_<unit>_<behaviour>`.
4. Do not change the code under test. If a test exposes a bug, mark it
   `@pytest.mark.xfail(reason="...", strict=True)` and tell me about it.
5. Run `uv run pytest -q <test file>` until every test passes or is
   marked xfail.

Finish with three short lists: tests added, behaviours covered, and
anything you could not test and why.
