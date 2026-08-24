---
name: map-journey
description: Map the end-to-end path a person takes, including what happens when things go wrong and who picks up the pieces. Use when a workflow spans multiple steps, systems, or people.
stage: 5
inputs: [artifacts/4-users.md, evidence/findings.md, artifacts/5-prd.md]
outputs: [artifacts/5-journey.md]
depth: standard | deep
---

# Map Journey

## Purpose

Lay out the actual path a person takes through a process, so the gaps between steps become
visible.

Requirements describe capabilities. Journeys describe sequences. Most enterprise failures
live in the seams — the handoff between two systems, the wait for an approval, the moment
someone must remember to do something nobody told them about. Those seams are invisible in
a requirements list and obvious in a journey map.

## When To Use

- Any workflow spanning multiple steps, systems, or people
- When something works in each part and fails as a whole
- Before specifying a replacement for an existing process — mapping the current journey
  usually surfaces requirements the inventory missed

## When Not To Use

- Single-step interactions
- Before evidence exists. A journey map drawn from imagination is a diagram of assumptions,
  and its neatness disguises that.

## Process

Follow `protocol/facilitation.md`.

**1. Map the current journey before the future one.** The existing path is evidenced; the
future one is design. Doing current-state first also reveals steps people forgot to mention
because they are habitual.

**2. Walk it step by step,** recording for each: what the person does, what system they are
in, what they need at that moment, how long it takes, and what they do if it fails.

**3. Mark the seams explicitly.** Every transition between systems, people, or sessions.
Seams are where work is dropped, duplicated, or delayed. For each, ask what carries the
context across — often the answer is "the person remembers", which is a requirement.

**4. Record waiting.** Time spent waiting for approval, data, or another person is
frequently the largest component of elapsed time and almost never appears in a requirements
document. It is also often the cheapest thing to improve.

**5. Record what happens when it goes wrong** at each step. Not just the error, but the
recovery — who notices, who fixes it, how long it takes, and whether the person can proceed
meanwhile.

**6. Record the emotional texture where evidence supports it.** Frustration, distrust, and
resignation are real and predict adoption. Cite them — a quote from an interview, an
observed workaround. **Do not invent them.** An invented feeling is as fabricated as an
invented number, and reads as more sympathetic, which makes it more persuasive and worse.

**7. Then map the future journey,** marking each change and which requirement delivers it.
Steps that persist unchanged are as important as those that change — they are what the new
thing must not break.

**8. Identify what the future journey does not fix.** Explicitly. This is where honest
scoping shows up and where stakeholder expectations get set correctly.

## Output Contract

**Path:** `artifacts/5-journey.md`

**Required sections:**
- `# Journey`
- `## Current Journey` — step by step, with actor, system, need, duration, failure behavior
- `## Seams` — transitions, and what carries context across each
- `## Waiting` — where time is spent not working
- `## Failure And Recovery` — what breaks, who notices, how it is fixed
- `## Future Journey` — the changed path, each change tied to a requirement
- `## Unchanged` — what stays the same and must not break
- `## Not Fixed` — what this project leaves as it is
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: journey`, `stage: 5`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** every step of the current journey, every duration,
every failure behavior, and every emotional claim.

**Durations are the most commonly invented content in a journey map.** "Takes about ten
minutes" is a guess unless someone timed it or said it. Cite or mark.

**May be reasoned:** the future journey, which is design, and the seam analysis — though
the existence of each seam should be evidenced.

## Pitfalls

**Pitfall 1 — Mapping the official process.**
*Symptom:* The journey matches the documented procedure. *Consequence:* You design for a
process nobody follows and miss every workaround. *Fix:* Map what people do, from
observation or specific accounts.

**Pitfall 2 — Skipping current state.**
*Symptom:* Only a future journey. *Consequence:* No baseline, no evidence, and the changes
cannot be justified. *Fix:* Current first.

**Pitfall 3 — Invented emotion.**
*Symptom:* Frustration markers with no citation. *Consequence:* A persuasive artifact built
on feelings nobody expressed. *Fix:* Quote someone, or leave it out.

**Pitfall 4 — Ignoring waiting.**
*Symptom:* Only active steps mapped. *Consequence:* You optimize the fast part of a slow
process. *Fix:* Record wait time as its own step.

**Pitfall 5 — No unchanged section.**
*Symptom:* Only what changes is mapped. *Consequence:* A step people depend on gets broken
because nobody noticed it mattered. *Fix:* List what persists.

## References

**Related skills:** `define-users` (stage 4), `write-prd` (stage 5),
`inventory-existing-artifacts` (stage 2)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**External frameworks:** Journey and service-blueprint mapping follow the service design
tradition — Shostack's service blueprint (1984), developed in Stickdorn and Schneider,
*This Is Service Design Thinking* (2011). Mapping observed rather than official practice
follows Beyer and Holtzblatt, *Contextual Design* (1997).
