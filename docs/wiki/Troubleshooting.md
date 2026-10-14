# Troubleshooting

## Quick table

| Symptom | Cause | Fix |
|---|---|---|
| `No module named ma` | wrong working directory | run from the repo root |
| No `[Memory Archive]` banner | hooks not firing | see below |
| `recall` returns nothing | empty archive, or project filter | `ma status`; retry without `--project` |
| Commit blocked | guard caught content | correct behaviour — see [[Data-Boundary]] |
| `ma init` kept an existing hook as `pre-commit.local` | a foreign hook was present | it runs after the guard; see below |
| `psycopg` ImportError | Postgres selected, no driver | set `storage.backend` to `sqlite` |
| Hook does nothing, silently | `python3` not on the hook's PATH | set `MA_PYTHON` in your shell profile |
| `ma init` says "not a git repo" | ran outside the clone | `cd` into the repo |
| Doctor says filesystem FAIL | repo location not writable | move it under your home directory |

## No `[Memory Archive]` banner

The most likely problem, because hook support varies across Claude Code
surfaces.

**1. Does the archive itself work?**

```bash
python3 -m ma recall
```

Output means the archive is fine and only injection is broken. An error means
start with `ma status`.

**2. Does the hook script run?**

```bash
bash scripts/session-start.sh
```

Errors here are usually the interpreter. Set `MA_PYTHON` to a working
`python3` and put it in your shell profile — hooks do not inherit an interactive
shell's environment.

**3. Are hooks declared?**

```bash
python3 -m ma doctor
```

The `hooks` probe reports what `.claude/settings.json` declares. If it says none,
`ma init` has not run.

**4. Try user-level settings.**

Copy the `hooks` block from `.claude/settings.json` into
`~/.claude/settings.json`, replacing `$CLAUDE_PROJECT_DIR` with an absolute path.
Some surfaces honour user settings when project settings are ignored.

**5. Fall back to `CLAUDE.md`.**

`CLAUDE.md` already instructs the model to run `ma recall` when no banner is
present. This is the designed fallback. You lose automatic injection, not data.

**Then record it:**

```bash
python3 -m ma capture learning "Hooks do not fire in <surface>" \
    "<what you tried>" --pin
```

## `recall` returns nothing

```bash
python3 -m ma status          # is anything stored?
python3 -m ma recall          # without a project filter
```

If `status` shows memories but `recall` is empty, the project filter is
excluding them — memories captured without `--project` do not match a filtered
recall. Check `identity.default_project` in `config.local.json`.

## Commit blocked by the guard

Working as designed. See [[Data-Boundary]].

- Captured content → do not commit it
- Framework code that landed in `data/` → move it out and commit from there

Do not use `--no-verify` to commit content.

If `ma init` says the existing hook was kept as
`.git/hooks/pre-commit.local`, the guard runs it after its own checks. If `ma init`
warns that both a foreign `pre-commit` hook and `pre-commit.local` exist, it leaves
both untouched; resolve which hook to keep before running `ma init` again.

## Postgres problems

**`psycopg` ImportError** — config says postgres, no driver installed. Either
install one (`pip install "psycopg[binary]"`) or set `storage.backend` to
`sqlite` in `config.local.json`. Nothing is lost either way.

**`doctor` says reachable but not authenticated** — a server exists but your
credentials do not work. SQLite is used automatically. Pursue this only if
Postgres is genuinely needed.

**Migration failed partway** — `ma migrate` is read-only on the source, so the
SQLite file is intact. Fix the cause and re-run; import is idempotent by id.

## Archive seems corrupted

```bash
python3 -m ma export --out ~/ma-rescue.json   # get content out first
```

Then, with the export safe, move `data/memory.db` aside, run `ma init`, and
`ma import ~/ma-rescue.json`.

## Starting over

```bash
python3 -m ma export --out ~/ma-backup.json   # if anything is worth keeping
rm data/memory.db
python3 -m ma init
```

## Diagnostics worth including in a report

```bash
python3 -m ma doctor --json
python3 -m ma status
python3 --version
```

Plus: which Claude Code surface you are on, and whether the banner appeared.
