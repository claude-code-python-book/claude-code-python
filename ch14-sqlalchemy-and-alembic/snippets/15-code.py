Session = make_sessionmaker(make_engine())  # from loyalty/db.py

async with Session.begin() as session:  # commits on success, rolls back on error
    points = await record_order(session, customer_id, Decimal("120.50"), placed_at)
