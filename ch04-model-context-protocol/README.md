# Chapter 4 — Model Context Protocol (MCP) with Python

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`mcp-demo`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-terminal.sh`](snippets/01-terminal.sh) | Terminal | bash | 5. Building Your First MCP Server with the Python SDK (FastMCP) |
| [`02-listing-4-1-hello-server-py-one-tool-one-resource-and-one.py`](snippets/02-listing-4-1-hello-server-py-one-tool-one-resource-and-one.py) | Listing 4-1: hello_server.py — one tool, one resource and one prompt | python | 5. Building Your First MCP Server with the Python SDK (FastMCP) |
| [`03-listing-4-2-test-hello-server-py-testing-the-server-in-me.py`](snippets/03-listing-4-2-test-hello-server-py-testing-the-server-in-me.py) | Listing 4-2: test_hello_server.py — testing the server in memory | python | 5. Building Your First MCP Server with the Python SDK (FastMCP) |
| [`04-listing-4-3-setup-db-sql-the-read-only-role.sql`](snippets/04-listing-4-3-setup-db-sql-the-read-only-role.sql) | Listing 4-3: setup_db.sql (the read-only role) | sql | 6. Exposing a PostgreSQL Database as an MCP Resource |
| [`05-listing-4-4-pg-server-py-part-1-settings-a-helper-and-two.py`](snippets/05-listing-4-4-pg-server-py-part-1-settings-a-helper-and-two.py) | Listing 4-4: pg_server.py, part 1 — settings, a helper and two resources | python | 6. Exposing a PostgreSQL Database as an MCP Resource |
| [`06-listing-4-5-pg-server-py-part-2-the-query-tool.py`](snippets/06-listing-4-5-pg-server-py-part-2-the-query-tool.py) | Listing 4-5: pg_server.py, part 2 — the query tool | python | 6. Exposing a PostgreSQL Database as an MCP Resource |
| [`07-terminal.sh`](snippets/07-terminal.sh) | Terminal | bash | 7. Connecting Your Server to Claude Code |
| [`08-code.json`](snippets/08-code.json) | Code | json | 7. Connecting Your Server to Claude Code |
| [`09-listing-4-6-api-bridge-py-claude-uses-a-local-mcp-server.py`](snippets/09-listing-4-6-api-bridge-py-claude-uses-a-local-mcp-server.py) | Listing 4-6: api_bridge.py — Claude uses a local MCP server's tools | python | 8. Calling MCP Tools from Python via the Claude API |
| [`10-listing-4-7-mcp-connector-py-the-api-connects-to-a-remote.py`](snippets/10-listing-4-7-mcp-connector-py-the-api-connects-to-a-remote.py) | Listing 4-7: mcp_connector.py — the API connects to a remote server | python | 8. Calling MCP Tools from Python via the Claude API |
| [`11-listing-4-8-fastapi-app-py-the-shop-db-server-inside-fast.py`](snippets/11-listing-4-8-fastapi-app-py-the-shop-db-server-inside-fast.py) | Listing 4-8: fastapi_app.py — the shop-db server inside FastAPI | python | 9. Mounting an MCP Server Inside a FastAPI App |
| [`12-terminal.sh`](snippets/12-terminal.sh) | Terminal | bash | 9. Mounting an MCP Server Inside a FastAPI App |
