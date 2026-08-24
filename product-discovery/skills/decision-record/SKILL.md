---
name: decision-record
description: Record a decision, its reasoning, and what would reverse it, so a future reader can tell whether it still holds. Use whenever a decision will outlive the memory of why it was made.
stage: 7
inputs: [the decision, evidence/findings.md, assumptions.md]
outputs: [artifacts/7-decision-<slug>.md]
depth: quick | standard
---

# Decision Record

## Purpose

Record what was decided, why, and what would change it — so that someone encountering the
decision later can tell whether it still holds.

The characteristic enterprise failure is not undocumented decisions. It is decisions
documented without their reasoning, which leaves future readers two bad options: follow a
rule whose basis may have evaporated, or overturn it without knowing what it was protecting.

The reasoning is the artifact. The decision is the headline.

## When To Use

- Any decision that will outlive the memory of why it was made
- Definition decisions, scope decisions, technology choices, deliberate exclusions
- Whenever you find yourself explaining the same decision a second time

## When Not To Use

- Reversible decisions with no downstream dependency
- As a substitute for deciding. A record of an undecided question is a status note.

## Process

Follow `protocol/facilitation.md`.

**1. State the decision in one sentence,** in the present tense, as a rule. "Net sales
excludes returns for merchandising reporting." A reader should be able to apply it without
reading further.

**2. Record the date and the decider.** A decision with no named decider reopens the first
time someone disagrees.

**3. State the context that made it necessary.** What was true at the time that required a
decision. This is what future readers use to judge whether circumstances have changed —
and it is the most commonly omitted section.

**4. State the options considered and why each was rejected.** The rejected options carry
most of the value. Someone proposing a change six months on is usually proposing something
already considered, and the record either saves that conversation or shows the
circumstances genuinely changed.

**5. State the reasoning,** with citations to the evidence that supported it. This is what
distinguishes a record from a decree.

**6. State the consequences accepted.** Every decision costs something. Naming the cost
prevents later readers concluding the tradeoff was overlooked — and prevents you being
told you overlooked it.

**7. State what would reverse it.** The specific change in circumstance, evidence, or
constraint that should trigger reconsideration. This makes the decision durable without
making it permanent.

**8. Record open assumptions the decision rests on,** by ID. If one is later invalidated,
the ledger's `what_it_affects` points here.

## Output Contract

**Path:** `artifacts/7-decision-<slug>.md` — one file per decision

**Required sections:**
- `# Decision: <the rule, in one sentence>`
- `## Date And Decider` — when, and who
- `## Context` — what made this necessary
- `## Options Considered` — each, with why rejected
- `## Reasoning` — why this one, cited
- `## Consequences Accepted` — what this costs
- `## What Would Reverse This` — the trigger for reconsideration
- `## Assumptions This Rests On` — by ID
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: decision-record`, `stage: 7`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite:** the evidence that supported the decision. A record whose reasoning cites
nothing documents that a decision was made, not that it was justified.

**Must cite or mark as assumption:** claims about consequences, costs, or what alternatives
would have required.

**May be reasoned:** the decision and the weighing of options — that is what deciding is.
State the reasoning so it can be evaluated.

## Pitfalls

**Pitfall 1 — Decision without reasoning.**
*Symptom:* What was decided, not why. *Consequence:* Future readers cannot judge whether it
still applies, so they either follow it blindly or discard it. *Fix:* Reasoning is the
point; write it first.

**Pitfall 2 — Omitting rejected options.**
*Symptom:* Only the chosen path recorded. *Consequence:* The same alternatives get
re-proposed indefinitely. *Fix:* One line each on why not.

**Pitfall 3 — No reversal trigger.**
*Symptom:* The record reads as permanent. *Consequence:* Either it is treated as immovable
long after its basis changed, or it is overturned casually. *Fix:* Name the trigger.

**Pitfall 4 — Hiding the cost.**
*Symptom:* No consequences section. *Consequence:* Reads as a decision with no downside,
which is never true and which undermines trust when the downside appears.
*Fix:* State what was given up.

**Pitfall 5 — Writing it later.**
*Symptom:* Reconstructed weeks after the fact. *Consequence:* The reasoning is rationalized
rather than recorded, and the rejected options are forgotten. *Fix:* Write it at the time.

## References

**Related skills:** `scope-decision` (stage 4), `govern-definitions` (analytics domain),
`exec-brief` (stage 7)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**External frameworks:** The format follows the Architecture Decision Record pattern
introduced by Michael Nygard (2011), extended here with explicit evidence citation, a
reversal trigger, and a link to the assumption ledger.
