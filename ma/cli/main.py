"""`ma` command-line interface.

Uses argparse from the standard library so the tool runs on a machine where
installing packages may not be possible. Invoke as ``python -m ma <command>``.
"""

import argparse
import json
import os
import sys

from .. import config as config_mod
from ..core import doctor as doctor_mod
from ..core.repository import (
    ENTITY_KINDS,
    MEMORY_TYPES,
    Repository,
    ValidationError,
    decode_tags,
    parse_link_spec,
)
from ..storage import get_backend


def _repo(args):
    cfg = config_mod.load()
    if getattr(args, "project", None):
        cfg.setdefault("identity", {})["default_project"] = args.project
    backend = get_backend(cfg)
    backend.init_schema()
    return Repository(backend, cfg), cfg


def _print_memory(memory, verbose=False):
    tags = decode_tags(memory.get("tags"))
    head = "[{}] {}".format(memory.get("type", "?"), memory.get("title", ""))
    if memory.get("pinned"):
        head = "* " + head
    print(head)
    meta = "    {}  importance={:.2f}".format(
        (memory.get("created_at") or "")[:16], float(memory.get("importance") or 0)
    )
    if memory.get("project"):
        meta += "  project={}".format(memory["project"])
    if tags:
        meta += "  tags={}".format(",".join(tags))
    print(meta)
    if verbose and memory.get("body"):
        for line in memory["body"].splitlines():
            print("    {}".format(line))
    if verbose:
        print("    id={}".format(memory.get("id")))


# ---- commands -----------------------------------------------------------

def cmd_doctor(args):
    probes = doctor_mod.run_all(config_mod.REPO_ROOT)
    backend, reason = doctor_mod.recommend_backend(probes)
    print(doctor_mod.format_report(probes, backend, reason))

    if args.write:
        cfg = config_mod.load()
        cfg.setdefault("storage", {})["backend"] = backend
        path = config_mod.save_local(cfg)
        print("\nWrote {}".format(path))
    else:
        print("\n(Run `ma doctor --write` to save this backend choice to config.local.json)")

    if args.json:
        print(json.dumps({"probes": [p.as_dict() for p in probes],
                          "backend": backend, "reason": reason}, indent=2))
    return 1 if any(p.status == doctor_mod.FAIL for p in probes) else 0


def cmd_init(args):
    repo, cfg = _repo(args)
    print("Initialised schema on {}".format(repo.status()["location"]))

    installed = _install_precommit_guard()
    print(installed)

    settings_path = os.path.join(config_mod.REPO_ROOT, ".claude", "settings.json")
    if os.path.isfile(settings_path):
        print("Project hooks present: .claude/settings.json")
    else:
        print("WARNING: no .claude/settings.json - context injection will rely on CLAUDE.md only")
    return 0


def _install_precommit_guard():
    """Install the guard that blocks committing captured content.

    The guard lives on the machine holding the content, which is why it is
    installed here rather than shipped as a committed hook.
    """
    git_dir = os.path.join(config_mod.REPO_ROOT, ".git")
    if not os.path.isdir(git_dir):
        return "Skipped pre-commit guard (not a git repo)"
    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    target = os.path.join(hooks_dir, "pre-commit")
    source = os.path.join(config_mod.REPO_ROOT, "scripts", "pre-commit-guard.sh")
    try:
        with open(source, "r", encoding="utf-8") as fh:
            body = fh.read()
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(body)
        os.chmod(target, 0o755)
        return "Installed pre-commit guard (blocks committing data/ and *.db)"
    except OSError as exc:
        return "WARNING: could not install pre-commit guard: {}".format(exc)


def cmd_capture(args):
    repo, _ = _repo(args)
    links = [parse_link_spec(spec) for spec in (args.link or [])]
    body = args.body or ""
    if args.stdin:
        body = (body + "\n" + sys.stdin.read()).strip()
    memory_id = repo.capture(
        args.type, args.title, body,
        project=args.project,
        importance=args.importance,
        tags=[t.strip() for t in (args.tags or "").split(",") if t.strip()],
        links=links,
        session_id=args.session,
        source=args.source,
        pinned=args.pin,
    )
    print("captured {} {}".format(args.type, memory_id))
    return 0


def cmd_recall(args):
    repo, cfg = _repo(args)
    project = args.project or cfg.get("identity", {}).get("default_project") or None
    result = repo.recall(project=project, token_budget=args.budget, max_items=args.limit)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    memories = result["memories"]
    if not memories:
        print("[Memory Archive] No memories yet. Capture with: python -m ma capture <type> <title>")
        return 0

    print("[Memory Archive] {} memories ({} of {} tokens){}".format(
        len(memories), result["tokens_used"], result["token_budget"],
        " | project={}".format(project) if project else ""))
    for memory in memories:
        _print_memory(memory, verbose=args.verbose)
    return 0


def cmd_search(args):
    repo, _ = _repo(args)
    results = repo.search(args.query, limit=args.limit)
    memories = results.get("memories", [])
    print("{} memories matching {!r}".format(len(memories), args.query))
    for memory in memories:
        _print_memory(memory, verbose=args.verbose)
    for kind in ENTITY_KINDS:
        rows = results.get(kind)
        if rows:
            label = "title" if kind == "item" else "name"
            print("\n{}s:".format(kind))
            for row in rows:
                print("  {}  ({})".format(row.get(label), row["id"][:8]))
    return 0


def cmd_context(args):
    repo, _ = _repo(args)
    kind, ref = parse_link_spec(args.target)
    found = repo.entity_context(kind, ref)
    if not found:
        print("No {} matching {!r}".format(kind, ref))
        return 1
    entity = found["entity"] or {}
    print("{}: {}".format(kind, entity.get("name") or entity.get("title")))
    for field in ("role", "team", "purpose", "status", "external_ref", "notes"):
        if entity.get(field):
            print("  {}: {}".format(field, entity[field]))
    print("\n{} linked memories:".format(len(found["memories"])))
    for memory in found["memories"]:
        _print_memory(memory, verbose=args.verbose)
    return 0


def cmd_entity(args):
    repo, _ = _repo(args)
    if args.action == "add":
        field = "title" if args.kind == "item" else "name"
        fields = {field: args.value}
        if args.notes:
            fields["notes"] = args.notes
        entity_id = repo.backend.add_entity(args.kind, **fields)
        print("added {} {}".format(args.kind, entity_id))
    else:
        rows = repo.backend.list_entities(args.kind, limit=args.limit)
        label = "title" if args.kind == "item" else "name"
        print("{} {}s".format(len(rows), args.kind))
        for row in rows:
            print("  {}  ({})".format(row.get(label), row["id"][:8]))
    return 0


def cmd_export(args):
    repo, _ = _repo(args)
    data = repo.export(redact=args.redact)
    text = (json.dumps(data, indent=2) if args.format == "json" else _as_markdown(data))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote {}".format(args.out))
    else:
        print(text)
    return 0


def _as_markdown(data):
    lines = ["# Memory Archive export", "", "Exported: {}".format(data["exported_at"]), ""]
    for memory in data["memories"]:
        lines.append("## [{}] {}".format(memory.get("type"), memory.get("title")))
        meta = "_{}_".format((memory.get("created_at") or "")[:16])
        if memory.get("project"):
            meta += " · project: {}".format(memory["project"])
        lines += [meta, ""]
        if memory.get("body"):
            lines += [memory["body"], ""]
    return "\n".join(lines)


def cmd_import(args):
    repo, _ = _repo(args)
    try:
        with open(args.path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as exc:
        print("error: cannot read {}: {}".format(args.path, exc), file=sys.stderr)
        return 1
    except ValueError as exc:
        print("error: {} is not valid JSON: {}".format(args.path, exc), file=sys.stderr)
        return 1

    stats = repo.import_data(data, skip_existing=not args.replace)
    print("imported {} memories, {} entities, {} links ({} skipped)".format(
        stats["memories"], stats["entities"], stats["links"], stats["skipped"]))
    return 0


def cmd_status(args):
    repo, cfg = _repo(args)
    info = repo.status()
    print("backend : {}".format(info["backend"]))
    print("location: {}".format(info["location"]))
    print("config  : {}".format(
        config_mod.LOCAL_CONFIG if os.path.isfile(config_mod.LOCAL_CONFIG) else "(defaults only)"))
    for table, count in sorted(info["counts"].items()):
        print("  {:<12} {}".format(table, count))
    return 0


def cmd_migrate(args):
    """Copy SQLite content into PostgreSQL.

    Read-only on the source: the SQLite file is left intact so a failed or
    partial migration is never destructive.
    """
    cfg = config_mod.load()
    source = get_backend({"storage": {"backend": "sqlite",
                                      "sqlite_path": cfg["storage"]["sqlite_path"]}})
    source.init_schema()

    dsn = args.dsn or cfg["storage"].get("postgres_dsn")
    if not dsn:
        print("No PostgreSQL DSN. Pass --dsn or set storage.postgres_dsn in config.local.json.")
        return 1

    from ..storage.postgres_backend import PostgresBackend
    target = PostgresBackend(dsn)
    target.init_schema()

    moved = 0
    for memory in source.list_memories(limit=1000000, include_expired=True):
        memory["tags"] = decode_tags(memory.get("tags"))
        memory["pinned"] = bool(memory.get("pinned"))
        try:
            target.add_memory(**memory)
            moved += 1
        except Exception as exc:  # noqa: BLE001 - report and continue
            print("skipped memory {}: {}".format(memory.get("id", "?")[:8], exc))

    for kind in ENTITY_KINDS:
        for row in source.list_entities(kind, limit=1000000):
            try:
                target.add_entity(kind, **row)
            except Exception:
                pass

    for memory in source.list_memories(limit=1000000, include_expired=True):
        for link in source.links_for_memory(memory["id"]):
            target.add_link(
                link["memory_id"], link["entity_type"], link["entity_id"], link.get("created_at")
            )

    print("migrated {} memories to PostgreSQL".format(moved))
    print("SQLite source left intact at {}".format(source.path))
    print("Set storage.backend='postgres' in config.local.json to switch.")
    return 0


# ---- parser -------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="ma", description="Memory Archive — portable context capture for AI coding sessions.")
    sub = parser.add_subparsers(dest="command")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--project", help="scope to a project/workstream")
    common.add_argument("-v", "--verbose", action="store_true")

    p = sub.add_parser("doctor", help="probe this machine and recommend a backend")
    p.add_argument("--write", action="store_true", help="save the result to config.local.json")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("init", parents=[common], help="create schema and install guards")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("capture", parents=[common], help="record a memory")
    p.add_argument("type", choices=MEMORY_TYPES)
    p.add_argument("title")
    p.add_argument("body", nargs="?", default="")
    p.add_argument("--tags", help="comma-separated")
    p.add_argument("--link", action="append", help="kind:ref, e.g. person:Jane (repeatable)")
    p.add_argument("--importance", type=float)
    p.add_argument("--session")
    p.add_argument("--source", default="manual")
    p.add_argument("--pin", action="store_true", help="always surface first in recall")
    p.add_argument("--stdin", action="store_true", help="append body from stdin")
    p.set_defaults(func=cmd_capture)

    p = sub.add_parser("recall", parents=[common], help="ranked context within a token budget")
    p.add_argument("--budget", type=int)
    p.add_argument("--limit", type=int)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_recall)

    p = sub.add_parser("search", parents=[common], help="keyword search")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("context", parents=[common], help="everything about one entity")
    p.add_argument("target", help="kind:ref, e.g. system:checkout")
    p.set_defaults(func=cmd_context)

    p = sub.add_parser("entity", parents=[common], help="manage people/systems/work items")
    p.add_argument("kind", choices=ENTITY_KINDS)
    p.add_argument("action", choices=("add", "list"))
    p.add_argument("value", nargs="?", default="")
    p.add_argument("--notes")
    p.add_argument("--limit", type=int, default=100)
    p.set_defaults(func=cmd_entity)

    p = sub.add_parser("export", parents=[common], help="dump the archive")
    p.add_argument("--format", choices=("json", "md"), default="json")
    p.add_argument("--redact", action="store_true", help="keep structure, drop content")
    p.add_argument("--out")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("import", parents=[common],
                       help="load an export file (how content moves between machines)")
    p.add_argument("path", help="path to a JSON export")
    p.add_argument("--replace", action="store_true",
                   help="re-add memories whose id already exists (default: skip)")
    p.set_defaults(func=cmd_import)

    p = sub.add_parser("status", parents=[common], help="backend and counts")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("migrate", parents=[common], help="copy SQLite content to PostgreSQL")
    p.add_argument("--to", choices=("postgres",), default="postgres")
    p.add_argument("--dsn")
    p.set_defaults(func=cmd_migrate)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except ValidationError as exc:
        print("error: {}".format(exc), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
