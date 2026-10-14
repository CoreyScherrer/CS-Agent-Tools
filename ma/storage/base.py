"""Storage seam.

Backends speak SQL over a DB-API 2.0 connection, so the shared subclass below
carries nearly all the logic and a concrete backend only supplies a connection
plus its placeholder style. Both backends run the same conformance suite
(``tests/test_storage_conformance.py``).
"""

import abc
import json
import uuid
from datetime import datetime, timezone

from . import schema


def now_iso():
    """UTC timestamp as ISO-8601 text — the only time format stored anywhere."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_id():
    return str(uuid.uuid4())


class StorageBackend(abc.ABC):
    """What core code is allowed to assume about persistence."""

    paramstyle = "qmark"

    @abc.abstractmethod
    def connect(self):
        """Return a live DB-API connection, opening one if needed."""

    @abc.abstractmethod
    def close(self):
        ...

    @abc.abstractmethod
    def init_schema(self):
        ...

    @property
    @abc.abstractmethod
    def name(self):
        """Short backend identifier, e.g. 'sqlite' — shown by `ma status`."""


class SQLBackend(StorageBackend):
    """DB-API implementation shared by SQLite and PostgreSQL."""

    def _q(self, sql):
        """Adapt placeholders to this backend's paramstyle."""
        return sql if self.paramstyle == "qmark" else sql.replace("?", "%s")

    def execute(self, sql, params=()):
        cur = self.connect().cursor()
        cur.execute(self._q(sql), params)
        return cur

    def query(self, sql, params=()):
        """Run a SELECT and return rows as plain dicts.

        Dicts rather than driver-specific row objects keep core code from
        depending on which backend produced the result.
        """
        cur = self.execute(sql, params)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        cur.close()
        return rows

    def commit(self):
        self.connect().commit()

    def init_schema(self):
        conn = self.connect()
        cur = conn.cursor()
        for stmt in schema.TABLES + schema.INDEXES:
            cur.execute(stmt)
        conn.commit()
        cur.close()

    # ---- memories -------------------------------------------------------

    def add_memory(self, **f):
        ts = now_iso()
        mid = f.get("id") or new_id()
        created_at = f.get("created_at") or ts
        updated_at = f.get("updated_at") or created_at
        self.execute(
            """INSERT INTO memories
               (id, type, title, body, project, importance, tags, source,
                agent_key, session_id, pinned, created_at, updated_at, expires_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                mid,
                f["type"],
                f["title"],
                f.get("body", ""),
                f.get("project"),
                float(f.get("importance", 0.5)),
                json.dumps(f.get("tags", [])),
                f.get("source", "manual"),
                f.get("agent_key"),
                f.get("session_id"),
                1 if f.get("pinned") else 0,
                created_at,
                updated_at,
                f.get("expires_at"),
            ),
        )
        self.commit()
        return mid

    def get_memory(self, memory_id):
        rows = self.query("SELECT * FROM memories WHERE id = ?", (memory_id,))
        return rows[0] if rows else None

    def list_memories(self, project=None, mtype=None, limit=100, include_expired=False):
        sql = "SELECT * FROM memories WHERE 1=1"
        params = []
        if project:
            sql += " AND project = ?"
            params.append(project)
        if mtype:
            sql += " AND type = ?"
            params.append(mtype)
        if not include_expired:
            sql += " AND (expires_at IS NULL OR expires_at > ?)"
            params.append(now_iso())
        sql += " ORDER BY pinned DESC, created_at DESC LIMIT ?"
        params.append(int(limit))
        return self.query(sql, tuple(params))

    def search_memories(self, term, limit=50):
        """Case-insensitive substring search over title, body and tags.

        LIKE rather than a full-text index: FTS support differs between the two
        backends, and portability matters more here than speed at this scale.
        """
        like = "%{}%".format(term.lower())
        return self.query(
            """SELECT * FROM memories
               WHERE lower(title) LIKE ? OR lower(body) LIKE ? OR lower(tags) LIKE ?
               ORDER BY pinned DESC, importance DESC, created_at DESC
               LIMIT ?""",
            (like, like, like, int(limit)),
        )

    def delete_memory(self, memory_id):
        self.execute("DELETE FROM links WHERE memory_id = ?", (memory_id,))
        cur = self.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        self.commit()
        return cur.rowcount

    # ---- entities -------------------------------------------------------

    def add_entity(self, kind, **f):
        table = schema.ENTITY_TABLES[kind]
        ts = now_iso()
        eid = f.get("id") or new_id()
        created_at = f.get("created_at") or ts
        updated_at = f.get("updated_at") or created_at
        if kind == "person":
            cols = ("id", "name", "role", "team", "aliases", "notes", "created_at", "updated_at")
            vals = (eid, f["name"], f.get("role"), f.get("team"),
                    json.dumps(f.get("aliases", [])), f.get("notes", ""), created_at, updated_at)
        elif kind == "system":
            cols = ("id", "name", "purpose", "owner_id", "notes", "links", "created_at", "updated_at")
            vals = (eid, f["name"], f.get("purpose", ""), f.get("owner_id"),
                    f.get("notes", ""), json.dumps(f.get("links", [])), created_at, updated_at)
        else:
            cols = ("id", "external_ref", "title", "status", "notes", "created_at", "updated_at")
            vals = (eid, f.get("external_ref"), f["title"], f.get("status", "open"),
                    f.get("notes", ""), created_at, updated_at)
        placeholders = ",".join("?" * len(cols))
        self.execute(
            "INSERT INTO {} ({}) VALUES ({})".format(table, ",".join(cols), placeholders),
            vals,
        )
        self.commit()
        return eid

    def list_entities(self, kind, limit=200):
        table = schema.ENTITY_TABLES[kind]
        return self.query(
            "SELECT * FROM {} ORDER BY created_at DESC LIMIT ?".format(table),
            (int(limit),),
        )

    def find_entity(self, kind, term):
        table = schema.ENTITY_TABLES[kind]
        field = "title" if kind == "item" else "name"
        like = "%{}%".format(term.lower())
        return self.query(
            "SELECT * FROM {} WHERE lower({}) LIKE ? LIMIT 25".format(table, field),
            (like,),
        )

    # ---- links ----------------------------------------------------------

    def add_link(self, memory_id, entity_type, entity_id, created_at=None):
        try:
            self.execute(
                "INSERT INTO links (memory_id, entity_type, entity_id, created_at) VALUES (?,?,?,?)",
                (memory_id, entity_type, entity_id, created_at or now_iso()),
            )
            self.commit()
        except Exception:
            # Links are idempotent by design: re-linking is a no-op, not an error.
            pass

    def memories_for_entity(self, entity_type, entity_id, limit=50):
        return self.query(
            """SELECT m.* FROM memories m
               JOIN links l ON l.memory_id = m.id
               WHERE l.entity_type = ? AND l.entity_id = ?
               ORDER BY m.pinned DESC, m.created_at DESC LIMIT ?""",
            (entity_type, entity_id, int(limit)),
        )

    def links_for_memory(self, memory_id):
        return self.query("SELECT * FROM links WHERE memory_id = ?", (memory_id,))

    # ---- misc -----------------------------------------------------------

    def save_env_report(self, report_json):
        self.execute(
            "INSERT INTO env_reports (id, report, created_at) VALUES (?,?,?)",
            (new_id(), report_json, now_iso()),
        )
        self.commit()

    def counts(self):
        out = {}
        for table in ("memories", "people", "systems", "work_items", "links"):
            try:
                out[table] = self.query("SELECT COUNT(*) AS c FROM {}".format(table))[0]["c"]
            except Exception:
                out[table] = 0
        return out
