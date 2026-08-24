---
name: exec-brief
description: Write a short brief for someone who will decide without reading the underlying work. Use when a decision needs executive approval or funding.
stage: 7
inputs: [all prior artifacts, evidence/findings.md, assumptions.md]
outputs: [artifacts/7-exec-brief.md]
depth: standard | deep
---

# Exec Brief

## Purpose

Give a decision-maker what they need to decide, in the space they will actually read,
without stripping out the uncertainty.

The pressure in this artifact runs entirely one direction: toward confidence. Executives
want a clear recommendation, brevity removes caveats first, and hedged writing reads as
weak. The result is the document most likely to contain an unsupported number in the whole
framework — and the one where such a number does the most damage, because it gets repeated
by someone with authority and becomes fact.

Brevity and honesty are compatible. "We estimate six hours a week per analyst, from a single
ticket we have not verified" is nine words longer than the same claim stated flatly, and it
is the difference between a brief and a liability.

## When To Use

- A decision needs executive approval, funding, or prioritization
- A project needs an escalation decision
- Someone senior needs to understand a recommendation without reading the artifacts

## When Not To Use

- As a substitute for the underlying work. A brief summarizing artifacts that do not exist
  is a proposal dressed as a conclusion.
- For peer or team communication — use `stakeholder-update`.

## Process

Follow `protocol/facilitation.md`.

**1. Lead with the decision requested.** First sentence. What you want them to decide,
approve, or fund. Executives read the first line and decide whether to read the rest;
burying the ask wastes that line on context.

**2. State the recommendation and the reasoning in three sentences.** If it takes more, the
reasoning is not yet clear enough to act on.

**3. Give the evidence basis honestly, and compactly.** How strongly is this supported —
what is known, what is assumed, what is the biggest open question. This is where briefs
usually fail. **The compact honest form is a sentence, not a section:** "Grounded in five
sources over six months; the cost figure rests on one unverified ticket."

**4. State what would change the recommendation.** Executives make better decisions when
they know the decision's fragility. It also protects you when circumstances change.

**5. Give the options not taken, in one line each.** Shows the recommendation is a choice,
not the only thing considered. Consistently the most-read part of a brief.

**6. State the ask precisely.** Decision, money, people, or a date. Vague asks produce
vague responses and another meeting.

**7. Keep it to one page.** If it does not fit, the thinking is not finished.

## Output Contract

**Path:** `artifacts/7-exec-brief.md`

**Required sections:**
- `# <Decision requested>` — the ask as the title
- `## Recommendation` — what to do, and why, in three sentences
- `## Why This Matters` — the problem, cited
- `## Evidence Basis` — one honest sentence on how well-grounded this is
- `## Key Uncertainty` — the biggest open assumption and what it would take to close
- `## Options Not Taken` — one line each
- `## The Ask` — precisely what is needed
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: exec-brief`, `stage: 7`. Requires `last_critique` before
`reviewed` — this artifact must be critiqued.

## Evidence Requirements

Per `protocol/evidence.md`. **Strictest application alongside `write-prd`.**

**Must cite or mark as assumption:** every number, without exception. Brevity is not a
license to drop markers — an uncited figure in a brief is the highest-risk content this
framework produces, because it will be repeated by someone whose repetition makes it true.

**Compression rule:** where an inline marker would break the flow, aggregate honestly in
the Evidence Basis line. What you may never do is silently drop the qualifier — stating a
figure flatly when it rests on one unverified source is a misrepresentation, not a
simplification.

**May be reasoned:** the recommendation itself, and the reasoning for it. State it as
judgment.

## Pitfalls

**Pitfall 1 — Caveats stripped for brevity.**
*Symptom:* Numbers stated flatly that are qualified in the PRD. *Consequence:* The executive
acts on a certainty that does not exist and repeats it. *Fix:* Compress into the Evidence
Basis line rather than deleting.

**Pitfall 2 — Burying the ask.**
*Symptom:* Context first, request at the end. *Consequence:* The decision is not made
because it was not seen. *Fix:* First sentence.

**Pitfall 3 — No options.**
*Symptom:* One recommendation with no alternatives. *Consequence:* Reads as advocacy rather
than analysis, and invites the executive to invent their own alternative.
*Fix:* One line each.

**Pitfall 4 — Hiding the key uncertainty.**
*Symptom:* Open assumptions omitted to appear confident. *Consequence:* It surfaces later,
and it surfaces as a credibility problem rather than a known risk.
*Fix:* Name the biggest one and what would close it. This builds credibility, not doubt.

**Pitfall 5 — Length.**
*Symptom:* Three pages. *Consequence:* Read diagonally; conclusions drawn from headings.
*Fix:* One page.

## References

**Related skills:** `write-prd` (stage 5), `decision-record` (stage 7),
`stakeholder-update` (stage 7), `critique-artifact` (any stage)

**Protocol:** `protocol/evidence.md`, `protocol/artifact-standards.md`
