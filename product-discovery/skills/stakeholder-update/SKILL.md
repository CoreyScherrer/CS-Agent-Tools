---
name: stakeholder-update
description: Tell the people affected what is happening, what changed, and what you need from them. Use on a regular cadence during delivery, and whenever something material changes.
stage: 7
inputs: [artifacts/1-stakeholders.md, current project state, assumptions.md]
outputs: [artifacts/7-update-<date>.md]
depth: quick | standard
---

# Stakeholder Update

## Purpose

Keep the people affected by this work informed enough to act, and surface problems while
they are still cheap.

Updates fail in two directions. Some are status theater — activity reported as progress,
nothing anyone can act on. Others are too candid too late, where a problem known for weeks
appears fully-formed in a status report and the reaction is about the concealment rather
than the problem.

A good update is short, says what changed, and asks for what is needed.

## When To Use

- On a regular cadence during delivery
- Whenever something material changes — scope, timeline, a risk materializing
- When an assumption is invalidated in a way that affects someone's work

## When Not To Use

- For executive decisions — use `exec-brief`
- As a substitute for talking to someone when something has gone wrong. Bad news travels
  better in a conversation.

## Process

Follow `protocol/facilitation.md`.

**1. Write per audience, not per project.** The definition owner, the platform team you
depend on, and the users whose process changes need different updates. One broadcast that
serves everyone serves nobody, and it teaches people to skim.

Use the stakeholder map. If someone is on it, they get an update shaped for them.

**2. Lead with what changed since last time.** Not what happened — what is *different*.
Activity is not progress, and reporting it as progress is the most common failure here.

**3. Say what it means for them specifically.** The point of segmenting. "The category
definition decision is now with Finance" means something different to Finance than to the
analysts waiting on it.

**4. Name what you need from them,** with a date. An update with no ask is a broadcast, and
broadcasts get filtered.

**5. Report problems early and plainly.** A risk that materialized, a slipped dependency, an
invalidated assumption. Early and plain costs less than late and explained. **Do not soften
a problem into invisibility** — "some challenges around data availability" tells nobody
anything and delays the help you need.

**6. Keep the assumption picture current** where it affects them. If you have been building
on something they could confirm or deny, say so — this is often how assumptions actually get
validated.

**7. Keep it short.** Longer updates are read less. Five sentences that get read beat two
pages that do not.

## Output Contract

**Path:** `artifacts/7-update-<YYYY-MM-DD>.md` — dated, one file per update

**Required sections:**
- `# Update: <date>`
- `## For` — which audience this is written for
- `## What Changed` — since the last update, not activity
- `## What This Means For You` — audience-specific implications
- `## What We Need` — asks, with names and dates
- `## Problems` — anything going wrong, stated plainly
- `## Open Questions You Could Answer` — assumptions this audience could close
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: stakeholder-update`, `stage: 7`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** any claim about status, timing, or what another team
will do. **Schedule claims are the most commonly invented content in status updates** —
"on track for end of month" with nothing behind it is an invented commitment that becomes
someone else's plan.

**Never report progress you have not verified.** Reporting a dependency as complete because
you expect it to be is how a schedule fails silently.

**May be reasoned:** the interpretation of what changes mean for an audience.

## Pitfalls

**Pitfall 1 — Activity as progress.**
*Symptom:* Lists of meetings held and documents written. *Consequence:* Readers cannot tell
whether anything moved, and stop reading. *Fix:* Report what is different.

**Pitfall 2 — One update for everyone.**
*Symptom:* A single broadcast. *Consequence:* Everyone skims and nobody acts.
*Fix:* Segment by the stakeholder map.

**Pitfall 3 — Softened problems.**
*Symptom:* Euphemism where a specific problem exists. *Consequence:* Nobody helps, because
nobody understood there was a problem. *Fix:* Say the specific thing.

**Pitfall 4 — Invented schedule claims.**
*Symptom:* "On track" with no basis. *Consequence:* A fictional commitment enters other
people's plans. *Fix:* Report what is verified, and say what is uncertain.

**Pitfall 5 — No ask.**
*Symptom:* Pure information. *Consequence:* Filed unread. *Fix:* Name what you need, from
whom, by when.

## References

**Related skills:** `map-stakeholders` (stage 1), `exec-brief` (stage 7),
`decision-record` (stage 7)

**Protocol:** `protocol/evidence.md`, `protocol/artifact-standards.md`
