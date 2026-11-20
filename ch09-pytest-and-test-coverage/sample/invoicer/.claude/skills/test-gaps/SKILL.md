---
description: Find behaviour the tests would not notice changing, then close the gaps.
argument-hint: <module path>
disable-model-invocation: true
allowed-tools: Bash(uv run pytest *)
---

Find the testing gaps in: $ARGUMENTS

1. Run `uv run pytest --cov=invoicer --cov-branch --cov-report=term-missing -q`
   and note missed lines, partial branches (`12->15`), and files at 0%.
2. Read the module and its tests. Coverage only says a line ran. For each
   condition, constant, and boundary, ask: if this changed, which test
   would fail? List every change no assertion would catch.
3. Check `CLAUDE.md` for code that matters outside the test suite.
4. Before writing tests, show me the list ranked by risk, with one line
   each on what could break. Mark anything that needs a product decision.
5. Once I pick items, write the tests with the generate-tests rules.
   Do not change code under test; a test that exposes a bug is
   `xfail(strict=True)`.

Never add a test only to raise the coverage number.
