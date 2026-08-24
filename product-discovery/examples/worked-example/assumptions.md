# Assumptions

Running ledger for this project. Format per `protocol/assumptions.md`.

Rules that matter:
- A **high**-impact open assumption blocks advancement past DEFINE.
- When validated, add the evidence entry and set `resolution` to its ID.
- When invalidated, revise every artifact listed in `what_it_affects` — do not just flip status.

<!-- Entries below. Next ID: A-010 -->

### A-001
- **assumption:** The true recurring-report effort is closer to the ticket's figure (about 6 hours per analyst per week) than to what the runbook's "about a day" per report would imply across five reports
- **why_assumed:** The two sources conflict [E-015] and the corpus cannot resolve them. The ticket is nine months newer than the runbook and was filed by the person who owns the team's capacity, so it is the better of two weak sources — but it is still self-reported and unmeasured [E-013].
- **impact_if_wrong:** high
- **what_it_affects:** Cost Of The Status Quo in artifacts/1-problem-statement.md; the entire business case for automating the recurring reports; whether this work is worth doing at all
- **owner:** The analytics manager (filer of OPS-2214)
- **how_to_validate:** Two weeks of time-tracking by the two analysts, split by report and by recurring-vs-ad-hoc. Cheaper alternative: ask each analyst to reconstruct last week by report. Either resolves it in under a fortnight.
- **status:** open
- **resolved_date:**
- **resolution:**

### A-002
- **assumption:** The 38 "why does this number not match" requests [E-011] are caused, at least in substantial part, by the divergent category mappings between reports [E-016]
- **why_assumed:** The two facts are individually evidenced and the causal link is the obvious reading, but no request text was available [S-004] and no request is linked to a mapping in any source. This is inference from adjacency.
- **impact_if_wrong:** high
- **what_it_affects:** The framing of the problem in artifacts/1-problem-statement.md as a definition problem rather than an access problem; whether fixing category definitions removes a quarter of the request volume or none of it; the priority of a self-service dashboard relative to a canonical data definition
- **owner:** The analytics manager, or either analyst
- **how_to_validate:** Read the 38 requests. They exist in the export already mined [S-004]; only the theme counts were extracted. One afternoon of reading resolves this.
- **status:** open
- **resolved_date:**
- **resolution:**

### A-003
- **assumption:** The "category fix - DO NOT DELETE" tab [E-005] is load-bearing — the report produces wrong numbers without it — and its content is maintained by hand rather than generated
- **why_assumed:** The defensive label reads as a response to a past incident, and "fix" implies correcting something upstream. Neither the tab's contents nor its edit history was mined [S-002].
- **impact_if_wrong:** medium
- **what_it_affects:** The characterization of manual maintenance burden in artifacts/1-problem-statement.md and artifacts/2-evidence-summary.md; whether any automation must reproduce this mapping or can bypass it
- **owner:** Either analyst
- **how_to_validate:** Open the tab. Ask who edits it and how often. Under an hour.
- **status:** open
- **resolved_date:**
- **resolution:**

### A-004
- **assumption:** The runbook, both workbooks, and the request-channel export originate from the same merchandising analytics team the stakeholder described
- **why_assumed:** The stakeholder presented them as one team's corpus, and the subject matter is consistent. No source in the corpus names its own author except OPS-2214 [E-014].
- **impact_if_wrong:** low
- **what_it_affects:** Attribution in evidence/sources.md; who to interview in DISCOVER
- **owner:** The stakeholder who supplied the corpus
- **how_to_validate:** Confirm authorship in one message. Minutes.
- **status:** open
- **resolved_date:**
- **resolution:**

### A-005
- **assumption:** The five recurring reports named in the runbook [E-001] are all still being produced today
- **why_assumed:** The runbook is nine months stale [S-001] and only two of the five appear as files in the corpus. The stakeholder said "the same handful of reports," which is consistent with five but does not confirm it.
- **impact_if_wrong:** medium
- **what_it_affects:** Scope of what would be automated in artifacts/1-problem-statement.md; the denominator for any effort estimate; whether A-001's arithmetic uses five reports or fewer
- **owner:** The analytics manager
- **how_to_validate:** Ask which of the five still run and on what cadence. Minutes.
- **status:** open
- **resolved_date:**
- **resolution:**

### A-006
- **assumption:** The request channel is the primary intake path, so its volume [E-009] is a reasonable proxy for total ad-hoc demand rather than a small fraction of it
- **why_assumed:** The stakeholder described Slack as where ad-hoc questions arrive. No source establishes whether requests also come by DM, email, meeting, or desk visit — a channel export can only ever count what reached the channel.
- **impact_if_wrong:** medium
- **what_it_affects:** The volume claims in artifacts/1-problem-statement.md and artifacts/2-evidence-summary.md; whether request volume is understated
- **owner:** Either analyst
- **how_to_validate:** Ask the two analysts where requests actually reach them, and in what proportion. One conversation.
- **status:** open
- **resolved_date:**
- **resolution:**

### A-007
- **assumption:** The people asking in the request channel are substantially the same eight merchandising business users the stakeholder described
- **why_assumed:** The stakeholder named eight users in merchandising; the export carries no requester identities [S-004], so the two populations cannot be matched.
- **impact_if_wrong:** medium
- **what_it_affects:** Who Is Blocked in artifacts/1-problem-statement.md; who to interview in DISCOVER; whether a self-service tool would serve eight people or a much wider group
- **owner:** The stakeholder who supplied the corpus
- **how_to_validate:** Re-export the channel with author fields, or ask the analysts who asks most. Under a day.
- **status:** open
- **resolved_date:**
- **resolution:**

### A-008
- **assumption:** The ad-hoc request load falls on the same two analysts who assemble the recurring reports, and is additional to the recurring effort recorded in OPS-2214 [E-013]
- **why_assumed:** The stakeholder described both loads as falling on two analysts. OPS-2214 addresses only recurring assembly and is silent on ad-hoc time, so the total analyst load is not established anywhere in the corpus.
- **impact_if_wrong:** high
- **what_it_affects:** Cost Of The Status Quo in artifacts/1-problem-statement.md — specifically whether the total cost is the recurring figure or meaningfully larger; the relative priority of automating reports versus deflecting requests
- **owner:** The analytics manager
- **how_to_validate:** Same time-tracking exercise as A-001, with an ad-hoc category. Two weeks, or one reconstruction conversation.
- **status:** open
- **resolved_date:**
- **resolution:**

### A-009
- **assumption:** No canonical, system-of-record category definition exists that either workbook could have used instead of its own mapping
- **why_assumed:** No data dictionary or category standard appears in the corpus [E-016], but the corpus contains no source that would describe upstream systems at all, so absence here is weak evidence of absence in the organization.
- **impact_if_wrong:** high
- **what_it_affects:** The framing of the category divergence as a missing-definition problem in artifacts/1-problem-statement.md and artifacts/2-evidence-summary.md; whether the fix is to define categories or merely to adopt an existing definition
- **owner:** Whoever owns the merchandising source system (not identified in the corpus)
- **how_to_validate:** Ask the analysts what the mappings are correcting against, then check whether that system has a governed category attribute. Days, not weeks.
- **status:** open
- **resolved_date:**
- **resolution:**
