@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    """Yield a session whose work is rolled back after the test."""
    engine = create_async_engine(APP_URL, poolclass=NullPool)
    async with engine.connect() as connection:
        transaction = await connection.begin()
        async with AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False,
        ) as session:
            yield session
        await transaction.rollback()
    await engine.dispose()
