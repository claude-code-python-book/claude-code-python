"""SQLite schema and seed data for the catalogue."""

import sqlite3

SCHEMA = """
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL,
    published INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE api_keys (owner TEXT NOT NULL, key TEXT NOT NULL);
"""

BOOKS = [
    ("Fluent Python", "Luciano Ramalho", 2022, 1),
    ("Python Testing with pytest", "Brian Okken", 2022, 1),
    ("Robust Python", "Patrick Viafore", 2021, 1),
    ("Architecture Patterns with Python", "Harry Percival", 2020, 1),
    ("100% Coverage, 0% Bugs", "Draft Author", 2026, 0),
    ("Untitled sequel", "Draft Author", 2027, 0),
]


def connect(path: str = ":memory:") -> sqlite3.Connection:
    """Open the database and create and seed it if it is empty."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    if not conn.execute("SELECT name FROM sqlite_master WHERE name='books'").fetchone():
        conn.executescript(SCHEMA)
        conn.executemany(
            "INSERT INTO books (title, author, year, published) VALUES (?, ?, ?, ?)",
            BOOKS,
        )
        conn.execute("INSERT INTO api_keys VALUES ('billing', 'sk_live_example_123')")
        conn.commit()
    return conn
