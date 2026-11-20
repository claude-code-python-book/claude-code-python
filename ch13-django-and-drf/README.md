# Chapter 13 — Django and Django REST Framework

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`ch13-sample`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-listing-13-1-where-things-go-and-the-django-conventions-in.md`](snippets/01-listing-13-1-where-things-go-and-the-django-conventions-in.md) | Listing 13-1: Where things go, and the Django conventions, in CLAUDE.md | markdown | 2. Teaching Claude Django Conventions in CLAUDE.md |
| [`02-prompt.txt`](snippets/02-prompt.txt) | Prompt | prompt | 2. Teaching Claude Django Conventions in CLAUDE.md |
| [`03-listing-13-2-the-bookings-site-layout.txt`](snippets/03-listing-13-2-the-bookings-site-layout.txt) | Listing 13-2: The bookings-site layout | text | 2. Teaching Claude Django Conventions in CLAUDE.md |
| [`04-listing-13-3-the-booking-rules-in-bookings-rules-py.py`](snippets/04-listing-13-3-the-booking-rules-in-bookings-rules-py.py) | Listing 13-3: The booking rules in bookings/rules.py | python | 3. Scaffolding an App: Models, Admin, URLs |
| [`05-output.txt`](snippets/05-output.txt) | Output | text | 3. Scaffolding an App: Models, Admin, URLs |
| [`06-output.txt`](snippets/06-output.txt) | Output | text | 3. Scaffolding an App: Models, Admin, URLs |
| [`07-listing-13-4-the-booking-model-in-bookings-models-py.py`](snippets/07-listing-13-4-the-booking-model-in-bookings-models-py.py) | Listing 13-4: The Booking model in bookings/models.py | python | 3. Scaffolding an App: Models, Admin, URLs |
| [`08-listing-13-5-a-first-draft-model-and-what-ruff-s-django-ru.py`](snippets/08-listing-13-5-a-first-draft-model-and-what-ruff-s-django-ru.py) | Listing 13-5: A first-draft model, and what Ruff's Django rules say | python | 3. Scaffolding an App: Models, Admin, URLs |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 3. Scaffolding an App: Models, Admin, URLs |
| [`10-code.py`](snippets/10-code.py) | Code | python | 3. Scaffolding an App: Models, Admin, URLs |
| [`11-code.py`](snippets/11-code.py) | Code | python | 3. Scaffolding an App: Models, Admin, URLs |
| [`12-listing-13-6-bookingserializer-in-bookings-serializers-py.py`](snippets/12-listing-13-6-bookingserializer-in-bookings-serializers-py.py) | Listing 13-6: BookingSerializer in bookings/serializers.py | python | 4. DRF Serializers, ViewSets, and Routers |
| [`13-listing-13-7-bookingviewset-in-bookings-views-py.py`](snippets/13-listing-13-7-bookingviewset-in-bookings-views-py.py) | Listing 13-7: BookingViewSet in bookings/views.py | python | 4. DRF Serializers, ViewSets, and Routers |
| [`14-code.py`](snippets/14-code.py) | Code | python | 5. Permissions and Authentication |
| [`15-code.py`](snippets/15-code.py) | Code | python | 5. Permissions and Authentication |
| [`16-listing-13-8-a-query-count-test-in-tests-django-test-api-p.py`](snippets/16-listing-13-8-a-query-count-test-in-tests-django-test-api-p.py) | Listing 13-8: A query-count test in tests/django/test_api.py | python | 6. Querysets: select_related, prefetch_related, and the N+1 Trap |
| [`17-code.py`](snippets/17-code.py) | Code | python | 6. Querysets: select_related, prefetch_related, and the N+1 Trap |
| [`18-output.txt`](snippets/18-output.txt) | Output | text | 6. Querysets: select_related, prefetch_related, and the N+1 Trap |
| [`19-code.py`](snippets/19-code.py) | Code | python | 7. Signals, Management Commands, and Settings Splits |
| [`20-code.py`](snippets/20-code.py) | Code | python | 7. Signals, Management Commands, and Settings Splits |
| [`21-listing-13-9-bookings-management-commands-purge-cancelled.py`](snippets/21-listing-13-9-bookings-management-commands-purge-cancelled.py) | Listing 13-9: bookings/management/commands/purge_cancelled.py | python | 7. Signals, Management Commands, and Settings Splits |
| [`22-listing-13-10-config-settings-prod-py.py`](snippets/22-listing-13-10-config-settings-prod-py.py) | Listing 13-10: config/settings/prod.py | python | 7. Signals, Management Commands, and Settings Splits |
| [`23-listing-13-11-bookings-migrations-0001-btree-gist-py.py`](snippets/23-listing-13-11-bookings-migrations-0001-btree-gist-py.py) | Listing 13-11: bookings/migrations/0001_btree_gist.py | python | 8. Django Migrations: Generating, Reviewing, Squashing |
| [`24-listing-13-12-claude-hooks-guard-migrations-py.py`](snippets/24-listing-13-12-claude-hooks-guard-migrations-py.py) | Listing 13-12: .claude/hooks/guard_migrations.py | python | 8. Django Migrations: Generating, Reviewing, Squashing |
| [`25-code.json`](snippets/25-code.json) | Code | json | 8. Django Migrations: Generating, Reviewing, Squashing |
| [`26-listing-13-13-tests-django-factories-py.py`](snippets/26-listing-13-13-tests-django-factories-py.py) | Listing 13-13: tests/django/factories.py | python | 9. Testing with pytest-django and Factory Boy |
| [`27-code.py`](snippets/27-code.py) | Code | python | 9. Testing with pytest-django and Factory Boy |
| [`28-code.py`](snippets/28-code.py) | Code | python | 9. Testing with pytest-django and Factory Boy |
| [`29-code.py`](snippets/29-code.py) | Code | python | 9. Testing with pytest-django and Factory Boy |
| [`30-output.txt`](snippets/30-output.txt) | Output | text | 9. Testing with pytest-django and Factory Boy |
| [`31-prompt.txt`](snippets/31-prompt.txt) | Prompt | prompt | 10. End-to-End Example: A Bookings Feature |
| [`32-listing-13-14-free-slots-in-bookings-rules-py.py`](snippets/32-listing-13-14-free-slots-in-bookings-rules-py.py) | Listing 13-14: free_slots() in bookings/rules.py | python | 10. End-to-End Example: A Bookings Feature |
| [`33-output.txt`](snippets/33-output.txt) | Output | text | 10. End-to-End Example: A Bookings Feature |
| [`34-listing-13-15-the-availability-action-in-bookings-views-py.py`](snippets/34-listing-13-15-the-availability-action-in-bookings-views-py.py) | Listing 13-15: The availability action in bookings/views.py | python | 10. End-to-End Example: A Bookings Feature |
