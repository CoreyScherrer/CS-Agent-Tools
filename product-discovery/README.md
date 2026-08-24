# Masterful Product Swashbuckling

_An enterprise product discovery framework. Evidence in, artifacts out._

Most product documents are written from memory and vibes. They read as authoritative,
and no reader can tell which parts are grounded and which were invented on the way to
the deadline. This framework exists to make that distinction visible and enforced.

**The core rule: every material claim is either cited or registered as an assumption.
There is no third state.**

## The spine

Seven stages. Every project runs all seven; a triage step sets how heavy each one is.
Stages are never skipped — that is how teams build the wrong thing quickly.

```
0. TRIAGE      → size the work, set stage depth
1. FRAME       → the problem, the outcome, who decides
2. MINE        → harvest what the org already knows
3. DISCOVER    → fill only the gaps mining could not
4. DEFINE      → opportunities, scope, non-goals
5. SPECIFY     → requirements, acceptance criteria
6. VALIDATE    → cheap tests before expensive builds
7. COMMUNICATE → artifacts shaped per audience
```

Two orderings here are deliberate departures from conventional discovery.

**MINE comes before DISCOVER.** In an enterprise, most of what you would ask in an
interview is already written down — in a ticket, a runbook, or a report that encodes a
requirement someone gathered years ago. Interviewing people to learn what a document says
spends your scarcest resource, stakeholder patience, on information you could have read.
Mine first, then interview only the gaps, and interview better for arriving informed.

**VALIDATE follows SPECIFY.** You validate the specified thing, and results feed back.
It is a loop, not a gate you pass once.

## The four gates

Artifact quality is enforced at four independent layers, so no single failure is silent.

| Gate | Layer | Catches |
|---|---|---|
| Evidence citation | Authoring | Confident fiction |
| Assumption ledger | Cross-stage state | Silent guessing |
| Adversarial critic | Pre-ship review | Gaps, weak reasoning |
| Structural lint | Two scripts, exit nonzero | Placeholders, broken refs, malformed evidence, ledger decay |

The linter matters most when this is handed to someone else. It is the only gate that does
not depend on a model behaving well.

## Quickstart

```bash
cp -r project-template/ ~/projects/my-initiative/
cd ~/projects/my-initiative/
# describe your available sources
$EDITOR corpus.yaml
```

Then, in Claude Code, work the stages in order. Start with `frame-problem`.

Or scaffold it in one step:

```bash
scripts/new-project.sh my-initiative ~/projects/my-initiative
```

Validate at any point — run **both**:

```bash
python3 scripts/lint-artifact.py ~/projects/my-initiative/   # artifacts
python3 scripts/lint-evidence.py ~/projects/my-initiative/   # findings + ledger
python3 scripts/lint-skill.py .                              # the framework itself
```

The second checks the two files everything else derives from, and is where you see
high-impact assumptions accumulating before they block DEFINE.

**Read `examples/worked-example/` first.** A complete FRAME + MINE pass on a realistic
scenario — it answers most format questions faster than the protocol docs do.

## Layout

```
protocol/          rules every skill obeys — read these first
skills/            the depth behind each stage — 25 core skills
scripts/           the mechanical gate — three linters plus the project scaffold
examples/          a complete worked example; read this first
project-template/  copied per engagement
domains/           optional domain packs — analytics/ ships with 3 skills
```

## The data boundary

**The framework is shareable. What it captures is not.**

`evidence/` holds material mined from internal systems — tickets, documents, threads,
existing reports. That is work product and stays where it was captured. Never commit an
`evidence/` directory, an `assumptions.md`, or a filled `artifacts/` directory from a real
engagement to a repository that leaves your control.

Run projects outside this repo. `project-template/` is a template; copy it elsewhere.

## Status

Vertical slice. The protocol layer, the linter, and four skills are complete
(`frame-problem`, `mine-corpus`, `write-prd`, `critique-artifact`) — enough to run
frame → mine → specify → critique end to end. Remaining skills are scaffolded, not written.

## On sources

Frameworks referenced here are cited to their originators in each skill's References
section — Christensen and Ulwick on jobs-to-be-done, Torres on continuous discovery and
opportunity mapping, Patton on story mapping, Moore on positioning, MITRE on problem
framing, North on behaviour-driven acceptance criteria. This repository contains no text
copied from third-party skill libraries.

## The skills

Twenty-five core skills, three analytics-domain skills. Every one writes an artifact to
disk with provenance, and every one is checked by `scripts/lint-skill.py`.

| Stage | Skills |
|---|---|
| 0 Triage | `size-the-voyage` |
| 1 Frame | `frame-problem` · `define-outcomes` · `map-stakeholders` |
| 2 Mine | `build-corpus-manifest` · `mine-corpus` · `inventory-existing-artifacts` · `synthesize-evidence` |
| 3 Discover | `identify-gaps` · `prep-interviews` · `synthesize-research` |
| 4 Define | `map-opportunities` · `define-users` · `scope-decision` · `prioritize` |
| 5 Specify | `write-prd` · `write-stories` · `define-acceptance` · `map-journey` |
| 6 Validate | `design-probe` · `assess-risk` |
| 7 Communicate | `exec-brief` · `stakeholder-update` · `decision-record` |
| Any | `critique-artifact` |
| Analytics domain | `inventory-reports` · `govern-definitions` · `spec-trust-requirements` |

Three skills carry the framework's weight and are worth reading first:

- **`identify-gaps`** — the hinge. Converts "what the corpus could not answer" into a
  prioritized agenda, and routinely finds that a gap is answerable from material already
  mined but unread. Without it, MINE-before-DISCOVER pays nothing.
- **`scope-decision`** — the gate. Checks for open high-impact assumptions before scope is
  set, because everything downstream inherits them.
- **`critique-artifact`** — the adversarial pass. Reads artifacts as the most skeptical
  person who will see them.
