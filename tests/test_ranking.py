"""Ranking is pure, so it is tested exactly — no fixtures, no database."""

import unittest
from datetime import datetime, timedelta, timezone

from ma.core import ranking

NOW = datetime(2026, 8, 7, 12, 0, 0, tzinfo=timezone.utc)


def mem(**kw):
    base = {
        "id": kw.get("id", "x"),
        "type": "learning",
        "title": kw.get("title", "t"),
        "body": kw.get("body", ""),
        "project": kw.get("project"),
        "importance": kw.get("importance", 0.5),
        "pinned": kw.get("pinned", False),
        "created_at": kw.get("created_at", NOW.isoformat()),
    }
    return base


class TestRecencyDecay(unittest.TestCase):
    def test_new_memory_has_no_decay(self):
        self.assertAlmostEqual(ranking.recency_decay(NOW.isoformat(), 30, NOW), 1.0)

    def test_one_half_life_halves_the_value(self):
        older = (NOW - timedelta(days=30)).isoformat()
        self.assertAlmostEqual(ranking.recency_decay(older, 30, NOW), 0.5, places=4)

    def test_two_half_lives_quarter_the_value(self):
        older = (NOW - timedelta(days=60)).isoformat()
        self.assertAlmostEqual(ranking.recency_decay(older, 30, NOW), 0.25, places=4)

    def test_unparseable_timestamp_does_not_raise(self):
        self.assertEqual(ranking.recency_decay("not-a-date", 30, NOW), 1.0)
        self.assertEqual(ranking.recency_decay(None, 30, NOW), 1.0)

    def test_naive_timestamp_is_treated_as_utc(self):
        naive = (NOW - timedelta(days=30)).replace(tzinfo=None).isoformat()
        self.assertAlmostEqual(ranking.recency_decay(naive, 30, NOW), 0.5, places=4)

    def test_future_timestamp_does_not_exceed_one(self):
        future = (NOW + timedelta(days=10)).isoformat()
        self.assertEqual(ranking.recency_decay(future, 30, NOW), 1.0)


class TestProjectFactor(unittest.TestCase):
    def test_match_boosts(self):
        self.assertGreater(ranking.project_factor("a", "a"), 1.0)

    def test_mismatch_penalises_but_survives(self):
        factor = ranking.project_factor("a", "b")
        self.assertLess(factor, 1.0)
        self.assertGreater(factor, 0.0)

    def test_missing_project_is_neutral(self):
        self.assertEqual(ranking.project_factor(None, "a"), 1.0)
        self.assertEqual(ranking.project_factor("a", None), 1.0)


class TestRank(unittest.TestCase):
    def test_pinned_outranks_a_higher_scoring_memory(self):
        pinned = mem(id="p", title="pinned", importance=0.1, pinned=True)
        strong = mem(id="s", title="strong", importance=1.0)
        self.assertEqual(ranking.rank([strong, pinned], now=NOW)[0]["id"], "p")

    def test_importance_orders_equals(self):
        low = mem(id="lo", importance=0.2)
        high = mem(id="hi", importance=0.9)
        self.assertEqual(ranking.rank([low, high], now=NOW)[0]["id"], "hi")

    def test_recent_beats_old_at_equal_importance(self):
        old = mem(id="old", created_at=(NOW - timedelta(days=90)).isoformat())
        new = mem(id="new", created_at=NOW.isoformat())
        self.assertEqual(ranking.rank([old, new], now=NOW)[0]["id"], "new")

    def test_matching_project_beats_other_project(self):
        here = mem(id="here", project="p1")
        away = mem(id="away", project="p2")
        self.assertEqual(ranking.rank([away, here], current_project="p1", now=NOW)[0]["id"], "here")

    def test_ordering_is_deterministic(self):
        items = [mem(id=str(i), importance=0.5) for i in range(6)]
        first = [m["id"] for m in ranking.rank(items, now=NOW)]
        second = [m["id"] for m in ranking.rank(items, now=NOW)]
        self.assertEqual(first, second)

    def test_empty_input(self):
        self.assertEqual(ranking.rank([], now=NOW), [])


class TestBudget(unittest.TestCase):
    def test_selection_stays_within_budget(self):
        items = [mem(id=str(i), body="word " * 100) for i in range(20)]
        chosen, used = ranking.select_within_budget(items, token_budget=200, now=NOW)
        self.assertLessEqual(used, 200)
        self.assertGreater(len(chosen), 0)

    def test_max_items_caps_selection(self):
        items = [mem(id=str(i)) for i in range(50)]
        chosen, _ = ranking.select_within_budget(items, 100000, max_items=5, now=NOW)
        self.assertEqual(len(chosen), 5)

    def test_oversized_item_is_skipped_not_terminal(self):
        huge = mem(id="huge", body="x" * 10000, importance=1.0)
        small = mem(id="small", body="tiny", importance=0.9)
        chosen, _ = ranking.select_within_budget([huge, small], token_budget=50, now=NOW)
        self.assertIn("small", [m["id"] for m in chosen])

    def test_zero_budget_selects_nothing(self):
        chosen, used = ranking.select_within_budget([mem()], token_budget=0, now=NOW)
        self.assertEqual(chosen, [])
        self.assertEqual(used, 0)

    def test_token_estimate_scales_with_length(self):
        self.assertGreater(
            ranking.estimate_tokens(mem(body="word " * 100)),
            ranking.estimate_tokens(mem(body="word")),
        )


if __name__ == "__main__":
    unittest.main()
