import sqlite3


def search_books(conn: sqlite3.Connection, query: str, sort: str = "title") -> list[dict]:
    sql = (
        "SELECT title, author, year FROM books WHERE published = 1 "
        f"AND (title LIKE '%{query}%' OR author LIKE '%{query}%') ORDER BY {sort}"
    )
    return [dict(row) for row in conn.execute(sql).fetchall()]
