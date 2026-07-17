import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import database


@pytest.fixture
def db_conn(tmp_path, monkeypatch):
    """Fresh sqlite DB per test, using the app's real schema (database.init_db())."""
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    database.init_db()
    conn = database.get_db()
    yield conn
    conn.close()
