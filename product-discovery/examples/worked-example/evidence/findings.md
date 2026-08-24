# Findings

Structured evidence base for this project. Format per `protocol/evidence.md`.

Append-only — never rewrite history. If a finding turns out to be wrong, add a new entry
recording the correction and note it in the original's `notes` field.

`date` is the date the SOURCE was created, not the date it was read.

<!-- Entries below. Next ID: E-017 -->

### E-001
- **claim:** The merchandising analytics team produces five recurring reports: Weekly Sales by Category, Vendor Performance, Promo Lift, Inventory Position, and Markdown Recovery
- **source:** Wiki page "Merch Reporting Runbook"
- **source_type:** document
- **date:** 2025-11-03
- **confidence:** medium
- **supports:** problem-statement, evidence-summary
- **notes:** Last edited 2025-11-03, roughly nine months before mining. Authored by the team it describes, which argues for higher confidence, but a wiki page unedited that long may not reflect current practice. No source in the corpus confirms all five are still produced; only two of the five appear as files.

### E-002
- **claim:** Assembling the Weekly Sales by Category report "takes about a day"
- **source:** Wiki page "Merch Reporting Runbook"
- **source_type:** document
- **date:** 2025-11-03
- **confidence:** low
- **supports:** problem-statement, evidence-summary
- **notes:** Hedged language ("about a day") with no stated measurement method and no named observer. Does not state whether this is one analyst-day of hands-on work or elapsed calendar time. Conflicts in magnitude with OPS-2214 [E-013]; see E-015.

### E-003
- **claim:** The Weekly Sales by Category workbook is on its fourteenth named version (`Weekly_Sales_by_Category_v14.xlsx`)
- **source:** Filename of `Weekly_Sales_by_Category_v14.xlsx`
- **source_type:** artifact
- **date:** 2026-07-30
- **confidence:** high
- **supports:** problem-statement, evidence-summary
- **notes:** The version number is directly observable in the filename. What the version number *means* — how often it increments, whether v1-v13 still exist, whether versions are weekly runs or structural revisions — is not established by the corpus.

### E-004
- **claim:** The Weekly Sales by Category workbook contains 11 tabs and 3 pivot sources
- **source:** `Weekly_Sales_by_Category_v14.xlsx`
- **source_type:** artifact
- **date:** 2026-07-30
- **confidence:** high
- **supports:** problem-statement, evidence-summary
- **notes:** Directly observed structure. Date is the file modification date, so the structure is current as of 2026-07-30. The corpus does not describe what the tabs contain or how the pivot sources are populated.

### E-005
- **claim:** The Weekly Sales by Category workbook contains a manually maintained mapping tab labeled "category fix - DO NOT DELETE"
- **source:** `Weekly_Sales_by_Category_v14.xlsx`
- **source_type:** artifact
- **date:** 2026-07-30
- **confidence:** high
- **supports:** problem-statement, evidence-summary
- **notes:** The tab label is directly observed. What the mapping corrects, against which upstream system, and who maintains it are not established by the corpus. The defensive label invites inference about past incidents; that inference is registered as A-003 rather than recorded here.

### E-006
- **claim:** The Weekly Sales by Category workbook was modified on 2026-07-30
- **source:** File metadata of `Weekly_Sales_by_Category_v14.xlsx`
- **source_type:** artifact
- **date:** 2026-07-30
- **confidence:** high
- **supports:** problem-statement, evidence-summary
- **notes:** Establishes the report was in active use within roughly a month of mining. Does not establish production cadence.

### E-007
- **claim:** The Vendor Performance workbook is named `Vendor_Performance_FINAL_v3.xlsx` and was modified on 2026-06-12
- **source:** File metadata of `Vendor_Performance_FINAL_v3.xlsx`
- **source_type:** artifact
- **date:** 2026-06-12
- **confidence:** high
- **supports:** problem-statement, evidence-summary
- **notes:** Modified roughly seven weeks earlier than the Weekly Sales workbook [E-006]. Whether that reflects a slower cadence, a lapsed report, or a copy held outside the mined folder is not established.

### E-008
- **claim:** The Vendor Performance workbook contains a category mapping that differs from the category mapping in the Weekly Sales by Category workbook
- **source:** `Vendor_Performance_FINAL_v3.xlsx` compared against `Weekly_Sales_by_Category_v14.xlsx`
- **source_type:** artifact
- **date:** 2026-06-12
- **confidence:** high
- **supports:** problem-statement, evidence-summary
- **notes:** Two reports over the same merchandising domain use different category definitions. Recorded as a conflict in E-016. The corpus does not say which mapping is correct, whether either is authoritative, or how large the divergence is.

### E-009
- **claim:** The merchandising request channel carried 143 requests between January and June 2026
- **source:** Slack request channel export, Jan-Jun 2026
- **source_type:** system
- **date:** 2026-06-30
- **confidence:** high
- **supports:** problem-statement, evidence-summary
- **notes:** A direct count from a channel export. `date` recorded as the end of the export window; the export has no stated creation date of its own. Whether requests also arrive by DM, email, or in person is not established, so this is a floor on request volume, not a total.

### E-010
- **claim:** 61 of the 143 channel requests are of the form "what were sales for X last week"
- **source:** Slack request channel export, Jan-Jun 2026
- **source_type:** system
- **date:** 2026-06-30
- **confidence:** medium
- **supports:** problem-statement, evidence-summary
- **notes:** The count is exact but the corpus describes the theme grouping as "rough", so the boundary against the one-off slices theme [E-012] is soft. Largest single theme in the channel.

### E-011
- **claim:** 38 of the 143 channel requests ask why a number does not match another report
- **source:** Slack request channel export, Jan-Jun 2026
- **source_type:** system
- **date:** 2026-06-30
- **confidence:** medium
- **supports:** problem-statement, evidence-summary
- **notes:** Theme grouping described as "rough" in the corpus. These are reconciliation questions, not data-retrieval questions. The corpus does not link any individual request to the category mapping divergence [E-008], so the relationship between this theme and that conflict is inference, registered as A-002.

### E-012
- **claim:** 24 of the 143 channel requests are one-off slices and 20 are miscellaneous
- **source:** Slack request channel export, Jan-Jun 2026
- **source_type:** system
- **date:** 2026-06-30
- **confidence:** medium
- **supports:** evidence-summary
- **notes:** Theme grouping described as "rough". The miscellaneous bucket is uncharacterized: the corpus says nothing about the content of those 20 requests.

### E-013
- **claim:** Analysts report spending approximately 6 hours per week each on recurring report assembly
- **source:** Ticket OPS-2214
- **source_type:** document
- **date:** 2026-02-19
- **confidence:** medium
- **supports:** problem-statement, evidence-summary
- **notes:** Secondhand and self-reported: the analytics manager reports what analysts report. No measurement method stated. The manager owns the team, which supports the figure, but does not do the work being timed. Covers recurring assembly only — the ticket says nothing about time spent answering ad-hoc requests. Conflicts in magnitude with the runbook [E-002]; see E-015.

### E-014
- **claim:** Ticket OPS-2214 was filed by the analytics manager on 2026-02-19
- **source:** Ticket OPS-2214
- **source_type:** document
- **date:** 2026-02-19
- **confidence:** high
- **supports:** evidence-summary
- **notes:** Establishes that the cost of recurring reporting was raised internally by the team's own manager roughly six months before mining. The ticket's status, its resolution, and any response to it are not in the corpus.

### E-015
- **claim:** CONFLICT — the runbook's per-report effort figure and the ticket's total effort figure cannot both be straightforwardly true
- **source:** Wiki page "Merch Reporting Runbook" compared against Ticket OPS-2214
- **source_type:** conflict
- **date:** 2026-02-19
- **confidence:** medium
- **supports:** problem-statement, evidence-summary
- **notes:** The runbook says one report takes "about a day" [E-002]; the ticket says all recurring assembly takes about 6 hours per analyst per week [E-013]. If "a day" means a working day of hands-on effort, one report roughly consumes the entire stated weekly recurring budget, leaving nothing for the other four reports [E-001]. Explanations the corpus cannot distinguish between: the runbook is stale (edited 2025-11-03, over three months before the ticket); "a day" is elapsed rather than hands-on time; the two analysts split one report between them; or the 6-hour figure understates. Which is true materially changes the size of the prize, so it is carried as A-001 rather than resolved here. `date` set to the later of the two sources.

### E-016
- **claim:** CONFLICT — two merchandising reports encode different category mappings, and no authoritative category definition is identifiable in the corpus
- **source:** `Weekly_Sales_by_Category_v14.xlsx` compared against `Vendor_Performance_FINAL_v3.xlsx`
- **source_type:** conflict
- **date:** 2026-07-30
- **confidence:** high
- **supports:** problem-statement, evidence-summary
- **notes:** The divergence itself is directly observed [E-008]. That one workbook carries a hand-maintained "category fix" tab [E-005] indicates category values are being corrected downstream of whatever system supplies them rather than defined once upstream. The corpus contains no data dictionary, no category standard, and no record of a decision about which mapping is correct. `date` set to the later of the two source dates.
