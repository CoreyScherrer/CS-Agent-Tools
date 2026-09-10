# Setup

Standing the archive up on a machine whose capabilities you cannot verify in
advance.

**Read [[Data-Boundary]] first** if this is an employer machine.

## Requirements

Python 3.9+. That is the entire list — the default path uses only the standard
library, because package installation may be restricted on a managed machine.

## Quick path

```bash
git clone https://github.com/CoreyScherrer/PORTABLE-WORK.git memory-archive
cd memory-archive

python3 -m ma doctor        # probe the machine — read this output
python3 -m ma doctor --write
python3 -m ma init
python3 -m ma status
```

If `doctor` reports no blocking failures, you are done. If it does, find the
matching section below.

## What `doctor` does

Read-only: nothing installed, no service started, no file written outside the
repo. It probes Python, pip, PostgreSQL, filesystem, editor surface, hooks,
network egress, and git — then recommends a backend and explains why.

Every probe is independently wrapped. A probe that fails becomes a warning in
the report, never a crash. That is deliberate: on an unfamiliar machine a
report is useful and a traceback is not.

## Reading the report

### `python` FAIL

The one hard requirement. Try `python3.11`, `python3.12`, or a company-provided
interpreter, then:

```bash
export MA_PYTHON=/path/to/python3
```

Put that in your shell profile too, so the session hooks find it.

### `filesystem` FAIL

The repo location is not writable. Move it somewhere local under your home
directory. Do not point the database at a network share — SQLite over a network
filesystem is unreliable.

### `filesystem` WARN — synced folder

The repo sits in OneDrive, Dropbox, or Google Drive, so captured content would
replicate off-machine. For employer work that is usually wrong. Move the repo to
a local path.

### `postgres` SKIP or WARN

Expected on a restricted machine, and not a problem. SQLite is a fully supported
destination, not a degraded mode.

**Do not spend your first working day installing a database.** The cost of not
capturing anything is higher than the cost of SQLite. `ma migrate --to postgres`
moves everything later, non-destructively, if the situation changes.

### `pip` WARN

Also fine. The default path needs no packages.

### `egress` WARN

Informational only. Phase 1 makes no network calls, so blocked egress changes
nothing.

## Verify context injection

This is the step most likely to behave differently on your machine — hook
support varies across Claude Code surfaces (terminal CLI, VS Code extension,
company-API-framework configurations).

First confirm the archive itself works:

```bash
python3 -m ma capture context "Setup test" "Verifying the archive" --project test
python3 -m ma recall --project test
```

A `[Memory Archive]` banner means the archive is fine.

Then **start a new Claude Code session in this repo** and look for the same
banner in the opening context.

**Banner appears** → hooks fire, nothing more to do.

**Banner missing** → hooks are not firing here. You have lost automatic
injection, not data. In order:

1. `bash scripts/session-start.sh` — if this errors, fix that first (usually
   `MA_PYTHON`)
2. Move the `hooks` block from `.claude/settings.json` into
   `~/.claude/settings.json`, replacing `$CLAUDE_PROJECT_DIR` with an absolute
   path
3. Rely on the `CLAUDE.md` fallback — it already instructs the model to run
   `ma recall` when no banner is present. This is the designed fallback, not a
   workaround.

Then record what you found:

```bash
python3 -m ma capture learning "Hooks do not fire in <surface>" \
    "<what you observed and tried>" --pin
```

That is exactly the kind of environment knowledge that is expensive to
rediscover.

## First captures

Seed the archive with what you already know but have not written down:

```bash
python3 -m ma capture context "Team structure" "<who does what>" \
    --link person:<name> --pin

python3 -m ma capture context "<system> ownership" "<what it does, who owns it>" \
    --link system:<name>

python3 -m ma capture learning "<constraint that surprised you>" "<why it matters>"
```

## Defaults

Edit `config.local.json` (gitignored):

```json
{
  "identity": {
    "agent_key": "claude-code-work",
    "default_project": "<your main workstream>"
  },
  "recall": { "token_budget": 2000 }
}
```

Raise `token_budget` if recall feels thin; lower it if session context feels
crowded.

## If cloning is blocked

Some managed machines block personal GitHub. Transfer as a bundle instead:

```bash
# source machine
git bundle create memory-archive.bundle --all

# target machine
git clone memory-archive.bundle memory-archive
```

## Worth reporting back

These four answers determine what Phase 2 can even be:

- full `ma doctor` output
- whether hooks fired, and on which Claude Code surface
- whether PostgreSQL was available
- whether package installation works
