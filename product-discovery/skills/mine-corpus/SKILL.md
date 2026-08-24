---
name: mine-corpus
description: Harvest what the organization already knows before interviewing anyone. Use at the start of discovery when documents, tickets, existing reports, or message history exist that bear on the problem.
stage: 2
inputs: [corpus.yaml, artifacts/1-problem-statement.md]
outputs: [evidence/findings.md, evidence/sources.md, artifacts/2-evidence-summary.md]
depth: quick | standard | deep
---

# Mine Corpus

## Purpose

Extract what the organization already knows, into a structured evidence base that every
later stage reads from. This runs **before** interviews, not after.

The reason is practical. In an enterprise, most of what you would ask in a discovery
interview has already been written down — in a ticket, a deck, a runbook, a thread, or
an existing report that encodes a real requirement someone gathered years ago. Interviewing
people to learn what a document already says spends your scarcest resource, stakeholder
patience, on information you could have read. Worse, it teaches stakeholders that talking
to you is low-value.

Mine first. Then interview only the gaps, and interview better because you arrive informed.

## When To Use

- Any project where the organization has written history bearing on the problem
- Especially: replacing or automating something that already exists, where the existing
  thing *is* the specification
- Before `prep-interviews`, always

## When Not To Use

- Genuinely greenfield with no organizational history (rare; check before believing it)
- The corpus is inaccessible and will remain so — then go straight to DISCOVER and note
  the gap in the evidence summary
- A trivial request that does not warrant an evidence base

## Inputs

`corpus.yaml` declares what is available. If it does not exist, run `build-corpus-manifest`
first. The problem statement scopes what to look for — mining without a frame returns
everything and establishes nothing.

## Process

Follow `protocol/facilitation.md`.

**1. Read the manifest.** Understand what sources exist, how to reach them, and what each
is likely to contain. Do not begin extracting until you know the shape of what you have.

**2. Triage sources by expected value.** Not all sources are equal. In rough order:

- **Existing artifacts that do the job today** (reports, dashboards, spreadsheets, scripts).
  Highest value by a wide margin. Each one is a specification someone already wrote, validated
  by the fact that people use it. It encodes a real question, a real definition, a real
  consumer, and a real cadence.
- **Intake records** (tickets, request queues, email asks). These show what people ask for
  in their own words, and how often.
- **Written decisions** (design docs, decision records, architecture notes). Show constraints
  and what was already tried.
- **Reference material** (wikis, runbooks, data dictionaries). Establishes definitions and
  current process.
- **Conversation history** (threads, channels). Highest noise, but uniquely captures friction
  and disagreement that never reaches a document.

**3. Extract findings, not summaries.** This is the discipline that makes the output useful.
A summary of a document is one undifferentiated blob nothing downstream can cite. A finding
is one claim, with one source, that supports a specific decision.

For each finding, record the full record per `protocol/evidence.md`: claim, source,
source_type, date, confidence, supports, notes.

**4. Date everything by source creation, not reading.** A confident finding from a
three-year-old deck is a low-confidence finding about today. Stale evidence presented as
current is the most common way a mined corpus misleads. When a source has no date, record
that as unknown rather than guessing — and drop confidence accordingly.

**5. Record conflicts as findings.** When two sources disagree, log both plus a third entry
naming the conflict. Do not silently pick one. A disagreement about a basic number almost
always means a definition problem, and definition problems found here are cheap; found
after launch they are expensive and embarrassing.

**6. Note what the corpus could not answer.** This is the direct input to `identify-gaps`
and the reason MINE-before-DISCOVER works. Track questions the problem statement raises
that no source addresses.

**7. Register assumptions for anything you inferred.** If you read between the lines, that
is an inference, not a finding. It goes in the ledger, not the evidence base.

**8. Write the summary artifact and lint.**

    python3 scripts/lint-artifact.py <project-dir>

## Output Contract

**Paths:**
- `evidence/findings.md` — the structured evidence base (append-only; never rewrite history)
- `evidence/sources.md` — one entry per source: what it was, when created, who authored,
  how accessed, how much was mined
- `artifacts/2-evidence-summary.md` — the human-readable synthesis

**Required sections in the summary artifact:**
- `# Evidence Summary`
- `## What The Corpus Covers` — sources mined, date range, volume
- `## Key Findings` — the findings that most affect the problem, cited by ID
- `## Conflicts` — where sources disagree, and what that suggests
- `## What The Corpus Could Not Answer` — the gap list feeding DISCOVER
- `## Corpus Quality` — staleness, coverage bias, what is missing and why
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: evidence-summary`, `stage: 2`.

## Evidence Requirements

Per `protocol/evidence.md`. This skill *produces* the evidence base, so the standard is
stricter than elsewhere:

- Every finding must have a resolvable source. "Someone mentioned" is not a source unless
  you name who and when, and then it is `source_type: conversation` at low confidence.
- No finding may be created from your own reasoning. Inference goes to the assumption ledger.
- Confidence is about the source, not your feeling about the claim.

## Pitfalls

**Pitfall 1 — Summarizing instead of extracting.**
*Symptom:* `findings.md` contains paragraphs about documents rather than discrete claims.
*Consequence:* Nothing downstream can cite it; the evidence base becomes an unusable
reading log. *Fix:* One claim, one ID, one source. If an entry contains "and", consider
splitting it.

**Pitfall 2 — Treating the corpus as truth.**
*Symptom:* Findings recorded at high confidence because they were written down.
*Consequence:* Documented-but-wrong propagates into requirements with a citation that
makes it look verified. *Fix:* Confidence reflects the source's authority over the claim.
A deck citing an unattached dashboard is medium at best.

**Pitfall 3 — Mining without a frame.**
*Symptom:* Hundreds of findings, no through-line. *Consequence:* Time spent, decisions
unaffected. *Fix:* The problem statement scopes the search. If a finding does not bear
on it, do not record it.

**Pitfall 4 — Recency bias in the corpus.**
*Symptom:* Everything mined is from the last quarter because that is what is searchable.
*Consequence:* You miss the original rationale for constraints and re-litigate settled
decisions. *Fix:* Deliberately seek the oldest relevant material. Note coverage bias in
Corpus Quality.

**Pitfall 5 — Skipping the "could not answer" list.**
*Symptom:* Mining ends with findings and no gap list. *Consequence:* DISCOVER has no
agenda and reverts to generic interviewing, losing the whole advantage of mining first.
*Fix:* Treat the gap list as a required output, not a nicety.

## References

**Related skills:** `build-corpus-manifest` (stage 2), `inventory-existing-artifacts`
(stage 2), `synthesize-evidence` (stage 2), `identify-gaps` (stage 3)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`,
`protocol/artifact-standards.md`

**Note on prior art:** Mining organizational history before primary research is standard
practice in research synthesis and in due diligence generally; the specific ordering
(mine → gap-list → interview only gaps) is this framework's own convention, adopted
because enterprise stakeholder time is the binding constraint.
