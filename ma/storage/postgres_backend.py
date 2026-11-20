"""PostgreSQL backend — used only when the environment genuinely allows it.

Requires a driver (``psycopg`` v3 or ``psycopg2``) that may not be installable on
a managed machine, so the import is deferred to ``connect`` and its absence is
reported as a clear, actionable error rather than an ImportError at startup.
"""

import re
from urllib.parse import unquote

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

# A key/value DSN's password, matched the way libpq reads values: quoted
# ('my \'secret\'', spaces allowed) or unquoted, where a backslash escapes the
# next character (`pass\ word` is one value). An unterminated quote masks
# everything after it rather than leaking the tail.
_KV_PASSWORD = re.compile(
    r"""(\bpassword\s*=\s*)('(?:[^'\\]|\\.)*(?:'|$)|(?:\\.|[^\s\\])+\\?)""",
    re.IGNORECASE,
)
_URI_SCHEMES = ("postgresql://", "postgres://")


def _scrub_dsn(dsn):
    """Return the DSN with any password replaced by ``***``.

    Covers both forms libpq accepts: a URI (``postgresql://user:pw@host/db``,
    including a ``password=`` query parameter) and a key/value string
    (``host=db user=me password=pw``). It splits the string the way libpq
    does, not the way a web URL parser would, and when in doubt hides more
    rather than less. Used before a DSN is printed or logged.
    """
    if not dsn:
        return dsn
    if dsn.lower().startswith(_URI_SCHEMES):
        return _scrub_uri(dsn)
    return _KV_PASSWORD.sub(lambda m: m.group(1) + _MASK, dsn)


def _scrub_uri(dsn):
    scheme, _, rest = dsn.partition("://")
    # Userinfo: libpq takes everything before the last '@' as user[:password].
    # Using the last '@' in the whole string means a password holding '@', '#',
    # '/' or '?' is still covered; at worst more than the password is masked.
    at = rest.rfind("@")
    if at != -1 and ":" in rest[:at]:
        user = rest[:at].split(":", 1)[0]
        rest = user + ":" + _MASK + rest[at:]
    # Query: everything after the first '?'. '#' is ordinary data to libpq.
    head, sep, query = rest.partition("?")
    if sep:
        pairs = []
        for pair in query.split("&"):
            key = pair.split("=", 1)[0]
            pairs.append(key + "=" + _MASK if unquote(key).strip().lower() == "password" else pair)
        rest = head + "?" + "&".join(pairs)
    return scheme + "://" + rest
