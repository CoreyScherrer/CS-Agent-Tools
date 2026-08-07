# Data Boundary

**The framework is shareable. What it captures is not.**

This is the most important page in the wiki. Everything else is convenience;
this is the rule that keeps the tool safe to use for employer work.

## The split

| | May be shared | Stays on the machine |
|---|---|---|
| Code (`ma/`, `tests/`, `scripts/`) | yes | |
| Docs, wiki, setup guides | yes | |
| `config.example.json` | yes | |
| `data/`, `*.db` — the archive | | **never** |
| `config.local.json` | | **never** |
| Un-redacted `ma export` output | | **never** |

Captured memory is work product: decisions, org context, system architecture,
ticket detail. It belongs to the employer, and it does not go to a personal
account, a personal remote, or an external service.

## How it is enforced

Convention is not enough — it gets forgotten under deadline. Three mechanisms:

**1. Gitignore.** `data/`, `*.db`, `config.local.json`, `.env` and export files
are ignored.

**2. A pre-commit guard.** Installed by `ma init` into `.git/hooks/pre-commit`.
It blocks the commit even when gitignore is bypassed with `git add -f` — which
is the case gitignore alone misses. It lives on the machine holding the content,
which is why it is installed rather than committed (git does not carry hooks
through a clone).

**3. No network calls.** Phase 1 sends nothing anywhere: no summarization, no
embeddings, no telemetry. Content cannot leak through a feature that does not
exist.

## If the guard fires

It caught something. That is the guard working, not a false alarm to route
around.

```
BLOCKED: this commit contains captured content or local config.
```

- **If it is genuinely captured content** — do not commit it. Nothing more to do.
- **If it is framework code that landed in `data/`** — move it out of `data/` and
  commit it from its proper location.

**Do not use `git commit --no-verify` to commit content.** The override exists
for unrelated edge cases, not for this.

## Moving content between machines

There is a real need to back up or transfer an archive. Git is the wrong tool
for it — a database is a binary blob that bloats history and can never be
removed once committed.

Use export/import instead. It produces plain text you can review before it
lands:

```bash
# on the source machine
python3 -m ma export --out ~/ma-backup.json

# on the target machine
python3 -m ma import ~/ma-backup.json
```

Import is idempotent by id, so re-running it changes nothing. Memories,
entities, and their links all survive the round trip.

Move the file the same way you would move any work document — approved storage,
an encrypted drive, whatever your policy allows. Not through a personal cloud
account.

## Sharing a pattern without the content

To show someone the structure — how the archive is used, what the schema looks
like — without exposing what is in it:

```bash
python3 -m ma export --redact
```

Metadata and structure survive; every piece of free text becomes `[redacted]`.
A redacted export cannot be imported, by design: it no longer contains the
content it describes.

## "But the repo is private"

Private today is not private forever:

- Visibility changes with one click
- Collaborators get added
- The framework is *intended* to be shared with the team eventually
- Git history is permanent — a committed database survives its own deletion and
  can only be removed by rewriting history across every clone

The boundary holds regardless of current visibility. That is what makes it a
boundary rather than a preference.
