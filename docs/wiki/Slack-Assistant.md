# Slack Assistant

_A personal AI assistant that lives in your Slack workspace: one channel for you,
one channel for your machines._

> Why, hello there, friend of the future! I see you've wandered into your next
> journey through the wonderful world of Artificial Intelligence and its many
> marvellous capabilities. On this particular expedition we'll stroll, step by
> confident step, through the choices and considerations that make **your very own
> Slack Assistant** a whimsical success — an ever-ready helper who answers in the
> channel you already have open, keeps an eye on your servers, and never once asks
> you to open a terminal. Hats on, gloves on — the future is calling, and it's on
> line one.

**Start here:** read §What this is and §What you need, decide §Free vs paid, then
hand this page to your AI agent and work the phases together.

## 1. What this tool is

A small always-on service on a machine you control that connects a Slack bot to a
large language model. You talk to it in a **personal-assistant** channel (or by DM),
and it answers questions, adds calendar events, summarises what you missed, and
files things you want to remember. A second **sites** channel is where your
scripts and services post health, alerts and "something needs you" messages, so
one Slack window is both your assistant and your ops console.

It is *not* an autonomous agent with shell access. It has no tools that touch
your filesystem, it only reacts to messages from an allowlist of people, it has a
daily spending cap, and it never runs unattended loops. That restraint is the
design — see the gotcha ledger for the self-hosted "open gateway" products this
replaces and why.

What you end up with:

- A Slack app installed in your workspace with a bot user.
- A Python web service receiving Slack events over a signed webhook, calling
  the model through the Anthropic API, and replying in-thread.
- A scheduler in the same process for a morning brief and reminders.
- Optional integrations: Google Calendar (read/write), Gmail (read-only), a
  phone push channel, and a memory store your agent can search.

## 2. Who this is for, and what you need

For one person (or a small trusted group) who already lives in Slack and wants an
assistant there rather than in yet another app. Comfortable asking an AI coding
agent to do the technical steps; willing to click through a few dashboards.

**Hardware**

- Any always-on machine that can run Python 3.12+ and be reached over HTTPS: a
  Mac mini (see [[Mac-Mini-Web-Server]]), a Linux box, or a small VPS. Nothing
  heavy; the service idles at a few hundred MB.

**Accounts and services**

| Service | Needed for | Free tier enough? |
|---|---|---|
| Slack workspace (you are admin) | the bot | **Yes** |
| Anthropic API account | the model | Pay-per-token; a cap of ~$2/day is plenty |
| A domain + Cloudflare (or any public HTTPS endpoint) | Slack's webhook | **Yes** (Cloudflare Free) |
| Google Cloud project | Calendar / Gmail (optional) | **Yes** |
| Pushover | phone push (optional) | one-time ~$5 |

**Software and tools** (the agent installs these)

- Python 3.12+, a virtualenv, `flask`, `gunicorn`, `slack-sdk`, `anthropic`,
  `google-api-python-client` + `google-auth-oauthlib` (optional).
- A reverse proxy (nginx or Caddy) and a tunnel to it (Cloudflare Tunnel).
- A process supervisor: `launchd` on macOS, `systemd` on Linux.

## 3. Setup time

| | Estimate |
|---|---|
| Human hands-on time | 1–2 hours: Slack app screens, Google consent + publish, pasting secrets, clicking Allow |
| AI agent working time | 2–4 hours across two or three sessions |
| Elapsed | One afternoon for the core bot; add a day of watching for silent failures (see gotchas) |

Human-blocking steps: creating the Slack app and installing it, the Google OAuth
consent screen and its "Publish" button, the browser consent for each Google
account, and pasting each secret into its env file.

## 4. Working with your AI agent on this guide

- **Where to run the agent.** Claude Code (or similar) in a terminal or IDE **on
  the machine that will host the service**, or over Remote-SSH into it. The
  service user, env file paths and the supervisor all have to be real.
- **Give it a browser.** The Slack app configuration, Google Cloud console and
  tunnel dashboard are all forms. Let the agent drive them — Claude Desktop with
  the Chrome extension or its built-in browser, or the Chrome extension from
  Claude Code — and you click the final Install / Allow / Publish.
- **Secrets never go through chat.** The bot token, signing secret, API key and
  OAuth client file are pasted by you into the env file the agent names. If one
  lands in a chat window, rotate it.
- **A way to talk to the result** is built in: it's Slack. By the end of Phase 4
  you DM the bot and it answers.

## 5. The phases

### Phase 0 — Decide the shape

**Goal:** make the four choices that are expensive to reverse.

| Decision | Options | Our default |
|---|---|---|
| How Slack reaches you | **Events API webhook** (needs a public HTTPS URL; works with any supervisor) vs **Socket Mode** (no public URL; a long-lived outbound websocket) | **Events API** if you are building the [[Mac-Mini-Web-Server]] anyway — one more route behind the tunnel. **Socket Mode** if you have no public endpoint and don't want one. |
| How the model is called | **Anthropic API** (pay-per-token, simple, cost-capped) vs driving a coding-agent subscription headlessly | **API.** Subscriptions are for building, not for a 24/7 service. |
| Memory | Slack thread history only (last ~10 messages) vs a local memory store the bot can search | Start with **threads only**; add the portable `ma` package from this repo ([[Memory-Archive]]) when you miss things. |
| Who may talk to it | Everyone in the workspace vs an **allowlist** of user IDs | **Allowlist**, always. This is what keeps an open bot from becoming an open wallet. |

**Done when:** the four answers are written at the top of the project's README.

### Phase 1 — Create the Slack app

**Goal:** a bot user with exactly the scopes it needs, installed in your
workspace, invited to two channels.

Human steps (agent fills forms where it can; you click Install):

1. At `api.slack.com/apps` create an app **from scratch** in your workspace.
2. **OAuth & Permissions → Bot Token Scopes.** Add:
   `chat:write`, `app_mentions:read`, `im:history`, `channels:history`,
   `reactions:read`, `files:read`, `files:write`, `links:read`. Add
   `channels:read` too — it costs nothing and saves you copying channel IDs by
   hand later (a real gotcha). Add `commands` only if you want slash commands.
3. **App Home → Agents & AI Apps.** Turn on the *Agent / assistant* experience
   (or, on older workspaces, enable the **Messages tab** under App Home). Without
   one of these, DMs to the bot fail with `restricted_action_read_only_channel`.
4. **Install to Workspace.** Copy the **Bot User OAuth Token** (`xoxb-…`) and,
   from **Basic Information**, the **Signing Secret**. Paste both into the env
   file the agent names in Phase 3 — nowhere else.
5. Create two channels: `#assistant` (you and the bot) and `#sites` (your
   machines and the bot). Invite the bot to both (`/invite @YourBot`).

Agent steps:

- Record the two channel IDs (from `conversations.list`, now that
  `channels:read` is on) and your user ID into the env file as
  `SLACK_CHANNEL_ASSISTANT`, `SLACK_CHANNEL_SITES`, `SLACK_ALLOWED_USERS`.

**Done when:** `curl -H "Authorization: Bearer $SLACK_BOT_TOKEN" https://slack.com/api/auth.test`
returns `"ok": true` with the bot's name.

**Gotchas in this phase**

- *Any scope change requires Reinstall.* Adding a scope in the dashboard does
  nothing to the token you already have. Reinstall, then re-paste the token.
- *No `channels:read` → no way to find a channel ID from code.* You end up
  right-clicking the channel in Slack and copying the ID by hand. Add the scope.
- *Slack's `search.messages` is not available to bot tokens at all.* Don't design
  around it.

### Phase 2 — Make a public HTTPS endpoint (Events API only)

**Goal:** `https://bot.example.com/slack/events` reaches your service, and
**nothing** in front of it asks the caller to log in.

Skip this phase if you chose Socket Mode.

Agent steps:

1. Add a reverse-proxy route: `/slack/` → `127.0.0.1:<port>`.
2. Expose it through the tunnel (Cloudflare Tunnel public hostname, or your
   provider's equivalent). Prefer a **dedicated hostname** for webhooks
   (`hooks.example.com`) so it never inherits a login wall later.
3. In Cloudflare, create a **Security rule**: *URI path equals `/slack/events`* →
   **Skip** all managed rules, Super Bot Fight Mode, Browser Integrity Check and
   rate limiting. Slack is a bot; bot protection blocks it with a 403 that your
   loopback tests will never show.

**Done when:** from *outside* your network,
`curl -s -o /dev/null -w '%{http_code}' -X POST https://hooks.example.com/slack/events`
returns `401` (your signature check), **not** `403`, `302` or an HTML login page.

**Gotchas in this phase**

- *URL verification fails with "didn't respond with the challenge" while loopback
  tests pass.* Cloudflare's bot protection ate the POST. Add the Skip rule above.
  Pattern: if loopback works and public 403s, it's the edge.
- *Webhook dies the day you add Cloudflare Access / mTLS to the hostname.* Access
  answers at the edge before your proxy runs; Slack can't log in. Keep webhooks on
  an ungated hostname or add a path bypass **before** gating.
- *Proxy says `auth off` but you still get a login redirect.* The running proxy
  cached an older config. Reload it first; it's free.

### Phase 3 — Build the service

**Goal:** a Flask app that verifies, filters, dispatches and replies — in that
order — plus an env file only the service user can read.

Agent steps (this is the part the agent writes; the shape matters more than the
code):

1. **Request pipeline, strictly in this order:**
   1. Verify Slack's signature (`X-Slack-Signature`, timestamp within 5 min).
   2. Answer the `url_verification` challenge.
   3. Kill switch (`BOT_DISABLED=1` → 200 and do nothing).
   4. Allowlist (`SLACK_ALLOWED_USERS`), then per-user rate limit (~10/min).
   5. Daily cost cap (`DAILY_COST_CAP_USD`); refuse politely when hit.
   6. Deduplicate on `event_id` for 60 s (Slack retries on slow replies).
   7. Dispatch. **Return 200 within 3 seconds** — do the work in a thread or
      queue and post the reply afterwards.
   8. Append one row to a local audit log (SQLite is fine) for every event,
      accepted or rejected.
2. **Events to subscribe:** `app_mention`, `message.im`, `message.channels`
   (filter to `#assistant` only; drop bot posts, edits and messages that also
   @-mention the bot or you'll answer twice).
3. **Routing.** Use the model's tool-use to pick an intent
   (`answer`, `add_event`, `summarise`, `catch_up_email`, `remember`). Put
   **exact-grammar commands first** as a plain regex pre-filter (`publish`,
   `discard`, `approve <id>`) so they never reach the model.
4. **Context.** On thread replies, fetch the last 10 messages of the thread and
   pass them in. That is the whole memory until you add a store.
5. **Untrusted text.** Anything from email, web pages or uploaded files is wrapped
   in `<untrusted_content>` tags before it reaches the model, and model output is
   escaped before it reaches Slack.
6. **No silent fallback.** If a model, a store or an API is unreachable, the reply
   says so (`⚠️ couldn't reach calendar`), never "nothing to report".
7. **Env file.** One file, mode 600, owned by the service user, listed explicitly
   in the supervisor config. Every process reads the same file.
8. **Tests** run with the allowlist empty and a temporary audit DB — never against
   the live one.

**Done when:** `curl -X POST localhost:<port>/slack/events` with a correctly
signed test body returns 200 and a row appears in the audit log; an unsigned one
returns 401.

**Gotchas in this phase**

- *Malformed `thread_ts` crashes the reply, then crashes the "sorry" message too.*
  Sanitise `thread_ts`; fall back to posting at channel root.
- *Double replies.* Your handler took >3 s, Slack retried, you processed both.
  Dedupe on `event_id` and reply asynchronously.
- *"publish" not recognised, duplicate draft created.* A footer the client
  appended ("Sent using …") broke an exact-match; the message fell through to the
  model. Match the first word only, and while a draft is pending never send the
  message to the router.
- *Cost cap never fired.* An import error made the guard fail **open**. Test
  guards against the real code path and log loudly when they are skipped.
- *Audit log never written.* The SQLite file was owned by a different user than
  the service. Keep state in a directory the service user owns.

### Phase 4 — Run it as a service

**Goal:** the bot survives reboots and crashes, and runs as a user that owns
nothing else.

Agent steps:

1. Create a dedicated service user (no login shell, no sudo).
2. Supervisor config with **KeepAlive / Restart=always**, stdout/stderr to a log
   directory the service user owns, and the env file path set explicitly.
3. Start it; confirm the port is bound by the service user, not by you.
4. In Slack **Event Subscriptions**, set the Request URL and watch it turn
   **Verified**. Save. Then DM the bot.

**Done when:** you DM "hello" and get a reply; the audit log shows the event; a
`Slackbot` POST appears in the proxy's access log.

**Gotchas in this phase**

- *The bot answers for weeks, then silently stops; every setting still looks
  right.* Slack stopped delivering (a paused subscription after repeated errors
  is one cause). Diagnose by grepping the proxy access log for `Slackbot` POSTs —
  none means Slack, not you. Re-save Event Subscriptions. Add a weekly heartbeat
  and alert if no event has arrived in 7 days.
- *On macOS: "works when I run it, dies under the supervisor".* A launchd job
  cannot execute or read anything under `~/Documents`, `~/Desktop` or
  `~/Downloads` without Full Disk Access. Keep the service tree outside those
  folders.
- *Supervisor restart commands chained with `&&` fail with I/O error 5 on macOS.*
  Run `bootout` and `bootstrap` as separate commands, or use `kickstart -k`.

### Phase 5 — Google Calendar and Gmail (optional)

**Goal:** the bot can read your calendar, add events, and summarise unread mail,
with tokens that don't expire every week.

Human steps:

1. Google Cloud Console → new project → enable **Calendar API** and **Gmail API**.
2. **OAuth consent screen:** External. Fill in app name, support email, a
   **homepage URL and a privacy-policy URL** (any page you control), then
   **Publish to production**. Do not leave it in Testing.
3. **Credentials → OAuth client ID → Desktop app.** Download `credentials.json`;
   place it where the agent says, mode 600.
4. Run the one-time consent script the agent provides, once per Google account
   (calendar and mail may be different accounts). Click Allow in the browser.

Agent steps: scopes `calendar` (read/write) and `gmail.readonly` only; token
refresh handled by the client library; email bodies wrapped as untrusted.

**Done when:** the morning brief lists tomorrow's events and the unread count.

**Gotchas in this phase**

- *Gmail dies with `invalid_grant` roughly every 7 days.* The OAuth app is in
  **Testing** mode, where refresh tokens expire weekly. Publish it (homepage +
  privacy URL required), then mint a fresh token. Verification is **not** needed
  for personal use with read-only scopes.
- *You added the API key / token but the feature still uses the fallback.* The
  web process and the background job read different env files, and a missing
  file is ignored silently. One env file, listed in every supervisor config.
- *Running the consent script over SSH opens nothing.* The browser consent has to
  happen on a machine with a screen; copy the resulting token file over
  afterwards.

### Phase 6 — The sites channel

**Goal:** your machines talk to you in `#sites` using the same bot.

Agent steps:

1. A tiny shell helper (`notify.sh "<message>"`) that POSTs to `chat.postMessage`
   with the bot token and `SLACK_CHANNEL_SITES`. Fall back to the assistant
   channel if the sites channel is unset.
2. Wire it into: service health checks, deploy scripts, backup jobs, security
   scans, OS-update reminders. Post **only on change or failure** plus one daily
   "all green" line — a channel that posts every five minutes gets muted.
3. Teach the bot to answer "status?" in `#sites` by reading the latest health
   summary.

**Done when:** a deliberately failed health check produces a message in `#sites`
within a minute.

## 6. Gotcha ledger

| Symptom | Cause | Fix |
|---|---|---|
| Bot silent for weeks, settings look right | Slack stopped delivering events | Grep proxy log for `Slackbot` POSTs; re-save Event Subscriptions; 7-day no-event alert |
| DM fails `restricted_action_read_only_channel` | Messages tab / Agent experience off | Enable it in App Home |
| Links/replies in channel ignored | Only `app_mention` subscribed | Add `message.channels`, filter to one channel, drop bot posts and edits |
| Scope added, still `missing_scope` | Token predates the scope | Reinstall the app, re-paste the token |
| Can't find channel ID from code | No `channels:read` | Add the scope (or copy the ID from channel details by hand) |
| URL verification fails, loopback OK | Edge bot protection 403s Slack | Cloudflare Skip rule for the webhook path |
| Webhook breaks after adding Access/mTLS | Edge auth runs before proxy | Ungated hostname for webhooks, or path bypass first |
| Login HTML in bot replies | Proxy running stale config | Reload the proxy |
| Double replies | >3 s handler, Slack retried | Dedupe `event_id`, reply async |
| `invalid_thread_ts` crash | Malformed ts | Sanitise; post at root |
| Cost cap never fires | Guard fails open on import error | Test the real path; log skips loudly |
| Audit DB empty | Wrong file owner | Service-user-owned state dir |
| Gmail `invalid_grant` weekly | OAuth app in Testing | Publish the consent screen; new token |
| Feature ignores new key | Two env files | One env file, listed in every supervisor config |
| Degraded output looks real | Silent fallback | Tag fallbacks; "⚠️ couldn't read", never "nothing to do" |
| Works in terminal, dies under launchd | macOS TCC blocks `~/Documents` etc. | Service tree outside protected folders |
| `bootout && bootstrap` → I/O error 5 | launchd race | Separate commands or `kickstart -k` |
| Prompt injection via email/web | Untrusted text reaches model | Wrap in `<untrusted_content>`; escape output; hold drafts with active content |
| Self-hosted "open gateway" agent products | Unauthenticated gateway port, unattended loops, frequent CVEs | Don't. Signed webhook + allowlist + cost cap + no shell tools is the whole point |

## 7. Free vs paid

| Service | Free tier enough? | What paid adds | Our call |
|---|---|---|---|
| Slack | Yes | Longer history, more integrations | **Free.** The bot needs only the last 10 thread messages. |
| Anthropic API | Pay-per-token | — | API account with a daily cap (~$2/day covers a chatty day). A Claude subscription is for *building* this, not running it. |
| Cloudflare | Yes (DNS, Tunnel, Security rules) | WAF extras you don't need | **Free.** |
| Google Cloud | Yes | — | **Free.** Publish the consent screen; no verification needed for read-only personal use. |
| Pushover | $5 one-time | — | Optional; worth it for "the bot is down" pings that don't depend on Slack. |

## 8. Talking to the tool

- **You:** DM the bot or post in `#assistant`. Reply in a thread to keep
  context. Say `remember: …` to file something; `publish` / `discard` to act on a
  draft it posted.
- **Your machines:** `notify.sh` into `#sites`; ask `status?` there.
- **Your AI coding agent:** give it the Slack MCP connector (or the bot token in
  its env) and it can read `#sites` and post on your behalf; give it the memory
  store's CLI (`python3 -m ma search …`) and it reads what the bot remembered.

## 9. Keeping it alive

Monthly, or when the bot goes quiet:

- [ ] `#sites` heartbeat arrived this week.
- [ ] Proxy access log shows `Slackbot` POSTs in the last 7 days.
- [ ] Google tokens refresh without `invalid_grant` (consent screen still Published).
- [ ] API spend for the month looks like a month, not a day.
- [ ] After any OS update: service is running, port bound, log directory exists.
- [ ] Rotate the bot token and signing secret yearly or on any suspected leak
  (Reinstall + re-paste).

---

_Built from the history of a real assistant that ran for most of a year — including
the month it was silently dead. Every gotcha above happened._
