from sqlalchemy import text


async def find_customer(session, email: str):
    sql = text(f"SELECT * FROM customers WHERE email = '{email}'")
    return (await session.execute(sql)).first()


async def orders_since(session, customer_id: int, days: int):
    sql = "SELECT * FROM orders WHERE customer_id = %s AND total > %s"
    return (await session.execute(text(sql % (customer_id, days)))).all()
