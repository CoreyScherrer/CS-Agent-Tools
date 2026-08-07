#!/bin/bash
# Stop hook — session-end sweep.
#
# Prompts rather than captures. Phase 1 makes no LLM call, so nothing here can
# decide what mattered in a session; the model (or you) does that by running the
# capture command. This is a deliberate reminder, not an extraction step.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${MA_PYTHON:-python3}"
PROJECT="${MA_PROJECT:-$PWD}"

command -v "$PYTHON" >/dev/null 2>&1 || exit 0

COUNT=$(cd "$REPO_ROOT" && "$PYTHON" - <<'PY' 2>/dev/null
import datetime, sys
try:
    from ma import config as config_mod
    from ma.storage import get_backend
    backend = get_backend(config_mod.load())
    backend.init_schema()
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    rows = backend.list_memories(limit=500)
    print(sum(1 for r in rows if (r.get("created_at") or "").startswith(today)))
except Exception:
    print("?")
PY
)

echo "[Memory Archive] Session ending. Captured today: ${COUNT:-?}"
echo "[Memory Archive] Worth keeping? Record it before the context is gone:"
echo "  cd $REPO_ROOT && $PYTHON -m ma capture decision \"<what was decided>\" \"<why>\" --project \"$PROJECT\""
echo "  types: decision | learning | pattern | context | preference | question"
exit 0
