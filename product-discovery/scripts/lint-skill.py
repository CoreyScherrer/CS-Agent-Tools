#!/usr/bin/env python3
"""Validate skill definitions for structural consistency.

Usage:
    lint-skill.py <framework-dir> [--quiet]

Skills are hand-written prose and drift silently. This catches missing frontmatter,
missing required sections, broken cross-references, and Output Contracts that do not
declare a path.
"""
import argparse
import re
import sys
from pathlib import Path

REQUIRED_FM = ["name", "description", "stage", "inputs", "outputs", "depth"]
REQUIRED_SECTIONS = [
    "## Purpose",
    "## When To Use",
    "## When Not To Use",
    "## Process",
    "## Output Contract",
    "## Evidence Requirements",
    "## Pitfalls",
    "## References",
]
VALID_STAGES = {"0", "1", "2", "3", "4", "5", "6", "7", "any"}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, text[end + 4:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("framework", type=Path)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    root = args.framework

    skills = sorted(root.glob("skills/*/SKILL.md")) + \
             sorted(root.glob("domains/*/skills/*/SKILL.md"))
    if not skills:
        print("no skills found", file=sys.stderr)
        return 2

    names = {}
    errors, warnings = [], []

    for p in skills:
        rel = p.relative_to(root)
        text = p.read_text()
        fm, body = parse_frontmatter(text)

        if fm is None:
            errors.append(f"{rel}: missing frontmatter")
            continue

        for k in REQUIRED_FM:
            if k not in fm:
                errors.append(f"{rel}: frontmatter missing '{k}'")

        nm = fm.get("name", "")
        if nm:
            if nm != p.parent.name:
                errors.append(f"{rel}: name '{nm}' != directory '{p.parent.name}'")
            if nm in names:
                errors.append(f"{rel}: duplicate skill name '{nm}' (also {names[nm]})")
            names[nm] = rel
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", nm):
                errors.append(f"{rel}: name '{nm}' is not kebab-case")

        desc = fm.get("description", "")
        if desc and not re.search(r"\bUse (when|during|at|after|alongside|before|"
                                  r"immediately|on|in|for|this|whenever|wherever|any)\b", desc):
            warnings.append(f"{rel}: description has no 'Use ...' trigger clause")
        if len(desc) > 400:
            warnings.append(f"{rel}: description is {len(desc)} chars (long)")

        st = fm.get("stage", "")
        if st and st not in VALID_STAGES:
            errors.append(f"{rel}: stage '{st}' not in {sorted(VALID_STAGES)}")

        # Required sections, in order
        pos = -1
        for sec in REQUIRED_SECTIONS:
            idx = body.find("\n" + sec)
            if idx == -1:
                errors.append(f"{rel}: missing section '{sec}'")
            elif idx < pos:
                errors.append(f"{rel}: section '{sec}' out of order")
            else:
                pos = idx

        # Output Contract must declare a path
        m = re.search(r"## Output Contract\n(.*?)(?=\n## )", body, re.S)
        # A skill either writes a new artifact (**Path:**) or modifies an existing
        # one (**Modifies:**). Both are legitimate contracts.
        if m and not re.search(r"\*\*(Path|Paths|Modifies)", m.group(1)):
            errors.append(f"{rel}: Output Contract declares neither "
                          f"**Path:** nor **Modifies:**")

        # Cross-references to protocol files must resolve
        for ref in set(re.findall(r"`(protocol/[a-z-]+\.md)`", body)):
            if not (root / ref).exists():
                errors.append(f"{rel}: references missing {ref}")

        # Referenced scripts must exist
        for ref in set(re.findall(r"`(scripts/[a-z-]+\.py)`", body)):
            if not (root / ref).exists():
                errors.append(f"{rel}: references missing {ref}")

    # Cross-skill references resolve to real skills
    for p in skills:
        rel = p.relative_to(root)
        body = p.read_text()
        m = re.search(r"\*\*Related skills:\*\*(.*?)(?=\n\n|\n\*\*)", body, re.S)
        if not m:
            warnings.append(f"{rel}: no 'Related skills' line in References")
            continue
        for cand in re.findall(r"`([a-z0-9-]+)`", m.group(1)):
            if cand not in names:
                errors.append(f"{rel}: Related skills names unknown skill '{cand}'")

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) "
              f"across {len(skills)} skill(s)")
        return 1
    if not args.quiet:
        print(f"\nOK — {len(skills)} skill(s) passed, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
