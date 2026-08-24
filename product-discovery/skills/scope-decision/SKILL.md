---
name: scope-decision
description: Decide what is in, what is out, and record why — including the high-impact assumption gate. Use at the end of DEFINE, before any specification work.
stage: 4
inputs: [artifacts/4-opportunities.md, artifacts/4-users.md, assumptions.md, artifacts/1-outcomes.md]
outputs: [artifacts/4-scope-decision.md]
depth: standard | deep
---

# Scope Decision

## Purpose

Decide what this project will and will not do, record the reasoning, and confirm the
evidence base can actually carry the decision.

This is the framework's most consequential gate. Everything downstream inherits it, and it
is the point where an unvalidated high-impact assumption stops being a manageable unknown
and becomes a silent foundation.

## When To Use

- At the end of DEFINE, before SPECIFY
- When scope has drifted and needs re-deciding — re-run rather than amending informally

## When Not To Use

- Before opportunities are mapped. A scope decision with no alternatives considered is
  not a decision, it is a default.

## The gate

**Before deciding scope, check the assumption ledger for open high-impact assumptions.**

    python3 scripts/lint-evidence.py <project-dir>

Per `protocol/assumptions.md`, a high-impact assumption is one whose wrong answer
invalidates scope, approach, or the business case. Scope decided over one is not a real
decision — it is a bet nobody knows they placed.

Three ways through, in order of preference:

1. **Validate it.** Often cheaper than expected. Check `how_to_validate` — the answer is
   frequently in material already mined.
2. **Reduce its impact** by narrowing scope so it no longer sits under the whole decision.
3. **Accept it** — `status: accepted`, with a **named person** accepting the risk, and the
   acceptance stated in this artifact's Risks section.

**Claude may not accept a risk on anyone's behalf.** If the gate blocks and nobody has
accepted, the correct output is to stop and report which assumptions block, what each would
take to validate, and what scope would look like if each turned out to be wrong. That report
is the deliverable, not a failure to finish.

## Process

Follow `protocol/facilitation.md`.

**1. Run the gate.** Resolve, reduce, or escalate before proceeding.

**2. State the options considered.** At minimum: the requested scope, a smaller scope, and
one materially different approach from the opportunity map. A decision with one option on
the table is not a decision.

**3. For each option, state what it serves and what it leaves.** Which opportunities does it
address, which outcomes does it move, what does it explicitly not do.

**4. Decide, and record why this one.** The reasoning is the artifact's most valuable
content — it is what lets a future reader (often you) understand a choice whose context has
been forgotten.

**5. Record what would change the decision.** Which finding, if it turned out differently,
would make this wrong? This makes the decision revisable rather than permanent, and it names
what to watch.

**6. State non-scope explicitly and generously.** Everything people will reasonably assume is
included. Each entry prevents a later argument, and this section is consistently
under-written because it feels negative.

**7. Name the decider and record their agreement.** A scope decision nobody with authority
agreed to is a proposal. Per `map-stakeholders`, name the person.

## Output Contract

**Path:** `artifacts/4-scope-decision.md`

**Required sections:**
- `# Scope Decision`
- `## Gate Check` — open high-impact assumptions and how each was resolved, reduced, or accepted
- `## Options Considered` — at least three, each with what it serves and leaves
- `## Decision` — what is in scope
- `## Why This One` — the reasoning
- `## Not In Scope` — explicit exclusions
- `## What Would Change This` — findings that would invalidate the decision
- `## Decider` — who agreed, and when
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: scope-decision`, `stage: 4`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite:** every claim about what an option would achieve, cost, or require.

**Must cite or mark as assumption:** effort and complexity estimates. These drive the
decision and are the most commonly invented content in a scope artifact.

**May be reasoned:** the decision itself and its rationale. A scope decision is a judgment
— what must be evidenced is the basis, not the conclusion.

## Pitfalls

**Pitfall 1 — Deciding over an open high-impact assumption.**
*Symptom:* The gate check section is missing or perfunctory. *Consequence:* Every downstream
artifact rests on an unexamined bet. *Fix:* Run `lint-evidence.py`. Resolve, reduce, or get
a named acceptance.

**Pitfall 2 — One option.**
*Symptom:* Options Considered lists the requested scope and nothing else.
*Consequence:* The decision was made before the project started. *Fix:* Pull alternatives
from the opportunity map, including a non-software one.

**Pitfall 3 — Thin non-scope.**
*Symptom:* One or two obvious exclusions. *Consequence:* Scope creep with no documented
basis to push back. *Fix:* Name what people will assume is included.

**Pitfall 4 — No named decider.**
*Symptom:* "Agreed by the team." *Consequence:* Nobody owns it, and it reopens.
*Fix:* Name a person and a date.

**Pitfall 5 — Recording the decision without the reasoning.**
*Symptom:* What, no why. *Consequence:* Six months on, nobody can tell whether changed
circumstances should change the decision. *Fix:* Write the reasoning and what would
invalidate it.

## References

**Related skills:** `map-opportunities` (stage 4), `prioritize` (stage 4),
`write-prd` (stage 5), `decision-record` (stage 7)

**Protocol:** `protocol/assumptions.md`, `protocol/evidence.md`

**Scripts:** `scripts/lint-evidence.py` — run this before deciding
