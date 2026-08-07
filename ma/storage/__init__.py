"""Backend factory — the single place a concrete backend is chosen.

Core code receives a backend and never learns which one it got.
"""

from .. import config as config_mod
from .base import StorageBackend, new_id, now_iso  # noqa: F401
from .sqlite_backend import SQLiteBackend


def get_backend(cfg=None):
    """Build the backend named by config.

    Postgres selected without a DSN falls back to SQLite rather than failing:
    losing the preferred backend is recoverable, losing the ability to capture
    anything is not.
    """
    cfg = cfg or config_mod.load()
    storage = cfg.get("storage", {})
    backend = (storage.get("backend") or "sqlite").lower()

    if backend == "postgres":
        dsn = storage.get("postgres_dsn") or ""
        if dsn:
            from .postgres_backend import PostgresBackend
            return PostgresBackend(dsn)

    return SQLiteBackend(config_mod.resolve_path(storage.get("sqlite_path", "data/memory.db")))
