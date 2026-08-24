# Artifact Standards

Every artifact this framework produces is a file on disk, in Markdown, with frontmatter.
Not a chat response. This is deliberate: artifacts must diff in git, survive the session
that made them, and paste into a wiki without reformatting.

## Location

    artifacts/<stage>-<artifact-name>.md

Example: `artifacts/1-problem-statement.md`, `artifacts/5-prd.md`

The numeric prefix is the stage, so a directory listing shows the shape of the work.

## Required frontmatter

    ---
    artifact: problem-statement
    stage: 1
    status: draft | reviewed | final
    created: 2026-08-20
    updated: 2026-08-20
    sources: [E-001, E-004, E-012]
    open_assumptions: [A-002, A-007]
    last_critique: 2026-08-20
    depth: quick | standard | deep
    ---

`sources` lists **finding IDs** (`E-nnn`) from `evidence/findings.md` — not source IDs
from `evidence/sources.md`. The naming is unfortunate and worth stating plainly: findings
are what artifacts cite; sources are what findings came from. `S-nnn` IDs appear in
`evidence/sources.md` and in prose where naming a source is useful, never in frontmatter.

`sources` and `open_assumptions` are lists of IDs, not counts. They make the artifact
self-describing: a reader sees immediately how well-grounded it is before reading a word
of the body.

An artifact with an empty `sources` list is legitimate only at `depth: quick` in stage 1,
before any mining has happened. Everywhere else it is a lint failure — it means the
document is entirely unsourced.

## Required body sections

Every artifact ends with:

    ## Provenance

    **Grounded in:** N findings from M sources, dated <oldest> to <newest>
    **Open assumptions:** N (X high-impact)
    **Gaps:** what this artifact could not establish and why
    **Last critique:** date, and what the critic flagged

The Gaps subsection is the one people skip and the one that matters most. An artifact that
claims complete knowledge is lying; every real piece of product work has holes. Naming them
is what lets the reader calibrate.

Skill-specific required sections are declared in each skill's Output Contract.

## Status lifecycle

- **draft** — written, not yet critiqued
- **reviewed** — passed `critique-artifact` and the flagged issues were addressed
- **final** — a human approved it

Only a human moves an artifact to `final`. Claude may move draft → reviewed after a critique
pass, and must say what changed. Both `reviewed` and `final` require `last_critique`.

On a small project the `sources` list will look nearly identical across artifacts and
convey little. That is expected — its value scales with the evidence base, and it costs
almost nothing at small size. Keep it.

## Prohibited

The linter fails on any of these:

- Unfilled placeholders: `TODO`, `TBD`, `[bracketed instruction]`, `XXX`, `FIXME`,
  `<placeholder>`, `Lorem ipsum`
- A quantitative claim with no `[E-nnn]` or `[ASSUMPTION A-nnn]` marker
- Missing required frontmatter fields
- Missing Provenance section
- A `sources` entry that does not resolve to `evidence/findings.md`
- An `open_assumptions` entry that does not resolve to `assumptions.md`, or that resolves
  to an entry whose status is not `open`
- An `[ASSUMPTION A-nnn]` marker in the body whose ID is not declared in
  `open_assumptions` frontmatter. Without this check the incentive runs toward listing as
  few as possible, which is assumption laundering by another name.
- `status: reviewed` or `final` with no `last_critique` date

That last check catches a real decay mode: an assumption gets validated, but the artifact
still shows it as open, so the reader distrusts a document that is actually well-grounded now.

## On placeholders

A placeholder that reaches a stakeholder is worse than a missing section. A missing section
reads as incomplete; a placeholder reads as complete and is not. Where content genuinely
cannot be written yet, write a sentence saying what is missing and why, and register the
gap. Never leave scaffolding text in a document that leaves your hands.
