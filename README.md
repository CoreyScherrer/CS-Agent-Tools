# Work Environment Frameworks

_Instructions to pass to my work environment._

Two independent, portable frameworks. Neither depends on the other; install either
or both.

| | What it does |
|---|---|
| **[Memory Archive](#memory-archive-framework)** (`ma/`) | Persistent memory across AI coding sessions |
| **[Product Discovery](product-discovery/)** (`product-discovery/`) | Enterprise discovery → requirements → artifacts |
| **[Agent Skills](skills/)** (`skills/`) | Working discipline for AI coding sessions |

Both follow the same rule: **the framework is shareable, what it captures is not.**
See [Data Boundary](docs/wiki/Data-Boundary.md).

---

# Memory Archive Framework

Persistent memory for AI coding sessions. Captures decisions, learnings and
context into a local database and injects the relevant parts back at the start of
the next session.

Built for a machine whose capabilities you cannot verify in advance: it probes
the environment rather than assuming one, and its default path needs nothing
beyond Python 3.9+ from the standard library.

## Setup

```bash
git clone https://github.com/CoreyScherrer/kroger.git memory-archive
cd memory-archive

python3 -m ma doctor --write   # probe the machine, choose a backend
python3 -m ma init             # create schema, install the commit guard
python3 -m ma status           # confirm
```

`doctor` reports what it found and why it chose a backend. It prefers PostgreSQL
when the server is reachable, a driver is installed, and authentication works —
and otherwise uses SQLite, which is fully supported rather than a fallback of
last resort. `ma migrate --to postgres` moves the content later if the situation
changes.

## Daily use

```bash
# capture
python3 -m ma capture decision "Chose X over Y" "Y needs an approval we don't have" \
    --project myproject --link system:checkout --link person:Jane

# retrieve
python3 -m ma recall --project myproject
python3 -m ma search "timeout"
python3 -m ma context system:checkout
```

Memory types: `decision` · `learning` · `pattern` · `context` · `preference` ·
`question`

Entities: `person` · `system` · `item` (ticket/work item). They are created on
first mention, so capture never stalls to pre-register anything.

## How context reaches the model

Three layers, degrading gracefully:

1. **`SessionStart` hook** → runs `ma recall`, injects ranked context. Primary.
2. **`Stop` hook** → prompts for a session-end capture. Secondary.
3. **`CLAUDE.md` instruction** → tells the model to run `ma recall` if no
   `[Memory Archive]` banner appeared. The fallback that matters when hook
   behaviour differs between Claude Code surfaces.

The hook prints a distinctive banner so its *absence* is visible. Silent failure
is how "the archive stopped working" usually presents.

## The data boundary

**The framework is shareable. What it captures is not.**

Captured content is work product and stays on the machine that captured it. This
is enforced structurally, not by convention:

- `data/`, `*.db` and `config.local.json` are gitignored
- a pre-commit guard (installed by `ma init`) blocks them even from `git add -f`
- `ma export --redact` shares structure without content

Nothing in this framework makes an outbound network call. No summarization, no
embeddings, no telemetry — captured content does not leave the machine.

### Backup and cross-machine transfer

Git is the wrong tool for moving an archive — a database is a binary blob that
bloats history and cannot be removed once committed. Use export/import, which
produces plain text you can review before it lands:

```bash
python3 -m ma export --out ~/ma-backup.json   # source machine
python3 -m ma import ~/ma-backup.json         # target machine
```

Import is idempotent by id, so re-running it changes nothing. Memories,
entities and their links all survive the round trip. Move the file the way you
would move any work document.

## Ranking

With no embeddings, recall quality is this scoring function:

```text
score = importance × recency_decay × project_match
```

Pinned memories always lead. Selection fills to a token budget, skipping
oversized items so one long memory cannot crowd out everything below it. It is
deterministic: same inputs, same ordering, verifiable without a model.

## Storage

Two backends behind one seam, both running the same conformance suite:

| Aspect | SQLite | PostgreSQL |
| --- | --- | --- |
| dependency | none (stdlib) | `psycopg` |
| use when | anywhere | server available and permitted |
| shared access | single machine | multi-machine capable |

The schema uses only text, integer, real and JSON-encoded-as-text, so the same
DDL runs on both.

## Tests

```bash
python3 -m unittest discover -s tests -t .
```

Standard-library `unittest`; no test framework to install. PostgreSQL
conformance runs when `MA_TEST_POSTGRES_DSN` is set:

```bash
MA_TEST_POSTGRES_DSN="postgresql://user@localhost/ma_test" \
    python3 -m unittest discover -s tests -t .
```

## Configuration

Precedence, lowest to highest: built-in defaults → `config.example.json` →
`config.local.json` (gitignored, written by `doctor`) → environment variables
(`MA_BACKEND`, `MA_SQLITE_PATH`, `MA_POSTGRES_DSN`, `MA_AGENT_KEY`, `MA_PROJECT`,
`MA_TOKEN_BUDGET`).

Nothing about the host machine is hardcoded.

## Scope

Phase 1 is capture, retrieval and injection. Deliberately excluded — each
additive later rather than a refactor: semantic search, LLM summarization,
knowledge-graph edges, MCP server, background sync daemon, web UI, shared
multi-user deployment.

## Documentation

- **Wiki:** `docs/wiki/` — [Home](docs/wiki/Home.md) · [Setup](docs/wiki/Setup.md) ·
  [Daily Use](docs/wiki/Daily-Use.md) · [Data Boundary](docs/wiki/Data-Boundary.md) ·
  [Architecture](docs/wiki/Architecture.md) ·
  [Troubleshooting](docs/wiki/Troubleshooting.md) · [Roadmap](docs/wiki/Roadmap.md)
- **Setup on a restricted machine:** `docs/SETUP-NEW-MACHINE.md`
- **Design rationale:** `docs/specs/2026-08-07-memory-archive-framework-design.md`
- **Decisions:** `docs/decisions/ADR-0001-phase-1-scope-and-constraints.md`

`docs/wiki/` is the source of truth and is version-controlled with the code.
`scripts/publish-wiki.sh` copies it to the GitHub wiki (which must be
initialised once through the web UI first).

---

# Product Discovery Framework

_Masterful Product Swashbuckling_ — enterprise product discovery, from raw
organizational information to artifacts a team can build from.

Lives in [`product-discovery/`](product-discovery/). Self-contained plain files —
no install, no dependencies beyond Python 3 for the linters.

## What makes it different

Most PM template libraries help you fill in a document. The document then reads as
authoritative whether or not anything in it is true.

This one makes artifacts **evidence-bound by construction**: every material claim
either cites a source or is registered as an assumption with a validation path.
There is no third state where a number gets quietly invented and later quoted in a
steering deck as fact.

Four gates, at four layers, so no single failure is silent:

| Gate | Layer | Catches |
|---|---|---|
| Evidence citation | Authoring | Confident fiction |
| Assumption ledger | Cross-stage state | Silent guessing |
| Adversarial critic | Pre-ship review | Reasoning gaps |
| Structural lint | Scripts that exit nonzero | Placeholders, broken refs, decay |

## The spine

```
0 TRIAGE → 1 FRAME → 2 MINE → 3 DISCOVER → 4 DEFINE → 5 SPECIFY → 6 VALIDATE → 7 COMMUNICATE
```

Every project runs all seven; triage sets how heavy each one is. **MINE comes before
DISCOVER on purpose** — in an enterprise, most of what an interview would surface is
already written down, and stakeholder patience is the binding constraint.

25 core skills, 3 analytics-domain skills, 3 linters.

## Quickstart

```bash
cd product-discovery
scripts/new-project.sh my-initiative ~/projects/my-initiative
```

Then fill in `corpus.yaml`, run `frame-problem`, run `mine-corpus`, continue down
the spine. Validate at any point:

```bash
python3 scripts/lint-artifact.py ~/projects/my-initiative    # artifacts
python3 scripts/lint-evidence.py ~/projects/my-initiative    # findings + ledger
python3 scripts/lint-skill.py .                              # the framework itself
```

**Read [`product-discovery/examples/worked-example/`](product-discovery/examples/worked-example/)
first** — a complete FRAME + MINE pass that answers most format questions faster
than the protocol docs do.

## Data boundary

Project state — `evidence/`, `assumptions.md`, `artifacts/` — is **work product**
and never goes in this repo. Same rule as the memory archive. Projects live outside
the framework directory; `scripts/new-project.sh` scaffolds them elsewhere by design.

---

# Agent Skills

Portable working discipline for AI coding sessions, in [`skills/`](skills/). Independent of
both frameworks above — install either, both, or neither.

| Skill | Use when |
|---|---|
| [`session-memory-discipline`](skills/session-memory-discipline/) | Deciding what to record from a session so the next one starts informed |
| [`writing-durable-instructions`](skills/writing-durable-instructions/) | Adding or editing a standing rule an agent will follow across sessions |

Both encode the same underlying problem: **agent sessions are amnesiac, and the things
written down to fix that decay silently.** One covers what to record; the other covers how
to write rules that stay true as systems change.

## Install

```bash
cp -R skills/session-memory-discipline ~/.claude/skills/
cp -R skills/writing-durable-instructions ~/.claude/skills/
```

Restart Claude Code or start a new session. Confirm with `ls ~/.claude/skills/`.

For a single project rather than globally, use `<project>/.claude/skills/` instead.
