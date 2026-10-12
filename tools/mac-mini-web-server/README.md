# Mac Mini Web Server

A home server on a Mac mini: public sites through an outbound-only tunnel, private
admin over a mesh VPN, one unprivileged macOS user per internet-facing service, a
protected `main`, drilled rollback, outbound backups. No port forwards.

**The guide is the wiki page:** [docs/wiki/Mac-Mini-Web-Server.md](../../docs/wiki/Mac-Mini-Web-Server.md).

`templates/` holds the files your agent copies and fills in:

| File | Use in phase |
|---|---|
| `com.example.service.plist` | Phase 5 — launchd daemon per service, with the gotchas as comments |
| `nginx-site.conf` | Phase 6 — a vhost with named upstream, real-IP, logs outside `/var/log`, single cache header |
| `tailscale-acl.jsonc` | Phase 3 — the smallest safe personal-tailnet policy |
| `unifi-firewall-rules.md` | Phase 2 — the VLAN and rule list, in order |
| `monthly-check.sh` | Phase 9/10 — the "keeping it alive" checklist as a script |
