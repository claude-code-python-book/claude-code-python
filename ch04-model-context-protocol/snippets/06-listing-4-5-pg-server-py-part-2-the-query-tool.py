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
