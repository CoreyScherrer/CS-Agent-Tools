# Floorplan in Codex

Floorplan works in [Codex](https://developers.openai.com/codex) the same way it works in Claude Code: the same skill, scripts and map, on your own ChatGPT sign-in. There are no API keys to set up.

## What you need

- Codex: the desktop app or the CLI, signed in with your ChatGPT account.
- [Node.js](https://nodejs.org) 18 or newer.

## Install

This bundle lives in a folder of the CS-Agent-Tools repository, so Codex installs it from a copy on your computer. With the [Codex CLI](https://developers.openai.com/codex/cli):

```bash
git clone https://github.com/CoreyScherrer/CS-Agent-Tools.git
codex plugin marketplace add ./CS-Agent-Tools/tools/floorplan
codex plugin add floorplan@floorplan
```

Then start a new chat. Codex copies the plugin into its own cache when you add it, so the clone can be deleted afterwards.

The app and the CLI share their plugins, so installing in one makes Floorplan available in both.

## Make your first map

Open your project in Codex and ask in plain words:

> Draw a floorplan of this codebase

To call the skill by name, type `$floorplan`. Everything after that is the same as in Claude Code ([Getting started](getting-started.md#make-your-first-map)): Codex scans the code, describes every part, file and web request, builds the map and opens it. Later, "update the floorplan" re-reads only what changed.

When Codex opens the map, it asks to run the map's server outside its sandbox. The server has to keep running after the command ends, and the Ask bar needs to reach Codex. If you'd rather not allow it, run the server yourself from the project folder:

```bash
node floorplan/serve.mjs
```

## Asking questions on the map

The map's Ask bar runs your own Codex on your computer: `codex exec` in Codex's **read-only** sandbox, in your project folder, with your ChatGPT sign-in. It reads the map and your source to answer, and can't change any files. These runs aren't saved to your Codex history; a follow-up question brings the last few questions and answers along instead.

The server uses whichever agent built the map, and falls back to the other one if that one isn't installed. To choose:

```bash
node floorplan/serve.mjs --engine codex
```

It finds `codex` on your PATH, and on Windows the CLI that comes with the Codex desktop app. If yours is somewhere else, pass `--codex /path/to/codex`. `--model <name>` picks the model; otherwise your Codex settings decide.

## What's different from Claude Code

- **No notes file.** In Claude Code, Floorplan can keep a short note in `CLAUDE.local.md` (personal and never committed, and only if you say yes) that points future sessions at the map. Codex has no personal, uncommitted equivalent (`AGENTS.md` is shared with your team), so in Codex Floorplan leaves your project's notes alone.
- **No Claude app.** Publishing the map to the Claude app is a Claude feature. In Codex the map opens in your browser, served from your computer.
- **"Fix with Codex".** The Health panel's ready-made fix prompts are for pasting into Codex. On a [blueprint](getting-started.md#plan-something-you-havent-built-yet), the same goes for **Build this with Codex**, and the Ask bar's **Change** switch runs Codex in its read-only sandbox too: Codex replies with the updated plan, and the map's server saves it.

## Update or remove it

To get the latest version, pull your clone (or clone again) and add the plugin again, which replaces Codex's cached copy:

```bash
git -C CS-Agent-Tools pull
codex plugin add floorplan@floorplan
```

To take it out:

```bash
codex plugin remove floorplan@floorplan
codex plugin marketplace remove floorplan
```

Your maps stay in each project's `floorplan/` folder until you delete them.

## Trying a working copy

Point Codex at your local clone instead of GitHub:

```bash
codex plugin marketplace add /path/to/floorplan
codex plugin add floorplan@floorplan
```

Codex copies a local plugin into its cache when you add it (unlike Claude Code, which runs a local plugin straight from the folder). After you change the plugin, run `codex plugin add floorplan@floorplan` again and start a new session.
