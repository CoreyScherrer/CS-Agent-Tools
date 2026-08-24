# Sources

One entry per source actually mined. Distinguishes "looked and found nothing" from
"never looked" — which changes how much the evidence base can be trusted.

<!-- Entries below. Next ID: S-005 -->

### S-001
- **label:** Wiki page "Merch Reporting Runbook"
- **type:** reference_doc
- **location:** Team wiki
- **authored_by:** Not stated in the corpus; presumed the analytics team, registered as A-004
- **date_range:** Single page, last edited 2025-11-03
- **mined_on:** 2026-08-22
- **coverage:** full
- **findings_extracted:** 2 (E-001, E-002), plus contribution to conflict E-015
- **notes:** Only edit date is known; no creation date and no revision history were available, so it is not possible to tell which parts are current and which are inherited from an older version. Nine months stale relative to mining. It is the only source that enumerates the recurring report set, so E-001 has no corroboration.

### S-002
- **label:** `Weekly_Sales_by_Category_v14.xlsx`
- **type:** existing_artifact
- **location:** Folder of current Excel reports
- **authored_by:** Not stated in the corpus; presumed the analytics team, registered as A-004
- **date_range:** Modified 2026-07-30
- **mined_on:** 2026-08-22
- **coverage:** partial
- **findings_extracted:** 4 (E-003, E-004, E-005, E-006), plus contribution to conflicts E-008 and E-016
- **notes:** Structure was inventoried (tab count, pivot source count, the "category fix" tab) but cell-level contents, formulas, and the actual mapping values were not examined. The report's data lineage — what feeds the three pivot sources — is therefore unknown. This is the highest-value unmined depth in the corpus.

### S-003
- **label:** `Vendor_Performance_FINAL_v3.xlsx`
- **type:** existing_artifact
- **location:** Folder of current Excel reports
- **authored_by:** Not stated in the corpus; presumed the analytics team, registered as A-004
- **date_range:** Modified 2026-06-12
- **mined_on:** 2026-08-22
- **coverage:** partial
- **findings_extracted:** 1 (E-007), plus contribution to conflicts E-008 and E-016
- **notes:** Mined only far enough to observe that its category mapping differs from S-002's. The nature and size of the difference were not characterized. Same depth limitation as S-002.

### S-004
- **label:** Merchandising request channel export, Jan-Jun 2026
- **type:** conversation
- **location:** Slack export
- **authored_by:** Requesters in the channel; export compiled by the analytics team
- **date_range:** 2026-01-01 to 2026-06-30 (approximately; the corpus states "Jan-Jun 2026")
- **mined_on:** 2026-08-22
- **coverage:** sampled
- **findings_extracted:** 4 (E-009, E-010, E-011, E-012)
- **notes:** Coverage is recorded as sampled rather than full because the corpus supplies only theme counts, described as "rough", not the individual request texts. The requests' own wording — the single most valuable thing a request channel offers — was not available. No requester identities, so the eight business users named by the stakeholder cannot be checked against the channel. The 20 miscellaneous requests are entirely uncharacterized.

### S-005
- **label:** Ticket OPS-2214
- **type:** intake
- **location:** Ticket system
- **authored_by:** The analytics manager
- **date_range:** Filed 2026-02-19
- **mined_on:** 2026-08-22
- **coverage:** partial
- **findings_extracted:** 2 (E-013, E-014), plus contribution to conflict E-015
- **notes:** Only the summary line and filing metadata were available. Ticket status, comments, resolution, and any linked tickets were not mined, so it is unknown whether this was acted on, closed, or ignored — which matters, because a six-month-old unactioned cost ticket from the team's own manager is a different signal from a resolved one.

## Sources declared but not mined

None. The five sources above are the entirety of what was made available.

## Sources known to exist but unavailable

- **The other three recurring reports** (Promo Lift, Inventory Position, Markdown Recovery)
  named in the runbook [E-001]. Files for these were not in the corpus. Their absence is
  itself uninterpretable: they may not exist, may live elsewhere, or may have been
  discontinued.
- **The eight merchandising business users.** No source in the corpus is authored by a
  report consumer. Every source is authored by, or about, the analytics team.
- **Upstream data systems.** Nothing in the corpus describes where the report data
  originates, which is what any automation or self-service work would have to build on.
