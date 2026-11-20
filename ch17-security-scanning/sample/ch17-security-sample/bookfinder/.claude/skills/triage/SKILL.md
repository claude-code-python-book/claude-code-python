---
description: Triage security scanner findings and propose tested fixes
argument-hint: "[path or scanner output file]"
disable-model-invocation: true
allowed-tools: Bash(uv run ruff check:*), Bash(uv run pytest:*)
---

# Security triage

Scope: $ARGUMENTS (default: `src/`).

1. Run `uv run ruff check --select S --output-format concise $ARGUMENTS`. If a
   file of Bandit, Semgrep or pip-audit output is given instead, read it.
2. For every finding, read the code around it and follow the data back to
   where it enters the program. Then classify it:
   - **Exploitable**: untrusted data reaches the sink. Give a concrete input
     and what it would do.
   - **Not exploitable**: say exactly why (for example "value comes from the
     SORT_COLUMNS dict"), and name the test that proves it or propose one.
   - **Needs a human**: you can't tell from the code (deployment, config,
     data source). Say what to check.
3. Show a table: file:line, rule, classification, one-line reason.
4. For each exploitable finding, propose a fix that follows the security
   rules in CLAUDE.md, starting with a failing test. Don't edit files until
   I approve the plan.
5. Never mark a finding as a false positive just to make the scanner pass.
