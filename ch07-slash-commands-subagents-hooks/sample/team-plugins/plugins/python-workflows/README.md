# python-workflows

Slash commands, subagents and hooks for Python projects that use uv,
pytest, Ruff and mypy.

- Commands: /python-workflows:generate-tests, review-code, add-docstrings,
  add-type-hints, add-logging, new-endpoint, check-security,
  upgrade-python, write-changelog and prep-pr.
- Subagents: test-writer and code-reviewer.
- Hooks: a Bash guard (PreToolUse), Ruff after every edit (PostToolUse)
  and a pytest gate before Claude stops (Stop).

The hook scripts need `python3` and `uv` on your PATH. Try the plugin
locally with `claude --plugin-dir ./plugins/python-workflows`.
