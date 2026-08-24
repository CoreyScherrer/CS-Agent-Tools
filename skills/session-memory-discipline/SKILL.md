---
name: session-memory-discipline
description: What to record from a working session so the next one starts informed, and what to leave out. Use before ending any session that touched code, config, or infrastructure, and whenever you discover something non-obvious.
---

# Session Memory Discipline

Agent sessions are amnesiac. Everything learned in one is gone by the next unless it was
written somewhere durable. The cost is invisible and compounding: the same gotcha gets
rediscovered, the same judgment call re-litigated, the same dead end re-entered.

This is the discipline for deciding what survives.

## Capture when any of these is true

- You hit a non-obvious error and resolved it — what failed, what fixed it, why
- You discovered something about the system that was not documented
- You made a judgment call between two reasonable approaches
- A scheduled job, deploy, or tool behaved differently than its documentation claimed
- The user corrected your approach

**A successful session still produces learnings.** The rule is not "capture when something
went wrong." Sessions that go smoothly often contain the most useful discoveries, and they
are the ones most likely to be lost because nothing forced a reflection.

## Do not capture

- Anything the code or version history already records
- Anything that only matters inside the current conversation
- Restatements of existing documentation
- Activity logs — what you did is not a learning; what you *found* is

The test: **would a future session make a worse decision without this?** If no, leave it out.
A memory store full of noise is worse than a small one, because nobody reads it.

## Categories

Pick deliberately — the category determines when it surfaces later.

| Type | For | Example |
|---|---|---|
| `learning` | Technical discovery, gotcha, resolution | "Migration needs the grant applied before the role exists, not after" |
| `decision` | An architectural or design choice with a trade-off | "Chose polling over webhooks — the source has no delivery guarantee" |
| `pattern` | A convention that should hold across the codebase | "Every service exposes /health returning JSON status" |
| `preference` | How this person wants work done | "Wants pushback before execution, not after" |
| `feedback` | A correction the user gave you | Keep separate from `learning` — it is about *how to work*, not about the system |

Keeping `feedback` distinct matters. Corrections about your working method need to surface
at the *start* of a session; technical learnings surface when you touch the relevant system.

## Format

A memory that cannot be acted on later is not worth storing.

    Title: <system> — <one-line takeaway>

    <The observation, in one sentence.>

    **Why this matters:** <the consequence of not knowing this>
    **How to apply:** <what a future session should actually do>
    **Provenance:** <when, and how you learned it — command run, file read, error seen>

The title carries most of the value, because it is what gets scanned. `"Deploy — rsync
skips unchanged mtimes, needs --checksum"` is findable. `"Deployment notes"` is not.

**Provenance is what makes a memory auditable.** A year on, the difference between "I
observed this" and "I inferred this" decides whether to trust it or re-verify.

## Absolute dates only

Convert every relative reference before storing. "Last week", "recently", "the current
sprint" are meaningless the moment the session ends and actively misleading a month later.

Write `2026-08-24`, not `today`.

## Update rather than duplicate

Before writing, check whether something already covers it. Extend that entry instead of
adding a near-duplicate — two entries that disagree are worse than one that is slightly
stale, because a reader cannot tell which is current.

**Delete what turns out to be wrong.** A memory store is not an append-only log. A learning
that was true about a system that has since changed is a trap, and it is more dangerous than
having nothing, because it will be trusted.

## Verify before relying on a recalled memory

Memories reflect what was true when written. If one names a file, a flag, a port, or an
interface, **check it still exists before acting on it.** Recalled context is a strong hint,
not a fact.

## Portability note

This skill describes the discipline, not any particular store. It works with a database, a
directory of markdown files, or a single append-only document. What matters is that the
decision of *what* to record is made deliberately rather than by whatever was easiest to
write down at the end of a long session.
