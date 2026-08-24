---
name: synthesize-evidence
description: Turn a pile of findings into a coherent picture with its weaknesses named. Use at the end of mining, and again after discovery adds new evidence.
stage: 2
inputs: [evidence/findings.md, evidence/sources.md, assumptions.md]
outputs: [artifacts/2-evidence-summary.md]
depth: standard | deep
---

# Synthesize Evidence

## Purpose

Turn discrete findings into a picture a person can reason about — and, equally, state what
that picture cannot support.

Mining produces atoms. Fifty findings is not understanding; it is inventory. Synthesis is
where patterns, conflicts, and absences become visible. It is also the last point before
the evidence base starts driving decisions, which makes it the right place to be honest
about its limits.

## When To Use

- At the end of MINE, always
- Again after DISCOVER adds findings — synthesis is re-run, not written once
- Whenever the evidence base has grown enough that nobody holds it in their head

## When Not To Use

- Before findings exist. Synthesis of three findings is just three findings.

## Process

Follow `protocol/facilitation.md`.

**1. Group findings by what they bear on,** not by source. Findings from a ticket, a deck,
and a spreadsheet that all bear on the same question belong together — that convergence is
itself evidence, and it is invisible when organized by origin.

**2. Identify what the evidence supports strongly.** Claims backed by multiple independent
sources, ideally of different types. Note the independence explicitly: three documents
authored by the same person are one source wearing three hats.

**3. Identify what it supports weakly.** Single-source claims, old sources, secondhand
figures. These are legitimate findings that cannot yet carry a decision.

**4. Surface every conflict.** Per `protocol/evidence.md`, conflicts are among the most
valuable outputs. Group them and look for a pattern — several conflicts about the same
concept usually indicates one underlying definition problem, not several data problems.

**5. Name the absences.** What does the problem statement raise that no finding addresses?
This becomes the DISCOVER agenda and is the payoff of mining first.

**6. Assess corpus quality honestly.** Three dimensions:

- **Staleness** — how old is the evidence relative to what it describes?
- **Coverage** — which parts of the problem have evidence and which do not?
- **Authorship bias** — **whose voice is in this corpus, and whose is absent?**

The third is the one most often skipped and most often decisive. A corpus authored entirely
by the team that built the current process will confirm that team's understanding of it. A
corpus with no user voice cannot tell you what users need, no matter how many findings it
contains.

**7. State what the evidence base cannot support.** Explicitly. A synthesis that reads as
complete invites decisions it cannot carry.

## Output Contract

**Path:** `artifacts/2-evidence-summary.md`

**Required sections:**
- `# Evidence Summary`
- `## What The Corpus Covers` — sources, types, date range, volume
- `## Well Supported` — claims with multiple independent sources
- `## Weakly Supported` — single-source or stale claims, flagged as not yet decision-grade
- `## Conflicts` — disagreements, grouped, with what each pattern suggests
- `## What The Corpus Could Not Answer` — the DISCOVER agenda
- `## Corpus Quality` — staleness, coverage, authorship bias
- `## What This Evidence Cannot Support` — decisions this base is insufficient for
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: evidence-summary`, `stage: 2`.

## Evidence Requirements

Per `protocol/evidence.md`.

Every claim in the synthesis cites the findings it rests on. Synthesis introduces **no new
claims about the world** — it only organizes and assesses existing findings. Anything that
feels like a new claim is either an inference (register it as an assumption) or a finding
you should have recorded during mining.

**The one thing synthesis may assert without citation** is its own assessment of corpus
quality, since that is a judgment about the evidence rather than about the world. State the
reasoning.

## Pitfalls

**Pitfall 1 — Narrative smoothing.**
*Symptom:* The synthesis reads as a coherent story with conflicts resolved.
*Consequence:* The most valuable findings — the disagreements — disappear, and a decision
gets made over an unreconciled definition. *Fix:* Conflicts get their own section and stay
unresolved.

**Pitfall 2 — Mistaking volume for strength.**
*Symptom:* Confidence proportional to finding count. *Consequence:* Forty findings from one
team read as overwhelming evidence. *Fix:* Assess independence, not quantity.

**Pitfall 3 — Skipping authorship bias.**
*Symptom:* Corpus Quality covers staleness and coverage only. *Consequence:* A one-sided
corpus reads as validated. *Fix:* Ask whose voice is absent. It is the single most useful
question in this skill.

**Pitfall 4 — Introducing claims.**
*Symptom:* Statements in the synthesis with no finding behind them. *Consequence:* The
evidence base appears to support something it never established. *Fix:* Every claim cites.
New claims go back to mining or into the ledger.

**Pitfall 5 — Writing it once.**
*Symptom:* Synthesis produced at the end of MINE and never updated.
*Consequence:* Downstream stages reason from a stale picture. *Fix:* Re-run after DISCOVER.

## References

**Related skills:** `mine-corpus` (stage 2), `inventory-existing-artifacts` (stage 2),
`identify-gaps` (stage 3), `critique-artifact` (any stage)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`
