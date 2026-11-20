# reviewbot

A pull-request review agent built on the Claude Agent SDK for Python
(Chapter 20 of *Claude Code for Python Developers*).

```bash
uv sync                                   # or: pip install -e ".[api]"
export ANTHROPIC_API_KEY=...              # from the Claude Console
uv run python -m reviewbot --base main    # review the current branch
uv run pytest                             # offline tests, no API key needed
uv run python -m reviewbot.evals evals/cases.toml   # live evals: costs money
uv run --extra api uvicorn reviewbot.api:app        # HTTP API (put auth in front)
```

Layout:

- `src/reviewbot/tools.py` – in-process MCP tools (`changed_files`, `file_diff`, `record_finding`)
- `src/reviewbot/policy.py` – the `can_use_tool` permission callback
- `src/reviewbot/hooks.py` – PreToolUse secrets guard, PostToolUse audit log
- `src/reviewbot/agent.py` – `build_options()` and `run_review()`
- `src/reviewbot/session.py` – multi-turn `ClaudeSDKClient` chat with an interrupt deadline
- `src/reviewbot/oneshot.py` – a minimal `query()` example
- `src/reviewbot/service.py`, `schemas.py`, `api.py` – FastAPI endpoint with guard rails
- `src/reviewbot/cost.py` – token and cost ledger (client-side estimates)
- `src/reviewbot/recording.py` – record a live session for offline replay
- `tests/fakecli.py` – a scripted stand-in for the CLI side of the protocol

`tests/fakecli.py` and `recording.py` implement the SDK's `Transport` class,
which the SDK documents as a low-level interface that may change between
releases. Pin `claude-agent-sdk` in your lock file and rerun the tests when you
upgrade.
