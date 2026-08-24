---
name: govern-definitions
description: Surface and reconcile competing definitions of business terms before scope is set. Use during DEFINE on any analytics project, especially where reports disagree.
stage: 4
domain: analytics
inputs: [artifacts/2-report-inventory.md, evidence/findings.md]
outputs: [artifacts/4-definitions.md]
depth: standard | deep
---

# Govern Definitions

## Purpose

Surface the competing definitions of terms the product will compute, and get them
reconciled or explicitly scoped before requirements are written.

In any organization of size, basic terms have multiple live definitions. What counts as a
sale — booked, shipped, delivered, net of returns? Which date — transaction, posting,
effective? Which hierarchy — the current one, or the one finance restates against? Each
definition is usually defensible and serves someone's real need. The problem is not that
they differ; it is that they differ invisibly.

Build over that and you ship the disagreement. Then every consumer who gets a number that
does not match their existing report concludes the new system is broken — and functionally,
for them, it is.

## When To Use

- Any analytics project where more than one report computes a similar measure
- Whenever the inventory or request history shows "why does this not match" traffic
- Before scope is set — scope decided over undefined terms is not a real decision

## When Not To Use

- A single-source, single-consumer tool with no reconciliation surface (rare)
- Before the report inventory exists — you will not know what conflicts

## Process

**1. Extract every measure and dimension the product will compute.** From the inventory,
the request history, and the problem statement.

**2. For each, find every definition in use.** Read the actual transformations, not the
labels. Two reports both saying "Net Sales" tell you nothing; the SQL and the mapping tabs
tell you everything.

**3. Record each definition with its owner and its rationale.** Definitions differ for
reasons. Finance nets returns because the P&L does. Merchandising does not because they are
measuring sell-through. Neither is wrong. Capturing *why* is what makes reconciliation
possible instead of political.

**4. Classify each term:**

- **Aligned** — one definition, agreed. Record it and move on.
- **Reconcilable** — multiple definitions, one can be agreed as canonical. Needs a decision
  and a named decider.
- **Legitimately plural** — multiple definitions that must coexist because they serve
  genuinely different questions. The product must then expose which one it is using, every
  time it shows a number. This is a requirement, and it is the case people most often
  mishandle by picking one silently.
- **Undefined** — nobody can state the rule. High risk. Register as an assumption with an
  owner.

**5. Route decisions to named people.** A definition conflict is a business decision, not a
data decision. Analytics teams routinely try to resolve these unilaterally and then own the
resulting argument. Name the decider.

**6. State what is out of scope.** Terms the product will not compute, and why. This is
often the fastest way to shrink an unbounded analytics scope.

## Output Contract

**Path:** `artifacts/4-definitions.md`

**Required sections:**
- `# Definitions`
- `## Canonical` — agreed definitions, with owner
- `## Contested` — competing definitions, each with owner, rationale, and named decider
- `## Legitimately Plural` — terms that must coexist, and how the product will disambiguate
- `## Undefined` — terms nobody can state, with assumption IDs and owners
- `## Out Of Scope` — terms this product will not compute
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: definitions`, `stage: 4`, `domain: analytics`.

## Evidence Requirements

Per `protocol/evidence.md`. Every definition must be traced to where it is actually
implemented — a query, a mapping, a documented rule — or attributed to the person who
stated it, with a date.

**Never write a definition from general knowledge of how the term is usually computed.**
The whole point is what this organization actually does. A textbook definition of gross
margin is worse than useless here; it is confidently wrong in a way that sounds right.

## Pitfalls

**Pitfall 1 — Resolving conflicts unilaterally.**
*Symptom:* The analytics team picks a definition and proceeds. *Consequence:* You own an
argument that belongs to the business, and consumers whose definition lost do not adopt.
*Fix:* Name a decider. Escalate if needed. Document the decision.

**Pitfall 2 — Treating plurality as a bug.**
*Symptom:* Forcing one definition where two genuinely serve different questions.
*Consequence:* One group's number becomes wrong for their purpose, and they go back to
their spreadsheet. *Fix:* Support both, label clearly, and make the active definition
visible on every number.

**Pitfall 3 — Definition drift after launch.**
*Symptom:* Definitions agreed and never revisited. *Consequence:* Silent divergence as
upstream systems change. *Fix:* Name an owner per definition and a review trigger.

**Pitfall 4 — Reading labels instead of logic.**
*Symptom:* Definitions taken from column names or report titles. *Consequence:* You record
agreement that does not exist. *Fix:* Read the transformation. The mapping tab is the
definition; the title is marketing.

## References

**Related skills:** `inventory-reports` (stage 2, analytics), `scope-decision` (stage 4),
`spec-trust-requirements` (stage 5, analytics)

**Protocol:** `protocol/evidence.md`, `protocol/assumptions.md`

**Domain:** `domains/analytics/DOMAIN.md`

**Note on prior art:** Semantic-layer and metric-governance practice is widely established
in data engineering; the classification scheme here (aligned / reconcilable / legitimately
plural / undefined) is this framework's own convention.
