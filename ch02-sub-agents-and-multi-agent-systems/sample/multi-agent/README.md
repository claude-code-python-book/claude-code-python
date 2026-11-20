# Chapter 2 sample: sub-agents and a multi-agent pipeline

- `subagent_basic.py`: Listing 2-1; `subagent_lib.py`: its `run_subagent`
  function as an importable module (used by `delegate.py`)
- `delegate.py`: Listing 2-2; `parallel_demo.py`: Listing 2-3
- `parallel_review.py`: Listing 2-4
- `pipeline.py`: Listings 2-5 to 2-9
- `.claude/agents/python-reviewer.md`: the Claude Code subagent from Section 2.3

Run against the real API (needs `ANTHROPIC_API_KEY`):

```bash
uv sync
uv run python parallel_demo.py          # no API key needed
uv run python pipeline.py "How Python's GIL affects threads"
```

Offline checks with a fake `anthropic` package: `uv run pytest -q`
