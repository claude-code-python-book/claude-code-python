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
