"""Repository behaviour: validation, link resolution, recall assembly, export."""

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
        self.repo.capture("decision", "Confidential title", "secret body",
                          links=[("person", "Jane Doe")])
        data = self.repo.export(redact=True)
        blob = str(data)
        self.assertNotIn("Confidential title", blob)
        self.assertNotIn("secret body", blob)
        self.assertNotIn("Jane Doe", blob)
        self.assertEqual(len(data["memories"]), 1)
        self.assertTrue(data["redacted"])


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
