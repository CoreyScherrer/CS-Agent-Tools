# CS-Agent-Tools

_Portable tools for AI-assisted work. Each is a guide you and your AI agent follow
together. Nothing here is specific to one person's machines, accounts or paths._

> Why, hello there! You've wandered into a small library of journeys through the
> wonderful world of Artificial Intelligence and its many marvellous
> capabilities. Each page below is one expedition: pick it, hand it to your
> trusty AI agent, and together you'll arrive somewhere delightful. The future is
> bright, the instructions are clear, and the gotchas have already been met so you
> needn't meet them yourself.

## The tools

| Tool | What you end up with | Human time | AI time |
|---|---|---|---|
| [[Memory-Archive]] | Persistent memory across AI coding sessions, no network calls | 20 min | 30 min |
| [[Mac-Mini-Web-Server]] | A home server on a Mac mini, safely reachable from the internet, with a private network for admin | 3–5 h | 6–10 h |
| [[Slack-Assistant]] | A personal AI assistant and ops console in your Slack workspace | 1–2 h | 2–4 h |
| [[Product-Discovery]] | An evidence-first product discovery framework with 25 skills | 10 min | — |
| [[Build-A-Tool]] | The agent that writes the next guide to the same standard | 5 min | per tool |

Times are honest estimates for a first run with an AI coding agent doing the
file and shell work; see each page's §Setup time for what drives them.

## How to use a guide

1. Read §What this is and §What you need. Decide §Free vs paid.
2. Open your AI coding agent **on the machine being set up** (or over SSH into
   it) and give it the page. Give it a browser too — dashboards are half the work.
3. Work the phases in order. You do the human steps (sign-ups, approvals,
   cables); the agent does the rest. Each phase ends with a check you can run.
4. When a step produces a secret, paste it where the agent says — never into chat.

## The rules every page follows

- **[[Guide-Standard]]** — ten sections, decisions with defaults, real gotchas only.
- **[[Data-Boundary]]** — the framework is shareable; what it captures is not.
- No real hostnames, IPs, handles or home paths anywhere (`scripts/check-neutral.sh`).

## Other pages

| Page | What it covers |
|---|---|
| [[Setup]] | Standing the Memory Archive up on a new or restricted machine |
| [[Daily-Use]] | Memory Archive capture and recall |
| [[Architecture]] | How the Memory Archive is built and why |
| [[Troubleshooting]] | Memory Archive symptoms, causes, fixes |
| [[Roadmap]] | What the Memory Archive's Phase 2 depends on |
