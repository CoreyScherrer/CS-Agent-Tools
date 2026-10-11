---
name: build-a-tool
description: Turn a working setup, a project history, or an idea into a portable tool guide in this repo — mined for real gotchas, neutral of any one person's infrastructure, written to docs/GUIDE-STANDARD.md. Use when someone says "make this a tool", "write the guide for X", "add X to CS-Agent-Tools", or opens the build-a-tool agent.
---

# Build a Tool

A "tool" in this repo is a guide plus templates that let a stranger and their AI
agent reproduce something that already works somewhere. The value is not the
steps — any model can list steps. The value is the **decisions with defaults** and
the **gotchas that actually happened**. This skill is how to harvest both.

**The core rule: nothing goes in a guide that was not either observed in a real
history or verified against current vendor documentation. Guessing is how guides
rot.**

## When to use

- A setup exists (a server, a bot, a pipeline) and should become reproducible.
- A project's history (memories, decision records, PRs, incident notes) holds
  lessons nobody has written down generically.
- A new guide is requested for something not yet built; then the output is a
  guide **draft** marked as unverified, and the build itself follows it.

## The six steps

### 1. Frame (with the human, five minutes)

Ask only what you cannot find:

- One sentence: what does the finished tool let a person do?
- What is in scope and what is explicitly left out this time?
- Which real system is the source of truth for "how it actually works"?

Write the answers at the top of a scratch file. Do not start mining without them.

### 2. Mine the history

Sources, in order of signal:

1. **Memory archives** — `python3 -m ma search "<topic>"` in this repo's MA, or
   whatever archive the source project uses. Search for symptoms, not features:
   `fail`, `silent`, `gotcha`, `broke`, `took hours`, `turned out`.
2. **Decision records and rulings** — `docs/decisions/`, `docs/adr/`,
   `docs/operator/` or equivalents in the source project.
3. **Incident and fix commits** — `git log --grep=fix --grep=gotcha --grep=broke
   -i` in the source repo, and PR descriptions.
4. **The code's own comments** — grep for `NOTE`, `gotcha`, `workaround`,
   `because`.
5. **Current vendor docs** — only to confirm that a free tier, a scope name, a
   setting still exists today. Record the date checked.

Delegate the mining to read-only subagents when there is more than one source
system; give each a source list and ask for a **gotcha ledger** in the standard
format (symptom / cause / generic fix / source path). Mining is the slow step —
budget most of the session for it.

### 3. Neutralise

Every gotcha and every step is rewritten so that it is true for anyone:

- Hostnames → `example.com`, `your-mini`, `hooks.example.com`.
- People, handles, companies → roles ("the workspace admin", "the tenant").
- Paths under a home directory → `/opt/<tool>`, `/etc/<tool>`, `$STATE_DIR`.
- Model IDs in standing text → "the current mid-tier model" plus an env var.
- A number that was specific (port 5017) → a placeholder with a sensible default.

Then run the neutrality grep in `scripts/check-neutral.sh` and fix every hit.
A gotcha that cannot be made generic is not a gotcha, it is a diary entry; drop it.

### 4. Decide the defaults

For each decision point found in mining, write the options table from
`docs/GUIDE-STANDARD.md` §6 and **mark a default**. The default is the choice that
the source history shows worked, unless current docs show it is gone. Where the
history shows a choice that was later reversed, the reversal is the default and
the original is a gotcha.

Free vs paid: default to free; recommend paid only where a specific step in the
guide is blocked on the free tier, and name the step.

### 5. Write

Write `docs/wiki/<Tool-Name>.md` to the ten sections of `docs/GUIDE-STANDARD.md`,
in order. Write the opener last — it is the easiest part and the most fun, and
writing it first tempts you to skip the ledger. Then:

- `tools/<tool-slug>/README.md` — one paragraph and a link to the wiki page.
- `tools/<tool-slug>/templates/` — every config file the guide tells the agent to
  "copy and fill in", with comments that repeat the relevant gotcha at the line
  it protects against.
- Add a row to `docs/wiki/Home.md` and the root `README.md`.

Reuse, do not re-explain: if a phase is another tool's whole guide (the web
server under the Slack bot), link to that page and state only the delta.

### 6. Verify

- [ ] Definition of done in `docs/GUIDE-STANDARD.md` — every box.
- [ ] `scripts/check-neutral.sh docs/wiki/<Tool-Name>.md tools/<tool-slug>` is clean.
- [ ] Every "Done when" is a command or observation an agent can execute.
- [ ] A second model (or a fresh session with no context) reads only the guide
  and lists what it would still have to guess. Fix those gaps.
- [ ] If the tool was built from the guide rather than mined from a working
  system, the page carries `**Status:** draft — not yet built from this page` until
  someone has.

## Skills to reach for while building

These exist on most Claude Code installs; invoke them rather than re-deriving:

| Need | Skill |
|---|---|
| Clarify intent before writing | `superpowers:brainstorming` |
| Multi-step plan from a spec | `superpowers:writing-plans` |
| Author or lint a SKILL.md | `superpowers:writing-skills`, `skill-creator` |
| Wrap an API as an MCP server | `mcp-builder`, `mcp-server-dev:build-mcp-server` |
| Slack app scaffolding and CLI | `slack:create-slack-app`, `slack:slack-cli` |
| Cloudflare Tunnel / Access / Zero Trust | `cloudflare:cloudflare-one` |
| Recommend hooks/agents for a codebase | `claude-code-setup:claude-automation-recommender` |
| Durable standing instructions | `writing-durable-instructions` (this repo) |

## What not to do

- Don't write steps from general knowledge and label them as lessons.
- Don't include a gotcha without its symptom; a fix with no symptom is unfindable.
- Don't put the narrator's voice anywhere but the opener and section lead-ins.
- Don't let the author's infrastructure leak in as "the example". Use `acme`,
  `example.com`, `you`.
- Don't publish the wiki from a branch; `scripts/publish-wiki.sh` replaces the
  whole wiki with `docs/wiki/`, so publish from `main` after merge.
