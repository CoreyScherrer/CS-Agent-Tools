#!/bin/bash
# SessionStart hook — injects archived context at the start of a session.
#
# Two properties matter more than features here:
#
#   Fail-loud. If the archive cannot be read, say so visibly. Silent failure is
#   the known root cause of context quietly never reaching the model.
#
#   Never block. Always exit 0. A broken hook must not stop the user working.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${MA_PYTHON:-python3}"
BUDGET="${MA_TOKEN_BUDGET:-2000}"
PROJECT="${MA_PROJECT:-$PWD}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "[Memory Archive] ERROR: '$PYTHON' not found. Context NOT loaded."
    echo "[Memory Archive] Set MA_PYTHON to a working interpreter."
    exit 0
fi

OUTPUT=$(cd "$REPO_ROOT" && "$PYTHON" -m ma recall \
    --project "$PROJECT" --budget "$BUDGET" 2>&1)
STATUS=$?

if [[ $STATUS -ne 0 ]]; then
    echo "[Memory Archive] ERROR: recall failed (exit $STATUS). Context NOT loaded."
    echo "[Memory Archive] Diagnose with: cd $REPO_ROOT && $PYTHON -m ma status"
    echo "$OUTPUT" | head -5
    exit 0
fi

echo "$OUTPUT"
echo "[Memory Archive] Capture with: $PYTHON -m ma capture <type> \"<title>\" \"<body>\""
exit 0
