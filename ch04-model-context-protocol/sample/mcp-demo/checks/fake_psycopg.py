"""Test-only stand-in for psycopg that runs each query through the real `psql`.

psycopg isn't installed where these checks were run, so this shim lets the
unchanged pg_server.py talk to a real PostgreSQL. Install psycopg to use the
server for real: uv add "psycopg[binary]".
"""
import csv
import io
import subprocess
from types import SimpleNamespace


class Error(Exception):
    pass


def _literal(value: str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


class _Cursor:
    def __init__(self, rows: list[dict[str, str]]) -> None:
        self.rows = rows

    def fetchmany(self, size: int) -> list[dict[str, str]]:
        return self.rows[:size]


class _Conn:
    def __init__(self, url: str) -> None:
        self.url = url

    def __enter__(self) -> "_Conn":
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def execute(self, sql: str, params: tuple[str, ...] | None = None) -> _Cursor:
        if params:
            sql = sql % tuple(_literal(p) for p in params)
        r = subprocess.run(["psql", self.url, "--csv", "-X", "-v", "ON_ERROR_STOP=1",
                            "-c", sql], capture_output=True, text=True)
        if r.returncode:
            raise Error(r.stderr.strip())
        return _Cursor(list(csv.DictReader(io.StringIO(r.stdout))))


def connect(url: str, **_: object) -> _Conn:
    return _Conn(url)


rows = SimpleNamespace(dict_row=object())
