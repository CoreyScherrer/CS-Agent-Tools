# Evidence Protocol

Every skill in this framework obeys this file. It is the reason artifacts here can be
trusted more than artifacts produced by filling in a template.

## The core rule

**Every material claim is either cited or registered as an assumption. There is no third state.**

A material claim is one that could change a decision: a number, a user behavior, a
system constraint, a stated need, a volume, a frequency, a cost. Non-material claims
(transitions, framing, restatements of things already established) need no citation.

When you do not know something, you do not guess silently. You either:
1. Cite a source that establishes it, or
2. Add it to the assumption ledger and mark it inline

Writing a plausible number without doing one of those two things is the single worst
failure mode of AI-assisted product work. It produces documents that read as authoritative
and are partly fiction. Nobody downstream can tell which parts.

## Citation format

Inline, immediately after the claim:

    Order volume peaks at roughly 3x baseline during the first week of the month [E-014].

The bracketed ID resolves to an entry in `evidence/findings.md`.

For an assumption instead:

    Order volume peaks during the first week of the month [ASSUMPTION A-007].

Both forms are machine-checkable. `lint-artifact.py` flags any paragraph containing a
number, a percentage, or a quantifier that carries neither marker.

## Finding record

Each entry in `evidence/findings.md`:

    ### E-014
    - **claim:** Order volume peaks at ~3x baseline in week 1 of each month
    - **source:** Q3 Fulfillment Review deck, slide 12
    - **source_type:** artifact | document | conversation | interview | system | observation
    - **date:** 2026-03-14
    - **confidence:** high | medium | low
    - **supports:** problem-statement, prd
    - **notes:** Deck cites a dashboard that was not attached. Number not independently verified.

`date` is the date the *source* was created, not the date you read it. A confident finding
from a three-year-old deck is a low-confidence finding about today. Stale evidence is the
most common way a mined corpus misleads.

Accepted date forms:
- `2026-03-14` — a known creation date
- `~2026-03-14` — approximate; the source suggests roughly this
- `2026-01-01..2026-06-30` — a range, for sources covering a window (an export, a channel
  archive). Staleness is judged from the later bound.
- `unknown` — the source carries no date and none can be inferred

`unknown` may not be paired with `confidence: high`. If you cannot date a source you cannot
know it still describes today, and that uncertainty is part of the claim's confidence.

`confidence` is about the source, not your feeling. Use:
- **high** — primary system data; a document whose author owns the thing described; or a
  fact you observed directly in an artifact (a file has eleven tabs; two files apply
  different mappings). Direct observation of a thing that is present is the most reliable
  class of evidence available.
- **medium** — secondhand but specific; a deck citing data you cannot see
- **low** — recollection, inference, a claim with no traceable origin

`supports` names the artifacts a finding bears on, using artifact names as they appear in
`artifact:` frontmatter — `problem-statement`, `prd`, `report-inventory`. It is a routing
hint, not a constraint; a finding may be cited by an artifact it does not list.

## Conflicting evidence

When sources disagree, record both findings and a third entry noting the conflict. Do not
silently pick the one that fits your narrative. Conflicts are findings — often the most
valuable ones, because a disagreement about a basic number usually means a definition
problem, and definition problems are worth surfacing early.

A conflict entry uses `source_type: conflict` and names the findings it reconciles rather
than a single source:

    ### E-016
    - **claim:** E-005 and E-011 give incompatible effort figures for the same reports
    - **source:** conflict between E-005 and E-011
    - **source_type:** conflict
    - **date:** 2026-07-30
    - **confidence:** high
    - **supports:** problem-statement, evidence-summary
    - **notes:** E-005 implies ~1 day for one report; E-011 gives 6 hrs/week for all five.
      Both cannot hold. Likely a scope-of-work definition difference. Unresolved.

`date` on a conflict entry is the later of the two sources — the conflict is only known to
exist as of then. `confidence` refers to the conflict being real, not to either claim.

**A conflict entry never resolves the conflict.** Recording it is the deliverable.
Resolution requires a person, and forcing one here is how a documentation task becomes an
unowned decision.

## What is not evidence

- Your own reasoning (that is analysis; label it as such)
- Another artifact you generated in this same project, unless it cites upstream sources
- General industry knowledge or benchmarks not sourced to a specific document
- Anything a model produced without a source
- General knowledge of how a term is *usually* computed. What matters is what this
  organization actually does.

That second one matters and is easy to violate. If the PRD cites the problem statement,
and the problem statement cited nothing, the PRD is uncited. Provenance has to reach
ground, not loop.
