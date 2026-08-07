# Setting up on a new (possibly restricted) machine

Written for the person or agent standing this up on a machine that was not
available when the framework was built. Work top to bottom; each step says what
to do when it fails.

**Read this whole page before running anything if the machine is
corporate-managed.** Step 0 is a judgement call that the rest depends on.

---

## Step 0 — Before you clone: the data-handling question

This framework captures work content into a local database. Before using it for
employer work, confirm for yourself:

1. **Is a local tool that stores notes about your work acceptable here?** It is
   functionally a notes file, but check policy rather than assume.
2. **Where does the repo live?** Not in a synced folder (OneDrive, Dropbox,
   Google Drive) unless replication of that content is acceptable. `ma doctor`
   flags this, but it can only detect the obvious cases.
3. **Where does the code come from?** The framework is safe to clone from a
   personal remote — it contains no work content. **Never push captured content
   back to a personal remote.** The pre-commit guard enforces this, and there is
   no legitimate reason to bypass it.

If a personal remote is blocked, transfer the framework as a bundle instead:

```bash
# on the source machine
git bundle create memory-archive.bundle --all

# on the target machine
git clone memory-archive.bundle memory-archive
```

---

## Step 1 — Probe the machine

```bash
cd memory-archive
python3 -m ma doctor
```

This is read-only: nothing is installed, no service started, no file outside the
repo written. It reports Python, pip, PostgreSQL, filesystem, editor surface,
hooks, egress and git, then recommends a backend.

**Read the report before continuing.** It tells you what this machine actually
allows, which is the input to every decision below.

### If `python` is FAIL

Python 3.9+ is the one hard requirement. Try `python3.11`, `python3.12`, or a
company-provided interpreter, then set:

```bash
export MA_PYTHON=/path/to/python3
```

Also set `MA_PYTHON` in your shell profile so the session hooks find it.

### If `filesystem` is FAIL

The repo location is not writable. Move it somewhere that is (a local path under
your home directory is usually right) and re-run. Do not work around this by
pointing the database at a network share — SQLite over a network filesystem is
unreliable.

### If `filesystem` is WARN (synced folder)

The repo sits in OneDrive/Dropbox/Google Drive, so captured content will
replicate off-machine. For employer work that is usually the wrong place. Move
the repo to a local path.

### If `postgres` is SKIP or WARN

Expected on a restricted machine, and not a problem. SQLite is a fully supported
destination, not a degraded mode. Continue — you can migrate later with
`ma migrate --to postgres` without losing anything.

Only pursue PostgreSQL if it is already available or trivially installable.
Do not spend your first working day on a database install; the cost of not
capturing anything is higher than the cost of SQLite.

### If `pip` is WARN

Also fine. The default path uses no third-party packages.

---

## Step 2 — Save the choice and initialise

```bash
python3 -m ma doctor --write   # writes config.local.json (gitignored)
python3 -m ma init             # creates schema, installs the pre-commit guard
python3 -m ma status           # confirm
```

`ma init` is required after every fresh clone: git does not carry hooks, so the
commit guard has to be installed locally.

---

## Step 3 — Verify context injection actually works

This is the step most likely to behave differently on your machine, because hook
support varies between Claude Code surfaces (terminal CLI, VS Code extension,
and company-API-framework configurations).

Test it directly first:

```bash
python3 -m ma capture context "Setup test" "Verifying the archive works" --project test
python3 -m ma recall --project test
```

If that prints a `[Memory Archive]` banner, the archive is working.

Then **start a new Claude Code session in this repo** and look for the same
banner in the session's opening context.

### If the banner appears

Hooks fire. Nothing more to do.

### If the banner does not appear

Hooks are not firing in this environment. The archive still works — you have
lost automatic injection, not data. In order of preference:

1. **Check the hook runs at all:** `bash scripts/session-start.sh` — if this
   errors, fix that first (usually `MA_PYTHON`).
2. **Try user-level settings** instead of project-level: copy the `hooks` block
   from `.claude/settings.json` into `~/.claude/settings.json`, using an
   absolute path in place of `$CLAUDE_PROJECT_DIR`.
3. **Rely on the CLAUDE.md fallback.** `CLAUDE.md` already instructs the model to
   run `ma recall` when no banner is present. This is why that instruction
   exists — it is the designed fallback, not a workaround.

Record what you find:

```bash
python3 -m ma capture learning "Hooks do not fire in <surface>" \
    "<what you observed and what you tried>" --pin
```

That memory is exactly the kind of environment knowledge that is expensive to
rediscover.

---

## Step 4 — First real captures

Seed the archive with what you already know but have not written down. Org
knowledge is the most expensive thing to reconstruct and the least likely to be
in any repo:

```bash
python3 -m ma capture context "Team structure" "<who does what>" \
    --link person:<name> --pin

python3 -m ma capture context "<system> ownership" "<what it does, who owns it>" \
    --link system:<name>

python3 -m ma capture learning "<constraint that surprised you>" "<why it matters>"
```

---

## Step 5 — Set your defaults

Edit `config.local.json` (gitignored):

```json
{
  "identity": {
    "agent_key": "claude-code-<machine>",
    "default_project": "<your main workstream>"
  },
  "recall": {
    "token_budget": 2000
  }
}
```

Raise `token_budget` if recall feels thin; lower it if session context feels
crowded.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `No module named ma` | wrong cwd | run from the repo root |
| No `[Memory Archive]` banner | hooks not firing | Step 3 |
| `recall` returns nothing | empty archive, or project filter | `ma status`; try without `--project` |
| Commit blocked | guard caught content | correct — do not use `--no-verify` |
| `psycopg` ImportError | Postgres selected without driver | set `storage.backend` to `sqlite` |
| Hook silently does nothing | `python3` not on the hook's PATH | set `MA_PYTHON` in your shell profile |

## What to report back

After setup, the useful findings for deciding Phase 2:

- the full `ma doctor` output
- whether hooks fired, and on which Claude Code surface
- whether PostgreSQL turned out to be available
- whether package installation works

Those four answers determine whether semantic search, an MCP server, or a shared
team backend are even possible here.
