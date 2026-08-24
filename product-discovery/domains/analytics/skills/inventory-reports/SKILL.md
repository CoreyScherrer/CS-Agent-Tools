---
name: inventory-reports
description: Catalogue every report and dashboard that exists today, treating each as a specification someone already wrote. Use during MINE on any analytics, reporting, or BI project.
stage: 2
domain: analytics
inputs: [corpus.yaml, artifacts/1-problem-statement.md]
outputs: [artifacts/2-report-inventory.md, evidence/findings.md entries]
depth: quick | standard | deep
---

# Inventory Reports

## Purpose

Catalogue what exists today. Every hand-built report encodes a real question, a real
consumer, a real definition, and a real cadence — validated by the fact that people keep
paying the cost of producing it. This is the richest corpus available on an analytics
project and the most commonly skipped, because it is tedious and looks like it is not
product work.

It is product work. A report inventory is a requirements document that has already been
field-tested.

## When To Use

- Any project replacing, automating, or supplementing existing reporting
- Any self-service analytics effort — what people build by hand tells you what they will
  ask the interface
- Runs inside MINE, before interviews

## When Not To Use

- Genuinely no existing reporting (verify this; there is usually a spreadsheet)
- The existing reports are inaccessible — note it as a corpus gap, do not guess at contents

## Process

**1. Enumerate.** Every recurring report, dashboard, and spreadsheet in scope. Include the
unofficial ones — the analyst's personal workbook is often the most-used artifact on the
team and never appears in an official list.

**2. For each, record:**

- **Question answered** — in the consumer's words where possible, not the report's title
- **Consumer** — who reads it, by role or name. If nobody can name a consumer, that is a
  finding.
- **Decision it drives** — what someone does differently because of it. "Awareness" is not
  a decision. A report driving no decision is a retirement candidate.
- **Cadence** — and whether the cadence matches the decision's rhythm
- **Source data** — tables, systems, extracts
- **Transformations** — joins, filters, aggregations, business rules applied
- **Manual steps** — every hand-fix, override, mapping tab, and "do not delete" cell
- **Effort** — time to produce, cited to a source, not estimated by you
- **Known issues** — reconciliation problems, late data, disputed numbers

**3. Flag every manual step as a candidate finding.** This is the highest-signal part of
the inventory. A manual fix-up marks a place where the available data does not support the
question being asked. A mapping tab means a hierarchy is missing or contested upstream. A
hardcoded override means a rule exists that no system encodes. Each one is a requirement
in disguise, and they are invisible from anywhere except inside the file.

**4. Note definitional conflicts between reports.** When two reports compute what sounds
like the same measure differently, record both and the conflict. Do not resolve it here —
that is `govern-definitions` in DEFINE. Recording it is what makes the later reconciliation
possible.

**5. Assess consolidation.** Which reports answer the same underlying question with
different slices? Which exist only because another was hard to change? Which should be
retired rather than rebuilt?

**6. Write findings into the evidence base** per `protocol/evidence.md`, then the inventory
artifact.

## Output Contract

**Path:** `artifacts/2-report-inventory.md`

**Required sections:**
- `# Report Inventory`
- `## Reports` — one subsection per report with the fields above
- `## Manual Steps And What They Reveal` — every hand-fix and the requirement it implies
- `## Definitional Conflicts` — where reports disagree on the same measure
- `## Consolidation Candidates` — overlapping or redundant reports
- `## Retirement Candidates` — reports with no identifiable consumer or decision
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: report-inventory`, `stage: 2`, `domain: analytics`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** effort figures, consumer identity, frequency of use,
any claim about why a report exists or how it is used.

**Never estimate effort yourself.** "This probably takes a few hours" is invention. Either
a source states it, someone tells you, or it is an open question. Effort figures drive
business cases; an invented one corrupts the whole case.

**May be reasoned:** what a manual step implies about missing data — but label it as
inference and register the underlying claim as an assumption if it will drive scope.

## Pitfalls

**Pitfall 1 — Cataloguing titles instead of questions.**
*Symptom:* The inventory lists report names and schedules. *Consequence:* You rebuild the
same reports rather than serving the underlying questions. *Fix:* For each, write the
question a consumer is actually asking. If you cannot, find out.

**Pitfall 2 — Skipping the manual steps.**
*Symptom:* Inventory records sources and outputs but not hand-fixes. *Consequence:* The
replacement is built on the assumption that upstream data is sufficient, which the manual
steps prove it is not. Discovered in build. *Fix:* Open the files. The fix-ups are only
visible inside.

**Pitfall 3 — Assuming existing means valuable.**
*Symptom:* Every report becomes a requirement. *Consequence:* You automate work that should
have stopped. *Fix:* Require a named consumer and a named decision. Absent both, it is a
retirement candidate.

**Pitfall 4 — Estimating effort.**
*Symptom:* Plausible hours-per-week figures with no source. *Consequence:* A fabricated
business case. *Fix:* Cite or ask. "Unknown" is a legitimate entry.

## References

**Related skills:** `mine-corpus` (stage 2), `govern-definitions` (stage 4, analytics),
`spec-trust-requirements` (stage 5, analytics)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**Domain:** `domains/analytics/DOMAIN.md`
