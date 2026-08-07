"""Portable DDL shared by every storage backend.

No backend-specific types anywhere: text, integer, and real only, with JSON
encoded as text. The same statements run on SQLite and PostgreSQL after a single
dialect substitution (see ``render``).
"""

# ``{now}`` is the dialect's "current timestamp as ISO-8601 text" expression.
TABLES = [
    """
    CREATE TABLE IF NOT EXISTS memories (
        id          TEXT PRIMARY KEY,
        type        TEXT NOT NULL,
        title       TEXT NOT NULL,
        body        TEXT NOT NULL DEFAULT '',
        project     TEXT,
        importance  REAL NOT NULL DEFAULT 0.5,
        tags        TEXT NOT NULL DEFAULT '[]',
        source      TEXT NOT NULL DEFAULT 'manual',
        agent_key   TEXT,
        session_id  TEXT,
        pinned      INTEGER NOT NULL DEFAULT 0,
        created_at  TEXT NOT NULL,
        updated_at  TEXT NOT NULL,
        expires_at  TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS people (
        id         TEXT PRIMARY KEY,
        name       TEXT NOT NULL,
        role       TEXT,
        team       TEXT,
        aliases    TEXT NOT NULL DEFAULT '[]',
        notes      TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS systems (
        id         TEXT PRIMARY KEY,
        name       TEXT NOT NULL,
        purpose    TEXT NOT NULL DEFAULT '',
        owner_id   TEXT,
        notes      TEXT NOT NULL DEFAULT '',
        links      TEXT NOT NULL DEFAULT '[]',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS work_items (
        id           TEXT PRIMARY KEY,
        external_ref TEXT,
        title        TEXT NOT NULL,
        status       TEXT NOT NULL DEFAULT 'open',
        notes        TEXT NOT NULL DEFAULT '',
        created_at   TEXT NOT NULL,
        updated_at   TEXT NOT NULL
    )
    """,
    # One join table instead of three foreign keys: a memory may touch a person,
    # a system and a ticket at once, and new entity types cost no schema change.
    """
    CREATE TABLE IF NOT EXISTS links (
        memory_id   TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id   TEXT NOT NULL,
        created_at  TEXT NOT NULL,
        PRIMARY KEY (memory_id, entity_type, entity_id)
    )
    """,
    # Records what `doctor` found, so a later session can see how the current
    # environment was resolved without re-probing.
    """
    CREATE TABLE IF NOT EXISTS env_reports (
        id         TEXT PRIMARY KEY,
        report     TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
]

INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_memories_project ON memories (project)",
    "CREATE INDEX IF NOT EXISTS idx_memories_type ON memories (type)",
    "CREATE INDEX IF NOT EXISTS idx_memories_created ON memories (created_at)",
    "CREATE INDEX IF NOT EXISTS idx_memories_session ON memories (session_id)",
    "CREATE INDEX IF NOT EXISTS idx_links_entity ON links (entity_type, entity_id)",
    "CREATE INDEX IF NOT EXISTS idx_people_name ON people (name)",
    "CREATE INDEX IF NOT EXISTS idx_systems_name ON systems (name)",
    "CREATE INDEX IF NOT EXISTS idx_work_items_ref ON work_items (external_ref)",
]

ENTITY_TABLES = {
    "person": "people",
    "system": "systems",
    "item": "work_items",
}


def render(statements, paramstyle="qmark"):
    """Adapt statements to a dialect.

    Only the placeholder style differs between the two supported backends, so the
    substitution is deliberately minimal — a bigger translation layer would be a
    sign the schema had stopped being portable.
    """
    if paramstyle == "qmark":
        return list(statements)
    return [s.replace("?", "%s") for s in statements]
