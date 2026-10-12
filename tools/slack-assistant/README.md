# Slack Assistant

A personal AI assistant in your Slack workspace: one channel for you, one channel
for your machines. Signed webhook, allowlist, daily cost cap, no shell tools.

**The guide is the wiki page:** [docs/wiki/Slack-Assistant.md](../../docs/wiki/Slack-Assistant.md).

`templates/` holds the files your agent copies and fills in:

| File | Use in phase |
|---|---|
| `slack-app-manifest.yaml` | Phase 1 — paste into "Create app from manifest" at api.slack.com/apps |
| `assistant.env.example` | Phase 3 — copy to the service's env file, mode 600 |
| `com.example.slack-assistant.plist` | Phase 4 — launchd daemon (macOS); the systemd unit is the same shape |
| `notify.sh` | Phase 6 — post to the sites channel from any script |
