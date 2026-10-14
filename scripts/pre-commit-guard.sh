#!/bin/bash
# Pre-commit guard — blocks captured content from ever entering git.
#
# Installed by `ma init` into .git/hooks/pre-commit. It lives on the machine
# holding the content, which is why it is installed rather than committed.
#
# The rule this enforces: the framework is shareable, the captured content is
# not. Gitignore alone is not enough — `git add -f` and a stray `git add -A`
# after an ignore-file edit both bypass it.

set -uo pipefail

STAGED=$(git diff --cached --name-only --diff-filter=ACMR)

BLOCKED=""
while IFS= read -r file; do
    # Framework files that share a name with project state. product-discovery/
    # ships a protocol document called assumptions.md, an empty project scaffold,
    # and a synthetic worked example — none of them are mined content. Exempted by
    # exact prefix so the rule below still catches real project state anywhere.
    case "$file" in
        product-discovery/protocol/*)                continue ;;
        product-discovery/project-template/*)        continue ;;
        product-discovery/examples/worked-example/*) continue ;;
    esac
    case "$file" in
        data/*|*/data/*)              BLOCKED+="  $file  (captured content)"$'\n' ;;
        *.db|*.sqlite|*.sqlite3)      BLOCKED+="  $file  (database)"$'\n' ;;
        config.local.json)            BLOCKED+="  $file  (local config)"$'\n' ;;
        *.env|.env)                   BLOCKED+="  $file  (secrets)"$'\n' ;;
        evidence/*|*/evidence/*)      BLOCKED+="  $file  (mined evidence)"$'\n' ;;
        assumptions.md|*/assumptions.md)
                                      BLOCKED+="  $file  (project ledger)"$'\n' ;;
        artifacts/*|*/artifacts/*)    BLOCKED+="  $file  (project artifact)"$'\n' ;;
    esac
done <<< "$STAGED"

if [[ -n "$BLOCKED" ]]; then
    cat <<EOF

BLOCKED: this commit contains captured content or local config.

$BLOCKED
The framework is shareable. What it captures is not — that stays on this
machine only.

If a file is genuinely framework code and not content, move it out of data/
and rename it. To override deliberately (rare, think first):

    git commit --no-verify

EOF
    exit 1
fi

LOCAL_HOOK="$(git rev-parse --git-dir)/hooks/pre-commit.local"
if [[ -x "$LOCAL_HOOK" ]]; then
    exec "$LOCAL_HOOK" "$@"
fi

exit 0
