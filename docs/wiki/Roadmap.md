# Roadmap

## Phase 1 — done

Capture, retrieval, session injection.

- `doctor` environment probing, backend selection
- SQLite + PostgreSQL behind one seam
- Capture with typed memories, entity links, tags, pinning
- Deterministic ranking under a token budget
- Search and entity context
- Export / import for cross-machine transfer
- Session hooks with a documented fallback
- Structural data boundary

## Phase 2 — gated on real findings

Nothing here is decided. Each item depends on facts about the work machine that
could not be known when Phase 1 was built. **Run `ma doctor` there first** — its
output is the input to all of this.

### The four answers that decide everything

1. **Do hooks fire, and on which surface?** If yes, injection is solved and
   effort goes elsewhere. If no, that becomes the priority.
2. **Is PostgreSQL available?** Decides whether a shared team backend is even
   possible.
3. **Does package installation work?** Gates anything needing a dependency —
   most obviously embeddings.
4. **What does the company API framework allow?** Decides whether any
   LLM-assisted feature is on the table at all.

### Candidates

**Semantic search.** Embeddings would improve recall on a large archive. Needs
an embedding model — either a local one (requires package installs) or an API
call (requires answering the data-handling question). Both gated on answers 3
and 4.

*Meanwhile:* the deterministic ranking is adequate for hundreds of memories.
Revisit when recall quality actually degrades, not before.

**MCP server.** Would let Claude call `capture` and `recall` as tools rather
than shell commands. More natural, and removes the discipline problem. Depends
on whether the company API framework supports MCP transport.

**Transcript auto-capture.** A watcher parsing session transcripts would raise
capture rate a lot. Needs background-process permission and a stable transcript
layout — answer 1 territory. The riskiest item here.

**Shared team backend.** The stated eventual goal. Needs PostgreSQL (answer 2),
plus decisions about access control, whose memories are visible to whom, and
where a shared instance may be hosted. Do not start this before the single-user
version has proven itself.

**Decay and curation.** As the archive grows, stale memories need pruning.
`expires_at` exists but nothing acts on it yet. Wait until there is enough
content to see what actually goes stale.

## Explicitly not planned

- **Web UI.** The CLI plus session injection covers the real use. A UI is
  maintenance without a matching payoff.
- **Knowledge-graph edges.** The `links` table covers the realistic use;
  free-form edges are high-maintenance in practice.
- **Telemetry.** Nothing about how this is used leaves the machine.

## Principles that should survive Phase 2

Whatever gets built next, keep these:

1. **The default path stays dependency-free.** A required dependency is a single
   point of total failure on a managed machine.
2. **The data boundary holds.** Framework shareable, content not.
3. **Failures stay loud.** Silent degradation is how this class of tool dies.
4. **New capability is additive.** If a feature cannot be turned off and leave a
   working archive behind, it is designed wrong.
