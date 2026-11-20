"""Search published books by title or author."""

import sqlite3
from typing import Any

SORT_COLUMNS = {"title": "title", "year": "year DESC, title"}
MAX_RESULTS = 50


def escape_like(text: str) -> str:
    r"""Escape LIKE wildcards so % and _ match themselves (escape char: \)."""
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def search_books(
    conn: sqlite3.Connection, query: str, sort: str = "title"
) -> list[dict[str, Any]]:
    """Return published books whose title or author contains ``query``."""
    if sort not in SORT_COLUMNS:
        raise ValueError(f"sort must be one of {sorted(SORT_COLUMNS)}")
    order_by = SORT_COLUMNS[sort]  # from the allowlist above, never from input
    pattern = f"%{escape_like(query)}%"
    sql = (
        "SELECT title, author, year FROM books "  # noqa: S608 - see comment below
        "WHERE published = 1 "
        "AND (title LIKE ? ESCAPE '\\' OR author LIKE ? ESCAPE '\\') "
        f"ORDER BY {order_by} LIMIT ?"
    )
    # S608 is a false positive here: the only interpolated value is a constant
    # from SORT_COLUMNS; user input goes through the ? placeholders.
    rows = conn.execute(sql, (pattern, pattern, MAX_RESULTS)).fetchall()
    return [dict(row) for row in rows]
