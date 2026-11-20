# Chapter 13 sample: bookings-site

Django 6.1 + Django REST framework 3.18 + PostgreSQL, with git history:
  481f50d  Scaffold the bookings app: rules, models, constraints, admin
  683b9a6  Add the API: serializers, viewsets, permissions, tests
  7b67fd7  Teach Claude the project: CLAUDE.md, migrations hook, README

See bookings-site/README.md to run it. The 25 tests in tests/test_rules.py and
tests/test_guard_migrations.py were run while writing the chapter; the tests in
tests/django/ need Django, DRF, pytest-django, Factory Boy and PostgreSQL.
