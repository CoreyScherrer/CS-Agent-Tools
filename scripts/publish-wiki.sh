#!/bin/bash
# Publish docs/wiki/*.md to the GitHub wiki.
#
# A GitHub wiki is a separate git repository (<repo>.wiki.git). GitHub does not
# create it until the first page is made through the web UI, so that one step
# cannot be automated — this script says so plainly rather than failing obscurely.
#
# Source of truth is docs/wiki/ in the main repo: version-controlled with the
# code, reviewable in PRs. The wiki is a published copy.
#
# Usage:  scripts/publish-wiki.sh [--dry-run]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WIKI_SRC="$REPO_ROOT/docs/wiki"
WIKI_REMOTE="${MA_WIKI_REMOTE:-https://github.com/CoreyScherrer/PORTABLE-WORK.wiki.git}"
DRY_RUN=0

[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

if [[ ! -d "$WIKI_SRC" ]]; then
    echo "ERROR: no docs/wiki/ directory at $WIKI_SRC" >&2
    exit 1
fi

PAGE_COUNT=$(find "$WIKI_SRC" -name '*.md' -type f | wc -l | tr -d ' ')
if [[ "$PAGE_COUNT" -eq 0 ]]; then
    echo "ERROR: no .md files in $WIKI_SRC" >&2
    exit 1
fi

echo "Publishing $PAGE_COUNT pages from docs/wiki/"
echo "Target: $WIKI_REMOTE"
echo

if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry run) would publish:"
    find "$WIKI_SRC" -name '*.md' -type f -exec basename {} \; | sort | sed 's/^/  /'
    exit 0
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

if ! git clone -q "$WIKI_REMOTE" "$TMP_DIR/wiki" 2>/dev/null; then
    cat <<EOF
ERROR: could not clone the wiki repository.

The most likely cause is that the wiki has never been initialised. GitHub only
creates <repo>.wiki.git after the first page is saved in the browser.

To fix (one time):
  1. Open the repository's Wiki tab on GitHub
  2. Click "Create the first page"
  3. Save anything at all — this script overwrites it
  4. Re-run: scripts/publish-wiki.sh

If the wiki IS initialised, check that you have push access and that
credentials are configured for: $WIKI_REMOTE
EOF
    exit 1
fi

# Replace rather than merge: docs/wiki/ is the source of truth, so a page
# deleted there should disappear from the published wiki too.
find "$TMP_DIR/wiki" -maxdepth 1 -name '*.md' -type f -delete
cp "$WIKI_SRC"/*.md "$TMP_DIR/wiki/"

cd "$TMP_DIR/wiki"
if [[ -z "$(git status --porcelain)" ]]; then
    echo "Wiki already up to date — nothing to publish."
    exit 0
fi

git add -A
git commit -q -m "docs: sync wiki from docs/wiki/ ($PAGE_COUNT pages)"
git push -q origin HEAD

echo "Published $PAGE_COUNT pages."
git -C "$TMP_DIR/wiki" log --oneline -1
