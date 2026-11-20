uv run uvicorn fastapi_app:app --host 127.0.0.1 --port 8000
claude mcp add --transport http shop-db-http http://127.0.0.1:8000/mcp
