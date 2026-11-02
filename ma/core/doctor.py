"""Environment discovery.

The framework is designed for a machine whose capabilities are unknown and
cannot be verified in advance, so it probes rather than assumes.

Two hard rules:

1. **No probe may abort the run.** Every probe is wrapped; an unexpected
   environment must produce a report, not a traceback. A doctor that crashes on
   a surprising machine is worse than no doctor.
2. **Probing is read-only.** Nothing is installed, no service is started, no
   file outside the repo is written.
"""

import json
import os
import platform
import shutil
import socket
import subprocess
import sys

PROBE_TIMEOUT = 5

OK = "ok"
WARN = "warn"
FAIL = "fail"
SKIP = "skip"


class Probe:
    def __init__(self, key, status, summary, detail=None):
        self.key = key
        self.status = status
        self.summary = summary
        self.detail = detail or {}

    def as_dict(self):
        return {
            "key": self.key,
            "status": self.status,
            "summary": self.summary,
            "detail": self.detail,
        }


def _safe(key, fn):
    """Run a probe so that any failure becomes a result rather than an exception."""
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001 - deliberate: unknown environment
        return Probe(key, WARN, "probe failed: {}".format(exc.__class__.__name__),
                     {"error": str(exc)})


def _run(cmd, timeout=PROBE_TIMEOUT):
    """Run a command, returning (rc, stdout+stderr). Never raises."""
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False,
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, str(exc)


# ---- individual probes --------------------------------------------------

def probe_python():
    version = sys.version_info
    supported = version >= (3, 9)
    return Probe(
        "python",
        OK if supported else FAIL,
        "Python {}.{}.{}".format(version.major, version.minor, version.micro),
        {
            "executable": sys.executable,
            "supported": supported,
            "platform": platform.platform(),
        },
    )


def probe_pip():
    """Whether packages can be installed — often proxied or blocked."""
    rc, out = _run([sys.executable, "-m", "pip", "--version"])
    if rc != 0:
        return Probe("pip", WARN, "pip unavailable (SQLite path needs no packages)",
                     {"output": out.strip()[:400]})
    return Probe("pip", OK, out.strip()[:120], {"index_check": "not attempted (offline-safe)"})


def _dsn_host_port(dsn):
    """Host and port from a URL-form DSN; ``(None, None)`` for anything else."""
    from urllib.parse import urlsplit
    if not dsn or "://" not in dsn:
        return None, None
    try:
        parts = urlsplit(dsn)
        return parts.hostname, parts.port
    except ValueError:
        return None, None


def _try_dsn(dsn):
    """Connect with the configured DSN through the driver. Returns (ok, error).

    The error is the exception's class name only: a driver message can echo the
    DSN, and the DSN can carry a password.
    """
    from ..storage.postgres_backend import _load_driver
    try:
        driver, _version = _load_driver()
        conn = driver.connect(dsn, connect_timeout=PROBE_TIMEOUT)
        conn.close()
        return True, ""
    except Exception as exc:  # any failure means "not usable"; reported, not raised
        return False, type(exc).__name__


def probe_postgres(dsn=None):
    """Three separate checks: client present, server reachable, DB usable.

    They are distinct on purpose — a psql binary on PATH says nothing about
    whether a server exists or whether this user may create a database.

    When a DSN is configured (``MA_POSTGRES_DSN`` or ``config.local.json``) it is
    what the archive will actually use, so authentication is tested by
    connecting with it through the driver. Without one, ``psql`` and the
    ``PG*`` environment stand in.
    """
    from ..storage.postgres_backend import driver_available

    detail = {
        "driver_installed": driver_available(),
        "psql_on_path": bool(shutil.which("psql")),
        "server_reachable": False,
        "can_create_db": False,
    }

    dsn_host, dsn_port = _dsn_host_port(dsn)
    host = dsn_host or os.environ.get("PGHOST", "127.0.0.1")
    port = int(dsn_port or os.environ.get("PGPORT", "5432"))
    detail["configured_dsn"] = bool(dsn)
    try:
        with socket.create_connection((host, port), timeout=2):
            detail["server_reachable"] = True
    except OSError:
        pass

    if not detail["server_reachable"]:
        return Probe("postgres", SKIP,
                     "no PostgreSQL server on {}:{} - SQLite will be used".format(host, port),
                     detail)

    if not detail["driver_installed"]:
        return Probe("postgres", WARN,
                     "server reachable but no psycopg driver installed", detail)

    if dsn:
        ok, err = _try_dsn(dsn)
        detail["can_create_db"] = ok
        if not ok:
            detail["dsn_error"] = err
            return Probe("postgres", WARN,
                         "configured DSN did not connect ({})".format(err), detail)
        return Probe("postgres", OK,
                     "PostgreSQL usable at {}:{} with the configured DSN".format(host, port),
                     detail)

    if not detail["psql_on_path"]:
        return Probe("postgres", WARN,
                     "server reachable but psql is not on PATH, so login could not be "
                     "tested - set MA_POSTGRES_DSN and re-run", detail)

    rc, out = _run(["psql", "-h", host, "-p", str(port), "-lqt"], timeout=PROBE_TIMEOUT)
    detail["can_create_db"] = rc == 0
    detail["psql_output"] = out.strip()[:300]
    if rc != 0:
        return Probe("postgres", WARN, "server reachable but not authenticated", detail)

    return Probe("postgres", OK, "PostgreSQL usable at {}:{}".format(host, port), detail)


def probe_filesystem(repo_root):
    """Can the archive be written here, and is the location safe?"""
    data_dir = os.path.join(repo_root, "data")
    detail = {"data_dir": data_dir, "writable": False, "synced_folder": False}

    try:
        os.makedirs(data_dir, exist_ok=True)
        probe_file = os.path.join(data_dir, ".write-probe")
        with open(probe_file, "w", encoding="utf-8") as fh:
            fh.write("ok")
        os.remove(probe_file)
        detail["writable"] = True
    except OSError as exc:
        detail["error"] = str(exc)
        return Probe("filesystem", FAIL, "cannot write to {}".format(data_dir), detail)

    # A synced folder means work content may be replicated off-machine, which is
    # a data-handling concern rather than a functional one.
    lowered = repo_root.lower()
    for marker in ("dropbox", "onedrive", "google drive", "cloudstorage", "icloud"):
        if marker in lowered:
            detail["synced_folder"] = True
            detail["sync_marker"] = marker
            return Probe("filesystem", WARN,
                         "repo sits inside a synced folder ({}) - captured content "
                         "may replicate off-machine".format(marker), detail)

    return Probe("filesystem", OK, "data dir writable", detail)


def probe_editor_surface():
    """Where Claude Code keeps state, and whether transcripts are readable.

    Informational in Phase 1 (no auto-capture), but it is what a later
    transcript-parsing phase would depend on.
    """
    home = os.path.expanduser("~")
    claude_dir = os.path.join(home, ".claude")
    projects_dir = os.path.join(claude_dir, "projects")
    detail = {
        "claude_dir": claude_dir,
        "claude_dir_exists": os.path.isdir(claude_dir),
        "projects_dir_exists": os.path.isdir(projects_dir),
        "settings_exists": os.path.isfile(os.path.join(claude_dir, "settings.json")),
    }
    if not detail["claude_dir_exists"]:
        return Probe("editor", WARN, "no ~/.claude directory found", detail)
    return Probe("editor", OK, "Claude Code state directory present", detail)


def probe_hooks(repo_root):
    """Whether this repo declares hooks. Firing is verified by running a session."""
    settings = os.path.join(repo_root, ".claude", "settings.json")
    detail = {"project_settings": settings, "exists": os.path.isfile(settings)}
    if not detail["exists"]:
        return Probe("hooks", WARN, "no project .claude/settings.json yet (run `ma init`)", detail)
    try:
        with open(settings, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        detail["declared"] = sorted((data.get("hooks") or {}).keys())
    except (OSError, ValueError) as exc:
        return Probe("hooks", WARN, "settings.json unreadable", {"error": str(exc)})
    return Probe("hooks", OK, "hooks declared: {}".format(", ".join(detail["declared"]) or "none"), detail)


def probe_egress():
    """Whether outbound network works. Reported only — Phase 1 calls nothing."""
    detail = {}
    try:
        with socket.create_connection(("1.1.1.1", 443), timeout=2):
            detail["outbound_443"] = True
    except OSError:
        detail["outbound_443"] = False
    status = OK if detail["outbound_443"] else WARN
    return Probe("egress", status,
                 "outbound HTTPS {}".format("available" if detail["outbound_443"] else "blocked"),
                 detail)


def probe_git(repo_root):
    detail = {"git_on_path": bool(shutil.which("git"))}
    if not detail["git_on_path"]:
        return Probe("git", WARN, "git not on PATH", detail)
    rc, out = _run(["git", "-C", repo_root, "remote", "-v"])
    detail["remotes"] = out.strip()[:400] if rc == 0 else ""
    detail["has_remote"] = bool(detail["remotes"])
    return Probe("git", OK,
                 "git present; remote {}".format("configured" if detail["has_remote"] else "not set"),
                 detail)


# ---- orchestration ------------------------------------------------------

def run_all(repo_root, dsn=None):
    return [
        _safe("python", probe_python),
        _safe("pip", probe_pip),
        _safe("postgres", lambda: probe_postgres(dsn)),
        _safe("filesystem", lambda: probe_filesystem(repo_root)),
        _safe("editor", probe_editor_surface),
        _safe("hooks", lambda: probe_hooks(repo_root)),
        _safe("egress", probe_egress),
        _safe("git", lambda: probe_git(repo_root)),
    ]


def recommend_backend(probes):
    """Pick a backend from the findings.

    Postgres only when genuinely usable end to end; anything less lands on
    SQLite. The failure being designed against is spending a first working
    session fighting a database install instead of capturing work.
    """
    by_key = {p.key: p for p in probes}
    pg = by_key.get("postgres")
    if pg and pg.status == OK and pg.detail.get("driver_installed") and pg.detail.get("can_create_db"):
        return "postgres", "PostgreSQL is reachable, authenticated and has a driver installed"
    reason = "PostgreSQL not fully usable"
    if pg:
        if not pg.detail.get("server_reachable"):
            reason = "no reachable PostgreSQL server"
        elif not pg.detail.get("driver_installed"):
            reason = "PostgreSQL reachable but no psycopg driver installed"
        elif not pg.detail.get("can_create_db"):
            reason = "PostgreSQL reachable but authentication failed"
    return "sqlite", "{} - using SQLite (fully supported; `ma migrate` can move later)".format(reason)


def format_report(probes, backend, reason):
    symbols = {OK: "[ok]", WARN: "[warn]", FAIL: "[FAIL]", SKIP: "[skip]"}
    lines = ["Environment report", "=" * 60]
    for probe in probes:
        lines.append("{:<7} {:<12} {}".format(symbols.get(probe.status, "[?]"), probe.key, probe.summary))
    lines += ["", "Selected backend: {}".format(backend), "Reason: {}".format(reason)]

    blockers = [p for p in probes if p.status == FAIL]
    if blockers:
        lines += ["", "Blocking problems:"]
        lines += ["  - {}: {}".format(p.key, p.summary) for p in blockers]
    return "\n".join(lines)
