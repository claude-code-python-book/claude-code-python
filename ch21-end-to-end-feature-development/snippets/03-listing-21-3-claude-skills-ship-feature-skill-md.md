---
name: ship-feature
description: Take a feature brief from docs/features through code, tests, review and a pull request. Use when asked to implement a documented feature end to end.
argument-hint: "[brief file]"
disable-model-invocation: true
---

Implement the feature described in $ARGUMENTS and stop before anything
ships.

Current branch and changes:
!`git status --short --branch`

1. **Plan.** Read the brief and CLAUDE.md, then the code you will touch.
   Reply with a plan: files, functions, the migration, and which
   acceptance criterion each change serves. Wait for my approval.
2. **Code.** Implement the plan. Rules go in `ratings.py` or
   `service.py`; adapters stay thin. Write a migration with a downgrade.
3. **Test.** Delegate to the test-writer subagent with the brief and the
   list of changed files. Read its report; fix real bugs it finds.
4. **Check.** Run `uv run ruff check .`, `uv run mypy`,
   `uv run --group security bandit -c pyproject.toml -r src` and
   `uv run pytest -q -m "not integration"`. All must pass.
5. **Review.** Delegate to the reviewer subagent with the brief, the
   output of `git diff` and the changed files. Fix
   every Blocking and Should-fix finding, then rerun step 4.
6. **Hand over.** Show the diff summary, each criterion with the test
   that proves it, and a draft commit message and PR description. Don't
   commit, push or open the PR until I say so.
