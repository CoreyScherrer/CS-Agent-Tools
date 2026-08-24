---
artifact: problem-statement
stage: 1
status: draft
created: 2026-08-22
updated: 2026-08-22
sources: [E-001, E-002, E-003, E-004, E-005, E-006, E-007, E-008, E-009, E-010, E-011, E-013, E-014, E-015, E-016]
open_assumptions: [A-001, A-002, A-003, A-005, A-006, A-007, A-008, A-009]
last_critique:
depth: standard
---

# Problem Statement

Merchandising business users cannot get a trusted answer to a routine sales question
without going through an analyst, and when they do get an answer they frequently cannot
reconcile it with another report they already have. Two analysts absorb this as recurring
manual assembly and a steady stream of interruptions [E-013]. The reports they maintain
encode conflicting definitions of the same business concept [E-016], so a portion of the
request traffic is not people asking for data at all — it is people asking which number
to believe [E-011]. A tool that delivers numbers faster does not resolve that second
question, and may multiply it.

## Request As Stated

Verbatim from the stakeholder:

> "Our analytics team gets constant one-off questions from about eight business users in
> merchandising. Right now two analysts spend most of their week building the same handful
> of reports by hand in Excel, plus answering ad-hoc questions in Slack. Leadership asked
> us to 'build a self-service dashboard' so people stop asking. We also want to automate
> the recurring reports. I've got a folder of the current Excel reports, our team wiki,
> and about six months of the request channel."

Two solutions are named in the request: a self-service dashboard, and automation of the
recurring reports. Both are retained here as stated, not adopted as the problem. Note also
the stated goal attached to the dashboard — "so people stop asking" — which is a deflection
target, not a user outcome, and is examined below.

## Who Is Blocked

**Merchandising business users** — the stakeholder describes about eight of them
[ASSUMPTION A-007]. They hit the problem at the moment they need a sales figure for a
category, a vendor, or a period, and have no way to obtain it except to ask. Over six
months, 61 requests in the channel took the form "what were sales for X last week" [E-010].
They hit it a second, distinct way when they hold two numbers that disagree:
38 requests [E-011] over the same window asked why a figure did not match another report.
In that second case the user is not blocked on access — they have the number.
They are blocked on trust.

**The two merchandising analysts.** They are blocked at two moments. First, when
assembling the recurring reports: five are documented [E-001] [ASSUMPTION A-005], and the
Weekly Sales workbook alone runs to 11 tabs across 3 pivot sources plus a hand-maintained
mapping tab labelled "category fix - DO NOT DELETE" [E-004] [E-005] [ASSUMPTION A-003].
Second, when an ad-hoc request interrupts that assembly. The corpus does not establish
how the two loads interact [ASSUMPTION A-008].

The distinction matters: the request names one beneficiary group, but the reconciliation
traffic points at a problem neither group can solve on its own, because the definitional
conflict lives in the reports rather than in either party's behaviour [E-016].

## What They Are Trying To Accomplish

Merchandising users are trying to **make a merchandising decision on a number they trust,
without waiting on a person.** Two components, both required, neither sufficient alone:
the number has to arrive without a human in the loop, and it has to be reconcilable with
every other number the organization shows them for the same concept.

Analysts are trying to **spend their week on analysis rather than assembly** — to stop
being the mechanism by which data moves from source systems into a spreadsheet shape.

Both are solution-independent. A dashboard could satisfy them. So could a governed
semantic layer with no dashboard at all, a scheduled report distribution, a chat-based
query interface, or simply agreeing on one category definition and republishing the
existing reports. The request's named solutions are candidates, not the goal — and the
evidence gives reason to doubt that a dashboard alone is the strongest candidate, since a
dashboard built on the current conflicting definitions [E-016] would answer the 61
retrieval questions [E-010] while leaving the 38 reconciliation questions [E-011]
untouched, and would arguably worsen them by adding a fourth authoritative-looking number
[ASSUMPTION A-002].

## Cost Of The Status Quo

**Analyst time on recurring assembly.** OPS-2214, filed by the analytics manager on
2026-02-19, records analysts reporting approximately 6 hours per week each [E-013]
on recurring report assembly [E-014]. This is self-reported and unmeasured, and it conflicts
with the runbook's claim that the Weekly Sales report alone "takes about a day" [E-002]
[E-015]. The two cannot both hold straightforwardly across five reports [E-001], and the
corpus cannot resolve which is closer to true. The figure carried forward here is the
ticket's [ASSUMPTION A-001] — the newer and better-owned of two weak sources. **This is a
high-impact open assumption and it gates the business case: the whole justification for
automation rests on a number nobody has measured.**

**Analyst time on ad-hoc requests.** Not established by any source. The stakeholder
describes it as a substantial second load, and 143 requests reached the channel [E-009]
over six months, but no source records time spent per request, and OPS-2214 covers only
recurring assembly [E-013]. The total analyst cost is therefore unknown, not merely
imprecise [ASSUMPTION A-008] [ASSUMPTION A-006]. **The framework's instruction here is to
resist producing a plausible figure, and no per-request time estimate appears in this
document for that reason.**

**Decision cost from conflicting definitions.** The most consequential cost is the one
with no number attached at all. Two current reports over the same domain encode different
category mappings [E-008] [E-016], and one carries a hand-maintained correction tab
[E-005]. Where 38 of 143 requests are reconciliation questions [E-011], merchandising
decisions are being made on figures the organization itself cannot reconcile — or delayed
while someone works out which is right. Neither the frequency of bad decisions nor their
financial consequence is established anywhere in the corpus, and this document does not
estimate either.

**Elapsed time to an answer.** Not established. The corpus contains request counts
[E-009] but no timestamps, no response times, and no record of what a user does while
waiting.

**Key risk in this section:** three of the four cost lines are unquantified, and the one
that is quantified is contested [E-015]. Any prioritization built on this statement should
treat A-001 and A-008 as the first things to resolve.

## How We Will Know It Is Solved

Observable changes in the world, each independent of the mechanism that achieves it:

1. **A merchandising user gets a routine sales figure without asking a person.** Measured
   as a fall in retrieval-type requests against the current baseline of 61 over six months
   [E-010].
2. **Reconciliation questions fall, and fall faster than retrieval questions.** Against
   the baseline of 38 over six months [E-011]. This is the criterion that distinguishes a
   real fix from a faster version of the current problem; if reconciliation traffic holds
   steady or rises while retrieval traffic drops, the definitional problem was not solved.
3. **Any two reports asked the same question return the same number**, or visibly state
   why they differ. Today they do not [E-016]. Verifiable at any time by running both.
4. **The "category fix" mapping is no longer maintained by hand** — either it is
   unnecessary or it is owned by a system [E-005] [ASSUMPTION A-003].
5. **Analysts' recurring-assembly time falls against a measured baseline.** Note the
   dependency: this criterion is not measurable until A-001 is resolved, because there is
   currently no trustworthy baseline to fall from.
6. **A new recurring report can be added without adding a new mapping tab.** Tests whether
   the underlying definition problem was fixed or merely worked around once.

Explicitly *not* success criteria: a dashboard exists; the recurring reports run on a
schedule; the request channel goes quiet. The third deserves comment, because it is close
to what the request asked for. Channel silence is ambiguous — it is equally consistent
with users being served and with users giving up and going back to their own spreadsheets,
which would make the definitional problem invisible rather than absent.

## Out Of Scope

These are decisions, not findings. They are the adjacent things most likely to be assumed
in scope.

- **Rebuilding the merchandising source systems.** The category divergence is corrected
  today inside spreadsheets [E-005]; whether the correct long-term home is upstream is a
  real question, but re-platforming source data is not this effort.
- **Analytics needs outside merchandising.** The corpus covers one team and one requester
  population. Nothing here establishes anything about other functions, and the artifact
  should not be read as if it does.
- **The three recurring reports not present in the corpus** — Promo Lift, Inventory
  Position, Markdown Recovery [E-001]. They are named in scope by the request but nothing
  is known about them [ASSUMPTION A-005]. In scope to *investigate*, out of scope to
  *design for* until mined.
- **Choosing a tool.** No BI platform, warehouse, or semantic-layer product is selected or
  ruled out here. The evidence does not yet support a build-versus-buy position.
- **Headcount decisions.** Whether time freed from assembly is redeployed or removed is a
  management decision this work informs but does not make. Worth stating explicitly: the
  people whose cooperation this effort needs are the two analysts whose hours it proposes
  to reduce.

## Provenance

**Grounded in:** 15 findings from 5 sources, dated 2025-11-03 to 2026-07-30

**Open assumptions:** 8 (3 high-impact — A-001, A-002, A-008; two further high-impact
entries A-009 and A-002 bear on framing and are tracked in the ledger)

**Gaps:** What this artifact could not establish, and why.

- *The real cost of the status quo.* The only quantified cost figure is self-reported,
  unmeasured, and contradicted by another source [E-015]. No source measures anything.
- *Any user's own words.* Every source in the corpus is authored by or about the analytics
  team. Not one is authored by a merchandising business user. The channel export supplies
  theme counts but not request text, so the 143 requests were counted [E-009] and never
  read. "Who is blocked" is therefore reconstructed from the analysts' side of the
  interaction.
- *Whether the eight users are the channel's requesters.* No requester identities were
  available [ASSUMPTION A-007].
- *Why the numbers disagree.* The divergence between the two mappings is observed [E-008];
  its cause, size, and which mapping is correct are not.
- *What users do when blocked.* No source records workarounds, shadow spreadsheets, or
  decisions made on stale numbers.
- *Whether anyone acted on OPS-2214.* The ticket was mined for its claim only; status and
  resolution were not available [E-014]. A six-month-old unactioned cost ticket from the
  team's own manager would be a meaningful signal about organizational appetite, and that
  signal is unread.
- *Leadership's actual objective.* "So people stop asking" is reported at second hand
  through the stakeholder. No source captures leadership's reasoning directly, so whether
  the goal is analyst capacity, user autonomy, or cost is not established.

**Last critique:** Not yet critiqued. Status remains `draft`; `critique-artifact` has not
been run.
