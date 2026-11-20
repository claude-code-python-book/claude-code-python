claude mcp add --transport stdio python-helper -- uv run hello_server.py
claude mcp add --env SHOP_DB_URL=postgresql://mcp_reader:change-me@localhost:5432/shop \
  --transport stdio shop-db -- uv run pg_server.py
