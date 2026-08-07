"""SQLite backend — the always-available path.

Standard library only. This is what the framework falls back to whenever a
managed machine turns out not to allow a database server, and it is a fully
supported destination, not a degraded mode.
"""

import os
import sqlite3

from .base import SQLBackend


class SQLiteBackend(SQLBackend):
    paramstyle = "qmark"

    def __init__(self, path):
        self.path = os.path.expanduser(path)
        self._conn = None

    @property
    def name(self):
        return "sqlite"

    def connect(self):
        if self._conn is None:
            parent = os.path.dirname(self.path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            self._conn = sqlite3.connect(self.path)
            # WAL survives an editor and a CLI touching the archive at once.
            # Some managed/network filesystems refuse it, so a failure here is
            # non-fatal — journal mode is an optimisation, not a requirement.
            try:
                self._conn.execute("PRAGMA journal_mode=WAL")
            except sqlite3.Error:
                pass
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def describe(self):
        return "sqlite: {}".format(self.path)
