---
description: Run the pre-PR checklist and draft the PR description.
argument-hint: [base branch; default main]
disable-model-invocation: true
allowed-tools:
  - Bash(git status *)
  - Bash(git diff *)
  - Bash(git log *)
  - Bash(uv run ruff *)
  - Bash(uv run mypy *)
  - Bash(uv run pytest *)
---

Prepare this branch for a pull request against: $ARGUMENTS
(use `main` if no base branch is given).

Current state:

!`git status --short --branch`

1. Run these in order. Stop at the first failure and show its output:
   - `uv run ruff format --check .`
   - `uv run ruff check .`
   - `uv run mypy src tests`
   - `uv run pytest -q`
2. Review the whole branch with `git diff <base>...HEAD` and
   `git log --oneline <base>..HEAD`. Flag:
   - leftover debugging: `print()`, `breakpoint()`, commented-out code
   - TODO comments without an issue number
   - secrets, `.env` values, large or generated files
   - behaviour changes without a test; user-visible changes without a
     CHANGELOG.md entry
3. Draft the PR description with these headings: Summary (two or three
   sentences: what and why), Changes, Testing (the commands you ran
   and their results), Notes for reviewers (risks, follow-ups).

Do not commit, push or open the pull request.
