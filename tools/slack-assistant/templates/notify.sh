#!/usr/bin/env bash
# notify.sh "message"  — post one line to the sites channel with the assistant's bot token.
# Reads the same env file as the service. Falls back to the assistant channel.
# Post only on change or failure, plus one daily "all green" line.
set -euo pipefail
ENV_FILE="${ENV_FILE:-/etc/slack-assistant/assistant.env}"
# shellcheck disable=SC1090
set -a; . "$ENV_FILE"; set +a
channel="${SLACK_CHANNEL_SITES:-$SLACK_CHANNEL_ASSISTANT}"
text="${1:?usage: notify.sh \"message\"}"
curl -sS -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H 'Content-type: application/json; charset=utf-8' \
  --data "$(printf '{"channel":"%s","text":%s}' "$channel" "$(printf '%s' "$text" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')")" \
  | grep -q '"ok":true' || { echo "notify.sh: Slack post failed" >&2; exit 1; }
