# Assumption Protocol

The assumption ledger is the second half of the evidence protocol. Citation stops
invention; the ledger stops *silent* invention — the case where something is genuinely
unknown and gets quietly filled in anyway.

## The ledger

One file per project: `assumptions.md`. It persists across every stage. Artifacts link
to entries rather than restating them, so validating an assumption once updates its
meaning everywhere it was relied upon.

Entry format:

    ### A-007
    - **assumption:** Order volume peaks in week 1 of each month
    - **why_assumed:** No volume data in the corpus; the fulfillment lead mentioned it in passing
    - **impact_if_wrong:** high | medium | low
    - **what_it_affects:** capacity requirements in PRD section 4
    - **owner:** name of the person who can confirm this
    - **how_to_validate:** pull 6 months of order data from the warehouse; one query
    - **status:** open | validated | invalidated | accepted
    - **resolved_date:** (when status leaves `open`)
    - **resolution:** (what was learned, and the evidence ID if it became a finding)

## Impact ratings

`impact_if_wrong` is the field that earns the ledger its keep. It is not about how likely
the assumption is to be wrong — it is about what breaks if it is.

- **high** — a wrong answer invalidates the scope, the approach, or the business case
- **medium** — a wrong answer changes requirements or sequencing but not the decision to build
- **low** — a wrong answer changes a detail

**A high-impact open assumption blocks stage advancement past DEFINE.** You may proceed
through FRAME, MINE, and DISCOVER with them open — indeed you should expect to.

This bears emphasis, because the gate is easy to misread as a general prohibition. FRAME is
precisely where you discover you do not know what the status quo costs, and cost is
high-impact by definition. **Accumulating high-impact assumptions in early stages is the
framework working, not failing.** They are the agenda for DISCOVER.

What the gate forbids is carrying them *past* DEFINE, because scope decided over an
unvalidated high-impact assumption is not a decision — everything downstream inherits it
silently.

Three ways through the gate, in order of preference:

1. **Validate it.** Usually the right answer, and often cheaper than it looks. Writing
   `how_to_validate` frequently reveals the answer is already in hand.
2. **Reduce its impact** by narrowing scope so the assumption no longer sits under the
   whole business case.
3. **Accept it.** Set `status: accepted` with a named person accepting the risk, and state
   it in the artifact's Risks section.

Option 3 requires a human. **Claude may not accept a risk on someone's behalf** — if no
person has accepted it, the correct action is to stop and say the gate is blocking, naming
the assumptions and what each would take to validate. Surfacing that clearly is the
required output, not a failure to complete the work.

Run `scripts/lint-evidence.py` at any stage to see open high-impact assumptions before they
become a blocker.

## Lifecycle

Assumptions are created at any stage and resolved at any stage. Most are created in FRAME
and MINE (where you discover what you do not know) and resolved in DISCOVER (where you go
ask). Some survive to the end and ship as known risks — that is fine, as long as they ship
*visibly*.

When an assumption is validated, it becomes a finding. Add the evidence entry, cite it
from the artifacts that previously carried the assumption marker, and set the ledger entry
to `validated` with the evidence ID in `resolution`.

When an assumption is invalidated, do not just flip the status. Find every artifact that
relied on it and revise. `what_it_affects` exists precisely so this is mechanical rather
than a memory exercise.

## Anti-patterns

**Ledger as graveyard.** Assumptions get added and never revisited. Mitigation: every
artifact's frontmatter carries `open_assumptions` count, and the critic pass flags any
high-impact assumption older than the current stage.

**Assumption laundering.** Restating an assumption in a later artifact without its marker,
so it reads as established. The linter catches the missing marker; the critic catches the
subtler version where it is reworded into an unfalsifiable generality.

**Over-registration.** Logging every trivial unknown until the ledger is noise and nobody
reads it. If it does not affect a decision, it is not an assumption — it is a detail. Leave
it out.
