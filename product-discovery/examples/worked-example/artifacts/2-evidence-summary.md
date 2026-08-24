---
artifact: evidence-summary
stage: 2
status: draft
created: 2026-08-22
updated: 2026-08-22
sources: [E-001, E-002, E-003, E-004, E-005, E-006, E-007, E-008, E-009, E-010, E-011, E-012, E-013, E-014, E-015, E-016]
open_assumptions: [A-001, A-002, A-003, A-004, A-005, A-006, A-007, A-008, A-009]
last_critique:
depth: standard
---

# Evidence Summary

## What The Corpus Covers

Five sources were mined, all supplied by the stakeholder, all originating from or about
the merchandising analytics team [ASSUMPTION A-004]:

| ID | Source | Type | Source date | Coverage |
|----|--------|------|-------------|----------|
| S-001 | Wiki page "Merch Reporting Runbook" | reference_doc | edited 2025-11-03 | full |
| S-002 | `Weekly_Sales_by_Category_v14.xlsx` | existing_artifact | modified 2026-07-30 | partial |
| S-003 | `Vendor_Performance_FINAL_v3.xlsx` | existing_artifact | modified 2026-06-12 | partial |
| S-004 | Request channel export, Jan-Jun 2026 | conversation | window ends 2026-06-30 | sampled |
| S-005 | Ticket OPS-2214 | intake | filed 2026-02-19 | partial |

Date range of the evidence: 2025-11-03 to 2026-07-30. Volume: 16 findings extracted,
of which 2 are conflict records. Nine assumptions were registered for inferences that
could not be grounded.

Coverage is uneven by design of what was available, not by choice. The two existing
artifacts are the highest-value source type per the mining protocol — each is a
specification someone already wrote and that people demonstrably use — but both were
mined only to structural depth, not to cell or formula level. See Corpus Quality.

## Key Findings

**The request channel is dominated by two very different questions.**
Of 143 requests [E-009] over six months, 61 are retrieval [E-010]
("what were sales for X last week") and 38 are reconciliation [E-011]
("why does this number not match"). The remainder are 24 one-off
slices and 20 uncharacterized [E-012]. The split matters more than the total: retrieval
questions are solved by access, reconciliation questions are solved by definition. The
request that opened this project names a solution — a dashboard — that addresses the first
category and not the second.

**The current reports disagree with each other about what a category is.** The Weekly Sales
and Vendor Performance workbooks encode different category mappings [E-008], and neither
the corpus nor any document in it identifies an authoritative definition [E-016]
[ASSUMPTION A-009]. This is a finding about the artifacts themselves, not a report of
someone's complaint, which makes it among the most solid things in this evidence base.

**Category correction happens by hand, downstream, inside a spreadsheet.** The Weekly Sales
workbook contains a tab labelled "category fix - DO NOT DELETE" [E-005]. Its contents were
not mined [ASSUMPTION A-003]. Whatever it does, it is being done in the last mile rather
than at the source.

**The recurring reports are substantial manual artifacts.** The Weekly Sales workbook has
11 tabs and 3 pivot sources [E-004] and is on its fourteenth named version [E-003]. Five
recurring reports are documented [E-001], though only two appear in the corpus
[ASSUMPTION A-005].

**The cost of all this is asserted, never measured.** OPS-2214 records approximately 6
hours per analyst per week on recurring assembly [E-013], filed by the analytics manager
on 2026-02-19 [E-014]. That is the only cost figure in the entire corpus, it is
self-reported at one remove, and it is contested [E-015]. No source measures ad-hoc time
at all.

**The team already flagged this internally, six months before this project.** OPS-2214
predates the current request [E-014]. Whether anything happened in response is not
recorded in the corpus.

## Conflicts

**Conflict 1 — effort figures that do not reconcile [E-015].** The runbook says the Weekly
Sales report alone "takes about a day" [E-002]. OPS-2214 says all recurring assembly is
about 6 hours per analyst per week [E-013]. Across five documented reports [E-001] these
cannot both be straightforwardly true: one report would consume the entire weekly budget.

What it suggests: most likely a definition problem about what is being timed — elapsed
time versus hands-on time, per-analyst versus per-report, one analyst versus two splitting
the work — rather than one source being simply wrong. It may also be pure staleness; the
runbook is over three months older than the ticket and nine months older than mining
[S-001]. Carried as A-001, high impact, because the business case rests on it.

**Conflict 2 — two definitions of category, no arbiter [E-016].** Two live reports over
the same domain map categories differently [E-008], and one maintains a manual correction
[E-005].

What it suggests: this is the same class of failure as Conflict 1 — a definitional
disagreement — but embedded in the artifacts rather than in prose about them, and it is
directly observable rather than reported. Given that 38 requests [E-011] ask why numbers
do not match, the strong hypothesis is that this conflict generates a measurable share of
the request traffic. That link is inference and is registered as A-002, not asserted here.

**A note on the pattern.** Both conflicts are definitional. The framework's evidence
protocol predicts this — "a disagreement about a basic number usually means a definition
problem" — and the corpus bore it out twice independently. That is a signal about the
problem class: this looks less like a tooling gap than a governance gap.

## What The Corpus Could Not Answer

The agenda for DISCOVER. Each item is a question the problem statement raises that no
available source addresses.

1. **What does the recurring reporting actually cost?** The only figure is contested
   [E-015] and unmeasured. Resolves A-001. *Highest priority — gates the business case.*
2. **What is the ad-hoc request load in analyst hours?** Nothing in the corpus measures
   this. Resolves A-008.
3. **What do the 38 reconciliation requests actually say?** The requests exist in an export
   already in hand [S-004]; only theme counts were extracted. This is the cheapest
   high-value item on the list and it resolves A-002.
4. **Which category mapping is correct, and is there an upstream definition?** [E-016]
   Resolves A-009.
5. **What is in the "category fix" tab, who maintains it, how often?** [E-005] Resolves
   A-003.
6. **Who are the eight users, and are they the channel's requesters?** No requester
   identities were available [E-009]. Resolves A-007.
7. **What do users do when they cannot get a number?** No source records workarounds,
   shadow spreadsheets, or decisions made on stale figures. Nothing to resolve — this is
   simply absent.
8. **Do the other three recurring reports still exist?** [E-001] Resolves A-005.
9. **Do requests arrive outside the Slack channel?** Resolves A-006.
10. **What happened to OPS-2214?** Status and resolution were not mined [E-014].
11. **What does leadership actually want?** "So people stop asking" reaches us at second
    hand through the stakeholder. No source captures leadership's own framing.
12. **What are the upstream data systems?** Nothing in the corpus describes where any of
    this data comes from — which is the foundation any automation would be built on.

## Corpus Quality

**Staleness.** Mixed and consequential. The runbook is roughly nine months old [S-001] and
is the sole source for the recurring report set [E-001] — the least corroborated finding
carries the oldest source. The workbooks are current, modified within roughly one and three
months of mining [E-006] [E-007]. OPS-2214 is six months old with unknown status [E-014].
The evidence base is strongest about what the reports *are* and weakest about what the work
*costs*, which is the inverse of what the business case needs.

**Coverage bias — the decisive weakness.** Every source is authored by, or is about, the
analytics team. Not one source is authored by a merchandising business user. The channel
export is the closest thing to a user voice in the corpus, and it arrived as theme counts
rather than text [S-004] — 143 requests [E-009] were counted and none were read. Every statement
in the problem statement about what users need is therefore reconstructed from the
supply side of the interaction. This is the single largest reason to treat the current
framing as provisional.

**Depth bias.** The two workbooks are the highest-value source type available and were
mined least deeply [S-002] [S-003]: structure only, no cells, no formulas, no lineage. The
mining protocol ranks existing artifacts first precisely because they encode real
requirements; that value is largely still unextracted here.

**Recency bias.** Present but mild in an unusual direction. Rather than everything being
recent, the oldest source is the one doing the most load-bearing work [E-001]. No source
older than 2025-11-03 was available, so the original rationale for the current reports —
why these five, why these definitions, who asked for them — is entirely unavailable.

**Volume.** 16 findings from 5 sources is a thin evidence base. It is thin because the
corpus is small, not because mining stopped early, with the exception of the depth
limitation noted above.

**What is missing and why.** The other three recurring reports [E-001] were not in the
supplied folder — absence that is uninterpretable, since it may mean discontinued, stored
elsewhere, or never existent. Upstream systems, ticket history, and any interview or
meeting record are absent because no such source was offered. No source was deliberately
excluded.

## Provenance

**Grounded in:** 16 findings from 5 sources, dated 2025-11-03 to 2026-07-30

**Open assumptions:** 9 (3 high-impact — A-001, A-002, A-008 — plus A-009, also high
impact, bearing on the framing of the definition problem)

**Gaps:** Enumerated in full under "What The Corpus Could Not Answer" above; the
structural reasons behind them are in "Corpus Quality". In short: this evidence base can
describe the current reporting apparatus with reasonable confidence, cannot quantify what
it costs, and contains no direct user voice at all. Two of the three high-impact
assumptions could be resolved from material already in hand — reading the request texts
in the existing export, and opening the two workbooks properly — which should happen
before any stakeholder is interviewed.

**Last critique:** Not yet critiqued. Status remains `draft`; `critique-artifact` has not
been run.
