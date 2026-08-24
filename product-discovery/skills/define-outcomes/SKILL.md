---
name: define-outcomes
description: Define what changes in the world if this succeeds, separately from what gets built. Use immediately after framing the problem, before any solution discussion.
stage: 1
inputs: [artifacts/1-problem-statement.md, evidence/findings.md]
outputs: [artifacts/1-outcomes.md]
depth: quick | standard | deep
---

# Define Outcomes

## Purpose

State what will be observably different if this works, and how you will know.

Teams routinely ship everything they planned and change nothing. This happens because
success was defined as delivery — the dashboard exists, the migration completed, the
feature launched — and delivery is not an outcome. It is a precondition for one.

An outcome is a change in behavior or a change in a number that someone cares about. It is
true or false independent of how you achieved it.

## When To Use

- Right after `frame-problem`, before anyone discusses solutions
- When a project has been running and nobody can say what success looks like
- Before prioritization — you cannot prioritize against an undefined goal

## When Not To Use

- Before the problem is framed. Outcomes derived from an unframed problem measure the
  wrong thing precisely.

## Process

Follow `protocol/facilitation.md`.

**1. Start from the problem statement's cost.** If the status quo costs something, the
outcome is that cost reducing. This keeps outcomes tied to evidence rather than to
aspiration.

**2. Write each outcome as an observable change.** The test: could a stranger determine
whether it happened, without knowing what you built? "Analysts stop rebuilding the weekly
report by hand" passes. "We deliver a reporting platform" does not.

**3. Separate leading from lagging.** Lagging outcomes are what you actually want and are
slow to move. Leading indicators move early and predict them. You need both — lagging
alone means you learn nothing for two quarters; leading alone means you optimize a proxy.

**4. Set a baseline for each.** An outcome with no baseline is unmeasurable — "reduce
reconciliation questions" means nothing without knowing today's volume. **Cite the
baseline or register it as an assumption.** A baseline you invented makes every subsequent
measurement meaningless while looking rigorous.

Where no baseline exists, that is itself a finding, and establishing one may be the first
piece of work.

**5. Set guardrails.** What must *not* get worse. Most initiatives can hit their target by
damaging something adjacent — speed at the cost of correctness, adoption at the cost of
trust, automation at the cost of the ability to answer novel questions. Name what you are
protecting.

**6. Name a target and a date only if you can source them.** Where a target is a genuine
business commitment, cite who set it. Where it is aspiration, say so. **Do not manufacture
a target percentage.** An invented "reduce by 40%" becomes the yardstick the project is
judged against, and nobody remembers it was made up.

**7. Name what you will not measure** and why. Prevents metric sprawl later.

## Output Contract

**Path:** `artifacts/1-outcomes.md`

**Required sections:**
- `# Outcomes`
- `## Lagging Outcomes` — what we actually want; each with baseline, target if sourced, owner
- `## Leading Indicators` — what moves early and predicts the above
- `## Guardrails` — what must not get worse
- `## Baselines` — current state per measure, cited or assumption-marked
- `## Not Measuring` — deliberate exclusions and why
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: outcomes`, `stage: 1`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** every baseline, every target, every claim that a
measure currently sits at a given level.

**May be reasoned:** the choice of which outcomes matter, guardrail selection, exclusions.
These are judgments — state the reasoning.

**Never invent:** a baseline, a target, or a percentage improvement. These are the numbers
most likely to be quoted back in a review, and the ones nobody re-derives.

## Pitfalls

**Pitfall 1 — Outcomes that are deliverables.**
*Symptom:* Every item is something you build. *Consequence:* You can ship completely and
change nothing, and the project reports success. *Fix:* Apply the stranger test — could
someone tell it happened without knowing what you built?

**Pitfall 2 — No baseline.**
*Symptom:* "Reduce X" with no current value. *Consequence:* Unfalsifiable; any result can
be narrated as progress. *Fix:* Establish it, or register the gap as an assumption and
make measuring it the first task.

**Pitfall 3 — Invented targets.**
*Symptom:* Round numbers with no attribution — 20% faster, 50% fewer.
*Consequence:* The project is judged against fiction. *Fix:* Cite who committed to it or
label it aspiration.

**Pitfall 4 — No guardrails.**
*Symptom:* Only things to increase. *Consequence:* The target gets hit by damaging
something nobody was watching. *Fix:* For each outcome ask how a cynical team could hit it
while making things worse. Guard that.

**Pitfall 5 — Leading indicators that are just activity.**
*Symptom:* Logins, page views, tickets closed. *Consequence:* You optimize motion.
*Fix:* A leading indicator must plausibly *cause* the lagging outcome. State the mechanism.

## References

**Related skills:** `frame-problem` (stage 1), `map-stakeholders` (stage 1),
`prioritize` (stage 4), `assess-risk` (stage 6)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**External frameworks:** Outcome-over-output framing follows Josh Seiden, *Outcomes Over
Output* (2019), and Teresa Torres, *Continuous Discovery Habits* (2021). The
leading/lagging distinction is standard management measurement practice; guardrail metrics
follow common experimentation practice as described by Kohavi, Tang, and Xu, *Trustworthy
Online Controlled Experiments* (2020).
