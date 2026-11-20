---
description: Diagnose a failed GitHub Actions run and propose a fix
argument-hint: "[run-id]"
disable-model-invocation: true
allowed-tools: Bash(gh run list:*), Bash(gh run view:*), Bash(uv run:*)
---

# Fix a failed CI run

Run: $ARGUMENTS. If no ID is given, find the latest failed run on this
branch with `gh run list --branch <branch> --status failure --limit 1`.

1. Fetch only the failed steps: `gh run view <id> --log-failed`. Note which
   jobs failed and which passed (OS, Python version).
2. Find the first error, not the last line of the log. Quote it.
3. Reproduce it locally with the same Python, for example
   `uv run --python 3.12 pytest tests/test_batching.py`. If it doesn't
   reproduce, list what differs between CI and here (OS, Python, lock file,
   environment variables, secrets) and stop.
4. Say whether the fix belongs in the code, the tests, the dependencies or
   the workflow, and why. Never hide a real failure: no `continue-on-error`,
   no dropping a matrix entry, no skipped tests.
5. Propose the smallest fix, plus a check that would catch the problem
   before CI next time. Don't edit files until I approve.
