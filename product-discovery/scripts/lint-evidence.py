#!/usr/bin/env python3
"""Validate the evidence base and assumption ledger.

Usage:
    lint-evidence.py <project-dir> [--quiet]

The framework's thesis is that the mechanical gate does not depend on a model behaving
well. Artifacts derive their trustworthiness from evidence/findings.md and assumptions.md,
so those two files need checking at least as much as the artifacts do.
"""
import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

FINDING_FIELDS = ["claim", "source", "source_type", "date", "confidence", "supports"]
ASSUMPTION_FIELDS = ["assumption", "why_assumed", "impact_if_wrong", "what_it_affects",
                     "owner", "how_to_validate", "status"]

SOURCE_TYPES = {"artifact", "existing_artifact", "document", "reference_doc",
                "conversation", "interview", "system", "intake", "observation", "conflict"}
CONFIDENCE = {"high", "medium", "low"}
IMPACT = {"high", "medium", "low"}
STATUS = {"open", "validated", "invalidated", "accepted"}
# `unknown` is legal where a source genuinely has no creation date; `~` prefixes an
# approximate date, and `..` separates a range (use the later bound for staleness).
DATE_OK = re.compile(r"^(unknown|~?\d{4}-\d{2}-\d{2}(\.\.\d{4}-\d{2}-\d{2})?)$")


def parse_blocks(text, prefix):
    """Return [(id, {field: value}, line_no)] for ### <PREFIX>-nnn blocks."""
    out = []
    for m in re.finditer(r"^###\s+(" + prefix + r"-\d+)\s*$", text, re.M):
        bid = m.group(1)
        line_no = text[:m.start()].count("\n") + 1
        nxt = re.search(r"^###\s+", text[m.end():], re.M)
        block = text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]
        fields = {}
        # `[^\S\n]*` = horizontal whitespace only. Plain `\s*` would let an empty
        # field swallow the following line as its value, silently hiding a missing field.
        for fm in re.finditer(r"^[^\S\n]*-[^\S\n]+\*\*(\w+):\*\*[^\S\n]*(.*)$",
                              block, re.M):
            fields[fm.group(1)] = fm.group(2).strip()
        out.append((bid, fields, line_no))
    return out


def check_findings(path: Path):
    errors, warnings = [], []
    if not path.exists():
        return [f"{path}: missing — mine-corpus must create it"], [], set()
    text = path.read_text()
    blocks = parse_blocks(text, "E")
    seen = set()
    today = date.today()

    for bid, f, ln in blocks:
        if bid in seen:
            errors.append(f"findings.md:{ln}: duplicate {bid}")
        seen.add(bid)

        for field in FINDING_FIELDS:
            if field not in f or not f[field]:
                errors.append(f"findings.md:{ln}: {bid} missing '{field}'")

        st = f.get("source_type", "")
        if st and st not in SOURCE_TYPES:
            errors.append(f"findings.md:{ln}: {bid} source_type '{st}' "
                          f"not in {sorted(SOURCE_TYPES)}")

        cf = f.get("confidence", "")
        if cf and cf not in CONFIDENCE:
            errors.append(f"findings.md:{ln}: {bid} confidence '{cf}' "
                          f"not in {sorted(CONFIDENCE)}")

        d = f.get("date", "")
        if d and not DATE_OK.match(d):
            errors.append(f"findings.md:{ln}: {bid} date '{d}' malformed "
                          f"(YYYY-MM-DD, ~YYYY-MM-DD, YYYY-MM-DD..YYYY-MM-DD, or 'unknown')")
        elif d and d != "unknown":
            latest = d.lstrip("~").split("..")[-1]
            try:
                parsed = datetime.strptime(latest, "%Y-%m-%d").date()
                if parsed > today:
                    errors.append(f"findings.md:{ln}: {bid} date {latest} is in the future")
                elif (today - parsed).days > 730:
                    warnings.append(f"findings.md:{ln}: {bid} source is over 2 years old "
                                    f"({latest}) — verify it still describes today")
            except ValueError:
                errors.append(f"findings.md:{ln}: {bid} date '{latest}' is not a real date")

        # An unknown or approximate date cannot support high confidence: if you cannot
        # date a source you cannot know it is current.
        if d in ("unknown",) and cf == "high":
            errors.append(f"findings.md:{ln}: {bid} confidence 'high' with unknown date")

        if cf == "high" and st == "conversation":
            warnings.append(f"findings.md:{ln}: {bid} conversation source at high "
                            f"confidence — recollection is rarely high")

    if not blocks:
        warnings.append("findings.md: no findings recorded")
    return errors, warnings, seen


def check_assumptions(path: Path, evidence_ids):
    errors, warnings = [], []
    if not path.exists():
        return [f"{path}: missing"], [], {}
    text = path.read_text()
    blocks = parse_blocks(text, "A")
    seen, by_id = set(), {}

    for bid, f, ln in blocks:
        if bid in seen:
            errors.append(f"assumptions.md:{ln}: duplicate {bid}")
        seen.add(bid)
        by_id[bid] = f

        for field in ASSUMPTION_FIELDS:
            if field not in f or not f[field]:
                errors.append(f"assumptions.md:{ln}: {bid} missing '{field}'")

        imp = f.get("impact_if_wrong", "")
        if imp and imp not in IMPACT:
            errors.append(f"assumptions.md:{ln}: {bid} impact_if_wrong '{imp}' "
                          f"not in {sorted(IMPACT)}")

        stat = f.get("status", "")
        if stat and stat not in STATUS:
            errors.append(f"assumptions.md:{ln}: {bid} status '{stat}' "
                          f"not in {sorted(STATUS)}")

        if stat in ("validated", "invalidated", "accepted"):
            if not f.get("resolution"):
                errors.append(f"assumptions.md:{ln}: {bid} status '{stat}' "
                              f"requires 'resolution'")
            if stat == "validated":
                refs = re.findall(r"E-\d+", f.get("resolution", ""))
                if not refs:
                    warnings.append(f"assumptions.md:{ln}: {bid} validated but resolution "
                                    f"cites no evidence ID")
                for r in refs:
                    if r not in evidence_ids:
                        errors.append(f"assumptions.md:{ln}: {bid} resolution cites {r}, "
                                      f"not in findings.md")
            if stat == "accepted" and not re.search(r"\w", f.get("owner", "")):
                errors.append(f"assumptions.md:{ln}: {bid} 'accepted' requires a named "
                              f"owner accepting the risk")

        if f.get("how_to_validate", "").lower() in ("unknown", "tbd", "n/a", "none"):
            errors.append(f"assumptions.md:{ln}: {bid} how_to_validate is empty in substance "
                          f"— an assumption with no validation path is a guess with an ID")

    return errors, warnings, by_id


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", type=Path)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    proj = args.project
    if not proj.is_dir():
        print(f"error: {proj} is not a directory", file=sys.stderr)
        return 2

    e1, w1, ev_ids = check_findings(proj / "evidence" / "findings.md")
    e2, w2, assums = check_assumptions(proj / "assumptions.md", ev_ids)

    errors, warnings = e1 + e2, w1 + w2

    # Surface the DEFINE gate early rather than letting it ambush at stage 4.
    open_high = [a for a, f in assums.items()
                 if f.get("status") == "open" and f.get("impact_if_wrong") == "high"]
    if open_high:
        warnings.append(
            f"assumptions.md: {len(open_high)} high-impact assumption(s) open "
            f"({', '.join(sorted(open_high))}) — these block advancement past DEFINE. "
            f"Validate them, or have a named person accept the risk.")

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) — "
              f"{len(ev_ids)} finding(s), {len(assums)} assumption(s)")
        return 1
    if not args.quiet:
        print(f"\nOK — {len(ev_ids)} finding(s), {len(assums)} assumption(s), "
              f"{len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
