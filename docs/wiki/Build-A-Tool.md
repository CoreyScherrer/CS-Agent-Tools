# Build a Tool

_The agent and skill that turn something that works into a guide anyone can follow._

> Why, hello there, intrepid tool-smith! You've reached the workshop at the end of
> the library — the place where journeys are *made*. Hand this agent a thing that
> already works, or a history full of hard-won lessons, and it will mine, neutralise
> and write the next expedition to the very same standard as every page here.
> Marvellous, isn't it? The future, it turns out, writes its own instructions.

## 1. What this tool is

Two files in this repo:

- `agents/build-a-tool.md` — a Claude Code agent definition. Drop it in your
  `~/.claude/agents/` (or symlink the `agents/` directory) and it appears as a
  subagent you can start with "use build-a-tool to …".
- `skills/build-a-tool/SKILL.md` — the six-step process the agent follows:
  **frame → mine → neutralise → decide defaults → write → verify**. The skill is
  also usable on its own by any agent that reads skills.

Both point at [[Guide-Standard]], which is the contract every page in this wiki
meets. The agent's output is always files in this repo — a wiki page, a
`tools/<slug>/` directory with templates, and index rows — never a change to a
live system.

## 2. Who this is for, and what you need

For anyone who has built something with an AI agent and wants the next person
(or their own future self on a fresh machine) to get there without the detours.

- **Hardware:** none beyond the machine you run your agent on.
- **Accounts:** none. A memory archive of the source project helps enormously;
  this repo's [[Memory-Archive]] is the portable one.
- **Software:** Claude Code (or an agent that reads `SKILL.md` files); this repo
  cloned; `scripts/check-neutral.sh` runnable (bash + grep).

## 3. Setup time

| | Estimate |
|---|---|
| Human hands-on time | 5 minutes to install; 5 minutes per tool to answer the framing questions |
| AI agent working time | 1–3 hours per tool, mostly mining history |
| Elapsed | One session per tool |

## 4. Working with your AI agent on this guide

- Run the agent from the root of your clone of this repo, on a branch.
- Point it at the **source of truth**: the repo, memory archive, decision records
  and incident notes of the thing being turned into a tool. Read-only access is
  enough; it never needs to touch the live system.
- Expect it to delegate mining to read-only subagents and come back with a
  gotcha ledger before it writes a word of the guide.

## 5. The phases

### Phase 1 — Install

Agent steps:

1. `ln -s "$PWD/agents/build-a-tool.md" ~/.claude/agents/build-a-tool.md`
   (or copy it).
2. Start a new session; confirm `build-a-tool` is listed among available agents.

**Done when:** "use build-a-tool to list its steps" returns the six steps.

### Phase 2 — Frame

Human steps: answer three questions in one message —

1. What does the finished tool let a person do? (one sentence)
2. What is in scope this time, and what is explicitly out?
3. Which real system is the source of truth for how it works?

**Done when:** the agent has written the answers to a scratch file and named the
sources it will mine.

### Phase 3 — Mine, neutralise, write

Agent steps: the skill, steps 2–5. You are not needed until it reports.

**Done when:** the agent reports files written, the definition-of-done checklist,
what it could not verify, and the questions only you can answer.

### Phase 4 — Review and merge

Human steps:

1. Read the gotcha ledger. Every row should make you nod; a row that makes you
   frown is either wrong or not yet generic. Say which.
2. Answer the open questions (usually: anything paid, anything public).
3. Merge the branch. Then, from `main`, run `scripts/publish-wiki.sh` to push the
   wiki.

**Gotchas in this phase**

- *Publishing from a branch removed pages.* `publish-wiki.sh` replaces the whole
  GitHub wiki with `docs/wiki/`; a branch missing a page deletes it. Publish from
  `main` only.
- *Guide written from general knowledge reads fine and is wrong in six months.*
  The skill forbids unsourced lessons for this reason. If the agent cannot name a
  source for a gotcha, it is cut.

## 6. Gotcha ledger

| Symptom | Cause | Fix |
|---|---|---|
| Wiki page vanished after publish | Published from a branch missing it | Publish from `main` after merge |
| Guide contains the author's hostnames or paths | Mining copied, didn't neutralise | `scripts/check-neutral.sh` before review; use `example.com`, `your-mini`, `acme` |
| Steps are plausible but never happened | Lessons written from general knowledge | Every gotcha names a source or is cut |
| Model name in a standing instruction is stale | Version-bound identifiers in text | "the current mid-tier model" plus an env var |
| Narrator voice in commands and tables | Fun leaked out of the opener | Opener and lead-ins only |

## 7. Free vs paid

| Service | Free tier enough? | Our call |
|---|---|---|
| Claude Code / an agent subscription | A subscription is needed to run the agent at all | Whatever you already use to code with an agent; nothing extra for this tool |

## 8. Talking to the tool

"Use build-a-tool to turn `<thing>` into a tool. Source of truth is `<repo or
archive>`." Then answer the three framing questions. It reports back in the
format above.

## 9. Keeping it alive

- [ ] When [[Guide-Standard]] changes, re-read the skill; the agent reads the
  standard fresh each run, so the two only drift if the skill's steps contradict it.
- [ ] Once a year, run `scripts/check-neutral.sh` over the whole wiki — new
  placeholder conventions and new vendor domains need adding to its allowlist.
