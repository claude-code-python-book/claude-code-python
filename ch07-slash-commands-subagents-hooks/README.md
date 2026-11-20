# Chapter 7 — Slash Commands, Subagents, and Hooks for Python Workflows

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`invoicer`, `team-plugins`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-listing-7-1-claude-skills-generate-tests-skill-md.md`](snippets/01-listing-7-1-claude-skills-generate-tests-skill-md.md) | Listing 7-1: .claude/skills/generate-tests/SKILL.md | markdown | 2. A Python Command Library |
| [`02-listing-7-2-claude-skills-review-code-skill-md.md`](snippets/02-listing-7-2-claude-skills-review-code-skill-md.md) | Listing 7-2: .claude/skills/review-code/SKILL.md | markdown | 2. A Python Command Library |
| [`03-terminal.sh`](snippets/03-terminal.sh) | Terminal | bash | 2. A Python Command Library |
| [`04-listing-7-3-claude-skills-new-endpoint-skill-md.md`](snippets/04-listing-7-3-claude-skills-new-endpoint-skill-md.md) | Listing 7-3: .claude/skills/new-endpoint/SKILL.md | markdown | 2. A Python Command Library |
| [`05-terminal.sh`](snippets/05-terminal.sh) | Terminal | bash | 2. A Python Command Library |
| [`06-output.txt`](snippets/06-output.txt) | Output | text | 2. A Python Command Library |
| [`07-listing-7-4-claude-skills-upgrade-python-skill-md.md`](snippets/07-listing-7-4-claude-skills-upgrade-python-skill-md.md) | Listing 7-4: .claude/skills/upgrade-python/SKILL.md | markdown | 2. A Python Command Library |
| [`08-code.py`](snippets/08-code.py) | Code | python | 2. A Python Command Library |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 2. A Python Command Library |
| [`10-listing-7-5-claude-skills-prep-pr-skill-md.md`](snippets/10-listing-7-5-claude-skills-prep-pr-skill-md.md) | Listing 7-5: .claude/skills/prep-pr/SKILL.md | markdown | 2. A Python Command Library |
| [`11-listing-7-6-claude-agents-test-writer-md.md`](snippets/11-listing-7-6-claude-agents-test-writer-md.md) | Listing 7-6: .claude/agents/test-writer.md | markdown | 4. Custom Subagents: A Test Writer and a Reviewer |
| [`12-listing-7-7-claude-agents-code-reviewer-md.md`](snippets/12-listing-7-7-claude-agents-code-reviewer-md.md) | Listing 7-7: .claude/agents/code-reviewer.md | markdown | 4. Custom Subagents: A Test Writer and a Reviewer |
| [`13-code.yml`](snippets/13-code.yml) | Code | yaml | 4. Custom Subagents: A Test Writer and a Reviewer |
| [`14-listing-7-8-the-hooks-section-of-claude-settings-json.json`](snippets/14-listing-7-8-the-hooks-section-of-claude-settings-json.json) | Listing 7-8: The hooks section of .claude/settings.json | json | 5. Hooks: What They Are and When They Fire |
| [`15-code.json`](snippets/15-code.json) | Code | json | 5. Hooks: What They Are and When They Fire |
| [`16-listing-7-9-claude-hooks-format-python-py.py`](snippets/16-listing-7-9-claude-hooks-format-python-py.py) | Listing 7-9: .claude/hooks/format_python.py | python | 6. Auto-Format with Ruff After Every Edit (PostToolUse) |
| [`17-code.py`](snippets/17-code.py) | Code | python | 6. Auto-Format with Ruff After Every Edit (PostToolUse) |
| [`18-terminal.sh`](snippets/18-terminal.sh) | Terminal | bash | 6. Auto-Format with Ruff After Every Edit (PostToolUse) |
| [`19-output.txt`](snippets/19-output.txt) | Output | text | 6. Auto-Format with Ruff After Every Edit (PostToolUse) |
| [`20-code.py`](snippets/20-code.py) | Code | python | 6. Auto-Format with Ruff After Every Edit (PostToolUse) |
| [`21-listing-7-10-claude-hooks-guard-bash-py.py`](snippets/21-listing-7-10-claude-hooks-guard-bash-py.py) | Listing 7-10: .claude/hooks/guard_bash.py | python | 7. Blocking Dangerous Commands (PreToolUse) |
| [`22-listing-7-11-tests-hooks-test-guard-bash-py.py`](snippets/22-listing-7-11-tests-hooks-test-guard-bash-py.py) | Listing 7-11: tests/hooks/test_guard_bash.py | python | 7. Blocking Dangerous Commands (PreToolUse) |
| [`23-terminal.sh`](snippets/23-terminal.sh) | Terminal | bash | 7. Blocking Dangerous Commands (PreToolUse) |
| [`24-output.txt`](snippets/24-output.txt) | Output | text | 7. Blocking Dangerous Commands (PreToolUse) |
| [`25-listing-7-12-claude-hooks-pytest-gate-py.py`](snippets/25-listing-7-12-claude-hooks-pytest-gate-py.py) | Listing 7-12: .claude/hooks/pytest_gate.py | python | 8. Running pytest Before Claude Stops (Stop Hook) |
| [`26-output.txt`](snippets/26-output.txt) | Output | text | 8. Running pytest Before Claude Stops (Stop Hook) |
| [`27-code.json`](snippets/27-code.json) | Code | json | 8. Running pytest Before Claude Stops (Stop Hook) |
| [`28-layout.txt`](snippets/28-layout.txt) | Layout | tree | 9. Packaging Commands, Agents, and Hooks as a Plugin |
| [`29-listing-7-13-claude-plugin-plugin-json.json`](snippets/29-listing-7-13-claude-plugin-plugin-json.json) | Listing 7-13: .claude-plugin/plugin.json | json | 9. Packaging Commands, Agents, and Hooks as a Plugin |
| [`30-terminal.sh`](snippets/30-terminal.sh) | Terminal | bash | 9. Packaging Commands, Agents, and Hooks as a Plugin |
| [`31-output.txt`](snippets/31-output.txt) | Output | text | 9. Packaging Commands, Agents, and Hooks as a Plugin |
| [`32-listing-7-14-team-plugins-claude-plugin-marketplace-json.json`](snippets/32-listing-7-14-team-plugins-claude-plugin-marketplace-json.json) | Listing 7-14: team-plugins/.claude-plugin/marketplace.json | json | 10. Sharing the Setup Across Your Team |
| [`33-terminal.sh`](snippets/33-terminal.sh) | Terminal | bash | 10. Sharing the Setup Across Your Team |
| [`34-output.txt`](snippets/34-output.txt) | Output | text | 10. Sharing the Setup Across Your Team |
| [`35-code.json`](snippets/35-code.json) | Code | json | 10. Sharing the Setup Across Your Team |
