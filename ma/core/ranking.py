"""Recall ranking — deterministic, no model in the loop.

With no embeddings in Phase 1 this scoring is the whole of recall quality, so it
is kept as pure functions: same inputs always produce the same ordering, which
makes it testable without an LLM.

    score = importance x recency_decay x project_match

Pinned memories bypass scoring and always come first.
"""

import math
from datetime import datetime, timezone

# Rough chars-per-token ratio for English prose. Deliberately conservative: the
# cost of overestimating is a slightly smaller context, of underestimating a
# blown budget.
CHARS_PER_TOKEN = 4

PROJECT_MATCH_BOOST = 1.5
PROJECT_MISMATCH_PENALTY = 0.6


def _parse(ts):
    try:
        parsed = datetime.fromisoformat(ts)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def recency_decay(created_at, half_life_days=30.0, now=None):
    """Exponential decay: a memory is worth half as much after one half-life.

    Unparseable or future timestamps score 1.0 rather than raising — bad data
    should degrade ranking, never break recall.
    """
    created = _parse(created_at)
    if created is None or half_life_days <= 0:
        return 1.0
    now = now or datetime.now(timezone.utc)
    age_days = (now - created).total_seconds() / 86400.0
    if age_days <= 0:
        return 1.0
    return math.pow(0.5, age_days / half_life_days)


def project_factor(memory_project, current_project):
    """Same-project memories rank up; other-project ones rank down but survive.

    Cross-project memories are not excluded: a lesson learned elsewhere is often
    exactly what is needed here.
    """
    if not current_project or not memory_project:
        return 1.0
    if memory_project == current_project:
        return PROJECT_MATCH_BOOST
    return PROJECT_MISMATCH_PENALTY


def score(memory, current_project=None, half_life_days=30.0, now=None):
    importance = float(memory.get("importance", 0.5) or 0.0)
    return (
        importance
        * recency_decay(memory.get("created_at"), half_life_days, now)
        * project_factor(memory.get("project"), current_project)
    )


def estimate_tokens(memory):
    text = "{} {}".format(memory.get("title", ""), memory.get("body", ""))
    return max(1, len(text) // CHARS_PER_TOKEN)


def rank(memories, current_project=None, half_life_days=30.0, now=None):
    """Return memories ordered best-first. Pinned always lead."""
    scored = [
        (bool(m.get("pinned")), score(m, current_project, half_life_days, now), m)
        for m in memories
    ]
    # Sort key: pinned first, then score, then recency as a stable tiebreak so
    # equal-scoring memories keep a predictable order.
    scored.sort(key=lambda t: (t[0], t[1], t[2].get("created_at") or ""), reverse=True)
    return [m for _pinned, _s, m in scored]


def select_within_budget(memories, token_budget, max_items=None,
                         current_project=None, half_life_days=30.0, now=None):
    """Take the best memories that fit the budget.

    Skips oversized items rather than stopping at the first one, so a single
    long memory cannot crowd out everything ranked below it.
    """
    ordered = rank(memories, current_project, half_life_days, now)
    chosen, used = [], 0
    for memory in ordered:
        if max_items is not None and len(chosen) >= max_items:
            break
        cost = estimate_tokens(memory)
        if used + cost > token_budget:
            if memory.get("pinned") and used < token_budget:
                chosen.append(memory)
                used += cost
            continue
        chosen.append(memory)
        used += cost
    return chosen, used
