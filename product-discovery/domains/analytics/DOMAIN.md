# Domain Pack: Analytics & Reporting

Extends the spine for internal analytics work — self-service question answering, report
automation, and replacing manually-assembled reporting.

Domain packs add skills and sharpen stage guidance. They never replace the spine or the
protocol.

## Why this domain needs a pack

Three risks dominate internal analytics work and are barely touched by general product
discovery:

**Correctness is the product.** An analytics answer that is subtly wrong is worse than no
answer, because it is acted upon. A slow dashboard is an annoyance; a dashboard that
quietly disagrees with the system of record destroys trust in every number it shows, and
that trust does not come back easily. Requirements must state what "correct" means, how it
is verified, and what the interface does when it is not confident.

**Definitions are the substrate.** In any organization of size, basic terms have multiple
live definitions — what counts as a sale, when a return nets out, which hierarchy applies,
whether a date is transaction or posting. Two reports disagreeing is usually not a bug; it
is two definitions, both defensible, never reconciled. Build on undefined terms and you
ship the disagreement.

**The existing manual reports are the specification.** Every hand-built report encodes a
real question, a real definition, a real consumer, and a real cadence — validated by the
fact that people still use it despite the effort. This is the richest corpus available and
the most commonly skipped, because inventorying it is tedious and looks like it is not
product work. It is.

## Added skills

- `inventory-reports` (stage 2) — catalogue what exists today: question answered, consumer,
  cadence, source data, transformations, hand-fixes. Runs inside MINE.
- `govern-definitions` (stage 4) — surface and reconcile competing definitions. Runs inside
  DEFINE, because scope decisions made over undefined terms are not real decisions.
- `spec-trust-requirements` (stage 5) — specify correctness, freshness, lineage, and
  low-confidence behavior. Runs inside SPECIFY.

## Stage emphasis

**MINE** — Existing reports outrank every other source. Manual fix-up steps are the highest
signal in the entire corpus: each one marks a place where the data does not support the
question being asked. A tab called "category fix - DO NOT DELETE" is a requirement.

**DISCOVER** — Request history often answers most of what interviews would. Look at what
people actually asked, how they phrased it, and how often. "Why does this number not match
that one" appearing repeatedly is a definition finding, not a UX finding.

**DEFINE** — Do not set scope over undefined terms. Run `govern-definitions` first.

**SPECIFY** — Trust requirements are first-class, not non-functional footnotes. Include
what happens when data is late, partial, or disputed.

**VALIDATE** — The cheapest meaningful test is usually reconciliation: does the new thing
agree with the existing thing on a known period? Disagreement before launch is a finding;
after launch it is an incident.

## Anti-patterns

**Building the requested dashboard.** "Build a self-service dashboard" is a solution. The
problem is usually that people cannot get answers without a human. A dashboard is one
answer and often the wrong one — it works when questions are known and repeated, and fails
when they are not, which is precisely when people ask a human.

**Automating a report nobody reads.** Existing does not mean valuable. Inventory includes
who consumes it and what decision it drives. Some recurring reports should be retired, not
automated, and that is a legitimate and valuable finding.

**Treating disagreement as a data quality bug.** Two numbers disagreeing usually means two
definitions. Fixing the pipeline does not fix that.
