"""Expose a PostgreSQL database to MCP clients, read-only.

Run it with:  SHOP_DB_URL=postgresql://... uv run pg_server.py
Needs:        uv add "mcp[cli]" "psycopg[binary]"
"""
import json
import os
import re
from typing import Any

import psycopg
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ResourceError, ToolError
from psycopg.rows import dict_row

DB_URL = os.environ["SHOP_DB_URL"]       # postgresql://mcp_reader:...@host/shop
MAX_ROWS = 100
SELECT_ONLY = re.compile(r"^\s*(select|with)\b", re.IGNORECASE)

mcp = MCPServer(
    "shop-db",
    instructions="Read-only access to the shop database. "
                 "Read postgres://tables before writing a query.",
)

def fetch(sql: str, params: tuple[str, ...] | None = None) -> list[dict[str, Any]]:
    """Run one statement and return at most MAX_ROWS rows as dicts."""
    with psycopg.connect(DB_URL, autocommit=True, row_factory=dict_row) as conn:
        return conn.execute(sql, params).fetchmany(MAX_ROWS)

@mcp.resource("postgres://tables")
def list_tables() -> str:
    """The tables in the public schema."""
    rows = fetch("SELECT table_name FROM information_schema.tables "
                 "WHERE table_schema = 'public' AND table_type = 'BASE TABLE' "
                 "ORDER BY table_name")
    return json.dumps([row["table_name"] for row in rows])

@mcp.resource("postgres://tables/{table}/schema")
def table_schema(table: str) -> str:
    """Column names, types and nullability for one table."""
    rows = fetch("SELECT column_name, data_type, is_nullable "
                 "FROM information_schema.columns "
                 "WHERE table_schema = 'public' AND table_name = %s "
                 "ORDER BY ordinal_position", (table,))
    if not rows:
        raise ResourceError(f"No table named {table!r}")
    return json.dumps(rows, indent=2)

@mcp.tool()
def run_query(sql: str) -> str:
    """Run one read-only SELECT query on the shop database.

    Returns at most 100 rows as JSON. Read postgres://tables first.
    """
    if not SELECT_ONLY.match(sql) or ";" in sql.strip().rstrip(";"):
        raise ToolError("Only a single SELECT (or WITH ... SELECT) is allowed.")
    try:
        rows = fetch(sql)
    except psycopg.Error as exc:
        raise ToolError(f"Database error: {exc}") from exc
    return json.dumps(rows, default=str, indent=2)

if __name__ == "__main__":
    mcp.run()
