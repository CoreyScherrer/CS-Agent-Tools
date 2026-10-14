"""Repository behaviour: validation, link resolution, recall assembly, export."""

import json
import os
import tempfile
import unittest

from ma.core.repository import (
    Repository,
    ValidationError,
    decode_tags,
    parse_link_spec,
)
from ma.storage.sqlite_backend import SQLiteBackend

CFG = {
    "identity": {"agent_key": "test-agent", "default_project": ""},
    "recall": {"token_budget": 2000, "max_items": 25, "recency_half_life_days": 30.0},
    "capture": {"default_importance": 0.5},
}


class RepoCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.backend = SQLiteBackend(os.path.join(self._tmp.name, "t.db"))
        self.backend.init_schema()
        self.addCleanup(self.backend.close)
        self.repo = Repository(self.backend, CFG)


class TestCapture(RepoCase):
    def test_capture_stores_agent_key_from_config(self):
        mid = self.repo.capture("decision", "Use SQLite")
        self.assertEqual(self.backend.get_memory(mid)["agent_key"], "test-agent")

    def test_unknown_type_rejected_with_helpful_message(self):
        with self.assertRaises(ValidationError) as ctx:
            self.repo.capture("nonsense", "t")
        self.assertIn("decision", str(ctx.exception))

    def test_empty_title_rejected(self):
        with self.assertRaises(ValidationError):
            self.repo.capture("learning", "   ")

    def test_importance_clamped_to_unit_range(self):
        high = self.repo.capture("learning", "a", importance=5.0)
        low = self.repo.capture("learning", "b", importance=-2.0)
        self.assertEqual(self.backend.get_memory(high)["importance"], 1.0)
        self.assertEqual(self.backend.get_memory(low)["importance"], 0.0)

    def test_tags_deduplicated_and_sorted(self):
        mid = self.repo.capture("learning", "t", tags=["b", "a", "b"])
        self.assertEqual(decode_tags(self.backend.get_memory(mid)["tags"]), ["a", "b"])

    def test_capture_creates_linked_entities_on_first_mention(self):
        mid = self.repo.capture("decision", "scale it", links=[("system", "checkout")])
        self.assertEqual(len(self.backend.links_for_memory(mid)), 1)
        self.assertEqual(len(self.backend.find_entity("system", "checkout")), 1)

    def test_repeated_mention_reuses_the_same_entity(self):
        self.repo.capture("decision", "one", links=[("person", "Jane")])
        self.repo.capture("decision", "two", links=[("person", "Jane")])
        self.assertEqual(len(self.backend.list_entities("person")), 1)

    def test_entity_match_is_case_insensitive(self):
        self.repo.capture("decision", "one", links=[("person", "Jane Doe")])
        self.repo.capture("decision", "two", links=[("person", "jane doe")])
        self.assertEqual(len(self.backend.list_entities("person")), 1)


class TestLinking(RepoCase):
    def test_link_to_missing_entity_rejected_without_create(self):
        mid = self.repo.capture("learning", "t")
        with self.assertRaises(ValidationError):
            self.repo.link(mid, "person", "Nobody", create_missing=False)

    def test_unknown_kind_rejected(self):
        mid = self.repo.capture("learning", "t")
        with self.assertRaises(ValidationError):
            self.repo.link(mid, "spaceship", "x", create_missing=True)


class TestRecall(RepoCase):
    def test_recall_respects_budget_and_reports_usage(self):
        for i in range(30):
            self.repo.capture("learning", "memory {}".format(i), "body " * 50)
        result = self.repo.recall(token_budget=300)
        self.assertLessEqual(result["tokens_used"], 300)
        self.assertEqual(result["token_budget"], 300)

    def test_pinned_memory_always_present(self):
        for i in range(30):
            self.repo.capture("learning", "noise {}".format(i), "body " * 40)
        self.repo.capture("context", "PINNED", "critical", pinned=True)
        titles = [m["title"] for m in self.repo.recall(token_budget=200)["memories"]]
        self.assertIn("PINNED", titles)

    def test_empty_archive_returns_empty_not_error(self):
        result = self.repo.recall()
        self.assertEqual(result["memories"], [])
        self.assertEqual(result["candidates"], 0)

    def test_project_scope_prefers_matching_memories(self):
        self.repo.capture("learning", "elsewhere", project="other")
        self.repo.capture("learning", "here", project="mine")
        first = self.repo.recall(project="mine")["memories"][0]
        self.assertEqual(first["title"], "here")


class TestSearchAndContext(RepoCase):
    def test_search_returns_memories_and_entities(self):
        self.repo.capture("learning", "checkout timeout", links=[("system", "checkout")])
        results = self.repo.search("checkout")
        self.assertEqual(len(results["memories"]), 1)
        self.assertIn("system", results)

    def test_entity_context_gathers_linked_memories(self):
        self.repo.capture("decision", "one", links=[("system", "checkout")])
        self.repo.capture("learning", "two", links=[("system", "checkout")])
        found = self.repo.entity_context("system", "checkout")
        self.assertEqual(len(found["memories"]), 2)

    def test_entity_context_missing_returns_none(self):
        self.assertIsNone(self.repo.entity_context("system", "ghost"))


class TestExport(RepoCase):
    def test_export_includes_all_sections(self):
        self.repo.capture("decision", "keep", links=[("person", "Jane")])
        data = self.repo.export()
        self.assertEqual(len(data["memories"]), 1)
        self.assertEqual(len(data["people"]), 1)
        self.assertIn("exported_at", data)

    def test_redacted_export_keeps_structure_and_drops_content(self):
        memory_id = self.repo.capture(
            "decision",
            "memory-title-sentinel",
            "memory-body-sentinel",
            project="/Users/jane/clients/acme-bank",
            tags=["memory-tags-sentinel"],
            source="memory-source-sentinel",
            agent_key="memory-agent-sentinel",
            session_id="memory-session-sentinel",
        )
        person_id = self.backend.add_entity(
            "person",
            name="person-name-sentinel",
            role="person-role-sentinel",
            team="person-team-sentinel",
            aliases=["person-alias-sentinel"],
            notes="person-notes-sentinel",
        )
        system_id = self.backend.add_entity(
            "system",
            name="system-name-sentinel",
            purpose="system-purpose-sentinel",
            notes="system-notes-sentinel",
            links=["system-links-sentinel"],
        )
        self.backend.add_link(memory_id, "person", person_id)
        self.backend.add_link(memory_id, "system", system_id)

        data = self.repo.export(redact=True)
        blob = json.dumps(data)
        for sentinel in (
            "memory-title-sentinel",
            "memory-body-sentinel",
            "/Users/jane/clients/acme-bank",
            "memory-tags-sentinel",
            "memory-source-sentinel",
            "memory-agent-sentinel",
            "memory-session-sentinel",
            "person-name-sentinel",
            "person-role-sentinel",
            "person-team-sentinel",
            "person-alias-sentinel",
            "person-notes-sentinel",
            "system-name-sentinel",
            "system-purpose-sentinel",
            "system-notes-sentinel",
            "system-links-sentinel",
        ):
            self.assertNotIn(sentinel, blob)
        self.assertEqual(len(data["memories"]), 1)
        self.assertEqual(data["memories"][0]["id"], memory_id)
        self.assertEqual(data["memories"][0]["type"], "decision")
        self.assertEqual(data["people"][0]["id"], person_id)
        self.assertEqual(data["systems"][0]["id"], system_id)
        self.assertTrue(data["redacted"])


class TestImport(RepoCase):
    """Export/import is how content moves between machines — it must round-trip."""

    def _second_repo(self):
        backend = SQLiteBackend(os.path.join(self._tmp.name, "second.db"))
        backend.init_schema()
        self.addCleanup(backend.close)
        return Repository(backend, CFG)

    def test_round_trip_preserves_memories_entities_and_links(self):
        self.repo.capture("decision", "keep this", "with reasoning",
                          tags=["a"], links=[("person", "Jane"), ("system", "checkout")])
        self.repo.capture("learning", "and this", project="p1")

        target = self._second_repo()
        stats = target.import_data(self.repo.export())

        self.assertEqual(stats["memories"], 2)
        self.assertEqual(stats["links"], 2)
        self.assertEqual(len(target.backend.list_memories()), 2)
        found = target.entity_context("system", "checkout")
        self.assertEqual(len(found["memories"]), 1)

    def test_round_trip_preserves_timestamps(self):
        created_at = "2025-01-01T00:00:00+00:00"
        updated_at = "2025-01-02T00:00:00+00:00"
        link_created_at = "2025-01-03T00:00:00+00:00"
        memory_id = self.backend.add_memory(
            type="decision",
            title="old memory",
            tags=["legacy"],
            created_at=created_at,
            updated_at=updated_at,
        )
        system_id = self.backend.add_entity(
            "system",
            name="legacy system",
            links=["service-id"],
            created_at=created_at,
            updated_at=updated_at,
        )
        self.backend.add_link(memory_id, "system", system_id, created_at=link_created_at)

        target = self._second_repo()
        target.import_data(self.repo.export())

        def normalize(row):
            result = dict(row)
            for field in ("tags", "aliases", "links"):
                if field in result and isinstance(result[field], str):
                    result[field] = json.loads(result[field])
            return result

        source_rows = (
            self.backend.get_memory(memory_id),
            self.backend.list_entities("system")[0],
            self.backend.links_for_memory(memory_id)[0],
        )
        target_rows = (
            target.backend.get_memory(memory_id),
            target.backend.list_entities("system")[0],
            target.backend.links_for_memory(memory_id)[0],
        )
        for source, imported in zip(source_rows, target_rows):
            self.assertEqual(normalize(imported), normalize(source))

    def test_import_is_idempotent(self):
        self.repo.capture("decision", "once", links=[("person", "Jane")])
        payload = self.repo.export()

        target = self._second_repo()
        target.import_data(payload)
        second = target.import_data(payload)

        self.assertEqual(second["memories"], 0)
        self.assertEqual(len(target.backend.list_memories()), 1)
        self.assertEqual(len(target.backend.list_entities("person")), 1)

    def test_importing_into_itself_changes_nothing(self):
        self.repo.capture("learning", "solo")
        self.repo.import_data(self.repo.export())
        self.assertEqual(len(self.backend.list_memories()), 1)

    def test_redacted_export_is_rejected(self):
        self.repo.capture("decision", "secret")
        with self.assertRaises(ValidationError) as ctx:
            self._second_repo().import_data(self.repo.export(redact=True))
        self.assertIn("redacted", str(ctx.exception))

    def test_empty_payload_is_harmless(self):
        self.assertEqual(self.repo.import_data({})["memories"], 0)

    def test_malformed_memory_is_skipped_not_fatal(self):
        payload = {"memories": [{"id": "bad"}, {"id": "ok", "type": "learning", "title": "fine"}]}
        stats = self.repo.import_data(payload)
        self.assertEqual(stats["memories"], 1)
        self.assertEqual(stats["skipped"], 1)

    def test_export_includes_links_section(self):
        self.repo.capture("decision", "linked", links=[("person", "Jane")])
        self.assertEqual(len(self.repo.export()["links"]), 1)


class TestHelpers(unittest.TestCase):
    def test_parse_link_spec(self):
        self.assertEqual(parse_link_spec("person:Jane Doe"), ("person", "Jane Doe"))
        self.assertEqual(parse_link_spec("item:ABC-123"), ("item", "ABC-123"))

    def test_parse_link_spec_rejects_bad_input(self):
        for bad in ("nocolon", "spaceship:x", "person:"):
            with self.assertRaises(ValidationError):
                parse_link_spec(bad)

    def test_decode_tags_tolerates_garbage(self):
        self.assertEqual(decode_tags('["a"]'), ["a"])
        self.assertEqual(decode_tags(None), [])
        self.assertEqual(decode_tags("not json"), [])
        self.assertEqual(decode_tags('{"a": 1}'), [])


if __name__ == "__main__":
    unittest.main()
