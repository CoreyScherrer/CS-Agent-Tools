# CLAUDE.md — Memory Archive Framework

Guidance for Claude Code working in this repo. Read this first.

## What this is

A portable memory archive: it captures decisions, learnings and context from AI
coding sessions into a local database, and injects the relevant parts back at the
start of the next session. Built to run on a machine whose capabilities are
unknown in advance — no assumptions about installed databases, background
process permissions, or package availability.

## MANDATORY: load context at session start

A `SessionStart` hook should print a `[Memory Archive]` banner automatically.

**If no `[Memory Archive]` banner appeared in this session, the hook did not
fire.** Hook support varies between Claude Code surfaces, so do not assume it
worked. Run this yourself before doing anything else:

```bash
python3 -m ma recall --project "$PWD"
```

This fallback is the point: the archive is useless if context silently fails to
load, and silence is exactly how that failure presents.

## MANDATORY: the data boundary

**The framework is shareable. What it captures is not.**

Captured content is work product and stays on the machine that captured it.
Never commit, push, paste into an issue, or send to any external service:

- `data/` and any `*.db` file — the archive itself
- `config.local.json` — machine-local configuration
- Anything produced by `ma export` without `--redact`

A pre-commit guard (installed by `ma init`) blocks these. **Never bypass it with
`--no-verify` to commit content.** If the guard fires on real framework code,
move that file out of `data/` rather than overriding.

To share a pattern without content: `python3 -m ma export --redact`.

## Capturing

Capture when something would be expensive to rediscover — a decision and its
reasoning, a non-obvious constraint, who owns what, a gotcha that cost time.

```bash
python3 -m ma capture <type> "<title>" "<body>" [options]
```

Types: `decision` · `learning` · `pattern` · `context` · `preference` · `question`

Useful options:

- `--project <name>` — scopes recall
- `--link person:Jane` / `--link system:checkout` / `--link item:ABC-123`
  (repeatable; entities are created on first mention)
- `--importance 0.0-1.0` — drives ranking
- `--pin` — always surface first, regardless of age
- `--tags a,b,c`

Write titles that will make sense in three months to someone without this
session's context. Put the *why* in the body — the what is usually recoverable
from code, the why never is.

## Retrieving

```bash
python3 -m ma recall --project <name>     # ranked context within a token budget
python3 -m ma search "<term>"             # keyword search
python3 -m ma context system:checkout     # everything linked to one entity
python3 -m ma status                      # backend and counts
```

## Repo map

```
ma/
  config.py            layered config: defaults < example < local < env
  storage/
    schema.py          portable DDL (text/integer/real + JSON-as-text only)
    base.py            StorageBackend seam + shared SQL implementation
    sqlite_backend.py  always-available path (stdlib only)
    postgres_backend.py optional; driver imported lazily
  core/
    ranking.py         pure scoring: importance x recency x project match
    repository.py      validation, link resolution, recall assembly, export
    doctor.py          environment probes
  cli/main.py          argparse CLI
scripts/               session hooks + pre-commit guard
docs/specs/            design documents
tests/                 stdlib unittest
```

## Conventions

- **Standard library only on the default path.** A managed machine may not allow
  package installs. `psycopg` is optional and imported lazily; the test suite
  uses `unittest`, not pytest. Do not add a required third-party dependency.
- **No backend-specific SQL.** Text, integer, real, and JSON-encoded-as-text.
  Both backends run the same conformance suite in
  `tests/test_storage_conformance.py` — add cases to the mixin, not to one
  backend.
- **Core never imports a storage concrete.** The CLI never imports storage at
  all; the factory in `ma/storage/__init__.py` is the only place a backend is
  chosen.
- **No outbound network calls.** Phase 1 sends nothing anywhere: no
  summarization, no embeddings, no telemetry. Content stays on the machine. This
  is a data-handling requirement, not a preference.
- **Doctor probes never raise.** Every probe is wrapped; an unexpected
  environment must produce a report, not a traceback.
- **Timestamps are ISO-8601 UTC text** everywhere, for cross-backend portability.

## Gotchas

- **`ma init` is required after clone.** It creates the schema and installs the
  pre-commit guard. Cloning alone leaves the guard uninstalled — git hooks are
  not carried by a clone.
- **Relative paths resolve against the repo root, not your cwd** (see
  `config.resolve_path`). This keeps hooks working regardless of where a session
  starts.
- **`ma recall` ranks in Python, not SQL.** Scoring blends recency, importance
  and project match, so SQL ordering alone picks the wrong candidates. It pulls a
  wide pool and ranks in memory.
- **Postgres is preferred but never assumed.** `ma doctor` only selects it when
  the server is reachable *and* a driver is installed *and* authentication works.
  Anything less lands on SQLite, which is a fully supported destination.

## Don'ts

- Don't add an LLM call anywhere in Phase 1 — it changes the data-handling story.
- Don't hardcode absolute paths. Everything is derived or configured.
- Don't add a required dependency to the default path.
- Don't commit captured content. See the data boundary above.
