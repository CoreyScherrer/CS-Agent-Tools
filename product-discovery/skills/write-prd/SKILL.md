---
name: write-prd
description: Write a requirements document that traces every requirement to evidence. Use when discovery is complete enough to specify what gets built, and engineering needs something actionable.
stage: 5
inputs: [artifacts/1-problem-statement.md, artifacts/2-evidence-summary.md, artifacts/4-scope-decision.md, evidence/findings.md, assumptions.md]
outputs: [artifacts/5-prd.md]
depth: quick | standard | deep
---

# Write PRD

## Purpose

Turn validated understanding into a document engineering can build from, where every
requirement traces to a reason. The tracing is the point. A requirements document whose
requirements have no stated origin cannot be prioritized, cut, or defended — when someone
asks "why is this in scope?", the honest answer is "someone wrote it down."

## When To Use

- Discovery has produced enough evidence to specify a solution
- Scope is decided and the build is real
- Engineering needs something more durable than a conversation

## When Not To Use

- The problem is not framed (go to `frame-problem`)
- High-impact assumptions are still open — per `protocol/assumptions.md`, these block
  advancement past DEFINE. Resolve or explicitly accept them first.
- The work is small enough that stories alone suffice (go to `write-stories`)
- You are writing it to look thorough rather than because someone will read it

## Inputs

The problem statement, the evidence summary, the scope decision, and both ledgers. A PRD
written without reading `assumptions.md` will silently restate assumptions as facts —
the failure mode `protocol/assumptions.md` calls assumption laundering.

## Process

Follow `protocol/facilitation.md`.

**1. Verify the gate.** Check `assumptions.md` for open high-impact entries. If any exist,
stop and report them. Proceeding requires a named person accepting each risk, recorded in
the ledger as `accepted`. Do not quietly proceed.

**2. Restate the problem from the artifact, not from memory.** Copy the framing forward
with its citations intact. Do not re-derive it — re-derivation is where drift enters.

**3. Write requirements, each traced.** Every requirement carries:
- What the system must do, in observable terms
- Priority (must / should / could for this release)
- **Why** — the finding ID or assumption ID that motivates it

A requirement with no traceable origin is a lint failure and, more importantly, a signal
that someone's preference entered the document unexamined. Either find the evidence or
register the assumption.

**4. Write acceptance criteria per requirement.** Observable, testable conditions. "The
report loads quickly" is not testable; "the report returns in under N seconds at P95, at
current data volume [E-nnn]" is. Where you cannot source a threshold, mark it as an
assumption rather than inventing a number that will be treated as a commitment.

**5. State non-goals explicitly.** What this deliberately does not do, and why. Non-goals
prevent the scope conversation from being relitigated in every review.

**6. Document dependencies and constraints,** each cited to where it was established.

**7. Carry open assumptions forward.** List every assumption this PRD relies on, with
impact and validation path. These are the risks in the plan; hiding them does not remove
them.

**8. Run the critic, then lint.**

    (invoke critique-artifact on artifacts/5-prd.md)
    python3 scripts/lint-artifact.py <project-dir>

Only after both pass may status move to `reviewed`. Only a human sets `final`.

## Output Contract

**Path:** `artifacts/5-prd.md`

**Required sections:**
- `# PRD: <name>`
- `## Problem` — carried forward with citations
- `## Users And Context` — who this serves, cited
- `## Goals` — outcomes, not deliverables
- `## Non-Goals` — explicit exclusions with reasons
- `## Requirements` — each with priority and a `why` traceable to an ID
- `## Acceptance Criteria` — observable and testable, per requirement
- `## Dependencies And Constraints` — cited
- `## Open Assumptions` — carried from the ledger with impact ratings
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: prd`, `stage: 5`.

## Evidence Requirements

Per `protocol/evidence.md`. Stricter here than elsewhere, because this document drives
spend:

**Must cite or mark as assumption:**
- Every requirement's `why`
- Every quantitative threshold in acceptance criteria
- Every claim about user need, volume, frequency, or current behavior
- Every stated constraint

**May be reasoned without citation:**
- The solution design itself (that is engineering judgment, and should be labeled as such)
- Priority ordering (a decision, though it should reference the prioritization artifact)
- Non-goal boundaries

**Provenance must reach ground.** Citing the problem statement is not sufficient if the
problem statement cited nothing. The chain has to terminate in a real source.

## Pitfalls

**Pitfall 1 — Requirements with no origin.**
*Symptom:* A requirements list that reads as self-evident. *Consequence:* Nothing can be
cut, because nobody knows what it was for. *Fix:* Every requirement gets a `why` with an
ID. Requirements that cannot get one are usually someone's preference — surface that
rather than encoding it.

**Pitfall 2 — Invented thresholds.**
*Symptom:* "Under 2 seconds", "99.9% uptime", "supports 500 concurrent users" with no
source. *Consequence:* Arbitrary numbers become contractual, and engineering spends real
money hitting a target nobody chose deliberately. *Fix:* Cite the source or mark it as an
assumption with an owner.

**Pitfall 3 — Assumption laundering.**
*Symptom:* Something registered as an assumption in DEFINE appears in the PRD as a plain
statement. *Consequence:* Risk disappears from view while remaining in the plan.
*Fix:* Read `assumptions.md` before writing. Every entry it lists as open must appear
either with its marker or in Open Assumptions.

**Pitfall 4 — Goals that are deliverables.**
*Symptom:* Goals section lists what you will build. *Consequence:* Success becomes
"we shipped", decoupled from whether anything improved. *Fix:* For each goal, ask whether
it would still be satisfied by a completely different implementation.

**Pitfall 5 — Writing for thoroughness.**
*Symptom:* Long PRD for small work; sections filled because the template had them.
*Consequence:* Nobody reads it, so it stops being a shared understanding.
*Fix:* Depth follows triage. At `depth: quick`, several sections legitimately collapse to
a line each. An honest short document beats a padded long one.

## References

**Related skills:** `frame-problem` (stage 1), `mine-corpus` (stage 2), `scope-decision`
(stage 4), `write-stories` (stage 5), `define-acceptance` (stage 5),
`critique-artifact` (any stage)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`,
`protocol/artifact-standards.md`, `protocol/facilitation.md`

**External frameworks:** Outcome-over-output goal framing follows Josh Seiden,
*Outcomes Over Output* (2019) and Teresa Torres, *Continuous Discovery Habits* (2021).
Observable acceptance criteria follow the Given/When/Then convention from Dan North's
Behaviour-Driven Development (2006). Requirement prioritization language (must/should/could)
follows MoSCoW, originated by Dai Clegg at Oracle (1994).
