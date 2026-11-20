import sqlite3


def search_books(conn: sqlite3.Connection, query: str, sort: str = "title") -> list[dict]:
    pattern = f"%{query}%"
    sql = (
        "SELECT title, author, year FROM books WHERE published = 1 "
        f"AND (title LIKE ? OR author LIKE ?) ORDER BY {sort}"
    )
    return [dict(row) for row in conn.execute(sql, (pattern, pattern)).fetchall()]
