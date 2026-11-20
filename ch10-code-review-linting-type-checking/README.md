# Chapter 10 — Code Review, Linting, and Type Checking: Catch Bugs Before the PR

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`README.md`, `invoicer`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-listing-10-1-src-invoicer-reminders-py-as-submitted.py`](snippets/01-listing-10-1-src-invoicer-reminders-py-as-submitted.py) | Listing 10-1: src/invoicer/reminders.py (as submitted) | python | 2. A Structured Workflow for AI Code Review |
| [`02-listing-10-2-tests-test-reminders-py-as-submitted.py`](snippets/02-listing-10-2-tests-test-reminders-py-as-submitted.py) | Listing 10-2: tests/test_reminders.py (as submitted) | python | 2. A Structured Workflow for AI Code Review |
| [`03-prompt.txt`](snippets/03-prompt.txt) | Prompt | prompt | 2. A Structured Workflow for AI Code Review |
| [`04-listing-10-3-the-widened-ruff-configuration-in-pyproject-t.toml`](snippets/04-listing-10-3-the-widened-ruff-configuration-in-pyproject-t.toml) | Listing 10-3: The widened Ruff configuration in pyproject.toml | toml | 4. Ruff: One Tool for Linting and Formatting |
| [`05-terminal.sh`](snippets/05-terminal.sh) | Terminal | bash | 4. Ruff: One Tool for Linting and Formatting |
| [`06-output.txt`](snippets/06-output.txt) | Output | text | 4. Ruff: One Tool for Linting and Formatting |
| [`07-listing-10-4-fetch-rates-in-src-invoicer-fx-py-after-the-f.py`](snippets/07-listing-10-4-fetch-rates-in-src-invoicer-fx-py-after-the-f.py) | Listing 10-4: fetch_rates in src/invoicer/fx.py after the fix | python | 4. Ruff: One Tool for Linting and Formatting |
| [`08-terminal.sh`](snippets/08-terminal.sh) | Terminal | bash | 4. Ruff: One Tool for Linting and Formatting |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 4. Ruff: One Tool for Linting and Formatting |
| [`10-terminal.sh`](snippets/10-terminal.sh) | Terminal | bash | 5. Type Checking with mypy and pyright |
| [`11-output.txt`](snippets/11-output.txt) | Output | text | 5. Type Checking with mypy and pyright |
| [`12-output.txt`](snippets/12-output.txt) | Output | text | 5. Type Checking with mypy and pyright |
| [`13-output.txt`](snippets/13-output.txt) | Output | text | 5. Type Checking with mypy and pyright |
| [`14-output.txt`](snippets/14-output.txt) | Output | text | 5. Type Checking with mypy and pyright |
| [`15-listing-10-5-the-pyright-configuration-in-pyproject-toml.toml`](snippets/15-listing-10-5-the-pyright-configuration-in-pyproject-toml.toml) | Listing 10-5: The pyright configuration in pyproject.toml | toml | 5. Type Checking with mypy and pyright |
| [`16-code.py`](snippets/16-code.py) | Code | python | 6. Bugs Claude Code Catches Well |
| [`17-output.txt`](snippets/17-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`18-listing-10-6-the-fixed-functions-in-src-invoicer-reminders.py`](snippets/18-listing-10-6-the-fixed-functions-in-src-invoicer-reminders.py) | Listing 10-6: The fixed functions in src/invoicer/reminders.py | python | 6. Bugs Claude Code Catches Well |
| [`19-output.txt`](snippets/19-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`20-output.txt`](snippets/20-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`21-output.txt`](snippets/21-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`22-output.txt`](snippets/22-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`23-listing-10-7-reminder-emails-in-src-invoicer-reminders-py.py`](snippets/23-listing-10-7-reminder-emails-in-src-invoicer-reminders-py.py) | Listing 10-7: reminder_emails in src/invoicer/reminders.py after the fix | python | 6. Bugs Claude Code Catches Well |
| [`24-output.txt`](snippets/24-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`25-output.txt`](snippets/25-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`26-listing-10-8-post-and-post-all-in-src-invoicer-reminders-p.py`](snippets/26-listing-10-8-post-and-post-all-in-src-invoicer-reminders-p.py) | Listing 10-8: post and post_all in src/invoicer/reminders.py after the fix | python | 6. Bugs Claude Code Catches Well |
| [`27-output.txt`](snippets/27-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`28-terminal.sh`](snippets/28-terminal.sh) | Terminal | bash | 6. Bugs Claude Code Catches Well |
| [`29-output.txt`](snippets/29-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`30-output.txt`](snippets/30-output.txt) | Output | text | 6. Bugs Claude Code Catches Well |
| [`31-code.py`](snippets/31-code.py) | Code | python | 7. Python Anti-Patterns to Refactor: Bare except, Overused Any and type: ignore |
| [`32-terminal.sh`](snippets/32-terminal.sh) | Terminal | bash | 7. Python Anti-Patterns to Refactor: Bare except, Overused Any and type: ignore |
| [`33-output.txt`](snippets/33-output.txt) | Output | text | 7. Python Anti-Patterns to Refactor: Bare except, Overused Any and type: ignore |
| [`34-output.txt`](snippets/34-output.txt) | Output | text | 7. Python Anti-Patterns to Refactor: Bare except, Overused Any and type: ignore |
| [`35-code.toml`](snippets/35-code.toml) | Code | toml | 8. Adding Types to an Untyped Codebase, One Module at a Time |
| [`36-terminal.sh`](snippets/36-terminal.sh) | Terminal | bash | 8. Adding Types to an Untyped Codebase, One Module at a Time |
| [`37-output.txt`](snippets/37-output.txt) | Output | text | 8. Adding Types to an Untyped Codebase, One Module at a Time |
| [`38-terminal.sh`](snippets/38-terminal.sh) | Terminal | bash | 10. Reviewing Diffs vs Reviewing Files |
| [`39-output.txt`](snippets/39-output.txt) | Output | text | 10. Reviewing Diffs vs Reviewing Files |
| [`40-listing-10-9-pre-commit-config-yaml.yml`](snippets/40-listing-10-9-pre-commit-config-yaml.yml) | Listing 10-9: .pre-commit-config.yaml | yaml | 11. pre-commit and the Quality Gate |
| [`41-listing-10-10-the-review-section-of-claude-md.md`](snippets/41-listing-10-10-the-review-section-of-claude-md.md) | Listing 10-10: The Review section of CLAUDE.md | markdown | 11. pre-commit and the Quality Gate |
| [`42-output.txt`](snippets/42-output.txt) | Output | text | 11. pre-commit and the Quality Gate |
