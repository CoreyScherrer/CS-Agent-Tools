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

# A key/value DSN's password (or sslpassword), matched the way libpq reads values: quoted
# ('my \'secret\'', spaces allowed) or unquoted, where a backslash escapes the
# next character (`pass\ word` is one value). An unterminated quote masks
# everything after it rather than leaking the tail.
_KV_PASSWORD = re.compile(
    r"""(\b\w*password\s*=\s*)('(?:[^'\\]|\\.)*(?:'|$)|(?:\\.|[^\s\\])+\\?)""",
    re.IGNORECASE | re.DOTALL,  # a backslash escapes any character, newline included
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


# A query pair anywhere in a URI: `?key=value` or `&key=value`. The value runs to
# the next '&', so it may hold '@', '?', '#' or '/'.
_URI_PAIR = re.compile(r"[?&]([^&?=]*)=([^&]*)")


def _scrub_uri(dsn):
    """Mask every span that could be a password, under any plausible reading.

    A URI password can sit in the userinfo (`user:pw@host`) or in a query pair
    (`?password=pw`), and '@', '?', '#' or '/' inside either one can move where
    a parser thinks the parts begin. So both readings are taken from the raw
    string and every span either one calls a password is masked. When they
    disagree, more is hidden than strictly needed, never less.
    """
    scheme, _, rest = dsn.partition("://")
    spans = []
    # Userinfo: from the first ':' to the last '@' (libpq takes the last '@').
    colon, at = rest.find(":"), rest.rfind("@")
    if colon != -1 and colon < at:
        spans.append((colon + 1, at))
    # Query values whose key decodes to something ending in "password".
    for m in _URI_PAIR.finditer(rest):
        if unquote(m.group(1)).strip().lower().endswith("password"):
            spans.append((m.start(2), m.end(2)))
    out, pos = [], 0
    for start, end in sorted(spans):
        if end <= pos:
            continue
        start = max(start, pos)
        out.append(rest[pos:start] + _MASK)
        pos = end
    out.append(rest[pos:])
    return scheme + "://" + "".join(out)
