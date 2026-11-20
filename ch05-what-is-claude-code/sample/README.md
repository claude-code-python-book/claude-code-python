# Chapter 5 sample: the invoicer project

- `invoicer/`: `pyproject.toml` (Listing 5-1, plus the pytest `pythonpath`
  setting from Section 13), `src/invoicer/tax.py` (Listing 5-2),
  `tests/test_tax.py` (Listing 5-3) and `.claude/settings.json` (Listing 5-5)
- `invoicer-env.sh`: Listing 5-4, for `CLAUDE_ENV_FILE` (it belongs in
  `~/.claude/envs/`, not in the repository)

```bash
cd invoicer
uv sync
uv run pytest -q && uv run ruff check . && uv run mypy src tests
```
