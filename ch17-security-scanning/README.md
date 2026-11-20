# Chapter 17 — Security Scanning and Dependency Auditing for Python

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`ch17-security-sample`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-listing-17-1-the-security-settings-in-pyproject-toml.toml`](snippets/01-listing-17-1-the-security-settings-in-pyproject-toml.toml) | Listing 17-1: The security settings in pyproject.toml | toml | 3. Setting Up the Scanners |
| [`02-listing-17-2-pre-commit-config-yaml.yml`](snippets/02-listing-17-2-pre-commit-config-yaml.yml) | Listing 17-2: .pre-commit-config.yaml | yaml | 3. Setting Up the Scanners |
| [`03-listing-17-3-semgrep-sql-fstring-yml-not-run.yml`](snippets/03-listing-17-3-semgrep-sql-fstring-yml-not-run.yml) | Listing 17-3: semgrep/sql-fstring.yml (not run) | yaml | 3. Setting Up the Scanners |
| [`04-listing-17-4-claude-skills-triage-skill-md.md`](snippets/04-listing-17-4-claude-skills-triage-skill-md.md) | Listing 17-4: .claude/skills/triage/SKILL.md | markdown | 4. Prompting Claude Code for Security Triage |
| [`05-listing-17-5-the-security-rules-in-claude-md.md`](snippets/05-listing-17-5-the-security-rules-in-claude-md.md) | Listing 17-5: The security rules in CLAUDE.md | markdown | 4. Prompting Claude Code for Security Triage |
| [`06-listing-17-6-the-first-version-of-search-books.py`](snippets/06-listing-17-6-the-first-version-of-search-books.py) | Listing 17-6: The first version of search_books() | python | 5. Worked Example: SQL Injection via f-Strings in a Search Endpoint |
| [`07-output.txt`](snippets/07-output.txt) | Output | text | 5. Worked Example: SQL Injection via f-Strings in a Search Endpoint |
| [`08-output.txt`](snippets/08-output.txt) | Output | text | 5. Worked Example: SQL Injection via f-Strings in a Search Endpoint |
| [`09-listing-17-7-exploit-regression-tests-in-tests-test-search.py`](snippets/09-listing-17-7-exploit-regression-tests-in-tests-test-search.py) | Listing 17-7: Exploit regression tests in tests/test_search.py | python | 5. Worked Example: SQL Injection via f-Strings in a Search Endpoint |
| [`10-listing-17-8-src-bookfinder-search-py.py`](snippets/10-listing-17-8-src-bookfinder-search-py.py) | Listing 17-8: src/bookfinder/search.py | python | 5. Worked Example: SQL Injection via f-Strings in a Search Endpoint |
| [`11-output.txt`](snippets/11-output.txt) | Output | text | 5. Worked Example: SQL Injection via f-Strings in a Search Endpoint |
| [`12-output.txt`](snippets/12-output.txt) | Output | text | 5. Worked Example: SQL Injection via f-Strings in a Search Endpoint |
| [`13-output.txt`](snippets/13-output.txt) | Output | text | 6. Common Python Vulnerability Patterns |
| [`14-output.txt`](snippets/14-output.txt) | Output | text | 6. Common Python Vulnerability Patterns |
| [`15-output.txt`](snippets/15-output.txt) | Output | text | 6. Common Python Vulnerability Patterns |
| [`16-listing-17-9-count-lines-in-src-bookfinder-importer-py.py`](snippets/16-listing-17-9-count-lines-in-src-bookfinder-importer-py.py) | Listing 17-9: count_lines() in src/bookfinder/importer.py | python | 6. Common Python Vulnerability Patterns |
| [`17-output.txt`](snippets/17-output.txt) | Output | text | 6. Common Python Vulnerability Patterns |
| [`18-listing-17-10-check-url-in-src-bookfinder-covers-py.py`](snippets/18-listing-17-10-check-url-in-src-bookfinder-covers-py.py) | Listing 17-10: check_url() in src/bookfinder/covers.py | python | 6. Common Python Vulnerability Patterns |
| [`19-output.txt`](snippets/19-output.txt) | Output | text | 6. Common Python Vulnerability Patterns |
| [`20-terminal.sh`](snippets/20-terminal.sh) | Terminal | bash | 8. Lock Files and Dependency Hygiene: uv.lock, poetry.lock, pip-tools |
| [`21-terminal.sh`](snippets/21-terminal.sh) | Terminal | bash | 8. Lock Files and Dependency Hygiene: uv.lock, poetry.lock, pip-tools |
| [`22-listing-17-11-github-dependabot-yml.yml`](snippets/22-listing-17-11-github-dependabot-yml.yml) | Listing 17-11: .github/dependabot.yml | yaml | 9. Dependabot and Renovate for Python |
| [`23-listing-17-12-renovate-json.json`](snippets/23-listing-17-12-renovate-json.json) | Listing 17-12: renovate.json | json | 9. Dependabot and Renovate for Python |
| [`24-output.txt`](snippets/24-output.txt) | Output | text | 10. Upgrading the Python Version Safely |
| [`25-output.txt`](snippets/25-output.txt) | Output | text | 11. Major Library Upgrades: Pydantic v1 → v2, SQLAlchemy 1.4 → 2.0, Django LTS |
| [`26-listing-17-13-github-workflows-security-yml-not-run.yml`](snippets/26-listing-17-13-github-workflows-security-yml-not-run.yml) | Listing 17-13: .github/workflows/security.yml (not run) | yaml | 12. Integrating Scans and Audits into CI |
