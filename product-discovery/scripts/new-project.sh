#!/usr/bin/env bash
# Start a new engagement from the project template.
#
# Usage: scripts/new-project.sh <project-name> [target-dir]
#
# Creates a project directory with the corpus manifest, empty evidence base, empty
# assumption ledger, and artifact directories. The framework repo stays clean; project
# state lives with the project.
set -euo pipefail

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ $# -lt 1 ]; then
    echo "usage: $0 <project-name> [target-dir]" >&2
    exit 2
fi

NAME="$1"
TARGET="${2:-./$NAME}"

if [ -e "$TARGET" ]; then
    echo "error: $TARGET already exists — refusing to overwrite" >&2
    exit 1
fi

cp -R "$FRAMEWORK_DIR/project-template" "$TARGET"
TODAY="$(date +%Y-%m-%d)"

# Seed the manifest with project name and date, portably (BSD and GNU sed differ on -i).
MANIFEST="$TARGET/corpus.yaml"
tmp="$(mktemp)"
sed -e "s|^project: \"\"|project: \"$NAME\"|" \
    -e "s|^updated: \"\"|updated: \"$TODAY\"|" \
    "$MANIFEST" > "$tmp" && mv "$tmp" "$MANIFEST"

cat > "$TARGET/README.md" <<INNER
# $NAME

Project workspace. Framework: Masterful Product Swashbuckling.

## State

- \`corpus.yaml\` — what this project can mine. Fill this in first.
- \`evidence/findings.md\` — the evidence base. Every artifact cites into this.
- \`evidence/sources.md\` — what was actually mined, and how completely.
- \`assumptions.md\` — running ledger. High-impact open assumptions block DEFINE.
- \`artifacts/\` — deliverables, numbered by stage.
- \`artifacts/critiques/\` — adversarial review records.

## Validate

    python3 $FRAMEWORK_DIR/scripts/lint-artifact.py .
    python3 $FRAMEWORK_DIR/scripts/lint-evidence.py .

Started $TODAY.
INNER

echo "Created $TARGET"
echo
echo "Next:"
echo "  1. Fill in corpus.yaml — declare what you can mine"
echo "  2. Run frame-problem to state the problem"
echo "  3. Run mine-corpus to build the evidence base"
echo
echo "See $FRAMEWORK_DIR/examples/worked-example/ for a complete FRAME + MINE pass."
