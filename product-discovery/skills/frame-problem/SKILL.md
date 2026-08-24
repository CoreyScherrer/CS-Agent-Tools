---
name: frame-problem
description: Frame the problem before anyone proposes a solution. Use when a request arrives as a solution ("build us a dashboard"), when the team disagrees about what is wrong, or at the start of any new initiative.
stage: 1
inputs: [request, stakeholder input, evidence/findings.md if MINE has run]
outputs: [artifacts/1-problem-statement.md]
depth: quick | standard | deep
---

# Frame Problem

## Purpose

Turn a request into a stated problem: who is blocked, what they are trying to accomplish,
what it costs that they cannot, and how we will know it is solved. Enterprise requests
almost always arrive pre-solved — someone asks for a dashboard, a report, an integration.
The named solution encodes assumptions nobody has examined, and building it faithfully is
how teams ship the wrong thing on time.

## When To Use

- A request arrives naming a solution rather than a problem
- Stakeholders disagree about what is actually wrong
- Starting any initiative above a trivial change
- An existing effort has drifted and nobody can state its goal in one sentence

## When Not To Use

- The problem is genuinely settled and documented, and you are picking up mid-stream
  (go to MINE, then DEFINE)
- A pure defect fix where the problem is self-evident
- Someone asked a question you can answer in a sentence — not everything is an initiative

## Inputs

The original request, verbatim. Whatever stakeholder context exists. If MINE has already
run, read `evidence/findings.md` first — do not ask people things the corpus answers.

## Process

Follow `protocol/facilitation.md`. Offer the three entry modes; default to context dump
when a corpus exists.

**1. Capture the request as stated.** Record it verbatim, including the solution if one
was named. You are not discarding it — you are noting what was asked so the gap between
request and problem stays visible.

**2. Find who is blocked.** Not "the business." A specific role doing a specific task.
If you cannot name a role, you do not have a problem yet — you have a preference. Ask
until you get to a person who does a thing.

**3. Establish what they are trying to accomplish.** The underlying goal, independent of
any solution. The test: could a completely different solution satisfy it? If not, you are
still describing a solution.

**4. Establish the cost of the status quo.** What does it cost that they cannot do this —
time, money, risk, decisions made badly or late? Cite evidence where it exists. Where it
does not, register an assumption. **Resist the temptation to invent a plausible number
here.** An unsourced cost figure is the most commonly fabricated element of a problem
statement and the most damaging, because it drives prioritization.

**5. Establish how we will know it is solved.** An observable change in the world, not a
deliverable. "Analysts get the number without filing a ticket" is an outcome. "We shipped
a dashboard" is not.

**6. Name what is out of scope.** At framing depth, the two or three adjacent things people
will assume are included. Cheap now, expensive later.

**7. Write the artifact and lint it.**

    python3 scripts/lint-artifact.py <project-dir>

Do not present the artifact until it passes.

## Output Contract

**Path:** `artifacts/1-problem-statement.md`

**Required sections:**
- `# Problem Statement` — the framed problem in 2-4 sentences
- `## Request As Stated` — verbatim, with the named solution if any
- `## Who Is Blocked` — role, and what they are doing when they hit it
- `## What They Are Trying To Accomplish` — solution-independent goal
- `## Cost Of The Status Quo` — cited or assumption-marked
- `## How We Will Know It Is Solved` — observable outcomes
- `## Out Of Scope` — explicit exclusions
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** per `protocol/artifact-standards.md`, `artifact: problem-statement`, `stage: 1`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:**
- Every element of Cost Of The Status Quo
- Any claim about frequency, volume, or number of affected people
- Any claim about what stakeholders want or believe

**May be reasoned without citation:**
- The framing itself
- Out Of Scope boundaries (these are decisions, not findings)
- How We Will Know It Is Solved, where it restates the goal

Stage 1 at `depth: quick` may have an empty `sources` list if MINE has not run. Any other
combination with no sources is a lint failure.

## Pitfalls

**Pitfall 1 — Accepting the named solution as the problem.**
*Symptom:* The problem statement is the request with different words. *Consequence:* You
validate a solution nobody examined and discover the real problem after building.
*Fix:* Ask what the person would do with the thing once they had it. Keep asking until
you reach a task, not an artifact.

**Pitfall 2 — Inventing the cost.**
*Symptom:* A confident hours-per-week or dollars-per-year figure with no source.
*Consequence:* Prioritization runs on fiction, and the number gets quoted in a steering
deck where it becomes fact. *Fix:* Cite it or mark it as an assumption with a validation
path. "We do not know what this costs" is a legitimate and useful finding.

**Pitfall 3 — Abstracting until unfalsifiable.**
*Symptom:* "Users need better visibility into operational performance." *Consequence:*
Nothing is out of scope, so everything is in. *Fix:* Name the role, the task, and the
moment they get stuck. If the statement could describe six teams, it is too abstract.

**Pitfall 4 — Outcomes that are deliverables.**
*Symptom:* Success criteria that are all things you build. *Consequence:* You can ship
everything and change nothing. *Fix:* For each criterion ask "would this still be true
if we solved the problem a completely different way?" If no, rewrite it.

## References

**Related skills:** `define-outcomes` (stage 1), `map-stakeholders` (stage 1),
`mine-corpus` (stage 2), `write-prd` (stage 5)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`,
`protocol/facilitation.md`, `protocol/artifact-standards.md`

**External frameworks:** Problem framing draws on MITRE's Problem Framing Canvas
(public domain, MITRE Corporation). The solution-independent-goal test derives from
Jobs-to-be-Done as developed by Clayton Christensen (*Competing Against Luck*, 2016)
and Anthony Ulwick (*Outcome-Driven Innovation*). Outcome-over-output framing follows
Teresa Torres, *Continuous Discovery Habits* (2021), and Josh Seiden, *Outcomes Over
Output* (2019).
