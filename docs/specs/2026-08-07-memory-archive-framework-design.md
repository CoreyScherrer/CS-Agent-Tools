# Memory Archive Framework — Design

**Date:** 2026-08-07
**Status:** Approved (Phase 1)

## Problem

Starting work in a new enterprise environment means accumulating a large amount of
context — org knowledge, system architecture, decisions, ticket history — that is
expensive to reconstruct and easy to lose between AI coding sessions. An existing
personal memory archive solves this, but it is welded to its host machine:
hardcoded absolute paths, secrets symlinked to a specific filesystem location,
a hook that calls a personally-owned remote host, and OS-level background daemons.

None of those assumptions survive a move to a corporate-managed machine.

## Constraint that shapes everything: the environment is unknown

The target machine's capabilities have not been verified and cannot be verified
from the authoring machine. It is not known whether a database server can be
installed, whether background processes can be registered, whether package
installs reach an index, or whether editor hooks fire the same way.

The framework's first job is therefore to **discover its environment**, not to
assume one. This is the central design principle and the reason for the storage
abstraction, the zero-dependency default path, and the `doctor` command.

## Non-goals (Phase 1)

Deliberately excluded, each additive later rather than a refactor:

- Vector embeddings / semantic search
- Any outbound LLM call (summarization, extraction, enrichment)
- Knowledge-graph edge modelling
- MCP server
- Background sync daemon
- Web UI
- Multi-user / shared server deployment

## Architecture

Four layers. The storage boundary is the key seam; everything above it is
written once and is backend-agnostic.

```
Injection    .claude/settings.json hooks + CLAUDE.md fallback
Interface    ma  (doctor init capture recall search context export migrate status)
Core         models · repository · ranking · redaction
Storage      StorageBackend ─┬─ SQLiteBackend (stdlib, always available)
                             └─ PostgresBackend (optional, if environment allows)
```

**Dependency rule.** Core never imports a storage concrete. CLI never imports
storage at all. Config resolves the backend once at startup and injects it.

**Zero required third-party dependencies.** The SQLite path is pure standard
library on Python 3.9+. `psycopg` is an optional extra. This matters because
package installation may be restricted or proxied on a managed machine.

**Rationale.** The injection layer is the outermost ring because it is the layer
most likely to behave differently under an editor extension. If it fails, the CLI
still works — the user loses convenience, not data.

## Data model

Five tables. `memories` is the spine; three thin entity tables link through one
join table.

### memories

| column | type | notes |
|---|---|---|
| id | text | UUID, portable across backends |
| type | text | decision, learning, pattern, context, preference, question |
| title | text | short, human-scannable |
| body | text | content |
| project | text | repo or workstream, scopes recall |
| importance | real | 0.0–1.0, drives ranking under a token budget |
| tags | text | JSON array as text — no array-type dependency |
| source | text | manual, session-sweep, import — provenance for trust-ranking |
| agent_key | text | who wrote it |
| session_id | text | groups memories from one working session |
| created_at | text | ISO-8601 |
| updated_at | text | ISO-8601 |
| expires_at | text | nullable, for deliberately temporary context |

### people

name, role, team, aliases (JSON text), notes, timestamps.
Highest-value table in a new role: org knowledge cannot be reconstructed from code.

### systems

name, purpose, owner (nullable → people.id), notes, links (JSON text), timestamps.

### work_items

external_ref (ticket key), title, status, notes, timestamps.

### links

`(memory_id, entity_type, entity_id)`. One join table rather than three foreign
keys keeps the schema flat and lets a single memory touch a person, a system, and
a ticket at once. This is what makes recall useful: querying a system returns
memories linked to it *plus* the people who own it.

**Portability rule.** No backend-specific types. Text, integer, real, and
JSON-encoded-as-text only. The same DDL runs on both backends with a single
dialect substitution.

**Omitted deliberately.** No embedding column (absent rather than dangling; adding
it later is a one-line migration). No KG edge table — `links` covers the realistic
use and edge tending has historically been high-maintenance.

## Environment discovery (`ma doctor`)

Interrogates the machine and writes findings to gitignored local config. Probes:

- **Python** — version; venv creation; whether pip reaches an index.
- **Postgres** — three separate checks: server present, connectable, may create a
  database. "psql exists" does not imply "you may create a DB".
- **Filesystem** — where writes actually succeed; whether the chosen data
  directory sits inside a synced/roaming folder.
- **Editor surface** — whether hooks fire, and where session transcripts live.
  Tested empirically rather than assumed.
- **Egress** — whether outbound network calls succeed. Reported only; Phase 1
  makes no external calls regardless of the result.
- **Git** — remote reachability.

**Robustness requirements.** Every probe is independently skippable. Failure of
any single probe never aborts the run. A doctor that crashes on an unexpected
environment is worse than no doctor.

**Backend selection.** Postgres is preferred when *genuinely usable* (all three
checks pass). Otherwise the framework silently lands on SQLite and reports what an
upgrade would require. The failure mode being designed against is spending the
first working session fighting a database install instead of capturing work.

## Data boundary

Enforced structurally, not by convention:

- `data/` and `*.db` gitignored; config split into committed `config.example.json`
  and gitignored `config.local.json`.
- A git **pre-commit hook**, installed by `ma init`, blocks committing the database
  or anything under `data/`.
- `ma export --redact` for sharing a pattern without the content.
- README and CLAUDE.md state the rule plainly.

**The rule:** the framework is shareable; captured content is not. The framework
repo contains zero work content by construction.

## Recall ranking

With no embeddings, ranking must be good on its own:

```
score = importance × recency_decay × project_match_boost
```

Pinned instructions always sort first, then fill to the token budget. Deterministic
— same inputs produce the same output — which makes it verifiable without an LLM in
the loop.

## Injection, with graceful degradation

1. `SessionStart` hook → `ma recall` → context injected. **Primary.**
2. `Stop` hook → session-end sweep. **Secondary.**
3. `CLAUDE.md` instruction to run `ma recall` when no context banner is present.
   **Fallback** for environments where editor hooks behave differently.

The hook prints a distinctive banner so its *absence* is visible. Silent failure is
the known root cause of context not reaching the model.

## Testing

Standard-library `unittest`; no test-framework dependency.

- Both storage backends run the same conformance suite.
- Ranking is pure-function tested.
- Doctor probes are individually mockable; a probe raising must not fail the run.

## Risks

| Risk | Mitigation |
|---|---|
| Editor hooks don't fire in the target environment | CLAUDE.md fallback; doctor tests hooks empirically |
| Postgres unavailable or restricted | SQLite default is always viable; migrate later |
| Schema wrong for the actual domain | Thin entity tables; `export` prevents lock-in |
| Work content committed to a shared remote | Pre-commit guard + gitignore + documented rule |
| Package installs blocked | Zero required third-party dependencies |

## Phase 2 candidates

Decided after `doctor` reports real findings from the target machine: semantic
search, MCP server, session-transcript auto-capture, shared/team backend.
