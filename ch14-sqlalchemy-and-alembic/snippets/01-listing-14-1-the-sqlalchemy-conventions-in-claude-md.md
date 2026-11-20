## SQLAlchemy conventions

- 2.0 style only: `select()`, `session.scalars()`, `session.get()`. Never
  `session.query()`; it is the legacy API.
- Models use `Mapped[]` and `mapped_column()`. Nullability comes from the
  annotation: `Mapped[str | None]` is NULL, `Mapped[str]` is NOT NULL.
- Relationships are `lazy="raise"`. Load what you need in the query:
  `selectinload()` for collections, `joinedload()` for many-to-one.
- Service functions take an `AsyncSession` already in a transaction and
  never commit. Callers use `async with Session.begin() as session:`.
- One `AsyncSession` per request or task; never share one between tasks.
- Lock before read-modify-write on a balance: `locked_account()`.
- Money is `Decimal` and `Numeric(12, 2)`. Times are timezone-aware.
- No string-built SQL. Use bound parameters, even in `text()`.

## Migrations

- One migration per change, generated with `--autogenerate`, then read
  line by line: autogenerate sees a rename as a drop plus an add.
- Never edit a migration that has been merged; write a new one.
- Big tables: indexes `postgresql_concurrently=True` inside
  `autocommit_block()`; NOT NULL via a validated `CHECK ... NOT VALID`.
- Removing or renaming a column takes two releases: expand, then contract.
- Data migrations copy the values they need. Never import from `loyalty`.
- Every migration has a working `downgrade()`, or says why it can't.
