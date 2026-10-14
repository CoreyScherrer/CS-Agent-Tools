"""Repository — the API core code and the CLI use.

Owns everything that is true regardless of backend: validation, link resolution,
recall assembly, export. Imports the abstract seam only, never a concrete
backend.
"""

import json

from ..storage.base import now_iso
from . import ranking

MEMORY_TYPES = ("decision", "learning", "pattern", "context", "preference", "question")
ENTITY_KINDS = ("person", "system", "item")


class ValidationError(ValueError):
    """Input rejected before it reaches storage."""


class Repository:
    def __init__(self, backend, cfg=None):
        self.backend = backend
        self.cfg = cfg or {}

    # ---- capture --------------------------------------------------------

    def capture(self, mtype, title, body="", project=None, importance=None,
                tags=None, links=None, agent_key=None, session_id=None,
                source="manual", pinned=False, expires_at=None):
        mtype = (mtype or "").strip().lower()
        if mtype not in MEMORY_TYPES:
            raise ValidationError(
                "unknown type {!r}; expected one of: {}".format(mtype, ", ".join(MEMORY_TYPES))
            )
        if not (title or "").strip():
            raise ValidationError("title is required")

        if importance is None:
            importance = self.cfg.get("capture", {}).get("default_importance", 0.5)
        importance = max(0.0, min(1.0, float(importance)))

        memory_id = self.backend.add_memory(
            type=mtype,
            title=title.strip(),
            body=body or "",
            project=project or self.cfg.get("identity", {}).get("default_project") or None,
            importance=importance,
            tags=sorted(set(tags or [])),
            source=source,
            agent_key=agent_key or self.cfg.get("identity", {}).get("agent_key"),
            session_id=session_id,
            pinned=pinned,
            expires_at=expires_at,
        )

        for kind, ref in (links or []):
            self.link(memory_id, kind, ref, create_missing=True)

        return memory_id

    def link(self, memory_id, kind, ref, create_missing=False):
        """Link a memory to an entity, resolving ``ref`` by id or by name.

        With ``create_missing`` the entity is created on first mention, so
        capturing never stalls to pre-register a person or system.
        """
        if kind not in ENTITY_KINDS:
            raise ValidationError(
                "unknown entity kind {!r}; expected one of: {}".format(kind, ", ".join(ENTITY_KINDS))
            )

        entity_id = self._resolve_entity(kind, ref)
        if entity_id is None:
            if not create_missing:
                raise ValidationError("no {} matching {!r}".format(kind, ref))
            field = "title" if kind == "item" else "name"
            entity_id = self.backend.add_entity(kind, **{field: ref})

        self.backend.add_link(memory_id, kind, entity_id)
        return entity_id

    def _resolve_entity(self, kind, ref):
        matches = self.backend.find_entity(kind, ref)
        if not matches:
            return None
        field = "title" if kind == "item" else "name"
        for row in matches:
            if (row.get(field) or "").lower() == ref.lower():
                return row["id"]
        return matches[0]["id"]

    # ---- retrieval ------------------------------------------------------

    def search(self, term, limit=50):
        results = {"memories": self.backend.search_memories(term, limit)}
        for kind in ENTITY_KINDS:
            found = self.backend.find_entity(kind, term)
            if found:
                results[kind] = found
        return results

    def recall(self, project=None, token_budget=None, max_items=None, pool=400):
        """Assemble the best context that fits a token budget."""
        recall_cfg = self.cfg.get("recall", {})
        token_budget = token_budget or recall_cfg.get("token_budget", 2000)
        max_items = max_items or recall_cfg.get("max_items", 25)
        half_life = recall_cfg.get("recency_half_life_days", 30.0)

        # Pull a wide pool and rank in Python: ranking blends recency with
        # importance and project match, so SQL ordering alone would pick the
        # wrong candidates to consider.
        candidates = self.backend.list_memories(limit=pool)
        chosen, used = ranking.select_within_budget(
            candidates, token_budget, max_items, project, half_life
        )
        return {
            "memories": chosen,
            "tokens_used": used,
            "token_budget": token_budget,
            "candidates": len(candidates),
        }

    def entity_context(self, kind, ref, limit=50):
        entity_id = self._resolve_entity(kind, ref)
        if entity_id is None:
            return None
        return {
            "entity": self._get_entity(kind, entity_id),
            "memories": self.backend.memories_for_entity(kind, entity_id, limit),
        }

    def _get_entity(self, kind, entity_id):
        for row in self.backend.list_entities(kind, limit=1000):
            if row["id"] == entity_id:
                return row
        return None

    # ---- export ---------------------------------------------------------

    def export(self, redact=False):
        """Dump everything to a plain dict — the anti-lock-in guarantee.

        ``redact`` keeps structure and metadata but drops free text, so a schema
        or usage pattern can be shared without sharing any work content.
        """
        memories = self.backend.list_memories(limit=100000, include_expired=True)
        links = []
        for memory in memories:
            links.extend(self.backend.links_for_memory(memory["id"]))

        data = {
            "exported_at": now_iso(),
            "memories": memories,
            "people": self.backend.list_entities("person", limit=100000),
            "systems": self.backend.list_entities("system", limit=100000),
            "work_items": self.backend.list_entities("item", limit=100000),
            "links": links,
        }
        if redact:
            data["redacted"] = True
            _redact_rows(data["memories"], {
                "id", "type", "importance", "pinned", "created_at", "updated_at", "expires_at",
            })
            for key in ("people", "systems", "work_items"):
                _redact_rows(data[key], {"id", "owner_id", "status", "created_at", "updated_at"})
        return data

    def import_data(self, data, skip_existing=True):
        """Load an ``export()`` payload into this archive.

        This is how content moves between machines. The export file is plain
        text, so it can be reviewed before it lands — unlike a database blob,
        which is why the archive itself is never committed to git.

        Idempotent by id: re-importing the same file changes nothing, so a
        partial or repeated import is safe.
        """
        if data.get("redacted"):
            raise ValidationError(
                "this export was redacted; its content was removed and cannot be imported"
            )

        existing = {m["id"] for m in self.backend.list_memories(limit=1000000,
                                                               include_expired=True)}
        stats = {"memories": 0, "entities": 0, "links": 0, "skipped": 0}

        for kind, key in (("person", "people"), ("system", "systems"), ("item", "work_items")):
            known = {e["id"] for e in self.backend.list_entities(kind, limit=1000000)}
            for row in data.get(key, []):
                if row.get("id") in known:
                    continue
                try:
                    self.backend.add_entity(kind, **row)
                    stats["entities"] += 1
                except Exception:
                    # One malformed row must not abort a transfer.
                    stats["skipped"] += 1

        for memory in data.get("memories", []):
            if skip_existing and memory.get("id") in existing:
                stats["skipped"] += 1
                continue
            payload = dict(memory)
            payload["tags"] = decode_tags(payload.get("tags"))
            payload["pinned"] = bool(payload.get("pinned"))
            try:
                self.backend.add_memory(**payload)
                stats["memories"] += 1
            except Exception:
                stats["skipped"] += 1

        for link in data.get("links", []):
            try:
                self.backend.add_link(
                    link["memory_id"], link["entity_type"], link["entity_id"], link.get("created_at")
                )
                stats["links"] += 1
            except Exception:
                stats["skipped"] += 1

        return stats

    def status(self):
        return {
            "backend": self.backend.name,
            "location": getattr(self.backend, "describe", lambda: "unknown")(),
            "counts": self.backend.counts(),
        }


def parse_link_spec(spec):
    """Parse a ``kind:ref`` CLI argument, e.g. ``person:Jane Doe``."""
    if ":" not in spec:
        raise ValidationError(
            "link must be kind:ref (e.g. person:Jane, system:checkout, item:ABC-123)"
        )
    kind, _, ref = spec.partition(":")
    kind = kind.strip().lower()
    if kind not in ENTITY_KINDS:
        raise ValidationError(
            "unknown entity kind {!r}; expected one of: {}".format(kind, ", ".join(ENTITY_KINDS))
        )
    if not ref.strip():
        raise ValidationError("link target is empty in {!r}".format(spec))
    return kind, ref.strip()


def decode_tags(raw):
    """Tags round-trip as JSON text; tolerate anything else stored there."""
    if isinstance(raw, list):
        return raw
    try:
        value = json.loads(raw or "[]")
        return value if isinstance(value, list) else []
    except (TypeError, ValueError):
        return []


def _redact_rows(rows, allowed_fields):
    for row in rows:
        for field, value in row.items():
            if field not in allowed_fields and value not in (None, "", "[]"):
                row[field] = "[redacted]"
