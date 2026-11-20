# bookings-site

Room bookings for the office: Django 6.1, Django REST framework 3.18 and
PostgreSQL. The sample project for Chapter 13 of *Claude Code for Python
Developers*.

## Run it

```bash
uv sync
createdb bookings                                  # PostgreSQL
uv run manage.py makemigrations bookings           # creates 0002 after 0001_btree_gist
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

The API is at http://127.0.0.1:8000/api/ and the admin at /admin/.

## Work on it

| Task | Command |
| --- | --- |
| Tests (needs PostgreSQL) | `uv run pytest -q` |
| Rules and hook tests only | `uv run pytest -q tests/test_rules.py tests/test_guard_migrations.py` |
| Lint and format | `uv run ruff check --fix .` and `uv run ruff format .` |
| Missing migrations? | `uv run manage.py makemigrations --check` |

Read `CLAUDE.md` before your first change.
