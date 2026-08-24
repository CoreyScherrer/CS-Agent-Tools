---
name: map-opportunities
description: Map the space of opportunities between the desired outcome and possible solutions, so scope is a choice among alternatives rather than the first idea. Use after discovery, before deciding what to build.
stage: 4
inputs: [artifacts/1-outcomes.md, artifacts/3-research-synthesis.md, evidence/findings.md]
outputs: [artifacts/4-opportunities.md]
depth: standard | deep
---

# Map Opportunities

## Purpose

Lay out the distinct ways the desired outcome could be reached, so that choosing one is a
decision among alternatives rather than commitment to whatever was proposed first.

Enterprise projects usually arrive with a solution attached. By the time discovery
finishes, the team has often spent weeks gathering evidence about a solution nobody ever
compared to anything. This skill inserts the comparison.

An opportunity is not a solution. It is an unmet need, obstacle, or friction point that,
if addressed, would move the outcome. Several solutions can serve one opportunity; the
same solution can serve several.

## When To Use

- After DISCOVER, before scope is decided
- When a request arrived pre-solved and nothing else has been considered
- When the team is arguing about solutions without agreeing on what problem each solves

## When Not To Use

- Before evidence exists. Opportunities invented without findings are just ideas.
- On genuinely trivial work with one obvious path — say so rather than performing the map.

## Process

Follow `protocol/facilitation.md`.

**1. Start from the outcome, not the request.** Write the target outcome at the top. Every
opportunity must plausibly move it.

**2. Derive opportunities from findings.** Each one traces to evidence — a friction point
observed, a workaround inventoried, a request theme, a conflict. **An opportunity with no
evidence behind it is a hypothesis you invented**, and it belongs in the assumption ledger
rather than on the map.

**3. Phrase them as needs or obstacles, not solutions.** "Analysts cannot answer novel
questions without writing SQL" is an opportunity. "Build a query builder" is a solution to
it. Keeping them separate is what lets you see that three proposed projects address the
same opportunity, or that the flagship one addresses none.

**4. Group and find the structure.** Which opportunities share a root cause? A cluster of
frictions traceable to one undefined term is one opportunity, not five — and addressing the
root serves all of them.

**5. Size each by evidence strength and outcome impact.** How well-supported is it, and how
much would resolving it move the outcome? Both matter: a well-evidenced trivial opportunity
and a speculative critical one are different bets, and neither dominates.

**6. Only then, sketch solutions.** Two or three per opportunity worth pursuing, deliberately
including one that is not software. Process changes, definition decisions, and stopping
something are legitimate solutions and frequently the cheapest.

**7. Note which opportunities the originally-requested solution addresses.** Often
illuminating, sometimes uncomfortable, and always worth knowing before the scope conversation.

## Output Contract

**Path:** `artifacts/4-opportunities.md`

**Required sections:**
- `# Opportunities`
- `## Target Outcome` — what all of this is meant to move
- `## Opportunities` — each with evidence IDs, outcome impact, evidence strength
- `## Clusters` — shared root causes, and what addressing the root would serve
- `## Candidate Solutions` — per opportunity, including at least one non-software option
- `## What The Original Request Addresses` — mapping the incoming ask onto this map
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: opportunities`, `stage: 4`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite:** every opportunity traces to findings. This is the hard rule of this skill —
an uncited opportunity is speculation, and a map of speculation produces a confidently
wrong scope decision.

**Must cite or mark as assumption:** any claim about how much an opportunity would move the
outcome.

**May be reasoned:** the clustering, the solution sketches, and the impact ratings — these
are judgments. State the reasoning.

## Pitfalls

**Pitfall 1 — Solutions disguised as opportunities.**
*Symptom:* Entries name features. *Consequence:* You compare implementations rather than
problems, and the map cannot show that two projects serve one need.
*Fix:* Rewrite each as a need or obstacle. If it names a mechanism, it is a solution.

**Pitfall 2 — Uncited opportunities.**
*Symptom:* Plausible entries with no evidence IDs. *Consequence:* Scope built on invention
that has passed through a formal-looking artifact. *Fix:* Cite or move to the ledger.

**Pitfall 3 — No non-software option.**
*Symptom:* Every candidate solution is a build. *Consequence:* You miss that a definition
decision or a retirement would serve the outcome for a fraction of the cost.
*Fix:* Require one per opportunity. It is often the right answer.

**Pitfall 4 — Skipping the request mapping.**
*Symptom:* The map never checks the original ask against it. *Consequence:* Nobody notices
the requested solution addresses a minor opportunity. *Fix:* Do it explicitly, and share it.

## References

**Related skills:** `define-outcomes` (stage 1), `synthesize-research` (stage 3),
`scope-decision` (stage 4), `prioritize` (stage 4)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**External frameworks:** The outcome → opportunity → solution → experiment structure is
Teresa Torres's Opportunity Solution Tree, from *Continuous Discovery Habits* (2021).
Framing opportunities as unmet needs rather than features follows Jobs-to-be-Done as
developed by Clayton Christensen (*Competing Against Luck*, 2016) and Anthony Ulwick.
