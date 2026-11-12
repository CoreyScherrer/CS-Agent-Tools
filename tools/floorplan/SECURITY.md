# Security policy

> **This copy is the CS-Agent-Tools bundle** of Floorplan 0.6.1. Report problems with it through the
> [CS-Agent-Tools repository](https://github.com/CoreyScherrer/CS-Agent-Tools): its **Security** tab, **Report a vulnerability**.
>
> **Known gap:** the original project has released 0.6.2 to 0.7.3 since this bundle was cut. Version 0.7.1 hardened
> the map against a repository, or a description written about one, that tries to break, leak from or stall the map.
> This bundle fixes the one case of that found in its own audit (a file name that ran as script in the map; see the
> changelog), but the rest of 0.7.1's hardening, including the page's content security policy, is not here yet. The
> map's server is also for one person on one computer: any program running as you can read its token and page key
> (other accounts on the computer cannot, except on Windows, where the files' permissions are not set). Until the
> bundle catches up, map only code you trust.

## Reporting a vulnerability

Please report security problems privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Don't open a public issue.

Helpful details:
- what the problem is, and what someone could do with it;
- the steps to reproduce it;
- which version of Floorplan you're on (see `.claude-plugin/plugin.json`).

You'll get a reply within a few days. Once a fix is out, you'll be credited unless you'd rather not be.

## What the plugin can do

[Is it safe to install?](docs/is-it-safe.md) lists everything Floorplan does on your computer: its one outbound request, every program it runs, and what it never does. [`tests/supply-chain.test.mjs`](tests/supply-chain.test.mjs) enforces that on every pull request that changes this bundle, and each release's `CHECKSUMS.txt` lets you confirm an installed copy matches it (`node tools/checksums.mjs --check <folder>`).

## Scope

In scope:
- the map's local server (`serve.mjs`);
- anything that could leak secrets or source code;
- anything that writes outside the project's `floorplan/` folder and `CLAUDE.local.md`.

Out of scope: issues in Claude Code itself, which go to [Anthropic](https://www.anthropic.com/responsible-disclosure-policy), and in Codex itself, which go to [OpenAI](https://help.openai.com/en/articles/6653653-how-to-report-security-vulnerabilities-to-openai).

## Supported versions

Only the latest release gets security fixes.
