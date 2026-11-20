"""Checks for the Chapter 4 code against a real PostgreSQL.

Needs a local PostgreSQL you can administer (createdb/psql). Run from the
chapter folder:  uv run pytest checks -q
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
URL = "postgresql://mcp_reader:change-me@localhost:5432/shop"
pytestmark = pytest.mark.skipif(shutil.which("psql") is None, reason="needs psql")


def psql(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["psql", "-X", "-v", "ON_ERROR_STOP=1", *args],
                          capture_output=True, text=True, check=check)


@pytest.fixture(scope="module")
def shop_db():
    subprocess.run(["dropdb", "--if-exists", "shop"], check=True)
    subprocess.run(["psql", "-X", "-d", "postgres", "-c", "DROP ROLE IF EXISTS mcp_reader"],
                   check=True, capture_output=True)
    subprocess.run(["createdb", "shop"], check=True)
    psql("-d", "shop", "-f", str(ROOT / "setup_db.sql"))
    yield URL


def test_setup_creates_tables_and_a_read_only_role(shop_db):
    r = psql(shop_db, "--csv", "-c", "SELECT count(*) AS n FROM orders")
    assert r.stdout.splitlines()[1] == "5"
    r = psql(shop_db, "-c", "INSERT INTO customers (name, email) VALUES ('x', 'x@x')",
             check=False)
    assert "read-only transaction" in r.stderr
    r = psql(shop_db, "-At", "-c", "SHOW statement_timeout")
    assert r.stdout.strip() == "5s"


@pytest.fixture
def pg_server(shop_db, monkeypatch):
    sys.path.insert(0, str(Path(__file__).parent))
    import fake_psycopg
    monkeypatch.setitem(sys.modules, "psycopg", fake_psycopg)
    monkeypatch.setitem(sys.modules, "psycopg.rows", fake_psycopg.rows)
    monkeypatch.setenv("SHOP_DB_URL", shop_db)
    sys.path.insert(0, str(ROOT))
    sys.modules.pop("pg_server", None)
    import pg_server
    return pg_server


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_pg_server_over_mcp(pg_server):
    from mcp import Client
    from mcp.server.mcpserver.exceptions import ToolError  # noqa: F401
    async with Client(pg_server.mcp) as client:
        tables = await client.read_resource("postgres://tables")
        assert json.loads(tables.contents[0].text) == ["customers", "orders"]
        schema = await client.read_resource("postgres://tables/orders/schema")
        assert '"column_name": "total"' in schema.contents[0].text
        r = await client.call_tool("run_query", {"sql": (
            "SELECT c.name, sum(o.total) AS spent FROM customers c "
            "JOIN orders o ON o.customer_id = c.id GROUP BY c.name ORDER BY spent DESC")})
        rows = json.loads(r.content[0].text)
        assert rows[0]["name"] == "Ben Okafor" and not r.is_error
        r = await client.call_tool("run_query", {"sql": "DELETE FROM orders"})
        assert r.is_error and "Only a single SELECT" in r.content[0].text
        r = await client.call_tool("run_query", {"sql": "SELECT 1; DROP TABLE orders"})
        assert r.is_error
        r = await client.call_tool("run_query", {"sql": (
            "WITH d AS (DELETE FROM orders RETURNING *) SELECT * FROM d")})
        assert r.is_error and "read-only transaction" in r.content[0].text
        r = await client.call_tool("run_query", {"sql": "SELECT * FROM nope"})
        assert r.is_error and "Database error" in r.content[0].text


def test_hello_server_tests_pass():
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        "test_hello_server.py"], cwd=ROOT, capture_output=True, text=True)
    assert "2 passed" in r.stdout, r.stdout
