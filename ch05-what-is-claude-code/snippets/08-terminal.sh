uv sync                  # creates .venv, installs the project and the dev group
uv run pytest -q         # runs inside the project environment
uv run ruff check .
uv run mypy src tests
