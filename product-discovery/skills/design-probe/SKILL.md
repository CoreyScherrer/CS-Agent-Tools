---
name: design-probe
description: Design the cheapest test that could show a risky assumption is wrong. Use when a high-impact assumption remains open and building the real thing would be expensive.
stage: 6
inputs: [assumptions.md, artifacts/4-scope-decision.md, artifacts/5-prd.md]
outputs: [artifacts/6-probe.md]
depth: standard | deep
---

# Design Probe

## Purpose

Design the cheapest thing that could tell you a belief is wrong, before that belief becomes
expensive.

The word to notice is *wrong*. A test designed to demonstrate that an idea works will
generally succeed — the design, the framing, and the interpretation all bend toward
confirmation without anyone intending it. A probe designed to disconfirm produces
information either way.

## When To Use

- A high-impact assumption is open and validation from existing sources is not possible
- The cost of building the real thing substantially exceeds the cost of testing the belief
- The team is confident but the evidence is thin — that combination is where probes pay best

## When Not To Use

- The assumption is answerable from material already in hand. Check `identify-gaps` first;
  running an experiment to learn something already sitting in an export is expensive theater.
- The thing is cheap enough that building it *is* the cheapest test. Say so.
- Low-impact assumptions. Not everything needs testing.

## Process

Follow `protocol/facilitation.md`.

**1. Name the belief in falsifiable terms.** Not "users want self-service" — something that
could be shown false: "when analysts can get this number themselves, they stop filing
requests for it." If you cannot state what would disprove it, you cannot test it, and that
is worth knowing before spending anything.

**2. State what result would change the decision.** Before designing anything. If no
plausible result would change what you do, do not run the probe — you already decided, and
the probe is being run for reassurance.

This is the single most useful question in the skill and the most frequently skipped.

**3. Choose the cheapest form that could disconfirm.** In rough cost order:

- **Read what exists** — the answer may already be in the corpus
- **Ask directly** — sometimes one conversation settles it
- **Manual simulation** — do the thing by hand for one user for one week. Often the highest
  information per unit cost available, and it surfaces operational reality that no mockup does.
- **Prototype in front of a person** — for questions about comprehension or workflow fit
- **Limited pilot** — one team, real work, bounded time
- **Instrumented build** — genuinely last resort

**4. Define the signal in advance.** What you will measure, what counts as disconfirmation,
and the threshold. Deciding after seeing results is how any outcome becomes success.

**5. Set a time bound and a stop rule.** Probes without an end date become projects.

**6. Design against your own bias.** Ask: if this belief were false, would this probe reveal
it? If the design cannot produce a disconfirming result, redesign it.

**7. Plan what happens either way.** What you do if disconfirmed is as important as the
other branch, and thinking it through beforehand prevents the result being explained away.

## Output Contract

**Path:** `artifacts/6-probe.md`

**Required sections:**
- `# Probe: <belief being tested>`
- `## Belief` — stated falsifiably, with the assumption ID
- `## What Would Change The Decision` — written before design
- `## Method` — what will be done, and why this is the cheapest form that could disconfirm
- `## Signal` — what is measured, threshold, what counts as disconfirmation
- `## Time Bound` — duration and stop rule
- `## If Disconfirmed` — what changes
- `## If Confirmed` — what changes, and what remains uncertain
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: probe`, `stage: 6`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite:** the assumption ID being tested, and the evidence that made it uncertain.

**Must cite or mark as assumption:** any claim about probe cost or duration.

**After running:** results become findings with `source_type: observation`. Update the
assumption's status and resolution per `protocol/assumptions.md`. **A probe whose results
never reach the evidence base was not worth running.**

## Pitfalls

**Pitfall 1 — Designing for confirmation.**
*Symptom:* No plausible result would disconfirm. *Consequence:* Expensive reassurance, and
false confidence afterward. *Fix:* State the disconfirming result first, then design toward
producing it if it is true.

**Pitfall 2 — No decision linkage.**
*Symptom:* Cannot say what result would change the plan. *Consequence:* The probe is
theater. *Fix:* If nothing would change, skip it and say the decision is already made.

**Pitfall 3 — Over-building the probe.**
*Symptom:* The test requires substantial engineering. *Consequence:* You have built the
thing to find out whether to build it. *Fix:* Work up the cost ladder from the cheapest form.

**Pitfall 4 — Post-hoc thresholds.**
*Symptom:* Success defined after results arrive. *Consequence:* Every outcome is a success.
*Fix:* Write the threshold before starting.

**Pitfall 5 — Results never recorded.**
*Symptom:* The probe runs, the team "learns", nothing enters the evidence base.
*Consequence:* The learning evaporates and the assumption stays open.
*Fix:* Findings and ledger update are part of the probe, not follow-up.

## References

**Related skills:** `identify-gaps` (stage 3), `assess-risk` (stage 6),
`scope-decision` (stage 4)

**Protocol:** `protocol/assumptions.md`, `protocol/evidence.md`

**External frameworks:** Cheap disconfirming tests follow the assumption-testing tradition
in Lean Startup (Ries, 2011) and Lean UX (Gothelf and Seiden, 2013). The emphasis on
falsifiability follows Karl Popper, *The Logic of Scientific Discovery* (1934). Manual
simulation before building echoes the concierge and Wizard-of-Oz patterns in early-stage
product practice.
