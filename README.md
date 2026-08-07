# Memory Archive Framework

Persistent memory for AI coding sessions. Captures decisions, learnings and
context into a local database and injects the relevant parts back at the start of
the next session.

Built for a machine whose capabilities you cannot verify in advance: it probes
the environment rather than assuming one, and its default path needs nothing
beyond Python 3.9+ from the standard library.

## Setup

```bash
git clone <this-repo> memory-archive
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

## Ranking

With no embeddings, recall quality is this scoring function:

```
score = importance × recency_decay × project_match
```

Pinned memories always lead. Selection fills to a token budget, skipping
oversized items so one long memory cannot crowd out everything below it. It is
deterministic: same inputs, same ordering, verifiable without a model.

## Storage

Two backends behind one seam, both running the same conformance suite:

| | SQLite | PostgreSQL |
|---|---|---|
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

Design rationale: `docs/specs/2026-08-07-memory-archive-framework-design.md`
