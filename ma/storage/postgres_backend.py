"""PostgreSQL backend — used only when the environment genuinely allows it.

Requires a driver (``psycopg`` v3 or ``psycopg2``) that may not be installable on
a managed machine, so the import is deferred to ``connect`` and its absence is
reported as a clear, actionable error rather than an ImportError at startup.
"""

import re
from urllib.parse import urlsplit, urlunsplit

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


_MASK = "***"

# A key/value DSN's password: `password=secret` or `password = 'it''s secret'`.
# Quoted values may hold spaces and backslash-escaped quotes (libpq rules).
_KV_PASSWORD = re.compile(r"""(\bpassword\s*=\s*)('(?:[^'\\]|\\.)*'|\S+)""", re.IGNORECASE)


def _scrub_dsn(dsn):
    """Return the DSN with any password replaced by ``***``.

    Covers both forms libpq accepts: a URI (``postgresql://user:pw@host/db``,
    including a ``password=`` query parameter) and a key/value string
    (``host=db user=me password=pw``). Used before a DSN is printed or logged.
    """
    if not dsn:
        return dsn
    if dsn.startswith(("postgresql://", "postgres://")):
        return _scrub_uri(dsn)
    return _KV_PASSWORD.sub(lambda m: m.group(1) + _MASK, dsn)


def _scrub_uri(dsn):
    parts = urlsplit(dsn)
    netloc = parts.netloc
    if "@" in netloc:
        userinfo, _, hosts = netloc.rpartition("@")
        if ":" in userinfo:
            userinfo = userinfo.split(":", 1)[0] + ":" + _MASK
        netloc = userinfo + "@" + hosts
    query = "&".join(
        (pair.split("=", 1)[0] + "=" + _MASK)
        if pair.split("=", 1)[0].lower() == "password" else pair
        for pair in parts.query.split("&")
    ) if parts.query else parts.query
    return urlunsplit((parts.scheme, netloc, parts.path, query, parts.fragment))
