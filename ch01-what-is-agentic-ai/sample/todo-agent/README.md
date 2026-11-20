# Chapter 1 sample: a minimal TODO-finding agent

Files assembled from the chapter's listings:

- `agent.py`: Listings 1-4, 1-5, 1-6, 1-9 and 1-10
- `explore.py`: Listings 1-7 and 1-8 (one round of the loop, by hand)
- `tool_schema.py`: Listing 1-2; `chatbot.py`: Listing 1-3
- `agent_loop_concept.py`: Listing 1-1 (pseudo-code, not meant to run)
- `demo_project/`: a tiny project with TODO comments to point the agent at

Run against the real API (needs `ANTHROPIC_API_KEY`):

```bash
uv sync
uv run python agent.py ./demo_project
```

Offline checks: `tests/` replaces the `anthropic` package with a small fake,
so the loop, the tools and `explore.py` run without a key or network:

```bash
uv run pytest -q
```
