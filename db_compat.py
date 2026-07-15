"""Turso/libsql compatibility shim.

The `libsql` package's remote (over-the-wire) client is Connection.execute()
/Cursor.fetchone()/fetchall()-compatible with sqlite3, but does NOT implement
`row_factory` or `executescript` (confirmed against tursodatabase/libsql-python
docs/api.md) — both of which this codebase relies on everywhere (`row["col"]`
access, and database.py's schema executescript). This module wraps a raw
libsql connection so call sites never notice the difference from sqlite3.

Used only when TURSO_DATABASE_URL is set (production); local dev keeps using
sqlite3 directly via database.py's get_db().
"""


class Row:
    """Mimics sqlite3.Row: supports row["col"] and row[0] access."""

    __slots__ = ("_values", "_index")

    def __init__(self, columns, values):
        self._values = tuple(values)
        self._index = {name: i for i, name in enumerate(columns)}

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._values[self._index[key]]
        return self._values[key]

    def keys(self):
        return list(self._index.keys())

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return repr(dict(zip(self._index.keys(), self._values)))


class CursorWrapper:
    def __init__(self, cursor):
        self._cursor = cursor

    def _wrap(self, row):
        if row is None:
            return None
        columns = [d[0] for d in self._cursor.description]
        return Row(columns, row)

    def fetchone(self):
        return self._wrap(self._cursor.fetchone())

    def fetchall(self):
        return [self._wrap(r) for r in self._cursor.fetchall()]

    def fetchmany(self, size=None):
        rows = self._cursor.fetchmany(size) if size is not None else self._cursor.fetchmany()
        return [self._wrap(r) for r in rows]

    def __iter__(self):
        for r in self._cursor:
            yield self._wrap(r)


class ConnectionWrapper:
    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql, params=()):
        return CursorWrapper(self._conn.execute(sql, params))

    def executemany(self, sql, params_list):
        return CursorWrapper(self._conn.executemany(sql, params_list))

    def executescript(self, script):
        """libsql has no executescript(); split on ';' and run each
        statement. Safe here because the schema has no semicolons inside
        string literals/defaults."""
        for statement in script.split(";"):
            statement = statement.strip()
            if statement:
                self._conn.execute(statement)

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


def connect(database_url: str, auth_token: str) -> ConnectionWrapper:
    import libsql

    conn = libsql.connect(database=database_url, auth_token=auth_token)
    return ConnectionWrapper(conn)
