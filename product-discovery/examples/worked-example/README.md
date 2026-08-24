# Worked Example

A complete FRAME + MINE pass on a realistic internal-analytics scenario. Read this before
starting your first project — it answers most format questions faster than the protocol
docs do.

The scenario: a merchandising analytics team gets ad-hoc questions from eight business
users, two analysts hand-build five recurring reports, and leadership has asked for "a
self-service dashboard."

Everything here was produced by following the skills against a fixed corpus of five
sources. Both linters pass.

## What to look at, and why

**`evidence/findings.md` — E-015 and E-016.** Conflict entries. E-015 catches that a
runbook's "about a day" per report and a ticket's "6 hrs/week" for all five cannot both
hold, lays out four explanations the corpus cannot distinguish between, and **refuses to
resolve it**. That refusal is the deliverable. Picking one would have manufactured a
number that then drives the business case.

**`assumptions.md` — A-002.** A high-impact assumption: that the "why doesn't this match"
requests are caused by the divergent category mappings. Both facts are evidenced; the
causal link is not. It is the natural narrative spine of the whole problem statement, and
it is registered rather than asserted. Note what `how_to_validate` reveals — the answer is
sitting in an export already mined, unread. Registering the assumption produced the
cheapest high-value next action on the project.

**`artifacts/2-evidence-summary.md` — What The Corpus Could Not Answer.** Every source is
authored by or about the analytics team. Not one is from a business user. The 143 requests
were counted, never read. A summary that skipped this section would have read as a solid
evidence base; the section is what exposes that it is one-sided.

**What is absent.** No cost-per-request figure. No annualized dollar cost. No claim about
what the "category fix" tab does. Each was reachable by plausible arithmetic and none is
sourced, so none appears.

## Verify it yourself

    python3 ../../scripts/lint-evidence.py .
    python3 ../../scripts/lint-artifact.py .

The evidence lint reports four open high-impact assumptions. That is correct and expected
at this stage — see `protocol/assumptions.md` on the DEFINE gate. Early stages are where
high-impact assumptions accumulate; the gate is at DEFINE, not here.

## Caveat

Produced non-interactively from a fixed corpus, with no stakeholder to question. A real
FRAME pass would resolve several of these assumptions by asking. The artifacts say so in
their Provenance.
