# Daily Use

## Capture

```bash
python3 -m ma capture <type> "<title>" "<body>" [options]
```

**Types**

| Type | Use for |
|---|---|
| `decision` | A choice made and the reasoning behind it |
| `learning` | Something discovered, often the hard way |
| `pattern` | A convention or recurring approach |
| `context` | Background: org, ownership, how things are arranged |
| `preference` | How you or the team want things done |
| `question` | Open, unresolved — worth revisiting |

**Options**

| Option | Effect |
|---|---|
| `--project <name>` | Scopes recall; same-project memories rank higher |
| `--link person:Jane` | Links to a person (created on first mention) |
| `--link system:checkout` | Links to a system |
| `--link item:ABC-123` | Links to a ticket or work item |
| `--importance 0.0-1.0` | Drives ranking; default 0.5 |
| `--pin` | Always surface first, regardless of age |
| `--tags a,b,c` | Free-form tags, searchable |
| `--stdin` | Append body from stdin, for long content |

`--link` is repeatable. Entities are created on first mention, so capture never
stalls to pre-register anything.

## What is worth capturing

The test: **would rediscovering this cost more than a minute?**

Worth capturing:

- A decision and *why* — the what is usually recoverable from code, the why never is
- A constraint that surprised you ("builds fail without VPN")
- Who owns what, and who to ask about which system
- A gotcha that cost you time
- Something you would have to ask a colleague about twice

Not worth capturing:

- Anything already in the repo or its docs
- Facts that will be stale next week
- Detail you can regenerate by reading code

**Write titles for your future self with none of today's context.** "Fixed the
thing" is worthless in three months. "Deploy fails without corp VPN" is not.

**Put the why in the body.** That is the part that does not survive anywhere
else.

## Retrieve

```bash
python3 -m ma recall --project <name>   # ranked context within a token budget
python3 -m ma search "<term>"           # keyword search
python3 -m ma context system:checkout   # everything linked to one entity
python3 -m ma context person:"Jane Doe"
python3 -m ma status                    # backend and counts
```

`recall` is what the session hook runs. `search` is for when you know roughly
what you are looking for. `context` is the one that pays off in a new role —
"everything I know about this system, plus who owns it."

## Entities

```bash
python3 -m ma entity person list
python3 -m ma entity system add "checkout" --notes "order pipeline"
python3 -m ma entity item add "ABC-123" --notes "login bug"
```

Usually unnecessary — `--link` creates entities on first mention. Use these to
browse, or to add notes to something already referenced.

## Backup and transfer

```bash
python3 -m ma export --out ~/ma-backup.json   # plain text, reviewable
python3 -m ma import ~/ma-backup.json         # idempotent by id
```

This is how content moves between machines. **Not git** — see [[Data-Boundary]].

## Ranking

`recall` ranks by:

```
score = importance × recency_decay × project_match
```

Pinned memories always lead. Recency halves the weight every 30 days by default.
Same-project memories are boosted; other-project ones are penalized but still
eligible, because a lesson learned elsewhere is often exactly what is needed.

Selection fills to a token budget and skips oversized items, so one long memory
cannot crowd out everything below it.

It is deterministic — same inputs, same ordering, no model involved.

## Tuning recall

- Recall feels thin → raise `recall.token_budget`
- Session context feels crowded → lower it
- Old memories crowding out new → lower `recency_half_life_days`
- Something must always appear → `--pin` it
- Wrong things ranking high → revisit their `--importance`
