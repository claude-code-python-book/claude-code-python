---
description: Review Python changes for bugs and test gaps. Read-only.
argument-hint: [path or git ref; default is uncommitted changes]
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *)
---

Review: $ARGUMENTS

If no target is given above, review the uncommitted changes:

!`git status --short`

!`git diff HEAD --stat`

Do not edit any file. Read each changed file in full, not only the
diff, and check:

- Correctness: edge cases, error handling, off-by-one errors, mutable
  default arguments, `float` where the project uses `Decimal`, naive
  datetimes, exceptions swallowed by a bare `except`.
- Design: functions doing more than one job, unclear names, duplicated
  logic, a change that leaks into unrelated modules.
- Types: public functions fully annotated; no unexplained `Any` or
  `# type: ignore` without an error code.
- Tests: every behaviour change has a test. Name the missing ones.
- Project rules: anything in CLAUDE.md the change breaks.

Report findings in this format, most severe first:

### Critical / Warning / Suggestion
- `path/to/file.py:LINE`: the problem, why it matters, the fix.

Write "None" under a heading with no findings. End with one line:
`Verdict: ready to merge`, `Verdict: merge after fixes` or
`Verdict: needs rework`.
