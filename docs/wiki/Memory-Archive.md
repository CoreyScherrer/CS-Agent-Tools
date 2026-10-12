# Memory Archive

Persistent memory for AI coding sessions on the machine you work from. Captures decisions,
learnings and context into a local database, and injects the relevant parts back
at the start of the next session.

**Start here:** [[Setup]] → [[Daily-Use]] → [[Data-Boundary]]

## Why this exists

Every Claude Code session starts from zero. In a new role that is expensive:
org knowledge, system ownership, the reason a decision went the way it did, the
constraint that cost you an afternoon — none of it survives to the next session,
and most of it was never in a repo to begin with.

This captures that knowledge deliberately and feeds it back automatically.

## The one rule

**The framework is shareable. What it captures is not.**

Captured content is work product. It stays on the machine that captured it —
never committed, never pushed, never pasted into an external service. This is
enforced by a pre-commit guard, not left to memory. See [[Data-Boundary]].

## Pages

| Page | What it covers |
|---|---|
| [[Setup]] | Standing it up on a new or restricted machine |
| [[Daily-Use]] | Capture and recall commands, what is worth capturing |
| [[Data-Boundary]] | What may leave the machine, and what may not |
| [[Architecture]] | How it is built and why |
| [[Troubleshooting]] | Symptoms, causes, fixes |
| [[Roadmap]] | What Phase 2 depends on |

## Current state

Phase 1: capture, retrieval, and session injection. Working and tested.

Deliberately absent — each additive later rather than a refactor: semantic
search, LLM summarization, knowledge-graph edges, MCP server, background sync
daemon, web UI, shared multi-user backend.

Nothing in this framework makes an outbound network call.
