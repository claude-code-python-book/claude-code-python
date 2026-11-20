---
name: python-house-style
description: Applies this team's Python conventions (type hints, Google-style docstrings, logging instead of print) when writing or changing Python code in src/. Use whenever creating or editing Python modules in this repository.
---

# Python house style

Apply these rules to every module you create or change under `src/`.
Test files under `tests/` are exempt from the type-hint and docstring rules.

- Add type hints to every function parameter and return value.
- Give every public function a Google-style docstring with `Args:`,
  `Returns:` and `Raises:` sections where they apply.
- Use `logging.getLogger(__name__)`, never `print`, for diagnostic output.
- Raise specific exceptions (`ValueError`, `KeyError`), never bare `Exception`.
- Keep functions under 40 lines; extract a helper when one grows longer.

After editing, run `uv run ruff check src/` and fix what it reports.
