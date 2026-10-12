# Product Discovery

_An enterprise product discovery framework. Evidence in, artifacts out._

> Why, hello there, discerning product person! You've wandered into a journey
> through the wonderful world of knowing what to build *before* you build it.
> On this particular expedition we'll guide you, with a wink and a well-cited
> footnote, through **Masterful Product Swashbuckling** — where every claim is
> grounded, every assumption is registered, and nobody writes a PRD from vibes
> ever again. Yo ho, and onward to the evidence!

## 1. What this tool is

Twenty-five agent skills, a protocol, three linters and a project template that
run a seven-stage discovery process: **triage → frame → mine → discover → define
→ specify → validate → communicate**. The core rule: **every material claim is
either cited or registered as an assumption; there is no third state.**

The full description, the reasoning behind the stage order, and the quickstart
live in [`product-discovery/README.md`](https://github.com/CoreyScherrer/CS-Agent-Tools/blob/main/product-discovery/README.md).
This page is the catalog entry.

## 2. Who this is for, and what you need

Product managers and the AI agents they work with, inside an organisation that
already has documents, tickets and reports worth mining before anyone is
interviewed.

- **Hardware:** none.
- **Accounts:** none.
- **Software:** Python 3 (for the linters), an AI agent that reads `SKILL.md`
  files, this repo cloned.

## 3. Setup time

| | Estimate |
|---|---|
| Human hands-on time | 10 minutes to scaffold a project |
| AI agent working time | Per project; a triage-sized project is an afternoon |
| Elapsed | Per project |

## 4. Working with your AI agent on this guide

Scaffold the project **outside** this repo (`product-discovery/scripts/new-project.sh`
does this on purpose) so that mined evidence can never be committed here. Point
the agent at the project directory and at `product-discovery/protocol/`.

## 5. The phases

The seven stages are the phases; each is a skill under
`product-discovery/skills/`. Start with `size-the-voyage` (triage), then
`frame-problem`.

**Done when:** `product-discovery/scripts/lint-artifact.py` passes on each
artifact, and `lint-evidence.py` finds no uncited claim.

## 6. Gotcha ledger

| Symptom | Cause | Fix |
|---|---|---|
| Mined evidence shows up in a commit | Project scaffolded inside the repo | Scaffold outside; the pre-commit guard blocks `evidence/`, `assumptions.md`, `artifacts/` paths |
| Artifact reads authoritative but nobody can tell what's grounded | Claims without citations or assumption registration | Run the linters; the protocol allows no third state |

## 7. Free vs paid

Nothing to buy.

## 8. Talking to the tool

Invoke the skills by name from your agent (`frame-problem`, `mine-corpus`,
`write-prd` …). The worked example under `product-discovery/examples/` shows a
complete run on synthetic material.

## 9. Keeping it alive

- [ ] Skills cite their originating frameworks; when a cited source changes
  materially, update the citation, not the copied text (there is none).
