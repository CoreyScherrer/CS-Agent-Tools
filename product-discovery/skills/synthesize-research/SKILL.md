---
name: synthesize-research
description: Turn interview and observation notes into findings in the evidence base, without smoothing away what was inconvenient. Use after discovery conversations, before defining anything.
stage: 3
inputs: [interview notes, observation notes, artifacts/3-gaps.md]
outputs: [evidence/findings.md entries, assumptions.md updates, artifacts/3-research-synthesis.md]
depth: standard | deep
---

# Synthesize Research

## Purpose

Convert what people said and did into findings the evidence base can hold, and close the
gaps that discovery was run to close.

Primary research is the most expensive evidence a project gathers and the most easily lost.
It arrives as prose, it is full of things that contradict each other, and the temptation to
resolve it into a tidy narrative is strong. Resolving it is exactly what destroys its value:
the contradictions are usually the finding.

## When To Use

- After interviews or observation sessions
- Before DEFINE — scope set over unsynthesized research is set over an impression

## When Not To Use

- As a substitute for recording findings during discovery. Synthesize soon after; memory
  degrades fast and unrecorded specifics are gone.

## Process

Follow `protocol/facilitation.md`.

**1. Extract claims, not impressions.** Same discipline as mining. "Analysts distrust the
vendor report" is an impression. "Two of three analysts said they re-check vendor numbers
against the source system before sending" is a finding, with a source and a date.

**2. Attribute precisely.** `source_type: interview`, the person or role, and the date.
Confidence for interview evidence is rarely high — people misremember frequency, rationalize
decisions, and describe intended process rather than actual process. **Medium is the honest
default**; reserve high for something you observed directly or that they showed you.

**3. Separate what people said from what they did.** Where you observed the work, record
observation separately from the account of it. Divergence between the two is among the most
valuable findings available, and it disappears if both are recorded as one thing.

**4. Record disagreement as disagreement.** When two people describe the same process
differently, that is a conflict entry per `protocol/evidence.md` — not an averaging
exercise. Often it means the process genuinely differs by person, which is itself a
requirement.

**5. Record what surprised you.** Anything that contradicted the picture built in MINE
deserves explicit attention. Surprises are where the mined corpus was wrong or one-sided,
and they are easy to unconsciously discount because they are inconvenient.

**6. Close the gaps.** Walk the gap list explicitly. For each: closed (with the finding ID),
partially closed, or still open. **Gaps that discovery failed to close are a result, not an
oversight** — they may need a different method or may be genuinely unknowable now.

**7. Update the assumption ledger.** Validated assumptions become findings with resolution
IDs. Invalidated ones require revising every artifact in their `what_it_affects` field —
per `protocol/assumptions.md`, this is a revision task, not a status flip.

**8. Re-run `synthesize-evidence`** so the combined picture reflects both mined and primary
evidence.

## Output Contract

**Path:** `artifacts/3-research-synthesis.md`

**Required sections:**
- `# Research Synthesis`
- `## Who We Talked To` — people, roles, dates, method
- `## What We Learned` — key findings by theme, cited
- `## Said Versus Observed` — divergences between account and practice
- `## Disagreements` — where accounts conflict, and what that suggests
- `## Surprises` — what contradicted the mined picture
- `## Gap Closure` — each gap: closed / partial / still open, with IDs
- `## Assumption Updates` — validated, invalidated, and what was revised as a result
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: research-synthesis`, `stage: 3`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite:** every claim traces to a specific conversation or observation, with date and
attribution.

**Never aggregate into an invented statistic.** "Most users find this difficult" from three
interviews is a fabrication in the shape of a statistic. Say "two of the three people we
spoke to described…". Small-sample research is legitimate evidence; small-sample research
dressed as quantitative is not.

**Never attribute a position to someone who did not state it.** Including inferring what a
person "really meant." Record what they said; note your interpretation separately as
inference.

## Pitfalls

**Pitfall 1 — Narrative smoothing.**
*Symptom:* A clean story with contradictions resolved. *Consequence:* The most valuable
finding — that people disagree about their own process — is erased.
*Fix:* Conflicts get their own section and stay unresolved.

**Pitfall 2 — Inventing statistics from small samples.**
*Symptom:* "Most", "the majority", percentages from three interviews.
*Consequence:* Qualitative evidence acquires unearned authority and gets quoted.
*Fix:* Give the raw count. Always.

**Pitfall 3 — Discounting surprises.**
*Symptom:* Findings that contradict the mined picture get softened or omitted.
*Consequence:* You preserve a comfortable understanding that discovery just disproved.
*Fix:* A dedicated Surprises section, written before the rest.

**Pitfall 4 — Not closing gaps explicitly.**
*Symptom:* Synthesis reports learnings without revisiting the gap list.
*Consequence:* Nobody can tell whether discovery achieved its purpose, and open gaps drift
into DEFINE unnoticed. *Fix:* Walk the list item by item.

**Pitfall 5 — Flipping assumption status without revising.**
*Symptom:* An assumption marked `invalidated`, downstream artifacts untouched.
*Consequence:* Artifacts silently rest on something known to be false.
*Fix:* Follow `what_it_affects` and revise each.

## References

**Related skills:** `prep-interviews` (stage 3), `identify-gaps` (stage 3),
`synthesize-evidence` (stage 2), `map-opportunities` (stage 4)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**External frameworks:** Separating observed practice from reported practice follows
Beyer and Holtzblatt, *Contextual Design* (1997). Guidance against soliciting or recording
speculative claims follows Rob Fitzpatrick, *The Mom Test* (2013).
