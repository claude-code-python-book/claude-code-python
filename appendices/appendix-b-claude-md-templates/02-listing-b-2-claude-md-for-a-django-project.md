# <project-name>

<What the site does, in one line.> Django <version>, Django REST
framework <version>, PostgreSQL, Python 3.12+. Apps: `<app>`; project
config in `config/`.

<!-- Maintainers: keep this file under 80 lines. Review edits like code. -->

## Commands
- Setup: `uv sync`, then `uv run manage.py migrate`
- Run: `uv run manage.py runserver` (settings: `config.settings.dev`)
- Tests: `uv run pytest -q` (needs PostgreSQL; settings: `config.settings.test`)
- Lint: `uv run ruff check --fix .` then `uv run ruff format .`
- Checks: `uv run manage.py check` and `uv run manage.py makemigrations --check`
- Before you report a task as done, run tests, Ruff and both checks.

## Where things go
- Business rules: `<app>/rules.py`, plain Python, no Django imports.
  Models, serializers and the admin call it; test it in `tests/test_rules.py`.
- Database rules: constraints in `Meta`.
- HTTP: thin viewsets in `views.py`, routes in `<app>/urls.py`.
- Side effects (email): called explicitly with `transaction.on_commit`.
  No signals inside this app.
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
- Every model has `__str__`; every admin has `list_display` and
  `search_fields`.

## Migrations
- Generate with `makemigrations`, then read the file and `sqlmigrate`.
  Report every operation that locks or rewrites a table.
- Never edit a committed migration. Add a new one.
- Data migrations: `RunPython` with a `reverse_code`, models from
  `apps.get_model()`, never imported.
- Schema change and data change go in separate migrations.

## Testing
- pytest-django and Factory Boy. Factories make valid objects; override
  only what the test is about.
- One API test for each status code an endpoint can return.

## Don't
- Don't call `full_clean()` in `save()`.
- Don't use `.extra()`, or `.raw()` with string formatting.
- Don't import `config.settings.prod` anywhere.
