---
name: assess-risk
description: Identify what could go wrong, including after launch, and decide what to do about each. Use before committing to build, and again before release.
stage: 6
inputs: [artifacts/5-prd.md, assumptions.md, artifacts/1-stakeholders.md, artifacts/5-journey.md]
outputs: [artifacts/6-risks.md]
depth: standard | deep
---

# Assess Risk

## Purpose

Identify what could go wrong, how bad it would be, and what you are doing about each —
including the risks that only appear after launch.

Risk registers fail in a predictable way: they list the risks everyone already discusses,
rate them with invented probabilities, and get filed. The value is not in the list. It is
in surfacing the risks nobody is talking about and in forcing an owner and a decision for
each.

## When To Use

- Before committing to build
- Again before release, when what you know has changed
- After any material scope change

## When Not To Use

- As a one-time formality. A register written once and never revisited is worse than none,
  because it creates an impression of diligence.

## Process

Follow `protocol/facilitation.md`.

**1. Start from the assumption ledger.** Every open assumption is a risk, already rated for
impact. This is the cheapest source and the most often overlooked — teams write risk
registers from scratch while a ledger of rated unknowns sits beside them.

**2. Then work the categories people skip:**

- **Operational** — who runs this, do they know, are they staffed for it
- **Dependency** — what you need from another team, and what happens if it slips
- **Adoption** — what if people keep doing it the old way. In internal tooling this is the
  most common failure and the least often registered.
- **Definitional** — what if a term this computes is disputed after launch
- **Data** — what if the source changes shape, arrives late, or is wrong
- **Trust** — what if the first visible error destroys confidence in the whole thing
- **Maintenance** — what happens when the people who built it move on

**3. Rate impact and likelihood — qualitatively.** High/medium/low. **Do not assign
probability percentages.** A "35% likelihood" is invention with a decimal point; it invites
arithmetic on a guess, and the arithmetic looks like analysis. Qualitative ratings are
honest about their own precision.

**4. For each, decide: mitigate, accept, transfer, or avoid.** A risk with no decision is
not managed. Accepting is legitimate and requires a named person.

**5. Name an owner per risk.** Unowned risks are unmanaged by definition.

**6. Define the trigger.** What would tell you this risk is materializing — the specific
signal, and who is watching for it. A risk with no detection plan is discovered by its
consequences.

**7. Identify the risks that would be discovered too late.** Some only become visible after
they have caused damage — silent data corruption, gradual trust erosion, a dependency that
degrades rather than fails. These need detection designed in, and they are the ones a
generic register misses.

## Output Contract

**Path:** `artifacts/6-risks.md`

**Required sections:**
- `# Risks`
- `## From Open Assumptions` — each open assumption as a risk, with its ID
- `## Operational` — running it, staffing, on-call
- `## Dependency` — external teams and systems
- `## Adoption` — what if people do not switch
- `## Data And Definition` — sources, shape changes, disputed terms
- `## Trust` — what a visible error would cost
- `## Late-Discovery Risks` — those that surface only after damage, and detection plans
- `## Decisions` — per risk: mitigate / accept / transfer / avoid, owner, trigger
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: risks`, `stage: 6`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** any claim about how likely something is, what it would
cost, or what a dependency team will do.

**Never assign a numeric probability.** Qualitative ratings only. A percentage on a
one-off organizational risk has no frequentist basis and its precision is entirely
rhetorical.

**May be reasoned:** the identification and categorization of risks, and the mitigation
choices — with reasoning stated.

## Pitfalls

**Pitfall 1 — Ignoring the ledger.**
*Symptom:* The register duplicates work already done in `assumptions.md`.
*Consequence:* Two drifting lists of the same unknowns. *Fix:* Start from the ledger and
reference IDs.

**Pitfall 2 — Invented probabilities.**
*Symptom:* Percentages, or scores multiplying impact by likelihood.
*Consequence:* Fabricated precision drives real prioritization. *Fix:* Qualitative only.

**Pitfall 3 — Missing adoption risk.**
*Symptom:* Only technical risks. *Consequence:* The most likely internal-tooling failure —
people keep using the spreadsheet — is unregistered. *Fix:* Ask what happens if nobody
switches.

**Pitfall 4 — Risks without owners or triggers.**
*Symptom:* A list with no names and no signals. *Consequence:* Nothing is watched, and
risks are discovered by their consequences. *Fix:* Owner and trigger for each.

**Pitfall 5 — Written once.**
*Symptom:* Never revisited after the initial pass. *Consequence:* Stale by release.
*Fix:* Re-run before release.

## References

**Related skills:** `design-probe` (stage 6), `scope-decision` (stage 4),
`map-stakeholders` (stage 1), `spec-trust-requirements` (analytics domain)

**Protocol:** `protocol/assumptions.md`, `protocol/evidence.md`

**Note on prior art:** Impact/likelihood registers are standard project risk management.
The prohibition on numeric probabilities and the late-discovery category are this
framework's own conventions, adopted because unfounded precision is this framework's
central concern.
