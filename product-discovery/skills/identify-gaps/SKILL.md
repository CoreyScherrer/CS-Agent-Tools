---
name: identify-gaps
description: Determine what the corpus could not answer and what it would take to find out. Use after mining, before any interview is scheduled.
stage: 3
inputs: [artifacts/2-evidence-summary.md, assumptions.md, artifacts/1-problem-statement.md]
outputs: [artifacts/3-gaps.md]
depth: quick | standard | deep
---

# Identify Gaps

## Purpose

Determine precisely what is still unknown, how much each unknown matters, and what the
cheapest way to resolve it is.

This is the hinge of the whole framework. MINE-before-DISCOVER only pays off if there is a
step that converts "what the corpus could not answer" into a specific, prioritized agenda.
Without it, discovery reverts to generic interviewing and the mining effort is wasted.

Done well, this skill also routinely discovers that a gap is answerable without talking to
anyone — the data is in an export already mined but unread, or one query resolves it.
Those are the cheapest wins available on any project.

## When To Use

- After MINE, before scheduling any interview
- After any stage that registers new assumptions
- When discovery feels unfocused — that is the symptom of a missing gap list

## When Not To Use

- Before mining. Gaps identified without a corpus are just a list of everything.

## Process

Follow `protocol/facilitation.md`.

**1. Collect every open question** from three places: the evidence summary's "could not
answer" section, the assumption ledger (every open assumption is a gap), and the problem
statement (anything asserted without support).

**2. For each gap, state what would resolve it.** Not "talk to users" — the specific thing:
which question, to whom, or which query against what data. A gap with a vague resolution
path does not get resolved.

**3. Classify by resolution method.** In cost order, and **check them in this order** —
this is where most of the value is:

- **Already in hand** — the answer is in mined material that was counted but not read, or
  in a file already exported. Startlingly common. Costs an afternoon.
- **One query** — answerable from a system you can already reach.
- **One question to one person** — a definition, an ownership, a constraint. A message.
- **Structured interview** — requires understanding someone's experience, not just a fact.
- **Observation** — requires watching the work happen, because people cannot accurately
  report their own process.
- **Experiment** — requires building something to learn. Defer to VALIDATE.

**4. Rate each gap by impact.** Use the same scale as the assumption ledger: does a wrong
answer invalidate scope and approach (high), change requirements (medium), or change a
detail (low)?

**5. Prioritize by impact ÷ cost.** High-impact gaps answerable from material already in
hand come first, always. They are free and they can reshape the project.

**6. Explicitly park the low-impact gaps.** Not every unknown deserves resolution. Say
which ones you are choosing to live with, so the choice is visible rather than accidental.

**7. Produce the interview agenda** — only the gaps that genuinely require a conversation,
grouped by who to talk to. This is the direct input to `prep-interviews`.

**Do not put a question on the interview agenda that the corpus already answered.** It
wastes the interview and signals you did not read what they gave you.

## Output Contract

**Path:** `artifacts/3-gaps.md`

**Required sections:**
- `# Gaps`
- `## Answerable From Material In Hand` — gaps resolvable by reading or querying what exists
- `## Requires One Question` — single facts, and who holds each
- `## Requires Interview` — grouped by person; the agenda for `prep-interviews`
- `## Requires Observation` — where reported process is unreliable
- `## Deferred To Validation` — gaps needing an experiment
- `## Parked` — low-impact unknowns we accept, and why
- `## Priority Order` — impact ÷ cost ranking, with the reasoning
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: gaps`, `stage: 3`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite:** each gap references the finding or assumption ID that generated it. A gap
with no provenance is usually a question you invented rather than one the evidence raised.

**Must cite or mark as assumption:** any claim about who holds an answer, or about what a
system contains.

**May be reasoned:** impact ratings and cost estimates for resolution. State the reasoning.

## Pitfalls

**Pitfall 1 — Skipping "already in hand."**
*Symptom:* Every gap routed to an interview. *Consequence:* You spend stakeholder time on
questions your own mined material answers, and lose credibility.
*Fix:* Check this category first, every time. It is the highest-yield step in the skill.

**Pitfall 2 — Gaps without resolution paths.**
*Symptom:* "Unclear how users prioritize." *Consequence:* Unactionable; it stays open all
project. *Fix:* Name the specific question and the specific person.

**Pitfall 3 — No parking.**
*Symptom:* Every gap marked for resolution. *Consequence:* Discovery expands until it
consumes the schedule. *Fix:* Park the low-impact ones explicitly.

**Pitfall 4 — Confusing gaps with assumptions.**
*Symptom:* Gaps listed that duplicate ledger entries. *Consequence:* Two lists drift apart.
*Fix:* An open assumption *is* a gap. Reference the ID rather than restating it.

**Pitfall 5 — Interviewing to confirm.**
*Symptom:* Agenda questions that check whether a finding is right. *Consequence:* You get
polite agreement and learn nothing. *Fix:* Interview for what the corpus cannot contain —
motivation, experience, tradeoffs — not for verification of documented facts.

## References

**Related skills:** `synthesize-evidence` (stage 2), `prep-interviews` (stage 3),
`synthesize-research` (stage 3)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`
