---
name: define-acceptance
description: Write conditions someone other than the author can use to determine pass or fail. Use alongside stories, before any work is estimated or started.
stage: 5
inputs: [artifacts/5-stories.md, artifacts/5-prd.md]
outputs: [artifacts/5-acceptance.md]
depth: standard | deep
---

# Define Acceptance

## Purpose

Write the conditions under which each requirement is satisfied, precisely enough that
someone who did not write them can determine pass or fail without asking.

That last clause is the whole test. Acceptance criteria that require their author to
adjudicate have not reduced ambiguity, they have relocated it — and the adjudication
happens at the worst possible time, when the work is already built.

## When To Use

- Alongside `write-stories`, before estimation
- When "done" keeps being disputed after delivery
- When work is repeatedly returned in review for reasons nobody anticipated

## When Not To Use

- Before requirements are specified. Criteria written first become the requirements,
  incompletely.

## Process

Follow `protocol/facilitation.md`.

**1. For each requirement, write the observable condition.** What is true after, that was
not true before. Observable means someone can check it — by using the system, running a
query, or watching the behavior.

**2. Use Given/When/Then where behavior is conditional.** Given a starting state, when
something happens, then something is observably true. Where the requirement is not
conditional, a plain checklist is clearer — do not force the form.

**3. Cover the failure paths.** Most acceptance criteria describe only the case where
everything works. The unspecified cases are where the arguments happen and where most
production defects live. For each requirement, state what happens when input is invalid,
data is missing, a dependency is unavailable, or the user does something unexpected.

**4. Include the non-obvious.** Performance where it matters, permissions, what happens
concurrently, what is logged. These are the criteria most often assumed and least often
written, and each one assumed is one argued about later.

**5. Make each independently checkable.** A criterion that depends on interpreting another
criterion is not a criterion.

**6. State what is explicitly not required.** Bounds the work and prevents gold-plating —
and prevents the reviewer who expects more than was agreed.

**7. Check each against the stranger test.** Could someone unfamiliar with the project
determine pass or fail from this text alone? If not, it needs specifics — a number, a
concrete state, an exact behavior.

## Output Contract

**Path:** `artifacts/5-acceptance.md`

**Required sections:**
- `# Acceptance Criteria`
- `## Criteria By Requirement` — grouped, each independently checkable
- `## Failure Paths` — invalid input, missing data, unavailable dependencies
- `## Non-Functional` — performance, permissions, logging, concurrency, where they matter
- `## Explicitly Not Required` — bounds on the work
- `## Open Questions` — criteria that cannot be written yet, and what blocks them
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: acceptance`, `stage: 5`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite or mark as assumption:** every threshold. A latency target, a volume the system
must handle, a freshness window, a tolerance — each is a real commitment with cost
implications.

**Never invent a threshold.** "Responds within two seconds" with no source is the most
common invented number in a specification, and it is invented in the place where it will
be built against, tested against, and defended. Either something establishes it — a
measured baseline, a stated requirement, an existing SLA — or it is an open question with a
named owner.

**May be reasoned:** the structure of the criteria and which failure paths matter.

## Pitfalls

**Pitfall 1 — Happy path only.**
*Symptom:* Every criterion describes success. *Consequence:* Failure behavior is decided ad
hoc during implementation and is inconsistent. *Fix:* A failure path per requirement, minimum.

**Pitfall 2 — Criteria needing their author.**
*Symptom:* "Works correctly", "is intuitive", "performs well". *Consequence:* Pass/fail
becomes a negotiation after the work is done. *Fix:* The stranger test.

**Pitfall 3 — Invented thresholds.**
*Symptom:* Round numbers for latency, volume, or freshness with no source.
*Consequence:* Engineering builds to a fictional target — sometimes at real cost.
*Fix:* Cite, or mark as open with an owner.

**Pitfall 4 — Missing the non-functional.**
*Symptom:* Only functional behavior specified. *Consequence:* Permissions and logging get
retrofitted, badly. *Fix:* Consider each category explicitly, and say when it does not apply.

**Pitfall 5 — Criteria that restate the requirement.**
*Symptom:* The criterion is the requirement rephrased. *Consequence:* No ambiguity removed.
*Fix:* Ask how you would verify it. Write that.

## References

**Related skills:** `write-stories` (stage 5), `write-prd` (stage 5),
`spec-trust-requirements` (analytics domain)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**External frameworks:** Given/When/Then comes from Behaviour-Driven Development as
formulated by Dan North (2006) and developed in Gojko Adzic, *Specification by Example*
(2011).
