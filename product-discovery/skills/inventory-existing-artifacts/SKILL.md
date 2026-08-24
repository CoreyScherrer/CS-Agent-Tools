---
name: inventory-existing-artifacts
description: Catalogue whatever does the job today, treating each existing thing as a specification someone already wrote. Use during mining on any project that replaces, automates, or supplements existing work.
stage: 2
inputs: [corpus.yaml, artifacts/1-problem-statement.md]
outputs: [artifacts/2-artifact-inventory.md, evidence/findings.md entries]
depth: quick | standard | deep
---

# Inventory Existing Artifacts

## Purpose

Catalogue what does the job today — the reports, spreadsheets, scripts, manual processes,
and workarounds people currently rely on — and extract the requirements they encode.

Anything that has survived in daily use is a specification that has already been
field-tested. Someone built it to answer a real question, other people adopted it, and it
persisted despite the cost of maintaining it. That is stronger evidence of a real need
than most interviews produce.

This is the domain-neutral form of the pattern. `domains/analytics/skills/inventory-reports`
applies it specifically to reporting.

## When To Use

- Any project replacing, automating, or supplementing existing work
- Especially where the existing thing is manual — the manual steps are the highest-signal
  evidence available
- Runs inside MINE, before interviews

## When Not To Use

- Genuinely greenfield with no current process. Verify this. "There is no current process"
  usually means "the current process is a spreadsheet nobody mentions."

## Process

Follow `protocol/facilitation.md`.

**1. Enumerate, including the unofficial.** The personal spreadsheet, the saved query, the
shared doc someone updates by hand. Unofficial artifacts are frequently the most-used and
never appear on any official list, precisely because nobody owns them.

**2. For each, record:**

- **What job it does** — the question it answers or task it completes, in the user's terms
- **Who uses it** — by name or role. If nobody can name a user, that is a finding.
- **What decision it supports** — what someone does differently because of it. "Awareness"
  is not a decision.
- **How often** — and whether that matches the decision's actual rhythm
- **What it depends on** — systems, data, other artifacts, specific people
- **Manual steps** — every hand-fix, override, correction, and re-key
- **Effort** — cited to a source, never estimated by you
- **Known problems** — what breaks, what is disputed, what people work around

**3. Treat every manual step as a candidate requirement.** This is the highest-value part
of the inventory and the reason it must be done by opening the artifacts rather than
reading their descriptions.

A manual step exists because a system does not do something people need. A hand-maintained
mapping means a relationship is undefined upstream. A hardcoded override means a business
rule exists that nothing encodes. A re-key between systems means an integration is missing.
Each one is a requirement wearing a workaround's clothes, and each is invisible from
outside the file.

**4. Note where artifacts disagree.** Two things computing the same quantity differently is
a finding, and usually a definition problem rather than a bug. Record both and the conflict
per `protocol/evidence.md`. Do not resolve it here.

**5. Assess consolidation and retirement.** Which artifacts answer the same question with
different slices? Which exist only because something else was hard to change? Which have no
identifiable user or decision?

**Retirement is a legitimate and valuable outcome.** Not everything that exists should be
rebuilt. Finding that three of eleven reports have no consumer is a real result.

**6. Write findings into the evidence base**, then the inventory artifact.

## Output Contract

**Path:** `artifacts/2-artifact-inventory.md`

**Required sections:**
- `# Artifact Inventory`
- `## Artifacts` — one subsection each, with the fields above
- `## Manual Steps And What They Reveal` — every workaround and the requirement it implies
- `## Disagreements` — where artifacts compute the same thing differently
- `## Consolidation Candidates`
- `## Retirement Candidates` — no identifiable user or decision
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: artifact-inventory`, `stage: 2`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** effort figures, who uses something, how often it is
used, why it exists.

**Never estimate effort.** "This probably takes a few hours" is invention, and effort
figures drive business cases. A source states it, someone tells you, or it is an open
question. "Unknown" is a legitimate entry and an honest one.

**Directly observed facts are high confidence** — a workbook has eleven tabs, two files
apply different mappings. You opened it and looked. That is the most reliable evidence
class in the corpus.

**May be reasoned, if labeled:** what a manual step implies about missing capability. Label
it as inference, and register the underlying claim as an assumption if it will drive scope.

## Pitfalls

**Pitfall 1 — Cataloguing names instead of jobs.**
*Symptom:* A list of titles and schedules. *Consequence:* You rebuild artifacts rather than
serving the jobs they do. *Fix:* Write the question each answers, in the user's words.

**Pitfall 2 — Not opening the files.**
*Symptom:* The inventory describes what artifacts are supposed to do.
*Consequence:* Every manual step stays invisible, and the replacement is built assuming
upstream data is sufficient — which the workarounds prove it is not. Discovered in build.
*Fix:* Open them. The evidence is inside.

**Pitfall 3 — Existing equals valuable.**
*Symptom:* Every artifact becomes a requirement. *Consequence:* You automate work that
should have stopped. *Fix:* Require a named user and a named decision.

**Pitfall 4 — Ignoring unofficial artifacts.**
*Symptom:* Only sanctioned tools inventoried. *Consequence:* You miss what people actually
use, and your replacement competes with a spreadsheet it does not know about.
*Fix:* Ask what people keep on their own machines.

## References

**Related skills:** `mine-corpus` (stage 2), `synthesize-evidence` (stage 2),
`inventory-reports` (analytics domain)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`
