# Chapter 3 sample: the writing-pytest-tests skill

- `.claude/skills/writing-pytest-tests/`: `SKILL.md` (Listing 3-2), the full
  `scripts/list_functions.py` and `scripts/check_tests.py` (Listings 3-4 and
  3-5 are their key functions) and `references/patterns.md`
- `.claude/skills/python-house-style/SKILL.md`: Listing 3-7
- `src/shop/pricing.py` (Listing 3-1), `tests/test_pricing.py` (Listing 3-3)
- `examples/test_bad.py` (Listing 3-6) and `examples/bad-skill/helper/`
- `validate_skill.py`: the validator from Section 8 (needs PyYAML)
- `sdk_skills.py`: loading skills from the Claude Agent SDK

```bash
uv sync
uv run pytest -q                                     # 17 passed
python3 .claude/skills/writing-pytest-tests/scripts/check_tests.py examples/test_bad.py
uv run python validate_skill.py .claude/skills/writing-pytest-tests .claude/skills/python-house-style
uv run pytest checks -q                              # the outputs shown in the chapter
```
