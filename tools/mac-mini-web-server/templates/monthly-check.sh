#!/usr/bin/env bash
# monthly-check.sh — the "keeping it alive" checklist as a script. Run on the server as admin.
# Edit the three variables; everything else is generic. Exit code = number of failures.
set -u
HOSTS="example.com admin.example.com"       # every public hostname
SERVICES="com.example.svc"                 # every launchd label
ROLE_FILE="/etc/acme/role"
fail=0; ok(){ echo "ok   $*"; }; bad(){ echo "FAIL $*"; fail=$((fail+1)); }

[ "$(cat "$ROLE_FILE" 2>/dev/null)" = "prod" ] && ok "role file says prod" || bad "role file missing or not prod"
pgrep -x nginx >/dev/null && ok "nginx running" || bad "nginx not running"
sudo nginx -t >/dev/null 2>&1 && ok "nginx -t" || bad "nginx -t (did an OS update delete a log dir?)"
for h in $HOSTS; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "https://$h/" || echo 000)
  case "$code" in 200|301|302) ok "$h -> $code";; *) bad "$h -> $code";; esac
done
for s in $SERVICES; do
  sudo launchctl print "system/$s" 2>/dev/null | grep -q 'state = running' && ok "$s running" || bad "$s not running"
done
tailscale status 2>/dev/null | grep -qi expired && bad "tailscale: a key is expired" || ok "tailscale: no expired keys"
listeners=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | grep -v '127.0.0.1\|\[::1\]' | grep -v '^COMMAND' || true)
[ -z "$listeners" ] && ok "no non-loopback listeners" || { bad "non-loopback listeners:"; echo "$listeners"; }
echo; echo "manual: tunnel shows exactly one connector; last backup on NAS + offsite; one restic restore; rulesets still four rules"
exit $fail
