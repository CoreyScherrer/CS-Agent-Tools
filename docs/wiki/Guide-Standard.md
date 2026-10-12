# Guide Standard

_How every tool guide in this repo is written. The build-a-tool agent follows this
page; a human adding a guide by hand follows it too._

A guide here is a set of instructions a person and their AI coding agent work
through **together**. The human makes the decisions and does the few things only a
human can do (sign up for an account, click "Approve" in a dashboard, plug in a
cable). The agent does everything else. The guide is written so that neither has
to guess what the other is doing.

**The core rule: a guide names every decision point, gives a recommended default,
and never leaves out a gotcha that cost someone an afternoon.**

## What a guide is for

- A stranger with no context picks it up, hands it to their AI agent, and ends up
  with a working tool.
- Nothing in it is specific to the author's machines, accounts, hostnames, people
  or paths. Examples use the placeholder domain `example.com`, the placeholder
  host `your-mini`, and the placeholder user `you`.
- It says what is free and what costs money, and recommends the free tier wherever
  the free tier is enough.

## Required sections, in this order

Every guide has these headings. Order matters: a reader decides whether to start
(1–4) before they are asked to do anything (5 onward).

### 1. The opener

One short paragraph in the voice of a sunny 1950s newsreel narrator: future-forward,
cheerful, slightly over the top. It names the tool and promises the journey. Each
guide gets its own variation on the theme; the shape is:

> Why, hello there! I see you've wandered into your next journey through the
> wonderful world of Artificial Intelligence and its many marvellous capabilities.
> On this particular expedition we'll guide you, step by confident step, through the
> choices and considerations that make **[Project Name]** a whimsical success — one
> that will delight, inspire, and very possibly impress the neighbours.

Keep the narration **in the opener and section lead-ins only**. Commands, tables,
checklists and gotchas are written plainly. (Same rule as the product-discovery
framework: theme in the framework's voice, out of the deliverables.)

### 2. What this tool is

Three to six sentences. What it does, what you end up with, what it is *not*.

### 3. Who this is for, and what you need

Three lists, each item one line:

- **Hardware** — exact enough to shop from (e.g. "any Apple-silicon Mac mini, 16 GB
  or more"), with a note on what is optional.
- **Accounts and services** — every account the reader will create, with the
  free-vs-paid call (see §Free vs paid below).
- **Software and tools** — what gets installed, by whom (human or agent).

### 4. Setup time

Two numbers, stated honestly, plus what drives them:

| | Estimate |
|---|---|
| Human hands-on time | e.g. 2–3 hours, mostly dashboards and waiting for DNS |
| AI agent working time | e.g. 4–6 hours across several sessions |
| Elapsed (calendar) | e.g. a weekend; DNS and account approvals add waiting |

Say which steps block on a human (approvals, physical cabling, OAuth consent).

### 5. Working with your AI agent on this guide

A short, standard block (copy it; adjust only the specifics):

- **Where to run the agent.** A coding agent in a terminal or IDE (Claude Code in
  VS Code or Cursor, or similar) does the file and shell work. Run it **on the
  machine being set up**, or over SSH/Remote-SSH into it, so paths and services are
  real.
- **Give it a browser.** Several steps happen in web dashboards (DNS, tunnels,
  OAuth consent screens, Slack app config). Let the agent drive those too:
  Claude Desktop with the Chrome extension or its built-in browser, or the
  Chrome extension from Claude Code. The agent fills the forms; you click the
  final "Approve" and paste back any secret it cannot see.
- **Secrets never go through chat.** When a step produces a token or key, the
  agent tells you which file to paste it into; you paste it there yourself.
  Anything pasted into a chat window should be treated as leaked and rotated.
- **Set up a way to talk to the result.** Every guide ends with the tool
  reachable from where you already are — a Slack channel, a chat window, an MCP
  connection, or a URL — so you are not opening a terminal to use it.

### 6. The phases

Numbered phases, each with:

- **Goal** — one line.
- **Decisions** — each decision point as a small table: option, when to pick it,
  cost, our default. The default is marked.
- **Human steps** and **Agent steps**, as two short checklists.
- **Done when** — a verifiable check (a command, a URL that returns 200, a
  message that arrives).
- **Gotchas in this phase** — see the format below.

Phases are ordered so that nothing later needs to be redone because of a choice
made earlier. If a phase is optional, say so in its heading.

### 7. Gotcha ledger

A table at the end collecting every gotcha from the phases, plus any that do not
belong to one phase. Format:

| Symptom | Cause | Fix |
|---|---|---|
| What you see | Why it happens | What to do instead, generically |

Rules for gotchas:

- It must have actually happened to someone. No hypotheticals.
- The fix is generic: no author hostnames, paths, or account names.
- If the gotcha is "this is not possible on the free tier", say so in §Free vs paid
  as well.

### 8. Free vs paid

One table of every account or subscription the guide touches:

| Service | Free tier enough? | What paid adds | Our call |
|---|---|---|---|

Default to free. Recommend paying only when the free tier blocks a step in the
guide, and say which step.

### 9. Talking to the tool

How the reader uses the result day to day, and how their AI agent connects to it
(MCP, API, CLI, Slack). This is the "you are done" section.

### 10. Keeping it alive

What breaks over time (OS updates, expiring tokens, certificate rotation) and the
small routine that prevents it. One checklist.

## Neutrality rules (enforced by review)

- No real hostnames, IPs, tailnet names, account handles, email addresses, people,
  company names, or filesystem paths under a real home directory.
- No version-bound model names in standing instructions ("use the current
  mid-tier model" rather than a model ID that will be stale in six months).
- No "always" without a trigger. Every instruction says WHO, WHEN, WHAT, WHY
  (see `skills/writing-durable-instructions` in the repo).
- Secrets are referenced by the file they live in, never by value, never by
  example value that looks real.

## Where a tool lives in this repo

```
tools/<tool-slug>/
  README.md          # one paragraph + link to the wiki page
  templates/         # config files the agent copies and fills in (optional)
  checklists/        # printable human-step checklists (optional)
docs/wiki/<Tool-Name>.md   # the guide itself (this wiki); flat file, Title-Case-Hyphenated
```

The wiki is flat and `scripts/publish-wiki.sh` publishes `docs/wiki/*.md` as the
whole GitHub wiki, so each guide is one top-level page, linked from `Home.md`.

## Definition of done for a guide

- [ ] All ten sections present, in order.
- [ ] Opener is in the narrator's voice; nothing else is.
- [ ] Every decision point has a marked default.
- [ ] Every phase has a "Done when" check an agent can run.
- [ ] Gotcha ledger has only real, generic gotchas with symptom/cause/fix.
- [ ] Free-vs-paid table covers every account named anywhere in the guide.
- [ ] Neutrality grep passes: no real hostnames, IPs, handles, or home paths.
- [ ] Linked from `docs/wiki/Home.md` and listed in `README.md`.

_Source of truth: `docs/GUIDE-STANDARD.md` in the repo; this wiki copy is published from it._
