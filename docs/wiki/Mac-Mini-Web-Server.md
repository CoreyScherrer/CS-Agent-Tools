# Mac Mini Web Server

_Your own always-on server at home: public sites through a tunnel, private admin
through a mesh VPN, one unprivileged user per thing that faces the internet._

> Why, hello there, home-owner of tomorrow! I see you've wandered into your next
> journey through the wonderful world of Artificial Intelligence and its many
> marvellous capabilities. On this particular expedition we'll guide you, step by
> confident step, through the choices and considerations that make **your very own
> Mac Mini Web Server** a whimsical success — a humming little box on a shelf that
> serves the world by day, backs itself up by night, and never once asks for a
> port forward. Roll up your sleeves; the future is small, silver, and surprisingly
> quiet.

**Start here:** read §1–§3, make the Phase 0 decisions, then hand this page to
your AI agent and work the phases in order. Building the [[Slack-Assistant]] on top
is a natural next journey; its server phase is this page.

## 1. What this tool is

A Mac mini on your home network that hosts websites and small services on the
public internet **without opening a single inbound port** on your router. Public
traffic arrives through an outbound-only tunnel (Cloudflare). You administer it
over a private mesh VPN (Tailscale). Every internet-facing service runs as its own
unprivileged macOS user from a deployed tree, not from your home folder, and
code reaches production only through a pull request on a protected branch.

What you end up with:

- A Mac mini with a role file, a dedicated service account per site, a reverse
  proxy (nginx), and a process supervisor (launchd) that survives reboots.
- Public hostnames on your domain, served through a Cloudflare Tunnel on the free
  plan, with an admin area behind Cloudflare Access.
- A private path (Tailscale) for SSH and anything that should never be public.
- A GitHub repo with a protected `main`, deploy keys per machine, and a deploy
  script that only deploys what is merged.
- Nightly backups pushed off the box, and a routine for OS updates that does not
  take the sites down.

What it is *not*: a Docker host (containers are a later, optional layer — the
isolation here is macOS users), a general cloud, or a replacement for a VPS if you
need five nines. It is the right size for personal sites, a handful of small
services, a family app, and the bots that talk to them.

## 2. Who this is for, and what you need

For one person who wants to own their infrastructure, is comfortable letting an
AI agent run the shell, and will do the few dashboard clicks only a human can.

**Hardware**

- Any Apple-silicon Mac mini. 16 GB RAM is comfortable; 8 GB works for static
  sites and small Python apps. (An Intel mini works but the toolchain paths
  differ — see the Homebrew gotcha — and Apple's support window is shorter.)
- Wired Ethernet to your router. Wi-Fi is a reliability gotcha, not a saving.
- A router that can make a separate VLAN and firewall rules between VLANs.
  UniFi gear is used as the worked example; any router with VLANs will do.
- Optional: a NAS or external disk for local backups; a UPS.

**Accounts and services**

| Service | Needed for | Free tier enough? |
|---|---|---|
| A domain name | public hostnames | ~$10–15/year, any registrar |
| Cloudflare | DNS, Tunnel, Access, WAF rules, origin cert | **Yes** (Free plan) |
| Tailscale | private admin network | **Yes** (Personal plan) |
| GitHub | code, protected `main`, deploy keys, CI | Free for public repos; **Pro or an org on Team** for branch rulesets on *private* repos — see §Free vs paid |
| Backblaze B2 (or any S3-compatible bucket) | offsite backup | 10 GB free, then pennies |
| Apple ID | the mini itself | Free |

**Software and tools** (the agent installs these)

- Homebrew; nginx; Python 3.12+; PostgreSQL (if any app needs a DB); `cloudflared`;
  Tailscale (the standalone/daemon build, not only the App Store app); `gh`;
  `restic`; `gitleaks`.

## 3. Setup time

| | Estimate |
|---|---|
| Human hands-on time | 3–5 hours: unboxing, Setup Assistant, router UI, Cloudflare and Tailscale dashboards, GitHub settings, pasting secrets |
| AI agent working time | 6–10 hours across several sessions |
| Elapsed | A weekend for a first site; a second weekend to harden, back up and drill rollback |

Human-blocking steps: first boot and account naming, router VLAN and firewall
rules, every "make this public" click (DNS, tunnel route, Access policy), GitHub
plan choice, and physical cabling.

## 4. Working with your AI agent on this guide

- **Where to run the agent.** For Phase 1 you are at the mini's keyboard (or
  Screen Sharing). From Phase 3 on, run the agent over SSH/Remote-SSH **into the
  mini** so every path, user and service is real. Start every session by having
  it run `hostname && whoami` — it is very easy to run a command on the wrong box.
- **Give it a browser.** Router UI, Cloudflare, Tailscale admin and GitHub
  settings are all forms. Let the agent drive them (Claude Desktop with the Chrome
  extension or built-in browser; or the Chrome extension from Claude Code) and
  you click the final Save / Approve.
- **Secrets never go through chat.** Tunnel tokens, API tokens and deploy keys
  are pasted by you into the file the agent names. Anything pasted into a chat is
  burned: rotate it.
- **GUI commands act on the mini's screen.** Over SSH, `open`, `pbcopy` and
  Keychain imports happen on the mini, not on the laptop you're typing on. Screen
  Share first, or avoid GUI steps.
- **A way to talk to the result:** by the end, your sites answer on your domain,
  your agent reaches the box over Tailscale, and (optionally) the box reports to
  you in a Slack channel via the [[Slack-Assistant]].

## 5. The phases

### Phase 0 — Decide the shape

**Goal:** five choices that are expensive to reverse, written down before anything
is installed.

| Decision | Options | Our default |
|---|---|---|
| Public ingress | **Cloudflare Tunnel** (outbound-only, no port forward, free) vs port-forward + Let's Encrypt | **Tunnel.** Port forwarding was considered and rejected: it exposes your home IP and needs inbound firewall holes. |
| Isolation model | **One macOS user per internet-facing service** vs Docker containers vs everything as admin | **Users.** Containers are "last, after the boundaries exist" — optional in Phase 11. Never admin. |
| Private admin path | **Tailscale** vs SSH over the tunnel vs LAN only | **Tailscale** for SSH; tunnel + Access for web admin pages. |
| Repo visibility | Public repo (free rulesets) vs private repo on **GitHub Pro / org Team** | **Private on a paid tier** if the repo will hold anything about your home setup; public only for code you'd publish anyway. |
| Disk encryption | FileVault **on** (secure at rest; needs a password at boot, so no unattended reboot) vs **off** + auto-login (unattended reboots, less at-rest security) | **Off + auto-login** for a headless server in your own home that must come back after a power cut; **on** if the box ever leaves the house. Decide once; the security scan will nag about whichever you pick. |

**Done when:** the five answers are at the top of your server repo's README.

### Phase 1 — First boot

**Goal:** a machine that comes back on its own after power loss and whose
identity is unambiguous.

Human steps:

1. **Pick the admin short name now and never change it.** Every service path,
   plist and script will embed `/Users/<shortname>`. Renaming later breaks
   everything.
2. Set the hostname to what the box *is* (`web-prod`, not `new-mini`). Later,
   nothing is allowed to gate on hostname — see step 5 — but humans read it.
3. Wired Ethernet in. Note the Ethernet MAC address (System Settings → Network →
   Details) — the router needs it in Phase 2.
4. Turn on Remote Login (SSH) and Screen Sharing for your admin user only.

Agent steps:

5. Create a **role file**: `sudo mkdir -p /etc/<org> && echo prod | sudo tee /etc/<org>/role`.
   Every scheduled job will check this file, so a backup/staging clone with an
   identical disk never runs production jobs. Hostnames lie; the role file
   doesn't.
6. Power behaviour: `sudo pmset -a autorestart 1 sleep 0 disksleep 0 womp 1`;
   Energy Saver → "Start up automatically after a power failure".
7. Auto-login on (if FileVault off), screen lock off, no sleep. Software Update:
   download automatically, **do not** install automatically (Phase 10 owns that).
8. `softwareupdate --install-rosetta --agree-to-license` only if you need Intel
   binaries.

**Done when:** `sudo pmset -g | grep -E 'autorestart|sleep'` shows `1`/`0`, and
`cat /etc/<org>/role` prints `prod`; pull the plug, plug back in, and SSH works
within two minutes without touching the keyboard.

**Gotchas in this phase**

- *The box named "-staging" was actually production.* Humans and scripts trusted
  the hostname. Use the role file for anything automated.
- *Two near-identical machines, same home paths.* Commands pasted into the wrong
  window. Name the machine in every instruction you write for yourself.

### Phase 2 — Router: a VLAN of its own (UniFi as the worked example)

**Goal:** the server lives on its own network segment that cannot reach your
laptops, phones and TVs, and nothing from the internet is forwarded to it.

> No historical lessons exist for this phase in the source project — it was set
> up once, early, and never caused an incident. The recommendations below are
> standard practice; verify menu names against your current UniFi Network version.

Human steps (the agent can drive the UI; you approve):

1. **Networks → Create:** a new network `Servers`, VLAN ID e.g. `20`, its own
   subnet (`192.168.20.0/24`), DHCP on. Keep "Isolate network" **off** (the mini
   must still reach the internet) — isolation is done with firewall rules so you
   can allow the one or two exceptions you want.
2. **DHCP reservation** for the mini's Ethernet MAC (`192.168.20.10`). At a future
   hardware swap, move the reservation to the new MAC — the IP follows.
3. **Firewall rules (LAN In), in this order:**
   - Allow `Servers` → `Servers` (itself).
   - Allow **established/related** return traffic.
   - **Drop** `Servers` → every other local network (your home LAN, IoT, guest).
   - Allow your home LAN → `Servers` on the ports you need for direct admin (SSH
     22, and nothing else), or skip this and admin only over Tailscale (our default).
   - Default: `Servers` → Internet allowed (the tunnel and Tailscale are outbound).
4. **Port forwarding: none.** Nothing in this guide needs it. If you see a
   forward you didn't create, that is a finding.
5. Put the mini's switch port on the `Servers` VLAN (native/untagged for that
   port), or set the VLAN on the mini's Ethernet if you prefer tagged.
6. Optional: a **UniFi traffic rule** blocking the `Servers` network from the
   router's own management UI except from your admin VLAN.

**Done when:** from the mini, `ping` to a device on your home LAN **fails** and
`curl -sI https://cloudflare.com` **succeeds**; from a laptop on the home LAN, SSH
to the mini's LAN IP fails (unless you chose the explicit allow) and works over
Tailscale after Phase 3.

**Gotchas in this phase**

- *The NAS is on the home LAN; the server can't reach it to back up.* That is the
  rule working. Reach it over Tailscale (Phase 3) or put the NAS on the Servers
  VLAN too, and keep a LAN-side recovery path you have actually tested.
- *An unmanaged switch inserted between a PoE source and a PoE device starves
  the device: no link light, looks like a dead cable.* Use a PoE switch or an
  active 802.3af/at injector; never a passive one.
- *Two boxes behind one WAN IP are indistinguishable to the outside.* Anything
  that identifies a machine by source IP (tunnel connectors, allowlists) will
  confuse them. Identify by role file, hostname header, or connector metadata.

### Phase 3 — Tailscale: the private path

**Goal:** you and your agent reach the mini over an encrypted mesh with no open
ports, and the box stays reachable after key expiry would have bitten.

Human steps:

1. Create a tailnet (sign in with GitHub or Google). Install Tailscale on your
   laptop and phone.
2. On the mini, install the **standalone daemon build** (`brew install tailscale`
   + `sudo brew services start tailscale`) rather than only the App Store app:
   the sandboxed app cannot run Tailscale SSH and its CLI crashes intermittently.
3. In the admin console: **disable key expiry** for the mini (Machines → … →
   Disable key expiry). Do the same for any NAS on the tailnet.
4. Decide your ACL. Simplest safe policy for a personal tailnet:

   ```jsonc
   {
     "acls": [
       { "action": "accept", "src": ["autogroup:member"], "dst": ["autogroup:self:*"] }
     ]
   }
   ```
   This lets *your* devices reach *your* devices and keeps any machine shared in
   from outside isolated. Only add `tag:` rules once you have actually applied
   tags — a device whose *name* looks like a tag is not tagged.

Agent steps:

5. `sudo tailscale up --ssh` if you want Tailscale SSH; **then prove it** —
   connect from the laptop and keep that shell open. Break-glass that has never
   been used is not break-glass.
6. Bind private-only services (databases, admin tools) to the mini's tailnet IP or
   `127.0.0.1`, never `0.0.0.0`.
7. Add `Host` aliases in `~/.ssh/config` on your laptop for the tailnet name, and
   `ssh-keyscan` after verifying the fingerprint — the same box has a LAN IP and a
   tailnet IP, and `known_hosts` trusts per address.

**Done when:** `ssh you@your-mini` works from a laptop on cellular (Wi-Fi off);
`tailscale status` on the mini shows no `expired`.

**Gotchas in this phase**

- *ACL rules match nothing; ping works but TCP doesn't.* Tags were never applied,
  or the packet filter is empty (which means deny-all; pings bypass ACLs). Check
  `tailscale debug netmap`; capture on `utunN`, not `any`.
- *`tailscale set --ssh` refuses.* App Store build. Use the daemon build or plain
  `sshd` over the tailnet IP as break-glass.
- *The always-on box dropped off the tailnet after six months.* Default 180-day
  key expiry. Disable it for servers.
- *A NAS shows "online" but doesn't answer.* Disk hibernation stops the Tailscale
  data path. Turn hibernation off; auto-start the package after power loss.
- *Restarting Tailscale remotely cuts off your own session and it doesn't come
  back.* Never restart it over the tailnet.
- *Funnel is public exposure.* `tailscale serve` is tailnet-only; `funnel` is the
  internet. Never Funnel a service that also sits behind nginx or the tunnel.

### Phase 4 — Toolchain

**Goal:** nginx, Python and (optionally) PostgreSQL installed in a way that root
can run without handing root to the admin user.

Agent steps:

1. Install Homebrew. On Apple silicon it lives at `/opt/homebrew`; on Intel at
   `/usr/local`. Every plist and config you write later must use the right prefix
   — this is the #1 cost of a later Intel→Apple-silicon move.
2. `brew install nginx python@3.12 postgresql@17 cloudflared gh restic gitleaks`.
3. **Ownership decision.** Homebrew is owned by the admin user. If root runs
   `brew`'s nginx or python (it will — launchd daemons run as root to bind :443),
   then anyone who can write to the Cellar can become root. Mitigate: no
   `NOPASSWD` sudo on brew binaries; system directories first in `PATH` for root
   jobs; consider a root-owned copy of nginx for the daemon.
4. `nginx -t` must pass before any reload, always. Put it in a shell alias and in
   every deploy script.

**Done when:** `brew doctor` is clean; `nginx -t` passes; `python3 --version` ≥ 3.12.

**Gotchas in this phase**

- *`git pull` in the wrong directory updated Homebrew.* `/opt/homebrew` is itself
  a git repo. Always `git -C <repo>`.
- *Migration Assistant from an old Mac brought every stale path with it.* Do a
  clean, scripted rebuild and keep the script in the repo.
- *Postgres major upgrade forced by the architecture change.* Binary formats
  differ: `pg_dumpall` → restore, and restore globals (roles) first.

### Phase 5 — Service identity

**Goal:** every internet-facing service runs as its own user from a deployed
tree, reads its secrets from a root-owned file, and cannot read your home folder.

Agent steps:

1. For each service `<svc>`: `sudo sysadminctl -addUser svc-<svc> -shell /usr/bin/false
   -home /var/empty` (a role account; no login, no sudo). One uid per tenant if
   you host for others.
2. Deployed tree at `/var/www/<svc>`, owned by `svc-<svc>`, mode 750. The service
   **never** runs from your dev checkout.
3. Secrets tree `/var/<org>/secrets/<svc>.env`, root-owned, mode 0640, group
   `svc-<svc>`; symlinked as `/var/www/<svc>/.env`. Tenants get a separate tree
   outside the shared one.
4. Logs at `/var/<org>/logs/<svc>/`, owned by the service user. **Not** under
   `/var/log` — see Phase 10.
5. Lock your admin home: `chmod 750 /Users/<admin>`. Check first that no service
   reads anything from it (grep plists and `.env` files for `/Users/`).
6. launchd daemon per service in `/Library/LaunchDaemons/com.<org>.<svc>.plist`
   with `UserName`, `WorkingDirectory` under `/var/www`, `KeepAlive`, explicit
   `EnvironmentVariables`, stdout/stderr into the service's log dir. Template:
   `tools/mac-mini-web-server/templates/com.example.service.plist`.
7. Before flipping any existing service to a new user, **run it by hand as that
   user on a scratch port**, then swap the plist. And grep its code for `sudo`
   shell-outs first — a service that quietly `sudo cat`s a secret will produce
   empty results, not an error, after the flip.

**Done when:** `ps -o user,command -p $(pgrep -f <svc>)` shows `svc-<svc>`;
`sudo -u svc-<svc> cat /Users/<admin>/.zshrc` is denied.

**Gotchas in this phase**

- *A service compromise would have landed in the admin group.* It ran as admin
  from the dev tree. The whole phase exists because of this.
- *Nightly job silently produced nothing after the identity flip.* `sudo cat` in
  code plus a non-fatal catch. Grep before you flip.
- *launchd job "works in the terminal, dies under launchd".* macOS TCC blocks
  launchd-spawned processes from `~/Documents`, `~/Desktop`, `~/Downloads`. Keep
  everything under `/var/www` or `/opt`.
- *`bootout && bootstrap` on one line → I/O error 5 and the service is gone.*
  Separate commands with a pause, or `launchctl kickstart -k` when the plist is
  unchanged. Root cannot bootstrap into `gui/<uid>`; do system jobs with sudo and
  gui jobs as the user.
- *A calendar job shows `runs = 0` after it ran.* The counter lies. Trust the
  log's mtime and owner.
- *Jobs that need the login keychain (e.g. a coding-agent CLI) fail as
  LaunchDaemons.* They must be gui LaunchAgents, which is one reason auto-login
  was chosen in Phase 0.
- *Daemons crash-loop at boot.* They started before Postgres. Add a
  wait-for-database loop.

### Phase 6 — nginx and the first site

**Goal:** a vhost in git, symlinked into nginx, serving a static site on
`127.0.0.1` ready for the tunnel.

Agent steps:

1. Keep vhosts in your repo (`ops/nginx/sites/example.com.conf`) and **symlink**
   them into `$(brew --prefix)/etc/nginx/servers/`. Never `sudo cp` over a symlink
   — it silently replaces the link with a file and the next deploy edits the wrong
   one.
2. Use **named upstreams** (`upstream app_<svc> { server 127.0.0.1:5001; }`),
   never a literal `127.0.0.1:PORT` in `proxy_pass`. A tiny validator script that
   greps for the literal form belongs in CI.
3. nginx listens on `127.0.0.1:443` (and `:80` → redirect) only. Behind the tunnel
   every request arrives from loopback, so add
   `set_real_ip_from 127.0.0.1; real_ip_header CF-Connecting-IP;` or every rate
   limit and log line will show one IP.
4. **Access and error logs under `/var/<org>/logs/nginx/`**, not `/var/log/nginx`.
   A macOS update deleted `/var/log/nginx`, `nginx -t` failed, and the apex sites
   502'd while a health banner said "healthy".
5. Cache headers: use **either** `expires` **or** `add_header Cache-Control`,
   never both — nginx emits two headers and the CDN picks the more aggressive one
   (a year of `immutable` on files that change).
6. Explicit `return 404;` deny blocks on the public vhost for anything that is
   dev-only. An auth gate is not separation.
7. One static `index.html` in `/var/www/<svc>/public` so there is something to see.

**Done when:** `curl -k -H 'Host: example.com' https://127.0.0.1/` returns your
page; `nginx -t` passes; the log files appear under your log dir.

### Phase 7 — Cloudflare: DNS, tunnel, origin cert, Access

**Goal:** `https://example.com` serves from the mini with no inbound port, and
`https://admin.example.com` asks for your email before it shows anything.

Human steps:

1. Add your domain to Cloudflare (Free plan); move nameservers at your registrar;
   wait for "Active".
2. **SSL/TLS → Origin Server → Create Certificate.** One **Origin CA** cert for
   `example.com` and `*.example.com`, 15-year validity. Paste cert and key into the
   files the agent names (root-owned, 0600). This is the origin cert nginx uses;
   you do not need Let's Encrypt behind the tunnel.
3. **Zero Trust → Networks → Tunnels → Create.** Choose the token-run install.
   Copy the install command's token into the file the agent names — not into
   chat. Note: a token-run tunnel keeps its routes **in the dashboard/API**, not on
   disk; `cloudflared tunnel list` on the box will fail and that is normal.
4. Add public hostnames to the tunnel: `example.com` → `https://localhost:443`,
   with **No TLS Verify: on** (the origin cert's name doesn't match `localhost`;
   with it off you get an edge 502 while nginx is perfectly healthy) and
   **Origin Server Name: example.com**. Repeat per hostname. Every hostname you
   route **must** have a matching nginx vhost or it falls through to whatever
   nginx's default server is.
5. **Zero Trust → Access → Applications → Add** for `admin.example.com`: policy
   "Allow", include Emails = yours. Do this *before* that hostname serves
   anything, so the first proof costs nothing. Access answers at the edge, before
   nginx ever runs — so anything on that hostname that needs an unauthenticated
   caller (OAuth issuers, webhooks, MCP bearer endpoints) will break. Put those on
   a separate ungated hostname (`hooks.example.com`).
6. **Security → Security Rules (formerly WAF):** for each webhook path, a rule
   `URI path equals /…/events` → **Skip** managed rules, Super Bot Fight Mode,
   Browser Integrity Check. External services are bots; bot protection blocks them
   with a 403 that loopback tests never show.
7. **Network → HTTP/3: off** if you will ever use client certificates (mTLS) —
   no client cert over QUIC. Optional hardening later: Cloudflare-issued client
   certs plus a WAF rule on `cf.tls_client_auth.cert_verified` to gate admin by
   device; bring-your-own CA is Enterprise-only.
8. Create an **API token** for the agent with exactly: Zone:Read, DNS:Edit,
   **Cloudflare Tunnel:Edit** (easy to miss — Access calls will succeed while
   tunnel calls fail), Access: Apps:Edit. Scope it to the one zone. Paste into the
   named file.

Agent steps:

9. `sudo cloudflared service install <token-from-file>` — creates
   `/Library/LaunchDaemons/com.cloudflare.cloudflared.plist`. Move the token out
   of the plist into a root-only env file when you can; the plist is
   world-readable by default.
10. Verify with the API, requiring a **non-empty** result: a missing token scope
    returns `success: true` with an empty list.
11. Install the token file safely: `sudo install -m 0600 -o root /dev/null
    /etc/<org>/cloudflare.token && sudo tee /etc/<org>/cloudflare.token` — BSD
    `install` can't read from a pipe.

**Done when:** `curl -sI https://example.com` returns 200 with `server: cloudflare`;
`https://admin.example.com` shows the Access login; a webhook-path POST from
outside returns your app's 401, not a 403.

**Gotchas in this phase**

- *Edge 502, nginx healthy.* Missing No-TLS-Verify on a `https://localhost` route,
  or a hostname with no vhost. Diagnose with
  `curl -k -H 'Host: x' https://127.0.0.1/` and a unique-path marker in the access
  log.
- *Intermittent sitewide 502 for weeks.* A retired machine still had the tunnel
  token and registered as a second connector that took a share of traffic.
  Rotate the tunnel secret, install the new token, **and delete the stale
  connection in the dashboard** — rotation alone does not evict a live session.
  Tell connectors apart by `arch` in the connections list, not IP (same WAN IP).
- *A bare `error code: 502` (16 bytes) is the edge failing to reach an origin.*
  The tunnel's own metrics can freeze and prove nothing; test from more than one
  network.
- *Rate limits throttled everyone together.* All requests looked like 127.0.0.1.
  `real_ip_header CF-Connecting-IP`.
- *Edge cached changing files for a year.* Double Cache-Control headers (Phase 6).
- *Purge "didn't work".* The origin was stale (Phase 9). Check the commit on disk
  before blaming the cache.
- *Moving a hostname behind Access broke public endpoints on it.* Classify every
  location block before gating a hostname.
- *User "added" but still 403.* The app's own allowlist and the Access policy both
  have to include them.
- *Retiring a hostname.* Measure traffic to zero first, then a hard 410.
- *Making anything public is a human decision.* DNS records, tunnel routes and
  Access policies are created by you (or by the agent with you watching), never
  by an unattended job.

### Phase 8 — GitHub: repo, protection, keys

**Goal:** `main` cannot be force-pushed, deleted or bypassed even by you; the mini
pulls with a key that can do nothing else.

Human steps:

1. **Plan.** Branch rulesets on a **private** repo need GitHub Pro (personal) or
   an organisation on **Team**. On Free, rulesets only work on public repos. If
   your server repo will contain anything about your home network — it will —
   make it private and pay the few dollars. (Verified against the pricing page at
   the time of writing; check it again.) An organisation also gives you the
   org-level deploy-key setting below and separates "you" from "the infra".
2. Create the repo. Add a **ruleset** on `main` with all **four** rules:
   `update` (require PR), `deletion`, `non_fast_forward`, `creation`; bypass
   actors: organisation admin only, or none. An `update` rule alone is *not*
   protection: a branch can be deleted and recreated at any commit.
3. Org **Settings → Deploy keys → Allow deploy keys for repositories: ON** and
   leave it on. It gates deploy-key *usage*, not just creation; with it off the
   key authenticates and every fetch says "Repository not found".
4. Required checks: `gitleaks` (secret scan) and whatever tests you have.

Agent steps:

5. On the mini, as **root**: `ssh-keygen -t ed25519 -f /var/root/.ssh/deploy-<repo>`;
   add the public key as a **read-only deploy key** on the repo. Root's deploy
   clone lives at `/var/<org>/deploy/<repo>` and is root-owned. Add `github.com`
   to root's `known_hosts`.
6. Never run `git` as root inside a checkout a tenant or service can write to:
   `.git/hooks/pre-push`, a repo-local `credential.helper`, and `$HOME/.gitconfig`
   via `env_keep` are all root escalation. Root uses its own clone, `env -i`, and
   `GIT_CONFIG_NOSYSTEM=1`.
7. The `gh` CLI's credential is an account-wide token. It belongs to your admin
   user only — never in a service or tenant account. Use deploy keys or a
   fine-grained PAT scoped to one repo for anything automated. If a private repo
   is used as a Claude plugin marketplace, run `gh auth setup-git` or the HTTPS
   fetch has no credential even though `gh auth status` is green.
8. Verify protection with `gh api repos/<o>/<r>/rulesets` — read `enforcement`
   and `current_user_can_bypass`. Classic branch-protection endpoints return 404
   when rulesets are in use; admin rights do not imply bypass.

**Done when:** `git push --force origin main` from your laptop is rejected with
`GH013`; `sudo git -C /var/<org>/deploy/<repo> fetch` succeeds; `sudo git push` from
there is rejected.

**Gotchas in this phase**

- *PR shows no checks and can't merge.* It conflicts with `main`; GitHub runs
  nothing. Merge `main` into the branch — don't close/reopen.
- *CI "green on main" meant nothing for weeks.* Path filters skipped it. Treat
  checks as a PR gate only.
- *Merged the wrong PR.* `gh pr merge` without an exact number and `--repo`.
  Always both.
- *`git add -A` staged a venv symlink.* Trailing-slash ignore patterns don't
  match symlinks. Never symlink a venv into a work tree; never stage-everything.
- *Dependabot reads manifests, not venvs,* and a venv rebuild brings stale pins
  back. Raise the pins in `requirements.txt` when you patch.
- *A secret in git history is burned.* `git filter-repo` and rotate; "deleted in
  the next commit" is not deleted.

### Phase 9 — Deploy and rollback

**Goal:** the only way code reaches `/var/www` is a merged commit on `main`, and
rollback has been drilled, not just written.

Agent steps:

1. One root-owned **deploy entry point** (`/usr/local/sbin/deploy`), the only
   thing in sudoers for the admin: `deploy|rollback|restart <svc> <sha>`. The
   `<sha>` must be on `origin/main` with green checks. Clean environment
   (`env -i`), root's clone, `rsync --delete` from that clone with an explicit
   exclude list (`.env`, `venv/`, data dirs), then `pip install` as the service
   user, then `launchctl kickstart -k`.
2. **Merging is not deploying.** The webroot is a git checkout (or an rsync of
   one); it serves 200 on a stale commit forever. Every deploy ends by printing
   the SHA on disk and curling a health URL that includes it.
3. Rollback = deploy the previous SHA. **Drill it** on day one. The source
   project's rollback script had never worked: macOS ships bash 3.2 (no
   `declare -A`) and it needed an interactive `read`.
4. Health checks must hit a **worker**, not the gunicorn master — the master
   answers while workers crash-loop.
5. A maintained list of deployable services drifts; generate it from a registry
   file in the repo.
6. Never give an agent a deploy capability it can wander into: `claude -p
   --allowedTools` still permits Bash; use `--restricted --tools`. Deny rules can
   be dodged by wording; enforce on the server (rulesets, the deploy door).

**Done when:** deploy a trivial change, see its SHA on disk and in the health
response; roll back; see the old SHA; both under five minutes.

**Gotchas in this phase**

- *Deploy printed OK but synced nothing.* It ran from a deleted working
  directory. `cd` somewhere real; grep the live file for the new string.
- *Dependency bump had no effect.* Deploy never ran `pip install`. Install per
  venv as the owner, `pip check`, then kickstart.
- *False "rolled back" warning on a clean deploy.* The script's own restart
  bypassed its health gate. Verify by SHA plus HTTP, not by the script's prose.
- *A change to the shared deploy library broke every deploy; an auto-created dir
  came out 0700.* Dry-run one real deploy before merging deploy-tooling changes.
- *rsync fallback without excludes overwrote live data.* Excludes are not optional.
- *An unpinned shared library pulled a new DB driver; workers died.* Pin.

### Phase 10 — Backups and OS updates

**Goal:** nightly backups leave the box outbound-only, an offsite copy exists, and
OS updates happen on your schedule with a full check afterwards.

Agent steps:

1. **Local backup: push, outbound, over SSH.** `rsync -e ssh` from the mini to the
   NAS over Tailscale, with a forced-command, rsync-only key on the NAS. Pulling
   *from* the NAS failed (inbound TCP to the mini blocked); SMB mounts from launchd
   failed (TCC). On a Synology add `--rsync-path=/usr/bin/rsync` or you get a
   misleading "Permission denied".
2. **Offsite: restic to B2** (`pg_dumpall` + `/var/www` + `/var/<org>` + nginx
   configs; `forget --keep-daily 14 --keep-weekly 8`; `check` weekly). Restore to a
   scratch directory once, now.
3. Every backup job checks the role file first — a staging clone must never
   push over production's backups.
4. **OS updates:** auto-install off (Phase 1). Monthly, in a window:
   `softwareupdate -l`, `pip freeze` for every venv, `softwareupdate -i -a -R`,
   then after reboot: `pgrep nginx`, `nginx -t`, curl every hostname, check every
   launchd service is running and its log dir exists. Post the result to your ops
   channel.
5. Patching live venvs: install as the venv owner, `pip check`, `kickstart -k`,
   then raise the pins in the repo so a rebuild can't undo it.

**Done when:** last night's backup appears on the NAS and in B2; a restic restore
of one file works; the update routine has run once with everything green after.

**Gotchas in this phase**

- *A macOS update deleted `/var/log/nginx`.* Logs live elsewhere (Phase 6);
  `pgrep nginx` after every update.
- *"No errors" in an empty stderr log.* The job wrote errors to stdout. Read both.
- *Backup failures meant the NAS was asleep,* not the server down. Fix hibernation
  (Phase 3).
- *World-writable log dir, world-readable `.env`, SSH password login on (macOS
  default).* `chmod`, and `PasswordAuthentication no` in `sshd_config`.

### Phase 11 — Optional layers

- **Monitoring into Slack.** The [[Slack-Assistant]] sites channel; post on change
  or failure plus one daily green line.
- **Security scanning.** A nightly `gitleaks`, listener audit
  (`lsof -iTCP -sTCP:LISTEN`), cert-expiry and HSTS check; the first run only sets
  a baseline.
- **Docker.** Only after the user boundaries exist. Containers do not replace
  them; the only compose file in the source history held a hard-coded DB password
  that then had to be rotated.
- **Hosting for others (tenants).** One macOS user per tenant, their own secrets
  tree outside the shared one, sudoers scoped to their deploy script only, and
  their own GitHub deploy key. Ask the tenant's org admin up front whether deploy
  keys are enabled — an outside collaborator cannot change it.
- **Cutover to a new box.** Write-freeze (non-GET → 503), an `X-Served-By`
  header per box, swap the role files, add the new tunnel connector then delete
  the old, type the hostname to confirm each irreversible step, keep the old box
  quiesced for 7 days.

## 6. Gotcha ledger

| Symptom | Cause | Fix |
|---|---|---|
| Renaming the admin account broke everything | Paths embed the short name | Pick it at first boot, never change it |
| Jobs ran on the wrong box / "staging" was prod | Gating on hostname | Role file in `/etc/<org>/role`; every job checks it |
| Command landed on the wrong machine | Two similar hosts, same paths | Name the machine in every instruction; `hostname && whoami` first |
| `open`/`pbcopy`/Keychain "did nothing" | GUI acts on the server's screen over SSH | Screen Share first or avoid GUI steps |
| Compromise would land in the admin group | Services ran as admin from dev tree | One service user, `/var/www`, `UserName` in plist |
| Nightly job silently empty after identity flip | `sudo cat` in code, non-fatal catch | Grep for sudo shell-outs before flipping |
| Works in terminal, dies under launchd | TCC blocks `~/Documents` etc. | Service tree under `/var/www` or `/opt` |
| `bootout && bootstrap` → I/O error 5, service gone | launchd race | Separate commands; `kickstart -k` |
| `runs = 0` after the job ran | launchd counter lies | Trust log mtime and owner |
| Daemon can't read the login keychain | LaunchDaemon vs LaunchAgent | gui LaunchAgent + auto-login |
| Daemons crash-loop at boot | Started before Postgres | Wait-for-DB loop |
| Health green, workers crash-looping | Master answers checks; GPU model not fork-safe | Health hits a worker; `device="cpu"` under gunicorn |
| New key in `.env` has no effect | Different user/env file/venv | One env file per process, listed in the plist |
| NAS unreachable from server | VLAN isolation working | Tailscale, or NAS on the server VLAN; tested LAN recovery path |
| New box didn't take the IP | DHCP reservation keyed to old MAC | Record MAC at first boot; move the reservation at cutover |
| PoE device dark behind a new switch | Non-PoE switch starved it | PoE switch or active injector |
| Tailscale ACL matches nothing | Names aren't tags | Apply tags or `autogroup:self` |
| Ping works, TCP doesn't on tailnet | Empty packet filter = deny-all | Fix ACL; capture on `utunN` |
| `tailscale set --ssh` refuses | App Store build | Daemon build or plain sshd |
| Break-glass didn't exist when needed | Never proven | Connect once and keep the shell open before gating |
| Node dropped after ~6 months | Key expiry | Disable expiry on servers |
| NAS "online" but silent | Disk hibernation | Hibernation off; auto-start |
| Restart Tailscale remotely → locked out | Self-inflicted | Never restart it over the tailnet |
| Host key verification failed on tailnet only | known_hosts per address | keyscan after fingerprint check; `Host` aliases |
| `cloudflared tunnel list` fails | Token-run tunnel keeps routes remote | Use the API/dashboard for routes |
| Edge 502, nginx healthy | No-TLS-Verify off / hostname has no vhost | Turn it on; explicit vhost per routed hostname |
| Intermittent 502 for weeks | Stale connector on a retired box | Rotate secret **and delete the connection** |
| Bare `error code: 502` | Edge can't reach origin; metrics frozen | Marker probe + origin log; test from two networks |
| API "succeeded", nothing changed | Missing scope returns empty success | Verify non-empty results; add Tunnel:Edit |
| Can't write the token file | BSD `install` can't read a pipe | Create 0600 file, then `tee` |
| Public endpoints broke behind Access | Edge auth precedes nginx | Ungated hostname for OAuth/webhooks/MCP |
| User added, still 403 | Two allowlists | Add to Access policy *and* app allowlist |
| Client certs never reach nginx | Tunnel terminates TLS | WAF rule on `cf.tls_client_auth.cert_verified`; HTTP/3 off |
| Edge cached for a year | `expires` + `add_header` both emitted | One Cache-Control source |
| Purge didn't work | Origin stale | Check SHA on disk first |
| Everyone rate-limited together | All requests from loopback | `real_ip_header CF-Connecting-IP` |
| `sudo cp` broke a vhost | Replaced the symlink | Edit in git, symlink into nginx |
| Apex 502 after OS update | `/var/log/nginx` deleted | Logs outside `/var/log`; `pgrep nginx` after updates |
| "Is main protected?" says 404 | Rulesets, not classic protection | `gh api .../rulesets`; read bypass |
| Branch "protected" but recreatable | Only an `update` rule | All four rules |
| Deploy key auths then "not found" | Org deploy-key usage setting off | Keep it on |
| Private repo fetch fails for the service user | Anonymous HTTPS; `sudo` kept the wrong HOME | SSH remote + explicit `HOME` |
| Root git in a tenant checkout | Hooks/config as root | Root-owned clone, `env -i`, `GIT_CONFIG_NOSYSTEM=1` |
| Plugin marketplace from private repo fails | git has no credential | `gh auth setup-git` |
| PR has no checks | Conflicts with main | Merge main in |
| Wrong PR merged | No number / no `--repo` | Always both |
| Venv symlink staged | Trailing-slash ignore misses symlinks | Never symlink venvs; never `add -A` |
| Site stale after "deploy" | Merge ≠ deploy; webroot on old commit | Print SHA on disk; health includes SHA |
| Deploy OK, nothing synced | Deleted cwd | `cd` to a real dir; grep the live file |
| Requirements bump inert | No `pip install` in deploy | Install per venv as owner |
| False rollback warning | Script's own restart bypassed its gate | Verify by SHA + HTTP |
| Rollback never worked | bash 3.2, interactive `read` | Drill it on day one |
| rsync overwrote live data | No excludes | Explicit exclude list |
| Workers died after lib update | Unpinned transitive driver | Pin |
| NAS pull backup fails | Inbound TCP blocked; SMB TCC | Outbound rsync-over-SSH push |
| Synology "Permission denied" | Wrong rsync binary | `--rsync-path=/usr/bin/rsync` |
| "No errors" in stderr | Errors on stdout | Read both |
| Token looks perfect, 401 | zsh `%` marker ate the last byte | `tail -c1 \| xxd` |
| `! cmd && …` did nothing | zsh negation | No `!` prefix in pasted commands |
| One token is a master key | Auth without authorisation | One token per person/machine |
| `.env` synced to a cloud drive | Repo inside a synced folder | Keep repos out of synced folders |

## 7. Free vs paid

| Service | Free tier enough? | What paid adds | Our call |
|---|---|---|---|
| Cloudflare | **Yes** — DNS, Tunnel, Access (up to 50 users), Security rules, Origin CA, Cloudflare-issued client certs | Bring-your-own CA (Enterprise), bigger WAF | **Free.** |
| Tailscale | **Yes** — Personal plan, plenty of devices, ACLs, SSH, Serve | More users, SSO | **Free.** |
| GitHub | Public repos: yes. **Private repos: rulesets need Pro ($4/mo) or an org on Team (~$4/user/mo)** | Rulesets on private repos, required checks, org deploy-key policy, CodeQL on private | **Pay.** Your server repo describes your house. The source project runs a 1-seat Team org; the step it unblocks is Phase 8 step 2. Re-check pricing — this changes. |
| Domain | — | — | ~$10–15/yr, any registrar; DNS moves to Cloudflare |
| Backblaze B2 | 10 GB free | Pennies per GB after | Free for most; a few dollars a month at worst |
| Anthropic / coding agent | A subscription you already have for building | — | Nothing extra. Services that call the API at runtime (bots, summaries) need an API key with a daily cap; budget under $5/mo for personal use |
| NAS / UPS | Hardware | — | Optional; the offsite copy is the one that matters |
| UniFi (or any VLAN router) | Hardware you own | Cloud features you don't need | Any router with VLANs + inter-VLAN firewall rules |

## 8. Talking to the tool

- **Your sites:** `https://example.com`. **Admin pages:** `https://admin.example.com`
  behind Access.
- **You and your agent → the box:** `ssh you@your-mini` over Tailscale; Remote-SSH
  in your editor; the agent runs there.
- **The box → you:** the ops channel in the [[Slack-Assistant]]; nightly backup and
  update results post there.
- **Deploying:** merge a PR; `sudo deploy <svc> <sha>` on the box (or the deploy
  door's API if you built one); watch for the SHA in the health response.

## 9. Keeping it alive

Monthly:

- [ ] `tailscale status` shows no expired keys; SSH over Tailscale works from
  cellular.
- [ ] `curl -sI` every public hostname: 200, `server: cloudflare`.
- [ ] Last night's backup exists on the NAS and in B2; one restic restore test.
- [ ] OS update routine (Phase 10) run in a window, full check after.
- [ ] `gh api repos/<o>/<r>/rulesets` still active with four rules.
- [ ] `lsof -iTCP -sTCP:LISTEN` shows nothing bound to `0.0.0.0` you don't expect.
- [ ] Cloudflare tunnel shows exactly one connector (yours).

Yearly: rotate the tunnel token, the API token, deploy keys, and any service
password; re-read §Free vs paid against current pricing.

---

_Built from a year and a half of running two of these — including the week a
retired machine kept half the traffic, the night an OS update deleted the log
directory, and the afternoon it turned out "main is protected" wasn't. Every gotcha
above happened._
