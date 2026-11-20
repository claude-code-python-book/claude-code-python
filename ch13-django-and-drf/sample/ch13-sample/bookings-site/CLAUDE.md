# bookings-site

Room bookings for the office: Django 6.1, Django REST framework 3.18,
PostgreSQL, Python 3.12+. One app, `bookings`; project config in `config/`.

<!-- Maintainers: keep this file under 80 lines. Review edits like code. -->

## Commands
- Setup: `uv sync`, then `uv run manage.py migrate`
- Run: `uv run manage.py runserver` (settings: `config.settings.dev`)
- Tests: `uv run pytest -q` (needs PostgreSQL; settings: `config.settings.test`)
- Lint: `uv run ruff check --fix .` then `uv run ruff format .`
- Checks: `uv run manage.py check` and `uv run manage.py makemigrations --check`
- Before you report a task as done, run tests, Ruff and both checks.

## Where things go
- Business rules: `bookings/rules.py`, plain Python, no Django imports.
  Models, serializers and the admin call it; test it in `tests/test_rules.py`.
- Database rules (overlaps, end after start): constraints in `Meta`.
- HTTP: thin viewsets in `views.py`, routes in `bookings/urls.py`.
- Side effects (email): `notifications.py`, called explicitly with
  `transaction.on_commit`. No signals inside this app.
- Settings: `base.py` plus `dev.py`, `test.py`, `prod.py`. Read
  environment variables only in `prod.py` and `base.py`.

## Django and DRF conventions
- Querysets: every viewset's `get_queryset()` scopes rows to the user and
  uses `select_related`/`prefetch_related` for every relation the
  serializer reads. Add a query-count test for every list endpoint.
- Object permissions don't filter lists: scope the queryset first,
  then add a permission class for single-object actions.
- The user comes from `request.user` (`perform_create`), never the body.
- Choices: `models.TextChoices`. Strings: never `null=True`; use "".
- Every model has `__str__`; every admin has `list_display`,
  `search_fields` and, for foreign keys, `autocomplete_fields`.
- No editing endpoints for bookings: cancel and rebook.

## Migrations
- Generate with `makemigrations`, then read the file and `sqlmigrate`.
  Report every operation that locks or rewrites a table.
- Never edit a committed migration (a hook asks first). Add a new one.
- Data migrations: `RunPython` with a `reverse_code`, models from
  `apps.get_model()`, never imported.
- Schema change and data change go in separate migrations.

## Testing
- pytest-django and Factory Boy (`tests/django/factories.py`). Factories
  make valid objects; override only what the test is about.
- One API test for each status code an endpoint can return.

## Don't
- Don't call `full_clean()` in `save()`.
- Don't use `.extra()`, or `.raw()` with string formatting.
- Don't import `config.settings.prod` anywhere.
