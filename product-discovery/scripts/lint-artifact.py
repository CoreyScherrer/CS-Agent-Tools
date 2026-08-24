#!/usr/bin/env python3
"""Validate artifacts against protocol/artifact-standards.md.

Usage:
    lint-artifact.py <project-dir> [--artifact PATH] [--quiet]

Exits nonzero if any artifact fails. This is the mechanical quality gate: it does not
depend on a model behaving well, which is what makes it the backstop for the other three.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

PLACEHOLDERS = [
    r"\bTODO\b", r"\bTBD\b", r"\bXXX\b", r"\bFIXME\b",
    r"\bLorem ipsum\b", r"<placeholder>", r"\[insert\b[^\]]*\]",
    r"\[your\b[^\]]*\]", r"\[describe\b[^\]]*\]", r"\[add\b[^\]]*\]",
]
REQUIRED_FM = ["artifact", "stage", "status", "created", "updated",
               "sources", "open_assumptions", "depth"]
VALID_STATUS = {"draft", "reviewed", "final"}
VALID_DEPTH = {"quick", "standard", "deep"}

# A paragraph making a quantitative claim needs a citation or assumption marker.
QUANT = re.compile(
    r"(?<![\w.])\d[\d,]*\.?\d*\s*(%|percent|x\b|hours?|days?|weeks?|months?|users?|"
    r"customers?|requests?|reports?|minutes?|seconds?|k\b|m\b|bn\b)", re.I)
CITED = re.compile(r"\[E-\d+\]|\[ASSUMPTION A-\d+\]")
# Prose that is structural rather than claim-making.
SKIP_LINE = re.compile(r"^\s*(#|\||```|-{3,}|\*\*(Grounded in|Open assumptions|"
                       r"Last critique|Gaps)\b)")


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end]
    body = text[end + 4:]
    fm = {}
    for line in raw.strip().splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm, body


def parse_ids(value):
    if not value:
        return []
    return re.findall(r"[EA]-\d+", value)


def load_ledger_ids(project: Path):
    """Return (evidence_ids, open_assumption_ids, all_assumption_ids)."""
    ev = set()
    findings = project / "evidence" / "findings.md"
    if findings.exists():
        ev = set(re.findall(r"^###\s+(E-\d+)", findings.read_text(), re.M))

    open_a, all_a = set(), set()
    ledger = project / "assumptions.md"
    if ledger.exists():
        text = ledger.read_text()
        for block in re.split(r"^###\s+", text, flags=re.M)[1:]:
            m = re.match(r"(A-\d+)", block)
            if not m:
                continue
            aid = m.group(1)
            all_a.add(aid)
            st = re.search(r"\*\*status:\*\*\s*(\w+)", block)
            if st and st.group(1).strip() == "open":
                open_a.add(aid)
    return ev, open_a, all_a


def lint(path: Path, project: Path, ev_ids, open_ids, all_ids):
    errors, warnings = [], []
    text = path.read_text()
    fm, body = parse_frontmatter(text)

    if fm is None:
        return [f"{path.name}: missing YAML frontmatter"], []

    for key in REQUIRED_FM:
        if key not in fm:
            errors.append(f"{path.name}: frontmatter missing '{key}'")

    if fm.get("status") and fm["status"] not in VALID_STATUS:
        errors.append(f"{path.name}: status '{fm['status']}' not in {sorted(VALID_STATUS)}")
    if fm.get("depth") and fm["depth"] not in VALID_DEPTH:
        errors.append(f"{path.name}: depth '{fm['depth']}' not in {sorted(VALID_DEPTH)}")

    # Placeholder leakage
    for pat in PLACEHOLDERS:
        for m in re.finditer(pat, body, re.I):
            line = body[:m.start()].count("\n") + 1
            errors.append(f"{path.name}:{line}: placeholder {m.group(0)!r}")

    # Provenance section
    if "## Provenance" not in body:
        errors.append(f"{path.name}: missing '## Provenance' section")
    elif "**Gaps:**" not in body:
        warnings.append(f"{path.name}: Provenance has no Gaps subsection")

    # Referential integrity
    srcs = parse_ids(fm.get("sources", ""))
    for sid in srcs:
        if sid not in ev_ids:
            errors.append(f"{path.name}: sources references {sid}, not in evidence/findings.md")

    for aid in parse_ids(fm.get("open_assumptions", "")):
        if aid not in all_ids:
            errors.append(f"{path.name}: open_assumptions references {aid}, not in assumptions.md")
        elif aid not in open_ids:
            errors.append(f"{path.name}: {aid} listed open but its ledger status is not 'open'")

    # Every assumption marked in the body must be declared in frontmatter.
    # Without this the incentive runs toward under-listing, which IS assumption
    # laundering — the anti-pattern protocol/assumptions.md names.
    declared = set(parse_ids(fm.get("open_assumptions", "")))
    for aid in set(re.findall(r"\[ASSUMPTION (A-\d+)\]", body)):
        if aid not in declared:
            errors.append(f"{path.name}: {aid} marked in body but not listed "
                          f"in open_assumptions frontmatter")

    # Unsourced artifact
    stage = fm.get("stage", "")
    if not srcs and not (stage == "1" and fm.get("depth") == "quick"):
        errors.append(f"{path.name}: empty sources list "
                      f"(allowed only at stage 1, depth quick)")

    # Uncited quantitative claims — evaluated per PARAGRAPH, not per line, so a
    # citation that wraps to the next line still counts. protocol/evidence.md
    # specifies paragraph scope.
    line_no = 1
    for para in re.split(r"\n\s*\n", body):
        start = line_no
        line_no += para.count("\n") + 1
        kept = [ln for ln in para.splitlines() if not SKIP_LINE.match(ln)]
        if not kept:
            continue
        text = " ".join(kept)
        if QUANT.search(text) and not CITED.search(text):
            warnings.append(f"{path.name}:{start}: quantitative claim without "
                            f"[E-nnn] or [ASSUMPTION A-nnn]")

    # Staleness
    if fm.get("status") in ("reviewed", "final") and not fm.get("last_critique"):
        errors.append(f"{path.name}: status '{fm['status']}' requires last_critique")

    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", type=Path)
    ap.add_argument("--artifact", type=Path)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    project = args.project
    if not project.is_dir():
        print(f"error: {project} is not a directory", file=sys.stderr)
        return 2

    ev_ids, open_ids, all_ids = load_ledger_ids(project)

    if args.artifact:
        targets = [args.artifact]
    else:
        adir = project / "artifacts"
        targets = sorted(adir.glob("*.md")) if adir.is_dir() else []

    if not targets:
        print("no artifacts found — nothing to lint")
        return 0

    all_err, all_warn = [], []
    for t in targets:
        e, w = lint(t, project, ev_ids, open_ids, all_ids)
        all_err += e
        all_warn += w

    for w in all_warn:
        print(f"  WARN  {w}")
    for e in all_err:
        print(f"  FAIL  {e}")

    n = len(targets)
    if all_err:
        print(f"\n{len(all_err)} error(s), {len(all_warn)} warning(s) across {n} artifact(s)")
        return 1
    if not args.quiet:
        print(f"\nOK — {n} artifact(s) passed, {len(all_warn)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
