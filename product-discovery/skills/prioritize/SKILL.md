---
name: prioritize
description: Order work by what the evidence supports, with the basis for each ranking visible. Use after scope is decided, when sequencing what to build first.
stage: 4
inputs: [artifacts/4-scope-decision.md, artifacts/4-opportunities.md, artifacts/1-outcomes.md]
outputs: [artifacts/4-priorities.md]
depth: quick | standard | deep
---

# Prioritize

## Purpose

Order the work so that what gets built first is what the evidence most supports and what
most reduces uncertainty.

Prioritization frameworks fail in enterprise settings for a specific reason: they produce a
number, the number looks objective, and the inputs that generated it were guesses. A RICE
score built on an invented reach figure and a confidence percentage someone felt like
typing is arithmetic performed on fiction, and it is harder to challenge than an honest
opinion because it looks like analysis.

This skill treats the **basis** of each ranking as the deliverable, not the ranking.

## When To Use

- After scope is decided, to sequence within it
- When a backlog has grown past what anyone can hold in mind
- When stakeholders disagree about order — the disagreement is usually about inputs, and
  making inputs visible resolves more than debating conclusions does

## When Not To Use

- Before scope is decided. Prioritizing an unbounded list is how scope decisions get made
  accidentally.
- On a list of three items. Discuss them.

## Process

Follow `protocol/facilitation.md`.

**1. Choose a method appropriate to what you actually know.**

- **Evidence-ranked ordering** — sort by strength of evidence and outcome impact, no
  scoring. Best default when inputs are qualitative, which in enterprise internal work they
  usually are.
- **Value versus effort** — two dimensions, plotted not scored. Works when effort is
  genuinely estimable.
- **Weighted scoring (RICE, ICE, and relatives)** — only when the inputs are measured
  rather than felt. **If you would have to invent reach or confidence numbers, do not use
  it.** A scoring framework applied to guesses launders them into apparent rigor.
- **Sequencing by uncertainty** — do the thing that resolves the biggest unknown first,
  regardless of value. Correct when a high-impact assumption is still shaping the work.

State which method and why. The choice is part of the artifact.

**2. Rank, and record the basis per item.** Each item carries the evidence IDs behind its
placement. An item whose rank rests on judgment says so — that is legitimate, provided it
is visible.

**3. Surface what is being deferred and what that costs.** Deferral is a decision with
consequences, and the consequences are usually invisible unless written down.

**4. Check for dependency ordering.** Some sequences are constrained regardless of value —
a definition must be agreed before anything computing it can be built. Note where dependency
overrides value ranking.

**5. Check for uncertainty ordering.** Where an open assumption materially shapes several
items, the work that resolves it may belong first even if it delivers no user value. Name
this trade explicitly rather than burying it.

**6. Record what would reorder this.** Priorities are perishable. Naming the trigger makes
re-prioritization a response rather than a crisis.

## Output Contract

**Path:** `artifacts/4-priorities.md`

**Required sections:**
- `# Priorities`
- `## Method` — which approach, and why it suits what is actually known
- `## Ranking` — ordered, each with basis and evidence IDs
- `## Dependency Constraints` — where sequence is forced regardless of value
- `## Uncertainty-Driven Ordering` — work sequenced to resolve unknowns, and the trade
- `## Deferred` — what is not being done now, and what deferring costs
- `## What Would Reorder This` — triggers for revisiting
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: priorities`, `stage: 4`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** every input to a ranking — impact claims, effort
estimates, reach figures, usage frequencies.

**Never fabricate a scoring input.** This is the specific failure this skill exists to
prevent. If a framework requires a number you do not have, either get the number, register
it as an assumption with its impact rated, or use a method that does not require it.

**May be reasoned:** the ranking itself, the method choice, and the dependency analysis.

## Pitfalls

**Pitfall 1 — Scores from invented inputs.**
*Symptom:* Precise scores whose components nobody can source.
*Consequence:* Fiction with a decimal point, and it is harder to challenge than an opinion.
*Fix:* Cite every input or switch methods.

**Pitfall 2 — Prioritizing before scope.**
*Symptom:* A ranked list spanning more than the agreed scope. *Consequence:* Scope expands
by implication, without a decision. *Fix:* Scope first.

**Pitfall 3 — Ignoring uncertainty.**
*Symptom:* Ranking purely by value while a high-impact assumption shapes several items.
*Consequence:* You build in a direction that a cheap experiment would have redirected.
*Fix:* Consider uncertainty-driven ordering explicitly.

**Pitfall 4 — Silent deferral.**
*Symptom:* Items drop off the list without appearing in Deferred. *Consequence:* Nobody
knows what was decided against, and it resurfaces as a surprise. *Fix:* Record it and its cost.

**Pitfall 5 — Treating the ranking as durable.**
*Symptom:* No revisit trigger. *Consequence:* A stale order followed long after its basis
changed. *Fix:* Name what would reorder it.

## References

**Related skills:** `scope-decision` (stage 4), `map-opportunities` (stage 4),
`design-probe` (stage 6)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**External frameworks:** RICE scoring originated at Intercom (Sean McBride, 2016);
weighted-shortest-job-first and cost-of-delay reasoning come from Donald Reinertsen,
*The Principles of Product Development Flow* (2009). The caution against scoring
unmeasured inputs is this framework's own position, adopted because unsourced scoring
inputs are the most common way invented numbers enter a decision.
