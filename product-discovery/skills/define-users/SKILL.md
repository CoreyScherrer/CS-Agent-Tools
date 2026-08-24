---
name: define-users
description: Define who this is for concretely, based on evidence rather than invented archetypes. Use during DEFINE, before scope is set.
stage: 4
inputs: [evidence/findings.md, artifacts/3-research-synthesis.md, artifacts/1-stakeholders.md]
outputs: [artifacts/4-users.md]
depth: quick | standard | deep
---

# Define Users

## Purpose

Establish who this serves, what they are trying to do, and how they differ from each other
— grounded in evidence rather than in a plausible archetype.

Enterprise internal work has an advantage most product work lacks: **the user set is often
nameable.** Eight people in merchandising is not a segment, it is eight people, several of
whom you can talk to. A framework that reaches for personas here is discarding precision it
already has.

Where the population is genuinely large or unknown, this skill produces a provisional
profile with its assumptions marked — not a persona presented as fact.

## When To Use

- During DEFINE, before scope decisions
- When the team is designing for "the business" or "users" without further specificity
- When different groups are being conflated into one requirement set

## When Not To Use

- Before research exists. A user definition written from imagination is worse than none,
  because it is confidently specific.

## Process

Follow `protocol/facilitation.md`.

**1. Determine whether the population is nameable.** If you can list them, list them. Names,
roles, teams. This is the single biggest difference between internal and consumer product
work, and it should change the artifact.

**2. Group by job, not by title.** Two people with different titles doing the same task are
one group here. Two people with the same title doing different tasks are two. Titles are a
poor proxy for what someone needs from a system.

**3. For each group, record what evidence establishes about them:**

- What they are trying to accomplish
- What they do today, including workarounds
- What blocks them
- What they would have to change to adopt something new
- What they will not give up

That last one is the most predictive of adoption and the most frequently omitted. People
abandon new tools that remove something they relied on, even when the replacement is better
overall.

**4. Distinguish users from beneficiaries from operators.** The person who reads the output,
the person whose decision it improves, and the person who keeps it running are frequently
different people with conflicting needs. Conflating them produces requirements that satisfy
nobody.

**5. Mark what is evidenced and what is assumed.** For a nameable population, most of this
should be evidenced or directly askable. Where you are extrapolating from two interviews to
eight people, say so — that extrapolation is an assumption with an impact rating.

**6. Note who is not served.** Explicitly out-of-scope groups. Prevents the requirement set
expanding to cover everyone who asks.

## Output Contract

**Path:** `artifacts/4-users.md`

**Required sections:**
- `# Users`
- `## Population` — nameable or not; if nameable, the actual list
- `## Groups` — by job, each with jobs, current practice, blockers, adoption cost
- `## What They Will Not Give Up` — per group
- `## Users, Beneficiaries, Operators` — who is which, and where their needs conflict
- `## Evidenced Versus Assumed` — what rests on research and what on extrapolation
- `## Not Served` — deliberate exclusions
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: users`, `stage: 4`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** every claim about behavior, need, frequency, or
preference.

**Never write a persona detail that no evidence supports.** Invented biographical texture —
a name, a tenure, a stated frustration nobody expressed — makes a profile feel real and
makes it harder to notice it rests on nothing. If a detail does not come from evidence, it
does not belong in the artifact.

**Never extrapolate silently.** Three interviews describing eight people is an assumption
about the other five. Rate its impact and register it.

## Pitfalls

**Pitfall 1 — Personas where a list would do.**
*Symptom:* An archetype for a population you could enumerate. *Consequence:* You design for
a fiction when the actual people were available to ask. *Fix:* List them.

**Pitfall 2 — Grouping by title.**
*Symptom:* Groups mirror the org chart. *Consequence:* Requirements aggregate people with
nothing in common. *Fix:* Group by the job being done.

**Pitfall 3 — Invented texture.**
*Symptom:* Vivid details with no citation. *Consequence:* The profile gains false
credibility and gets designed against. *Fix:* Cite every detail or cut it.

**Pitfall 4 — Ignoring what they will not give up.**
*Symptom:* Only needs and pains recorded. *Consequence:* You build something better on
average that removes the one thing they depended on, and they do not adopt.
*Fix:* Ask directly. It is usually a specific, small thing.

**Pitfall 5 — Conflating users and operators.**
*Symptom:* One requirement set for everyone touching the system. *Consequence:* Operational
needs go unspecified and surface after launch. *Fix:* Separate them explicitly.

## References

**Related skills:** `synthesize-research` (stage 3), `map-stakeholders` (stage 1),
`map-opportunities` (stage 4), `write-prd` (stage 5)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**External frameworks:** Grouping by job rather than by demographic or title follows
Jobs-to-be-Done (Christensen, *Competing Against Luck*, 2016; Ulwick, *Outcome-Driven
Innovation*). The caution against evidence-free persona detail follows the
provisional-persona practice described in Lean UX (Gothelf and Seiden, 2013), where
assumptions are made explicit and slated for validation.
