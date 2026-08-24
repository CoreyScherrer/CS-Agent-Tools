---
name: critique-artifact
description: Attack an artifact before a stakeholder does. Use before moving any artifact from draft to reviewed, and before anything leaves your hands.
stage: any
inputs: [the artifact, evidence/findings.md, assumptions.md]
outputs: [critique appended to the artifact's Provenance, revised artifact]
depth: standard | deep
---

# Critique Artifact

## Purpose

Find what is wrong with an artifact while it is still cheap to fix. The linter catches
mechanical failures — placeholders, broken references, missing sections. This catches the
failures a script cannot see: reasoning that does not hold, evidence that does not support
the claim it is attached to, and the confident gap where something important is simply absent.

The stance is adversarial on purpose. A critic looking for reasons to approve will find
them. The job here is to argue against the artifact as a skeptical stakeholder would, then
let it survive that or not.

## When To Use

- Before any artifact moves from `draft` to `reviewed` (required)
- Before an artifact goes to a stakeholder, always
- When an artifact has been revised substantially since its last critique
- When you feel confident about a document — that is when this is most useful

## When Not To Use

- As a substitute for the linter; run both, they catch different things
- On an artifact you are still actively drafting — critique a complete draft

## Inputs

The artifact, plus both ledgers. A critique that does not check claims against
`evidence/findings.md` is an opinion, not a verification.

## Process

Work through each lens in order. Record every finding, including ones you decide not to
act on — a critique that only reports problems you already fixed is theater.

**Lens 1 — Does the evidence support the claim?**
For each cited claim, open the finding. Ask: does this source actually establish this?
Common failures: a finding about one team cited to support a claim about the organization;
a three-year-old source cited for a present-tense claim; a finding at `low` confidence
carrying a load-bearing conclusion; a citation attached to a sentence adjacent to the one
it supports.

**Lens 2 — What is claimed without evidence?**
Beyond what the linter catches. Qualitative claims escape the quantitative regex: "users
find this frustrating", "the current process is inefficient", "stakeholders agree". Each
is a factual claim about the world and needs a source or a marker.

**Lens 3 — What is missing?**
The hardest lens, because absence is invisible. Prompts: What would the person who
disagrees say? Which stakeholder group is unmentioned? What happens when this fails?
What does it cost? What are we not doing that a reader would assume we are? If this
succeeds completely, what breaks downstream?

**Lens 4 — Is the reasoning sound?**
Look for: conclusions that do not follow from stated premises; correlation presented as
cause; a solution that does not address the stated problem; goals that are deliverables;
acceptance criteria that cannot actually be observed.

**Lens 5 — Assumption integrity.**
Cross-check `assumptions.md`. Every open assumption relevant to this artifact must appear,
marked. Look specifically for laundering: an assumption reworded into a general statement
so it reads as established. Check that no high-impact assumption is open past its gate.

**Lens 6 — Would this survive its audience?**
Name the actual reader. What is the first question they ask? The most likely objection?
The number they check first? If the artifact does not answer these, it will be sent back.

**Then:**
1. Report findings by severity: blocking / should-fix / consider
2. Fix the blocking and should-fix items
3. Append the critique record to the artifact's Provenance section
4. Update `last_critique` in frontmatter
5. Run the linter
6. Move status to `reviewed` only if no blocking findings remain

## Output Contract

**Modifies:** the artifact under critique.

**Appends to its `## Provenance` section:**

    **Last critique:** <date>
    - Blocking: <n> — <one line each, and what was done>
    - Should-fix: <n> — <one line each, and what was done>
    - Considered and declined: <n> — <one line each, with the reason>

That last category matters. A critique record showing only fixed items hides the judgment
calls, which are exactly what a later reader needs to evaluate.

## Evidence Requirements

The critique itself makes claims about the artifact and must be specific: name the section,
quote the sentence, name the finding ID. "The evidence is weak" is not actionable.
"Section 3 cites E-004 for a claim about all eight users, but E-004 is a single ticket from
one user" is.

## Pitfalls

**Pitfall 1 — Performative critique.**
*Symptom:* Findings are stylistic; nothing substantive is challenged. *Consequence:* The
gate provides false assurance — worse than no gate, because it certifies. *Fix:* If a
critique produces no blocking or should-fix findings on a first draft, assume the critique
was too gentle rather than the draft flawless.

**Pitfall 2 — Not opening the evidence.**
*Symptom:* Citations are checked for existence, not for support. *Consequence:* Misapplied
evidence survives with a citation that makes it look verified. *Fix:* Read each finding.
Every one.

**Pitfall 3 — Fixing by hedging.**
*Symptom:* Unsupported claims get softened to "may" or "could" rather than sourced or
marked. *Consequence:* The document becomes unfalsifiable mush that commits to nothing.
*Fix:* Cite it, mark it as an assumption, or delete it. Hedging is none of those.

**Pitfall 4 — Skipping the missing-content lens.**
*Symptom:* Critique covers only what is present. *Consequence:* The most expensive errors —
the unconsidered stakeholder, the unhandled failure mode — sail through. *Fix:* Lens 3 is
mandatory. Spend real effort there, and write down what you looked for even when you find
nothing.

## References

**Related skills:** every artifact-producing skill in the framework.

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`,
`protocol/artifact-standards.md`

**Note on prior art:** Adversarial review is a general practice from security review
and scientific peer review; red-teaming as a distinct discipline is well documented in
both. The six-lens structure here is this framework's own convention.
