---
name: size-the-voyage
description: Size the engagement and set how heavy each stage should be. Use at the very start of any project, before framing, to decide how much process this work actually warrants.
stage: 0
inputs: [the request, whatever context exists]
outputs: [artifacts/0-triage.md]
depth: quick
---

# Size The Voyage

## Purpose

Decide how much process this work warrants, and record that decision.

Every project runs all seven stages. What varies is depth. A question that takes an
afternoon and a platform replacement that takes two quarters both need framing, mining,
and specification — but one gets an hour of each and the other gets weeks.

Getting this wrong in either direction is costly. Too heavy and people route around the
framework, which is worse than not having one because it looks like governance while
being theater. Too light and you skip the thinking that would have caught the wrong
problem.

## When To Use

- At the start of every project, before `frame-problem`
- When a project's scope changes materially mid-flight — re-triage rather than carrying
  a stale depth setting

## When Not To Use

- Never skipped. It is fifteen minutes at `quick` depth and it sets everything downstream.

## Process

Follow `protocol/facilitation.md`.

**1. Establish reversibility.** How hard is this to undo once shipped? A report nobody
depends on yet is nearly free to change. A definition that propagates into other systems,
a data contract, or anything a downstream team builds against is not. **Reversibility
drives depth more than size does.** A small irreversible change deserves more process than
a large reversible one.

**2. Establish blast radius.** Who is affected if this is wrong — one team, a function, the
whole company, customers? Include the people who operate it after launch, not just the
people who asked for it.

**3. Establish decision cost.** What does it cost to be wrong: rework, a bad decision made
on bad numbers, lost trust, regulatory exposure? Cite where evidence exists.

**4. Establish how much is already known.** A well-documented problem with an existing
evidence base needs less discovery than a vague ask in an area nobody has mapped.

**5. Set depth per stage.** Not one global setting — stages vary independently, and this
is where triage earns its keep. Common shapes:

- *A replacement for something that exists:* MINE deep (the existing thing is the spec),
  DISCOVER quick (the corpus answers most of it), SPECIFY standard.
- *A net-new capability in a mapped domain:* MINE standard, DISCOVER deep, VALIDATE deep.
- *A small change to a well-understood system:* everything quick, but nothing skipped.
- *Anything irreversible:* VALIDATE deep regardless of size.

**6. Name the decider and the audience.** Who approves this, and who reads the artifacts.
An artifact set for one engineering team is different from one going to a steering
committee. Naming it now prevents rewriting everything at COMMUNICATE.

**7. Set the artifact list.** Which artifacts this project will actually produce. Not every
project needs every artifact, and saying so up front prevents both gaps and ceremony.

## Output Contract

**Path:** `artifacts/0-triage.md`

**Required sections:**
- `# Triage`
- `## Request` — what was asked, verbatim
- `## Reversibility` — how hard to undo, and why
- `## Blast Radius` — who is affected, including operators and downstream teams
- `## What Is Already Known` — existing documentation, prior work, available corpus
- `## Depth Per Stage` — a table: stage, depth, one-line rationale
- `## Decider And Audience` — who approves, who reads
- `## Artifact List` — what this project will produce
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: triage`, `stage: 0`, `depth: quick`.

Stage 0 at `depth: quick` may have an empty `sources` list — nothing has been mined yet.

## Evidence Requirements

Per `protocol/evidence.md`. Light at this stage, with one hard rule:

**Must cite or mark as assumption:** any claim about blast radius size, cost of being
wrong, or how much prior work exists. These drive the depth decision, and an invented
number here miscalibrates the entire project.

**May be reasoned:** the depth settings themselves. These are judgments — state the
reasoning, which is what makes them revisable.

## Pitfalls

**Pitfall 1 — Sizing by effort instead of by consequence.**
*Symptom:* Depth set by how big the build looks. *Consequence:* A two-day change that
alters a shared definition gets two days of process and breaks four teams.
*Fix:* Reversibility and blast radius first. Build size is the weakest signal.

**Pitfall 2 — One global depth.**
*Symptom:* The whole project marked "standard." *Consequence:* You spend discovery effort
where the corpus already had answers, and skimp on validation where it mattered.
*Fix:* Set each stage independently and say why.

**Pitfall 3 — Triage as a formality.**
*Symptom:* Filled in after the work is underway to satisfy the process.
*Consequence:* No calibrating function; pure overhead. *Fix:* Do it first, in fifteen
minutes, before framing.

**Pitfall 4 — Never re-triaging.**
*Symptom:* Scope triples and the depth settings never change. *Consequence:* A now-major
project running on quick-depth process. *Fix:* Re-triage on material scope change and note
what changed.

## References

**Related skills:** `frame-problem` (stage 1), `map-stakeholders` (stage 1)

**Protocol:** `protocol/facilitation.md`, `protocol/artifact-standards.md`

**Note on prior art:** Sizing process to reversibility follows the widely-used
one-way-door / two-way-door distinction popularized by Amazon's shareholder letters
(Bezos, 1997 and 2015). Its application to discovery depth is this framework's own
convention.
