# Chapter 4 sample: MCP servers in Python

- `hello_server.py` (Listing 4-1) and `test_hello_server.py` (Listing 4-2)
- `setup_db.sql`: the `shop` database; its last part is Listing 4-3
- `pg_server.py`: Listings 4-4 and 4-5
- `api_bridge.py` (4-6), `mcp_connector.py` (4-7), `fastapi_app.py` (4-8)
- `.mcp.json`: the project-scoped server configuration

```bash
uv sync
uv run pytest test_hello_server.py -q
createdb shop && psql -d shop -f setup_db.sql        # as a PostgreSQL superuser
claude mcp add --transport stdio python-helper -- uv run hello_server.py
```

`checks/` runs `pg_server.py` against a real local PostgreSQL. It recreates
the `shop` database and the `mcp_reader` role, so use it on a development
machine only: `uv run pytest checks -q`.
