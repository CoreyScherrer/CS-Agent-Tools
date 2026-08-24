---
name: spec-trust-requirements
description: Specify what correct means, how it is verified, and what the product does when it is not confident. Use during SPECIFY on any analytics product where a wrong answer would be acted upon.
stage: 5
domain: analytics
inputs: [artifacts/4-definitions.md, artifacts/5-prd.md]
outputs: [artifacts/5-trust-requirements.md]
depth: standard | deep
---

# Spec Trust Requirements

## Purpose

Specify correctness, freshness, lineage, and low-confidence behavior as first-class
requirements.

For an analytics product, correctness is not a non-functional requirement — it is the
product. A slow dashboard is an annoyance. A dashboard that quietly disagrees with the
system of record destroys trust in every number it displays, including the correct ones,
and that trust does not return easily. People go back to their spreadsheets and stay there.

The failure is rarely a wrong calculation. It is an unstated one: a number displayed with
no indication that its source is stale, partial, or computed under a definition the viewer
does not share.

## When To Use

- Any product that presents numbers people act on
- Especially replacements for existing reporting, where consumers will reconcile against
  what they had — and they will, on day one
- Runs inside SPECIFY, after definitions are governed

## When Not To Use

- Exploratory or directional tooling where consumers understand the numbers are indicative,
  and this is stated in the product. Say so explicitly rather than assuming it.

## Process

**1. Establish the reconciliation target.** What does this need to agree with, and to what
tolerance? Usually an existing report or a system of record. If nothing is authoritative,
that is a finding worth surfacing loudly — it means the organization has no ground truth
and the new product will be blamed for revealing it.

**2. Specify freshness per measure.** When was the underlying data last updated, how is
that surfaced, and what happens when it is later than expected. Freshness is not global —
different sources land at different times, and a view mixing them is only as fresh as its
oldest input.

**3. Specify completeness.** What does the product do with partial data? Showing a partial
day as if complete is among the most damaging defects possible, because the number looks
normal and is wrong in a way nobody checks.

**4. Specify lineage.** For any number, can a consumer determine where it came from and
which definition produced it? For contested or legitimately plural terms this is mandatory,
not optional.

**5. Specify low-confidence behavior.** What the product does when it cannot stand behind
an answer: stale source, partial data, ambiguous question, definition mismatch. Options
include showing the caveat, refusing to answer, or routing to a human. **The one
unacceptable option is answering anyway with no signal.**

For a natural-language interface this extends further — what happens when the question is
ambiguous, out of scope, or maps to no available data. Guessing at intent and returning a
confident answer is the same failure in a different costume.

**6. Specify verification.** How correctness is tested before release and monitored after.
Reconciliation against the target on a known period is usually the cheapest meaningful
test, and it should run continuously, not once.

**7. Specify the escalation path.** When a consumer believes a number is wrong, what do
they do? An unclear path means disputes surface as loss of trust rather than as tickets you
can act on.

## Output Contract

**Path:** `artifacts/5-trust-requirements.md`

**Required sections:**
- `# Trust Requirements`
- `## Reconciliation Target` — what this must agree with, and tolerance
- `## Freshness` — per source and per view, with surfacing behavior
- `## Completeness` — partial-data behavior
- `## Lineage` — traceability from number to source and definition
- `## Low-Confidence Behavior` — what happens when the product cannot stand behind an answer
- `## Verification` — pre-release testing and ongoing monitoring
- `## Escalation` — the dispute path
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: trust-requirements`, `stage: 5`, `domain: analytics`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** current refresh schedules, existing reconciliation
tolerances, known data quality issues, actual landing times.

**Never invent a refresh schedule or a tolerance.** These are checkable facts about real
systems. An invented "data refreshes nightly" in a requirements document becomes a design
assumption and then a production defect.

## Pitfalls

**Pitfall 1 — Trust as a non-functional footnote.**
*Symptom:* Correctness appears as one line under "Quality". *Consequence:* It gets traded
away under schedule pressure, and the product ships with no confidence signals.
*Fix:* First-class requirements with acceptance criteria.

**Pitfall 2 — No reconciliation target.**
*Symptom:* Nobody can say what the product must agree with. *Consequence:* Every
disagreement is unresolvable, and adoption stalls. *Fix:* Name a target or escalate the
absence as a finding.

**Pitfall 3 — Confident answers under uncertainty.**
*Symptom:* No specified behavior for stale, partial, or ambiguous cases. *Consequence:*
The product answers anyway and is wrong silently — the worst available outcome.
*Fix:* Specify it. Silence is a design decision made by default.

**Pitfall 4 — Verification as a launch gate only.**
*Symptom:* Reconciliation tested once before release. *Consequence:* Drift goes undetected
until a consumer finds it, which costs more trust than the original defect.
*Fix:* Continuous reconciliation with alerting.

## References

**Related skills:** `govern-definitions` (stage 4, analytics), `write-prd` (stage 5),
`define-acceptance` (stage 5)

**Protocol:** `protocol/evidence.md`, `protocol/artifact-standards.md`

**Domain:** `domains/analytics/DOMAIN.md`
