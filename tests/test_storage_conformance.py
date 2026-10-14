"""Backend conformance.

Every backend must satisfy this suite identically. SQLite runs here always;
PostgreSQL runs the same cases when MA_TEST_POSTGRES_DSN is set, which is how
the abstraction is kept honest rather than merely intended.
"""

import os
import tempfile
import unittest

from ma.storage.sqlite_backend import SQLiteBackend


class BackendConformanceMixin:
    """Shared cases. Subclasses provide ``make_backend``."""

    def setUp(self):
        self.backend = self.make_backend()
        self.backend.init_schema()

    def tearDown(self):
        self.backend.close()

    def test_init_schema_is_idempotent(self):
        self.backend.init_schema()
        self.assertEqual(self.backend.counts()["memories"], 0)

    def test_add_and_get_memory(self):
        mid = self.backend.add_memory(type="decision", title="Chose SQLite", body="portable")
        stored = self.backend.get_memory(mid)
        self.assertEqual(stored["title"], "Chose SQLite")
        self.assertEqual(stored["type"], "decision")
        self.assertEqual(stored["source"], "manual")

    def test_add_memory_preserves_created_at(self):
        created_at = "2025-01-01T00:00:00+00:00"
        mid = self.backend.add_memory(type="decision", title="old", created_at=created_at)
        self.assertEqual(self.backend.get_memory(mid)["created_at"], created_at)

    def test_tags_round_trip_as_json_text(self):
        mid = self.backend.add_memory(type="learning", title="t", tags=["a", "b"])
        self.assertEqual(self.backend.get_memory(mid)["tags"], '["a", "b"]')

    def test_list_filters_by_project_and_type(self):
        self.backend.add_memory(type="learning", title="x", project="p1")
        self.backend.add_memory(type="decision", title="y", project="p2")
        self.assertEqual(len(self.backend.list_memories(project="p1")), 1)
        self.assertEqual(len(self.backend.list_memories(mtype="decision")), 1)

    def test_expired_memories_hidden_by_default(self):
        self.backend.add_memory(type="context", title="stale", expires_at="2000-01-01T00:00:00+00:00")
        self.assertEqual(len(self.backend.list_memories()), 0)
        self.assertEqual(len(self.backend.list_memories(include_expired=True)), 1)

    def test_search_is_case_insensitive_across_fields(self):
        self.backend.add_memory(type="learning", title="Checkout Timeout", body="raise limit")
        self.assertEqual(len(self.backend.search_memories("checkout")), 1)
        self.assertEqual(len(self.backend.search_memories("RAISE")), 1)
        self.assertEqual(len(self.backend.search_memories("absent")), 0)

    def test_pinned_memories_sort_first(self):
        self.backend.add_memory(type="learning", title="normal")
        self.backend.add_memory(type="context", title="pinned", pinned=True)
        self.assertEqual(self.backend.list_memories()[0]["title"], "pinned")

    def test_entities_and_links(self):
        person = self.backend.add_entity("person", name="Jane Doe", role="EM")
        system = self.backend.add_entity("system", name="checkout", purpose="orders")
        mid = self.backend.add_memory(type="decision", title="scale checkout")
        self.backend.add_link(mid, "person", person)
        self.backend.add_link(mid, "system", system)

        self.assertEqual(len(self.backend.memories_for_entity("system", system)), 1)
        self.assertEqual(len(self.backend.links_for_memory(mid)), 2)

    def test_duplicate_link_is_a_noop_not_an_error(self):
        mid = self.backend.add_memory(type="learning", title="t")
        pid = self.backend.add_entity("person", name="Sam")
        self.backend.add_link(mid, "person", pid)
        self.backend.add_link(mid, "person", pid)
        self.assertEqual(len(self.backend.links_for_memory(mid)), 1)

    def test_failed_insert_does_not_leave_connection_aborted(self):
        self.backend.add_memory(id="duplicate-id", type="learning", title="first")
        with self.assertRaises(Exception):
            self.backend.add_memory(id="duplicate-id", type="learning", title="duplicate")

        mid = self.backend.add_memory(type="learning", title="after duplicate")
        pid = self.backend.add_entity("person", name="Sam")
        self.backend.add_link(mid, "person", pid)
        self.assertEqual(len(self.backend.links_for_memory(mid)), 1)

    def test_find_entity_matches_partial_name(self):
        self.backend.add_entity("person", name="Alexandra Chen")
        self.assertEqual(len(self.backend.find_entity("person", "alex")), 1)

    def test_work_item_uses_title_field(self):
        self.backend.add_entity("item", external_ref="ABC-12", title="Fix login")
        self.assertEqual(len(self.backend.find_entity("item", "login")), 1)

    def test_delete_memory_removes_links(self):
        mid = self.backend.add_memory(type="learning", title="t")
        pid = self.backend.add_entity("person", name="Sam")
        self.backend.add_link(mid, "person", pid)
        self.backend.delete_memory(mid)
        self.assertIsNone(self.backend.get_memory(mid))
        self.assertEqual(len(self.backend.memories_for_entity("person", pid)), 0)

    def test_counts_reports_every_table(self):
        counts = self.backend.counts()
        for table in ("memories", "people", "systems", "work_items", "links"):
            self.assertIn(table, counts)


class TestSQLiteBackend(BackendConformanceMixin, unittest.TestCase):
    def make_backend(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        return SQLiteBackend(os.path.join(self._tmp.name, "test.db"))

    def test_creates_parent_directory(self):
        nested = os.path.join(self._tmp.name, "a", "b", "test.db")
        backend = SQLiteBackend(nested)
        backend.init_schema()
        self.assertTrue(os.path.isfile(nested))
        backend.close()


@unittest.skipUnless(os.environ.get("MA_TEST_POSTGRES_DSN"),
                     "set MA_TEST_POSTGRES_DSN to run PostgreSQL conformance")
class TestPostgresBackend(BackendConformanceMixin, unittest.TestCase):
    def make_backend(self):
        from ma.storage.postgres_backend import PostgresBackend
        backend = PostgresBackend(os.environ["MA_TEST_POSTGRES_DSN"])
        backend.init_schema()
        cur = backend.connect().cursor()
        for table in ("links", "memories", "people", "systems", "work_items", "env_reports"):
            cur.execute("TRUNCATE TABLE {}".format(table))
        backend.commit()
        cur.close()
        return backend


if __name__ == "__main__":
    unittest.main()
