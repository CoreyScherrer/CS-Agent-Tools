"""PostgreSQL backend — used only when the environment genuinely allows it.

Requires a driver (``psycopg`` v3 or ``psycopg2``) that may not be installable on
a managed machine, so the import is deferred to ``connect`` and its absence is
reported as a clear, actionable error rather than an ImportError at startup.
"""

from .base import SQLBackend


def driver_available():
    """True when some psycopg is importable. Used by `doctor`, never assumed."""
    try:
        import psycopg  # noqa: F401
        return True
    except ImportError:
        pass
    try:
        import psycopg2  # noqa: F401
        return True
    except ImportError:
        return False


def _load_driver():
    try:
        import psycopg
        return psycopg, 3
    except ImportError:
        pass
    try:
        import psycopg2
        return psycopg2, 2
    except ImportError as exc:
        raise RuntimeError(
            "PostgreSQL backend selected but no driver is installed.\n"
            "Install one (`pip install psycopg[binary]`) or switch to SQLite by "
            "setting storage.backend to 'sqlite' in config.local.json."
        ) from exc


class PostgresBackend(SQLBackend):
    paramstyle = "pyformat"

    def __init__(self, dsn):
        self.dsn = dsn
        self._conn = None

    @property
    def name(self):
        return "postgres"

    def connect(self):
        if self._conn is None:
            driver, _version = _load_driver()
            self._conn = driver.connect(self.dsn)
        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def describe(self):
        return "postgres: {}".format(_scrub_dsn(self.dsn))


def _scrub_dsn(dsn):
    """Strip any password before a DSN is printed or logged."""
    if "@" not in dsn:
        return dsn
    head, _, tail = dsn.rpartition("@")
    if ":" in head:
        prefix, _, _secret = head.rpartition(":")
        return "{}:***@{}".format(prefix, tail)
    return "{}@{}".format(head, tail)
