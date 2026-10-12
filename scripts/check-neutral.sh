#!/usr/bin/env bash
# check-neutral.sh [paths...] — flag text that looks like someone's real
# infrastructure rather than a portable example. Exit 1 on any hit.
#
# Usage: scripts/check-neutral.sh docs/wiki/Slack-Assistant.md tools/slack-assistant
# Default: docs/wiki tools skills agents README.md
#
# It is a heuristic, not a secret scanner. Pair it with gitleaks or similar for
# credentials. Allowed placeholders: example.com, example.net, acme, your-mini,
# hooks.example.com, 192.0.2.x / 198.51.100.x / 203.0.113.x (RFC 5737), 100.64.0.0/10
# shown as 100.x.y.z only when all octets are literally "x", "y", "z".
set -uo pipefail
cd "$(dirname "$0")/.."
paths=("$@")
[ ${#paths[@]} -eq 0 ] && paths=(docs/wiki tools skills agents README.md)

fail=0
hit() { printf '%s\n' "$1"; fail=1; }

# 1. Real-looking hostnames that are not documentation domains.
out=$(grep -rnoE '\b[a-z0-9-]+\.(com|net|org|io|dev|app|ts\.net)\b' "${paths[@]}" 2>/dev/null \
  | grep -vE '(example\.(com|net|org)|slack\.com|api\.slack\.com|cloudflare\.com|github\.com|anthropic\.com|google\.com|googleapis\.com|tailscale\.com|ui\.com|apple\.com|claude\.com|claude\.ai|docs\.[a-z]+\.com|developers\.[a-z]+\.com|console\.[a-z]+\.com|one\.dash\.cloudflare\.com|dash\.cloudflare\.com|fonts\.googleapis\.com|pushover\.net|open-meteo\.com|login\.tailscale\.com|brew\.sh|python\.org|homebrew\.[a-z]+|nginx\.org|github\.io|caddyserver\.com|letsencrypt\.org|openai\.com|pypi\.org|npmjs\.com|microsoft\.com|ubnt\.com|unifi\.ui\.com)' )
[ -n "$out" ] && hit "Hostnames that are not documentation domains:
$out"

# 2. IPv4 addresses outside RFC 5737 documentation ranges and the obvious loopback.
out=$(grep -rnoE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "${paths[@]}" 2>/dev/null \
  | grep -vE '(127\.0\.0\.1|0\.0\.0\.0|192\.0\.2\.|198\.51\.100\.|203\.0\.113\.|192\.168\.(1|10|20|30|100)\.(0|1|254)|10\.0\.0\.(0|1)|100\.64\.0\.0|255\.255\.255\.)')
[ -n "$out" ] && hit "IP addresses that are not documentation addresses:
$out"

# 3. Home-directory paths and macOS user paths that are not placeholders.
out=$(grep -rnoE '/Users/[A-Za-z0-9_-]+|/home/[A-Za-z0-9_-]+' "${paths[@]}" 2>/dev/null \
  | grep -vE '/Users/(you|svc-[a-z-]+|web|acme|<[a-z-]+>|\$[A-Z_]+)|/home/(you|svc-[a-z-]+|acme|<[a-z-]+>|\$[A-Z_]+)')
[ -n "$out" ] && hit "Real-looking home paths:
$out"

# 4. Slack/Google/Cloudflare-looking identifiers that are not the zero placeholders.
out=$(grep -rnoE '\b(xox[bap]-[A-Za-z0-9-]{10,}|[UC]0[A-Z0-9]{8,}|AKIA[0-9A-Z]{16}|sk-ant-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{10,})\b' "${paths[@]}" 2>/dev/null \
  | grep -vE '([UC]0{10}|xoxb-paste-here)')
[ -n "$out" ] && hit "Identifiers that look real:
$out"

# 5. Email addresses other than documentation ones.
out=$(grep -rnoE '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}\b' "${paths[@]}" 2>/dev/null \
  | grep -vE '@example\.(com|net|org)')
[ -n "$out" ] && hit "Email addresses:
$out"

if [ $fail -eq 0 ]; then
  echo "check-neutral: clean (${paths[*]})"
fi
exit $fail
