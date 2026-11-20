"""Search behaviour, including the injection payloads that once worked."""

import sqlite3

import pytest

from bookfinder.search import escape_like, search_books

PAYLOADS = [
    "' OR '1'='1",
    "x' UNION SELECT owner, key, 0 FROM api_keys --",
    "'; DROP TABLE books; --",
]


def titles(rows: list[dict[str, object]]) -> list[object]:
    return [row["title"] for row in rows]


def test_finds_published_books_by_title_or_author(conn: sqlite3.Connection) -> None:
    assert titles(search_books(conn, "pytest")) == ["Python Testing with pytest"]
    assert titles(search_books(conn, "Ramalho")) == ["Fluent Python"]


def test_unpublished_books_stay_hidden(conn: sqlite3.Connection) -> None:
    assert search_books(conn, "Draft") == []


@pytest.mark.parametrize("payload", PAYLOADS)
def test_injection_payloads_are_just_text(
    conn: sqlite3.Connection, payload: str
) -> None:
    assert search_books(conn, payload) == []
    assert conn.execute("SELECT count(*) FROM books").fetchone()[0] == 6


def test_like_wildcards_match_literally(conn: sqlite3.Connection) -> None:
    assert search_books(conn, "%") == []  # "100% Coverage" is unpublished
    assert search_books(conn, "_") == []
    assert escape_like("50%_off\\") == "50\\%\\_off\\\\"


def test_sort_must_come_from_the_allowlist(conn: sqlite3.Connection) -> None:
    assert titles(search_books(conn, "Python", sort="year"))[0] == "Fluent Python"
    with pytest.raises(ValueError, match="sort must be one of"):
        search_books(conn, "Python", sort="year; DROP TABLE books")
