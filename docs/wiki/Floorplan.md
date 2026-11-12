# Floorplan

_An interactive, plain-English map of your codebase, drawn by your AI coding agent._

> Why, hello there! Step right up to the drafting table of tomorrow, where your
> very own Artificial Intelligence unrolls a crisp blueprint of the software you
> already own. On this expedition we'll guide you, step by confident step, to a
> **Floorplan**: every room of your application named, every corridor between
> them drawn, and a helpful inspector pointing out the doors you left unlocked.
> The neighbours, we are assured, will ask where you got it.

## What this tool is

Floorplan is a plugin for Claude Code and Codex. You ask your agent for a
floorplan of a project; it scans the code, decides what the main parts are, writes
a one-line description of every file and web request, and builds a map you open in
a browser. The map has a Health check (exposed keys, endpoints anyone can change),
a list of your app's screens, guided flows, and an Ask bar that answers questions
about the code.

You end up with a `floorplan/` folder inside the project. It holds the map and is
kept out of git on its own.

It is **not** a hosted service, a code scanner you run in CI, or documentation
that updates itself: the map changes when you ask your agent to update it.

**Where it comes from.** The plugin in [`tools/floorplan/`](https://github.com/CoreyScherrer/CS-Agent-Tools/tree/main/tools/floorplan)
is Hayden Smith's open-source Floorplan (MIT), version 0.6.1, with changes to the
viewer that put the map first: names you can read when zoomed out, a tighter
layout, outside services in columns, one title, a flows column on the left, and an
embed mode. Its [changelog](https://github.com/CoreyScherrer/CS-Agent-Tools/blob/main/tools/floorplan/CHANGELOG.md) lists each one
under **Unreleased**. Everything else is the original.

**Known gap.** The original has since released 0.6.2 to 0.7.3. Its 0.7.1 hardened
the map against a repository that tries to break, leak from or stall it. Those
changes are not in this bundle yet, so **map only code you trust**.

## Who this is for, and what you need

Anyone who wants to see how an app fits together: the person who built it with an
AI agent and never saw the whole shape, a new teammate, or a client who will never
read the code.

**Hardware**

- Any computer that runs your coding agent. Nothing extra.

**Accounts and services**

- A Claude Code or Codex sign-in you already have. No API key. See §Free vs paid.

**Software and tools**

- Node.js 18 or newer (human installs it once; check with `node --version`).
- Claude Code (desktop app Code tab, or the CLI) **or** Codex (app or CLI).
- Recommended with Claude Code: the Claude Code CLI, even if you use the desktop
  app. The map's Ask bar uses it to read your real code.
- `git`, only if the project is a git repository. Floorplan reads from it and
  never writes to it.

## Setup time

| | Estimate |
|---|---|
| Human hands-on time | 5 minutes: two install commands, one sentence to ask for the map |
| AI agent working time | 3–10 minutes for a small app; 20–40 minutes for a few hundred files |
| Elapsed (calendar) | Under an hour |

The agent's time is driven by the number of files: it writes a description for
each one. The only steps that block on a human are installing Node.js and
approving the plugin's `node` scripts the first time they run.

## Working with your AI agent on this guide

- **Where to run the agent.** Open your coding agent **in the project you want
  mapped**. If the app is split across several repositories that sit side by
  side, open the folder that contains them all.
- **Give it a browser.** Not needed for setup. The map opens in your own browser
  or the agent app's browser pane.
- **Secrets never go through chat.** Floorplan asks for none. If the Health check
  finds a key in your code, the map shows the file and line, not the value. Do
  not paste the value into chat to "check" it; rotate it.
- **Set up a way to talk to the result.** The map's Ask bar is that way: type a
  question on the map and the answer points at the parts involved.

## The phases

### Phase 1 — Install the plugin

**Goal:** the `floorplan` skill is available in your agent.

**Decisions**

| Decision | Option | When to pick it | Cost | Default |
|---|---|---|---|---|
| Which agent | Claude Code | You use Claude Code | none | **✓** |
| | Codex | You use Codex | none | |
| Install source | This repository as a marketplace | Almost always | none | **✓** |
| | A local clone | You want to read or change the plugin first | a `git clone` | |

**Human steps**

- [ ] Install Node.js 18 or newer if `node --version` fails.

**Agent steps (Claude Code)**

- [ ] Run:
  ```bash
  claude plugin marketplace add CoreyScherrer/CS-Agent-Tools
  claude plugin install floorplan@cs-agent-tools
  ```
- [ ] Tell the human to start a new session.

**Agent steps (Codex)** — from the plugin's own Codex instructions; this bundle's
Codex path has not been run by this guide's author.

- [ ] Run:
  ```bash
  git clone https://github.com/CoreyScherrer/CS-Agent-Tools.git
  codex plugin marketplace add ./CS-Agent-Tools/tools/floorplan
  codex plugin add floorplan@floorplan
  ```
- [ ] Tell the human to start a new chat.

**Done when:** `claude plugin list` (or `codex plugin list`) shows `floorplan`
as installed and enabled, in a session started after the install.

**Gotchas in this phase**

- The skill is missing right after installing. Plugins load when a session
  starts; start a new one.
- You already have the original Floorplan installed. Both plugins are named
  `floorplan`, so remove the other one first or you will not know which viewer
  you are looking at.

### Phase 2 — Make the first map

**Goal:** a map of your project opens in the browser.

**Decisions**

| Decision | Option | When to pick it | Cost | Default |
|---|---|---|---|---|
| What to map | The whole project folder | One repository | none | **✓** |
| | The parent folder of several repositories | A front end and an API in separate repos | a longer first run | |
| Remember the map for later sessions (Claude Code asks) | Yes | You will keep working in this project | a marked section in `CLAUDE.local.md`, kept out of git | **✓** |
| | No | A one-off look at someone else's code | none | |

**Human steps**

- [ ] Ask: "Make me a floorplan of this app."
- [ ] Approve the plugin's `node` scripts when asked. Choose "always allow for
  this project".

**Agent steps**

- [ ] Run the skill. It scans, decides the parts, describes every file and
  builds the map.
- [ ] Report the address the map opened at and the most serious Health finding.

**Done when:** `floorplan/index.html` exists in the project, and the address the
agent printed (by default `http://127.0.0.1:4378`) shows the map.

**Gotchas in this phase**

- "`floorplan/` already exists here and isn't a map." The project has its own
  folder with that name. Ask the agent to build the map elsewhere; the scripts
  take `--out <folder>`.
- The address is not port 4378. The port was busy and the server took the next
  free one. Use the address the agent printed.

### Phase 3 — Read the Health check before acting on it

**Goal:** every Health issue is either fixed or marked "Not a problem" with a reason.

**Decisions**

| Decision | Option | When to pick it | Cost | Default |
|---|---|---|---|---|
| A flagged key or password | Treat as a lead: open the file and line, decide | Always | minutes | **✓** |
| | Rotate at once | The value is real and the file is tracked in git | a rotation | |
| A false alarm | Mark **Not a problem** with a reason | The value is a placeholder, a hash or a test fixture | none | **✓** |

**Human steps**

- [ ] Open **Health** on the map and read each issue.
- [ ] For a real secret in a tracked file: rotate it at the provider. Removing
  the line does not remove it from git history.

**Agent steps**

- [ ] For each issue, open the file and line and say whether the value is live,
  a placeholder or a fixture.
- [ ] Fix what is real when asked; never print the value in chat.

**Done when:** the Health count on the map is zero, or every remaining issue has
a "Not a problem" reason.

**Gotchas in this phase**

- Health flags a value that is not a secret. It reads patterns, not intent, so
  example keys in docs and fixtures in tests can match. Check before rotating
  anything.
- The "report a false alarm" box and the "Floorplan Cloud" waitlist card go to
  the original author, not to this repository. Both are opt-in and show you what
  they send first.

### Phase 4 — Share or embed the map (optional)

**Goal:** someone without your agent can see the map.

**Decisions**

| Decision | Option | When to pick it | Cost | Default |
|---|---|---|---|---|
| How to share | **Export** one HTML file | Sending it to a person | none | **✓** |
| | Embed it in a page you already have | An internal admin or docs page | a frame and a few lines of script | |

**Human steps**

- [ ] Decide who may see the map. It shows names and descriptions of every part
  and endpoint, not source code, but that is still a description of your system.

**Agent steps**

- [ ] Export: press **Export** on the map (it needs the map's server running:
  `node floorplan/serve.mjs`).
- [ ] Embed: load the exported file in a frame with `?embed=1` on its address.
  The map then hides its own search box and buttons and hands them to your page.
  Put it behind whatever sign-in protects the page around it.

**Done when:** the exported file opens from a different computer with no
network, or the embedded map draws inside your page with one top bar, not two.

**Gotchas in this phase**

- The embedded map shows its tour on every visit. A sandboxed frame blocks
  storage, so the map cannot remember the tour ran. In this bundle the tour opens
  only from its button in that case.
- You updated the plugin and the map looks the same. The browser cached the old
  page. Reload without the cache (Cmd+Shift+R or Ctrl+Shift+R).

### Phase 5 — Keep it current

**Goal:** the map matches the code after each piece of work.

**Human steps**

- [ ] After a change, ask: "Update the floorplan."

**Agent steps**

- [ ] Re-run the skill. Moved files keep their descriptions; only what is new or
  changed is rewritten. An open tab reloads itself.

**Done when:** the cards for the files you just changed are highlighted under
**Recent work**.

**Gotchas in this phase**

- `git status` lists files under `floorplan/`. They were committed before the
  folder ignored itself. Untrack them and keep the files:
  `git rm -r --cached floorplan`.

## Gotcha ledger

| Symptom | Cause | Fix |
|---|---|---|
| The skill does not appear after installing | Plugins load at session start | Start a new session; confirm with `claude plugin list` |
| Two plugins named `floorplan`, unclear which viewer you have | The original and this bundle share a name | Uninstall one before installing the other |
| "`floorplan/` already exists here and isn't a map" | The project has its own folder of that name | Build elsewhere with `--out <folder>` |
| The map is not at port 4378 | The port was in use | Use the address the agent printed |
| The Ask bar says it needs the Claude Code CLI | The map was opened from its file, or the CLI is not installed | Install the CLI and run `node floorplan/serve.mjs` |
| The CLI is installed but not found | It is not on `PATH` | `node floorplan/serve.mjs --claude /path/to/claude` |
| The agent keeps asking to run `node` scripts | Permission settings | Choose "always allow for this project" |
| Health flags something that is not a secret | Pattern match on a placeholder, hash or fixture | Verify at the file and line; mark **Not a problem** with a reason |
| A connection between two parts is missing | The address exists only in settings, not in code | Ask the agent to add it; it is kept on every update |
| A file sits under "Unassigned" | No part's path pattern matches it | Ask the agent to move it, or edit `paths` in `floorplan/architecture.json` |
| The tour replays every visit when the map is embedded | Storage is blocked in a sandboxed frame | Nothing to do in this bundle: the tour opens only from its button there |
| The map looks unchanged after updating the plugin | Browser cache | Reload without the cache |
| `git status` shows files under `floorplan/` | Committed before the folder ignored itself | `git rm -r --cached floorplan` |

## Free vs paid

| Service | Free tier enough? | What paid adds | Our call |
|---|---|---|---|
| Floorplan plugin | Yes. It is free and open source | Nothing | Free |
| Claude Code or Codex | Whatever plan you already use. The first map of a large project uses a noticeable amount of it | Higher limits | Use the plan you have; map a large project when you are not near a limit |
| Node.js | Yes | Nothing | Free |

Nothing in this guide needs a new account. The opt-in "Floorplan Cloud" waitlist
card on the map is the original author's and is not part of this guide.

## Talking to the tool

- **Ask your agent:** "make me a floorplan", "update the floorplan", "what does
  the checkout part depend on?". With the map made, the agent uses it to answer.
- **Ask on the map:** type a question in the Ask bar. Answers light up the parts
  involved. This needs the map's server and the Claude Code or Codex CLI.
- **Open it yourself:** `node floorplan/serve.mjs` from the project, or
  double-click `floorplan/index.html` (everything but the Ask bar works).
- **Stop the server:** `node floorplan/serve.mjs --stop`. It also stops by itself
  two hours after the last tab closes.
- **Keys on the map:** **F** fits the map to the screen; **P** opens and closes
  the details panel.

## Keeping it alive

- [ ] After each piece of work: "Update the floorplan."
- [ ] Monthly: update the plugin (`claude plugin update floorplan@cs-agent-tools`),
  then start a new session and reload the map without the cache.
- [ ] After a plugin update: read the top of the plugin's changelog.
- [ ] Before trusting an installed copy: from a clone of this repository, run
  `node tools/checksums.mjs --check <installed folder>` inside `tools/floorplan`.
  It compares every file the plugin runs from with the list in `CHECKSUMS.txt`.
- [ ] When removing it: `claude plugin uninstall floorplan@cs-agent-tools`, then
  delete each project's `floorplan/` folder and the Floorplan section of
  `CLAUDE.local.md`.

The plugin's own pages go deeper:
[using the map](https://github.com/CoreyScherrer/CS-Agent-Tools/blob/main/tools/floorplan/docs/using-the-map.md),
[is it safe to install?](https://github.com/CoreyScherrer/CS-Agent-Tools/blob/main/tools/floorplan/docs/is-it-safe.md),
[troubleshooting](https://github.com/CoreyScherrer/CS-Agent-Tools/blob/main/tools/floorplan/docs/troubleshooting.md).
