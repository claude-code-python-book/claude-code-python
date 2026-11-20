# Chapter 14 — SQLAlchemy 2.0, Database Queries, and Alembic Migrations

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`loyalty-service`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-listing-14-1-the-sqlalchemy-conventions-in-claude-md.md`](snippets/01-listing-14-1-the-sqlalchemy-conventions-in-claude-md.md) | Listing 14-1: The SQLAlchemy conventions in CLAUDE.md | markdown | 2. Why Claude Code Helps with Database Code |
| [`02-prompt.txt`](snippets/02-prompt.txt) | Prompt | prompt | 3. Setting the Stage: Our Example Project |
| [`03-listing-14-2-the-loyalty-service-layout.txt`](snippets/03-listing-14-2-the-loyalty-service-layout.txt) | Listing 14-2: The loyalty-service layout | text | 3. Setting the Stage: Our Example Project |
| [`04-listing-14-3-points-for-order-in-loyalty-rules-py.py`](snippets/04-listing-14-3-points-for-order-in-loyalty-rules-py.py) | Listing 14-3: points_for_order() in loyalty/rules.py | python | 3. Setting the Stage: Our Example Project |
| [`05-output.txt`](snippets/05-output.txt) | Output | text | 3. Setting the Stage: Our Example Project |
| [`06-listing-14-4-the-base-class-customer-and-order-in-loyalty.py`](snippets/06-listing-14-4-the-base-class-customer-and-order-in-loyalty.py) | Listing 14-4: The base class, Customer and Order in loyalty/models.py | python | 4. Mapping Models with Mapped[] and mapped_column |
| [`07-output.txt`](snippets/07-output.txt) | Output | text | 4. Mapping Models with Mapped[] and mapped_column |
| [`08-listing-14-5-customers-with-orders-since-in-loyalty-servic.py`](snippets/08-listing-14-5-customers-with-orders-since-in-loyalty-servic.py) | Listing 14-5: customers_with_orders_since() in loyalty/service.py | python | 5. Relationships and Loading Strategies (selectinload, joinedload) |
| [`09-listing-14-6-a-statement-count-test-in-tests-db-test-servi.py`](snippets/09-listing-14-6-a-statement-count-test-in-tests-db-test-servi.py) | Listing 14-6: A statement-count test in tests/db/test_service.py | python | 5. Relationships and Loading Strategies (selectinload, joinedload) |
| [`10-listing-14-7-one-redemption-as-plain-sql-run-with-psql.sql`](snippets/10-listing-14-7-one-redemption-as-plain-sql-run-with-psql.sql) | Listing 14-7: One redemption, as plain SQL run with psql | sql | 6. Writing Queries in the 2.0 select() Style |
| [`11-output.txt`](snippets/11-output.txt) | Output | text | 6. Writing Queries in the 2.0 select() Style |
| [`12-listing-14-8-locked-account-in-loyalty-service-py.py`](snippets/12-listing-14-8-locked-account-in-loyalty-service-py.py) | Listing 14-8: locked_account() in loyalty/service.py | python | 6. Writing Queries in the 2.0 select() Style |
| [`13-code.py`](snippets/13-code.py) | Code | python | 6. Writing Queries in the 2.0 select() Style |
| [`14-output.txt`](snippets/14-output.txt) | Output | text | 6. Writing Queries in the 2.0 select() Style |
| [`15-code.py`](snippets/15-code.py) | Code | python | 7. Async SQLAlchemy with asyncpg |
| [`16-prompt.txt`](snippets/16-prompt.txt) | Prompt | prompt | 7. Async SQLAlchemy with asyncpg |
| [`17-listing-14-9-run-migrations-online-in-migrations-env-py.py`](snippets/17-listing-14-9-run-migrations-online-in-migrations-env-py.py) | Listing 14-9: run_migrations_online() in migrations/env.py | python | 8. Alembic Migrations in Depth: Autogenerate, Review, Data Migrations |
| [`18-output.txt`](snippets/18-output.txt) | Output | text | 8. Alembic Migrations in Depth: Autogenerate, Review, Data Migrations |
| [`19-listing-14-10-the-backfill-in-migrations-versions-0003-back.py`](snippets/19-listing-14-10-the-backfill-in-migrations-versions-0003-back.py) | Listing 14-10: The backfill in migrations/versions/0003_backfill_loyalty_tier.py | python | 8. Alembic Migrations in Depth: Autogenerate, Review, Data Migrations |
| [`20-output.txt`](snippets/20-output.txt) | Output | text | 8. Alembic Migrations in Depth: Autogenerate, Review, Data Migrations |
| [`21-output.txt`](snippets/21-output.txt) | Output | text | 8. Alembic Migrations in Depth: Autogenerate, Review, Data Migrations |
| [`22-output.txt`](snippets/22-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`23-output.txt`](snippets/23-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`24-output.txt`](snippets/24-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`25-output.txt`](snippets/25-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`26-output.txt`](snippets/26-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`27-output.txt`](snippets/27-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`28-listing-14-11-upgrade-in-migrations-versions-0004-index-ord.py`](snippets/28-listing-14-11-upgrade-in-migrations-versions-0004-index-ord.py) | Listing 14-11: upgrade() in migrations/versions/0004_index_orders_by_customer.py | python | 9. Zero-Downtime Migration Patterns |
| [`29-output.txt`](snippets/29-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`30-output.txt`](snippets/30-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`31-listing-14-12-upgrade-in-migrations-versions-0005-require-l.py`](snippets/31-listing-14-12-upgrade-in-migrations-versions-0005-require-l.py) | Listing 14-12: upgrade() in migrations/versions/0005_require_loyalty_tier.py | python | 9. Zero-Downtime Migration Patterns |
| [`32-output.txt`](snippets/32-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`33-output.txt`](snippets/33-output.txt) | Output | text | 9. Zero-Downtime Migration Patterns |
| [`34-code.py`](snippets/34-code.py) | Code | python | 10. Running and Verifying the Database Layer |
| [`35-output.txt`](snippets/35-output.txt) | Output | text | 10. Running and Verifying the Database Layer |
| [`36-output.txt`](snippets/36-output.txt) | Output | text | 10. Running and Verifying the Database Layer |
| [`37-listing-14-13-the-rollback-fixture-in-tests-db-conftest-py.py`](snippets/37-listing-14-13-the-rollback-fixture-in-tests-db-conftest-py.py) | Listing 14-13: The rollback fixture in tests/db/conftest.py | python | 10. Running and Verifying the Database Layer |
| [`38-output.txt`](snippets/38-output.txt) | Output | text | 10. Running and Verifying the Database Layer |
