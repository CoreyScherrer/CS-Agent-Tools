# Architecture

## Shape

Four layers. The storage boundary is the key seam; everything above it is
written once and does not care which backend it got.

```
Injection    hooks (SessionStart, Stop) + CLAUDE.md fallback
Interface    ma  (doctor init capture recall search context export import migrate status)
Core         ranking · repository · doctor
Storage      StorageBackend ─┬─ SQLiteBackend    (stdlib, always available)
                             └─ PostgresBackend  (optional, if permitted)
```

**Dependency rule.** Core never imports a storage concrete. The CLI never
imports storage at all — the factory in `ma/storage/__init__.py` is the only
place a backend is chosen.

**Injection is the outermost ring** because it is the layer most likely to
behave differently under an editor extension. If it fails the CLI still works:
you lose convenience, not data.

## Repo map

```
ma/
  config.py             layered config: defaults < example < local < env
  storage/
    schema.py           portable DDL
    base.py             seam + shared SQL implementation
    sqlite_backend.py   always-available path
    postgres_backend.py optional; driver imported lazily
  core/
    ranking.py          pure scoring functions
    repository.py       validation, links, recall assembly, export/import
    doctor.py           environment probes
  cli/main.py           argparse CLI
scripts/                session hooks + pre-commit guard
docs/wiki/              this wiki
tests/                  stdlib unittest
```

## Data model

Five tables. `memories` is the spine; three thin entity tables join through one
`links` table.

**memories** — id, type, title, body, project, importance, tags, source,
agent_key, session_id, pinned, created_at, updated_at, expires_at

**people** — name, role, team, aliases, notes
**systems** — name, purpose, owner_id, notes, links
**work_items** — external_ref, title, status, notes

**links** — `(memory_id, entity_type, entity_id)`

One join table rather than three foreign keys keeps the schema flat, lets a
single memory touch a person *and* a system *and* a ticket, and means a new
entity type costs no schema change. It is also what makes `ma context` useful:
querying a system returns its memories plus the people linked to them.

**Portability rule.** Text, integer, real, and JSON-encoded-as-text only. No
backend-specific types anywhere, so the same DDL runs on both backends with a
single placeholder substitution.

## Design decisions

Full rationale in `docs/decisions/ADR-0001`.

### Discover the environment, do not assume one

The target machine's capabilities could not be verified in advance. So `doctor`
probes rather than assuming, every probe is wrapped, and a failing probe becomes
a warning instead of a crash. A doctor that dies on a surprising machine is
worse than no doctor.

### SQLite is always viable

PostgreSQL is preferred, but only when the server is reachable **and** a driver
is installed **and** authentication works. Anything less lands on SQLite.

The failure mode being designed against: spending a first working day fighting a
database install instead of capturing work.

### Zero required third-party dependencies

Standard library only on the default path. `psycopg` is optional and imported
lazily; tests use `unittest`. Package installation may be restricted on a
managed machine, and a required dependency is a single point of total failure.

### No outbound network calls

No summarization, no embeddings, no telemetry. Captured content is employer work
product; sending it anywhere is a decision that cannot be made responsibly before
the company's API framework and policies are understood.

The cost is semantic search. That is a Phase 2 conversation.

### Explicit capture, not a daemon

The `Stop` hook prompts; it does not extract. Auto-extraction needs either an
LLM call (rejected above) or transcript parsing that depends on file layout and
background-process permissions — the two things least likely to hold on the
target machine.

### Three-layer injection

`SessionStart` hook (primary), `Stop` hook (secondary), `CLAUDE.md` instruction
(fallback). The hook prints a distinctive banner so its *absence* is visible.
Silent failure is how this class of system stops working without anyone noticing.

## Testing

```bash
python3 -m unittest discover -s tests -t .
```

Standard-library `unittest`, no framework to install.

- Both backends run the same conformance suite — add cases to the mixin, not to
  one backend
- Ranking is pure-function tested with a frozen clock
- Doctor probes are tested for resilience: a raising probe must not fail the run
- Export/import round-trip is tested, because it is the migration path

PostgreSQL conformance runs when a DSN is provided:

```bash
MA_TEST_POSTGRES_DSN="postgresql://user@localhost/ma_test" \
    python3 -m unittest discover -s tests -t .
```

## Configuration

Precedence, lowest to highest:

1. Built-in defaults (`ma/config.py`)
2. `config.example.json` (committed)
3. `config.local.json` (gitignored, written by `doctor`)
4. Environment: `MA_BACKEND`, `MA_SQLITE_PATH`, `MA_POSTGRES_DSN`,
   `MA_AGENT_KEY`, `MA_PROJECT`, `MA_TOKEN_BUDGET`

Nothing about the host machine is hardcoded. Relative paths resolve against the
repo root rather than the caller's cwd, which is what keeps hooks working
regardless of where a session starts.
