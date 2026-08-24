---
name: write-stories
description: Break specified requirements into deliverable units that each stand on their own. Use after the PRD, when work needs to be sized and sequenced for delivery.
stage: 5
inputs: [artifacts/5-prd.md, artifacts/4-priorities.md]
outputs: [artifacts/5-stories.md]
depth: quick | standard | deep
---

# Write Stories

## Purpose

Break requirements into units small enough to build, estimate, and deliver independently,
without losing the reason each exists.

The failure this prevents is not badly-formatted stories. It is stories that have become
disconnected from their evidence — a backlog of tasks nobody can trace to a need, which
gets worked through faithfully and delivers nothing anyone wanted.

## When To Use

- After the PRD, when moving to delivery planning
- When a requirement is too large to estimate or sequence
- When a backlog item has been carried across several cycles without being started — that
  usually means it is too big or too vague

## When Not To Use

- Before requirements are specified. Stories written from an unwritten PRD become the
  specification by accident, and an incomplete one.
- For work with no user-visible outcome — infrastructure and enabling work is legitimate
  and does not need to be contorted into user-story shape.

## Process

Follow `protocol/facilitation.md`.

**1. Start from requirements, carrying their citations.** Every story traces to a PRD
requirement, which traces to evidence. This chain is what keeps the backlog honest.

**2. Write each as who, what, why.** The `why` is the part that matters and the part that
degrades first — it is what lets someone building it make a sensible judgment call, and
what lets someone challenge whether it is still needed.

**3. Split by value, not by layer.** A story delivering "the database table" is not
deliverable — nobody can use it and nobody can tell whether it worked. Useful split
patterns:

- By workflow step — the path through, before the branches
- By rule complexity — the simple rule first, the exceptions after
- By data variation — one category, then the rest
- By interface — one entry point before all of them
- By happy path — the working case, then the failures

Each split should produce something independently demonstrable.

**4. Keep each independently valuable where possible.** Where stories genuinely must be
sequential, say so rather than pretending independence. False independence produces
sprint plans that cannot actually execute.

**5. Size relatively, and stop when uncertain.** Where a story cannot be sized because
something is unknown, that unknown is an assumption — register it. A story nobody can size
is usually a research task in disguise, and naming it as one is more useful than guessing.

**6. Note what each story does not include.** Prevents scope drift inside the story, which
is where most estimate overruns actually originate.

## Output Contract

**Path:** `artifacts/5-stories.md`

**Required sections:**
- `# Stories`
- `## Stories` — each with who/what/why, requirement ID, evidence IDs, out-of-story notes
- `## Sequencing` — genuine dependencies, stated as such
- `## Unsizable` — stories blocked by an unknown, with assumption IDs
- `## Split Rationale` — how large requirements were divided and why
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: stories`, `stage: 5`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite:** each story references its PRD requirement. The requirement carries the
evidence; the story inherits it. **A story that cannot name its requirement is one someone
added without a source** — a common and quiet way scope grows.

**Must cite or mark as assumption:** any claim about user behavior embedded in a story's
`why`.

**May be reasoned:** the splitting, the sequencing, the sizing.

## Pitfalls

**Pitfall 1 — Orphan stories.**
*Symptom:* Backlog items with no traceable requirement. *Consequence:* The backlog accretes
work nobody can justify, and it gets built because it is there. *Fix:* Every story names its
requirement, or it is removed.

**Pitfall 2 — Splitting by technical layer.**
*Symptom:* Stories for the schema, the API, the UI. *Consequence:* Nothing is demonstrable
until all are done, so you lose the feedback the split was meant to enable.
*Fix:* Split so each slice does something observable.

**Pitfall 3 — Hollow why.**
*Symptom:* "so that we can have X." *Consequence:* Nobody can make a judgment call while
building, and nobody can challenge whether it is still needed. *Fix:* State the outcome for
the person.

**Pitfall 4 — False independence.**
*Symptom:* Everything marked independent. *Consequence:* Plans that cannot execute in the
stated order. *Fix:* Record real dependencies.

**Pitfall 5 — Guessing at unsizable work.**
*Symptom:* An estimate on something nobody understands. *Consequence:* A number enters
planning with no basis. *Fix:* Mark it unsizable, register the unknown, and consider a
research spike first.

## References

**Related skills:** `write-prd` (stage 5), `define-acceptance` (stage 5),
`prioritize` (stage 4)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**External frameworks:** The who/what/why story form and the INVEST heuristics come from
Mike Cohn, *User Stories Applied* (2004), building on Kent Beck's original XP formulation.
Vertical-slice splitting follows the patterns catalogued by Richard Lawrence and the
Humanizing Work story-splitting literature.
