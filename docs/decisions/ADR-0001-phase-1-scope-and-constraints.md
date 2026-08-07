# ADR-0001 — Phase 1 scope and constraints

**Date:** 2026-08-07
**Status:** Accepted

## Context

An existing personal memory archive works well but is welded to its host: absolute
paths, secrets symlinked to a fixed location, a hook calling a personally-owned
remote, OS-level daemons. The target is a new corporate-managed machine whose
capabilities cannot be verified in advance — a Claude Code VS Code integration
running against a company API framework, with no account login.

The operative constraint, stated by the owner: *"I only know that I do not know
anything."*

## Decisions

### 1. Discover the environment; do not assume one

`ma doctor` probes Python, pip, PostgreSQL, filesystem, editor surface, hooks,
egress and git, then selects a backend. Probes are read-only and individually
wrapped: a probe that raises becomes a warning, never a crash.

*Why:* every alternative requires knowing something about the machine that is not
knowable from here. A doctor that crashes on a surprising environment is worse
than no doctor.

### 2. Two backends behind one seam; SQLite always viable

PostgreSQL is preferred, but only when the server is reachable *and* a driver is
installed *and* authentication succeeds. Anything less lands on SQLite.

*Why:* the requested preference order was Postgres-first, but the failure mode to
avoid is spending a first working day fighting a database install instead of
capturing work. Preference is honoured; the failure mode is removed.

### 3. Zero required third-party dependencies on the default path

Standard library only; `psycopg` optional and lazily imported; tests use
`unittest`.

*Why:* package installation may be restricted or proxied on a managed machine. A
required dependency is a single point of total failure.

### 4. No outbound network calls in Phase 1

No summarization, no embeddings, no telemetry. Search is keyword-based; ranking
is a deterministic scoring function.

*Why:* captured content is employer work product. Sending it anywhere is a
data-handling decision that cannot be made responsibly before the company's API
framework and policies are understood. Deferring costs only semantic search.

### 5. Explicit capture plus a session-end prompt

No transcript-parsing daemon. The `Stop` hook prompts; it does not extract.

*Why:* auto-extraction needs either an LLM call (rejected, see 4) or transcript
parsing that depends on file layout and background-process permissions — the two
things least likely to hold on the target machine.

### 6. Three-layer injection with a documented fallback

`SessionStart` hook (primary), `Stop` hook (secondary), CLAUDE.md instruction
(fallback). The hook prints a distinctive banner so its absence is visible.

*Why:* hook behaviour varies across Claude Code surfaces and cannot be verified
remotely. Silent failure is the known way this class of system stops working.

### 7. The data boundary is structural

Framework is shareable; captured content is not. Enforced by gitignore, a
pre-commit guard installed by `ma init` (which catches `git add -f`, unlike
gitignore alone), and `export --redact`.

*Why:* the framework is intended for a personal remote while the content is
employer work product. A convention would eventually be forgotten; a guard on
the machine holding the content will not be.

### 8. Generic memories plus three thin entity tables

`memories` + `people` + `systems` + `work_items`, joined through one `links`
table.

*Why:* the generic core mirrors what the existing archive converged on after real
use. The three entity types were chosen deliberately: in a new role, org
knowledge is the sharpest pain and the least recoverable from code. One join
table rather than three foreign keys keeps the schema flat and lets a memory
touch a person, a system and a ticket at once.

## Consequences

- Works on a machine nobody has inspected, including a heavily restricted one.
- No semantic search until Phase 2 — ranking quality rests entirely on the
  scoring function.
- Capture depends on discipline; the session-end prompt mitigates but does not
  remove this.
- Postgres migration is available but untested against a real server; the
  conformance suite runs against PostgreSQL when `MA_TEST_POSTGRES_DSN` is set.

## Phase 2 inputs

Decided only after `ma doctor` reports from the real machine: semantic search,
MCP server, transcript auto-capture, shared team backend.
