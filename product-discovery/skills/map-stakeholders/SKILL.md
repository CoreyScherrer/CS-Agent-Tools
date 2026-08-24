---
name: map-stakeholders
description: Map who decides, who is affected, and who can block. Use during framing on any project touching more than one team, and before any decision that needs approval.
stage: 1
inputs: [artifacts/1-problem-statement.md, artifacts/0-triage.md]
outputs: [artifacts/1-stakeholders.md]
depth: quick | standard | deep
---

# Map Stakeholders

## Purpose

Establish who decides, who is affected, who must cooperate, and who can stop this.

In enterprise work, the most common cause of a well-built thing failing is not that it was
built badly. It is that a definition owner never agreed, a platform team was never asked,
or the people whose process it replaced were never consulted and quietly kept doing it the
old way.

This skill exists to make those people visible while there is still time to involve them.

## When To Use

- Any project touching more than one team
- Before any decision requiring approval — including definition decisions
- When a project keeps stalling on unclear approval

## When Not To Use

- Genuinely single-team work with no external dependency. Verify this rather than assuming
  it; shared data and shared definitions create stakeholders that org charts do not show.

## Process

Follow `protocol/facilitation.md`.

**1. List by role, then name people.** Roles first prevents anchoring on who you already
know. Then fill in actual names — an unnamed role is not a stakeholder, it is a hope.

**2. Classify each:**

- **Decider** — approves, or owns something you need changed. Includes definition owners,
  which people consistently forget.
- **Affected** — their work changes because of this
- **Dependency** — you need something from them; they may not care about your project
- **Blocker** — can stop this, whether or not they are a decider. Security, compliance,
  platform, procurement, and anyone who owns a system you must touch.
- **Informed** — needs to know, no action required

One person may hold several roles. Note when a decider is also a dependency — that
combination is where projects stall silently.

**3. Find the people nobody listed.** Enterprise work characteristically misses four
groups, and it misses them consistently:

- **Whoever operates this after launch.** Often not the requesting team.
- **Whoever owns the upstream system** you will depend on.
- **Whoever performs the process being replaced.** Their cooperation determines whether
  the old process actually stops.
- **Whoever inherits the maintenance** when the project team moves on.

**4. For each, record what they need and what they fear.** The fear column is the useful
one. Resistance is almost always rational from where the person sits — a definition owner
fears being blamed for numbers computed differently; an ops team fears carrying a system
they did not design. Naming it early is what makes it addressable rather than mysterious.

**5. Record what you actually know versus assume.** "Finance owns this definition" is a
claim. Cite it or register it. Assumed approval paths are a common and expensive error.

**6. Note who has not been consulted,** and make that visible. An artifact built without
talking to the affected parties is not wrong, but it is provisional, and it should say so.

## Output Contract

**Path:** `artifacts/1-stakeholders.md`

**Required sections:**
- `# Stakeholders`
- `## Deciders` — name, what they decide, evidence they hold that authority
- `## Affected` — name or role, how their work changes
- `## Dependencies` — what you need, from whom, and whether they know
- `## Blockers` — who can stop this and on what grounds
- `## Not Yet Consulted` — who has not been talked to, and what that leaves uncertain
- `## Needs And Concerns` — per stakeholder, what they need and what they fear
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: stakeholders`, `stage: 1`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** who holds decision authority, who owns a system or
definition, any claim about what a stakeholder wants or believes.

**Never state what a stakeholder thinks without a source.** Attributing a position to a
named person who never said it is worse than an invented number — it is invented on someone
else's behalf, and it can reach them. If you have not spoken to them, the entry says what
you expect and why, marked as an assumption.

**May be reasoned:** the classification itself, and which unlisted groups to go looking for.

## Pitfalls

**Pitfall 1 — Roles without names.**
*Symptom:* "The data team" as a stakeholder. *Consequence:* Nobody is accountable and no
conversation happens. *Fix:* Name a person. If you cannot, finding out is the next task.

**Pitfall 2 — Missing the operators.**
*Symptom:* The map has requesters and builders only. *Consequence:* You ship something
nobody is prepared to run. *Fix:* Ask explicitly who runs this on an ordinary Tuesday six
months from now.

**Pitfall 3 — Attributing positions.**
*Symptom:* "Finance wants X." *Consequence:* You design around a position nobody holds, and
it surfaces at review. *Fix:* Cite the conversation or mark it as your expectation.

**Pitfall 4 — Treating resistance as irrational.**
*Symptom:* A stakeholder is described as an obstacle. *Consequence:* You plan around them
instead of addressing a concern that is probably legitimate. *Fix:* Write down what they
would lose. It is usually specific and often fixable.

**Pitfall 5 — Mapping once.**
*Symptom:* The map is written in FRAME and never revisited. *Consequence:* Stakeholders
discovered later never get added, and the artifact misleads. *Fix:* Update it whenever a
new one surfaces.

## References

**Related skills:** `frame-problem` (stage 1), `size-the-voyage` (stage 0),
`stakeholder-update` (stage 7), `assess-risk` (stage 6)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**Note on prior art:** Influence/interest stakeholder classification is long-standing
project management practice. The four commonly-missed groups named here are this
framework's own convention, drawn from where enterprise delivery characteristically fails.
