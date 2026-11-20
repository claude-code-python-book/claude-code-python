---
name: writing-pytest-tests
description: Writes pytest unit tests for a Python module, covering normal cases, edge cases and error paths, then checks and runs them. Use when the user asks to write, add or generate tests, or to improve test coverage for Python code.
---

# Writing pytest tests

## Overview

Write focused pytest tests for one Python module at a time. Test the
module's public behaviour, not its private details, and finish only when
the new tests pass.

## Workflow

Copy this checklist into your reply and tick items off as you go:

- [ ] 1. List the module's functions: `python3 scripts/list_functions.py <module.py>`
- [ ] 2. Read the source of each function you will test
- [ ] 3. Write the tests in `tests/test_<module>.py`, following the rules below
- [ ] 4. Check them: `python3 scripts/check_tests.py tests/test_<module>.py`
- [ ] 5. Run them: `uv run pytest tests/test_<module>.py -q`
- [ ] 6. Fix any problem and repeat steps 4 and 5 until both pass

Run the two scripts; do not read them. On Windows, use `python` instead of
`python3`. If the project does not use uv, run `python -m pytest` instead.

## Rules

- Put the tests for `src/pkg/name.py` in `tests/test_name.py`.
- Name each test `test_<function>_<behaviour>`, for example
  `test_apply_discount_rejects_negative_price`.
- Each test checks one behaviour and contains at least one `assert` or
  `pytest.raises`.
- Cover a normal case, the edge cases (empty input, zero, boundaries) and
  every exception the function raises.
- Use `@pytest.mark.parametrize` when the same check runs over several inputs.
- Use pytest's `tmp_path` and `monkeypatch` fixtures instead of real files,
  environment variables or network calls.

## Warnings

- Never change the code under test to make a test pass. If you believe the
  code is wrong, write the test for the correct behaviour, mark it with
  `@pytest.mark.xfail(reason="...")`, and tell the user why.
- Never call real networks, databases or paid APIs. Replace them with
  `monkeypatch` or `unittest.mock`.
- Do not use `time.sleep` in tests.

## Example

For this function:

```python
def parse_quantity(text: str) -> int:
    value = int(text.strip())
    if value < 1:
        raise ValueError("quantity must be at least 1")
    return value
```

write tests like these:

```python
@pytest.mark.parametrize(("text", "expected"), [("3", 3), (" 12 ", 12)])
def test_parse_quantity_accepts_whole_numbers(text, expected):
    assert parse_quantity(text) == expected

@pytest.mark.parametrize("text", ["0", "-2", "abc", ""])
def test_parse_quantity_rejects_invalid_input(text):
    with pytest.raises(ValueError):
        parse_quantity(text)
```

## More patterns

For fixtures, mocking, temporary files and floating-point checks, read
[references/patterns.md](references/patterns.md).
