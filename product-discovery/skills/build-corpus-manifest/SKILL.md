---
name: build-corpus-manifest
description: Declare what this project can actually mine, and what it cannot reach. Use before mining, whenever corpus.yaml is empty or stale.
stage: 2
inputs: [artifacts/1-problem-statement.md, artifacts/1-stakeholders.md]
outputs: [corpus.yaml, evidence/sources.md]
depth: quick | standard
---

# Build Corpus Manifest

## Purpose

Establish what evidence this project can reach, in a form the mining skill can work from,
and record what it cannot reach and why.

The manifest exists so the framework is portable. It declares evidence by **type**, not by
tool. A team with Confluence and a team with SharePoint write different `location` values
and the same `type`. Nothing in the skills needs to change.

The exclusion list matters as much as the inclusion list. "We looked and found nothing" and
"we never looked" produce identical silence in an evidence base, and they mean opposite
things about how far to trust it.

## When To Use

- Before `mine-corpus`, always
- When corpus access changes — new system granted, an export expires
- When picking up a project whose manifest is stale

## When Not To Use

- Never skipped when mining. An unmanifested mining pass has no record of coverage, and
  its gaps are indistinguishable from absences.

## Process

Follow `protocol/facilitation.md`.

**1. Start from the problem, not from the tool list.** Ask what would answer the open
questions, then ask where that would live. Starting from available systems biases the
corpus toward whatever is easy to search.

**2. Enumerate by type:**

- `existing_artifact` — things that do the job today: reports, dashboards, spreadsheets,
  scripts, runbooks-as-executed. **Highest value.** Each is a specification someone wrote
  and that people validated by continuing to use it.
- `intake` — tickets, request queues, email asks. How people phrase needs, and how often.
- `reference_doc` — wikis, data dictionaries, design docs, decision records.
- `conversation` — threads, channels. Highest noise; uniquely captures friction.
- `system` — the systems themselves, where you can query them.

**3. For each, record access reality.** `connector` (queryable directly), `export` (a
dump exists or can be made), or `manual` (someone copies things into a folder). Manual is
legitimate — a folder of pasted files is a corpus. Do not describe access you do not have.

**4. Record date range and volume.** Both shape what mining can conclude. A channel export
covering six months cannot tell you about last year, and knowing that in advance prevents
overclaiming.

**5. Record exclusions with reasons.** Access denied, out of scope, superseded, too costly
to obtain. Each exclusion is a known limit on the evidence base, and each should be
revisitable — "access denied" today may be a request you can make.

**6. Record known gaps** — questions the problem raises that *no* available source covers.
These go straight to DISCOVER and are often the highest-value interviews you will run.

**7. Sanity-check for one-sidedness.** The most common corpus defect is that every source
comes from one side of the problem. A corpus authored entirely by the team building the
thing will confirm that team's view. Ask explicitly whose voice is absent.

## Output Contract

**Paths:** `corpus.yaml` (the manifest), `evidence/sources.md` (seeded with declared sources)

`corpus.yaml` follows the template in `project-template/corpus.yaml`. Every source needs
`id`, `type`, `label`, `location`, `access`, and honest `date_range` / `est_volume`.

Replace the template's `access: manual | connector | export` option lists with the actual
value. A manifest left with pipe-delimited placeholders has not been filled in.

**Frontmatter:** `corpus.yaml` is YAML, not a Markdown artifact — it carries no artifact
frontmatter and is not checked by `lint-artifact.py`.

## Evidence Requirements

Per `protocol/evidence.md`. The manifest is a plan, not evidence — it makes no claims about
the world beyond what exists and is reachable.

**Do not list a source you have not confirmed exists.** A manifest naming a data dictionary
nobody has seen sends mining after a ghost and produces an unexplained gap. If you believe
something exists but have not confirmed it, put it in `known_gaps` as a question.

## Pitfalls

**Pitfall 1 — Starting from tools.**
*Symptom:* The manifest mirrors the company's software stack. *Consequence:* You mine what
is searchable, not what is relevant. *Fix:* Start from open questions.

**Pitfall 2 — Empty exclusion list.**
*Symptom:* No `excluded` entries. *Consequence:* A reader cannot distinguish a thorough
corpus from a convenient one. *Fix:* Everything has limits; record them.

**Pitfall 3 — Placeholder option lists left in.**
*Symptom:* `access: manual | connector | export` in a live manifest. *Consequence:* Nothing
consumes it and mining proceeds unguided. *Fix:* Pick one.

**Pitfall 4 — One-sided corpus.**
*Symptom:* Every source authored by the same team. *Consequence:* Mining confirms an
existing view and reads as validated. *Fix:* Name whose voice is missing, in `known_gaps`.

**Pitfall 5 — Overstating access.**
*Symptom:* `access: connector` for something requiring a request nobody has made.
*Consequence:* Mining stalls or silently skips it. *Fix:* Record the access you have today.

## References

**Related skills:** `mine-corpus` (stage 2), `inventory-existing-artifacts` (stage 2),
`identify-gaps` (stage 3)

**Protocol:** `protocol/evidence.md`, `protocol/facilitation.md`

**Template:** `project-template/corpus.yaml`
