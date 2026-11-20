import sqlite3
from collections.abc import Iterator

import pytest

from bookfinder.db import connect


@pytest.fixture
def conn() -> Iterator[sqlite3.Connection]:
    db = connect()
    yield db
    db.close()
