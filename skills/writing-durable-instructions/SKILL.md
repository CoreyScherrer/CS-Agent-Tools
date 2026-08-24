---
name: writing-durable-instructions
description: Write standing instructions for AI agents that stay accurate as systems change, and reject the ones that will rot. Use whenever adding or editing a rule an agent will follow across sessions, including CLAUDE.md files.
---

# Writing Durable Instructions

A standing instruction is a rule an agent follows across every future session. That
persistence is the whole value and the whole danger: **a wrong instruction is followed
faithfully for months.**

Most instruction sets decay the same way. They accumulate rules written for a system that
has since changed, nobody can tell which are still true, and eventually the whole set gets
ignored — including the rules that still matter.

This is how to write ones that age well.

## Required structure

Every instruction states four things near the top:

- **WHO** it applies to — every session? one service? one machine?
- **WHEN** to apply it — every prompt? before editing X? after deploying Y?
- **WHAT** to do — concrete commands or paths, not aspirations
- **WHY** — one line

**The WHY is what makes the rule maintainable.** Without it, a future reader who suspects
the rule is obsolete has no way to check. They will either follow something pointless or
delete something load-bearing, and both are bad.

## Reject on sight

**Aspirational rules.** "X should automatically happen when Y" where no implementation
exists. That is a feature request wearing an instruction's clothes. An agent reading it
will either try to do something impossible or assume it is already handled.

**Hardcoded version-bound identifiers.** Specific model names, package versions, or API
versions as defaults. These change. Reference the *role* — "the fast model", "the current
stable release" — and let resolution happen at use time.

**Paths that drift.** Absolute paths to things that move. Prefer discovery — an environment
variable, `git rev-parse`, a config lookup — over a literal that will be wrong after one
reorganization.

**"Always do X" with no trigger.** Always *when*? An instruction that applies to every
possible moment applies to none, because it cannot be checked.

**Long preambles.** If the actionable content starts in paragraph four, it will be skimmed
past. Lead with the rule.

**Rules that restate a default.** "Write clean code." An instruction that changes no
behavior is pure dilution — it makes the set longer and therefore less likely to be read.

## Write for the reader who has no context

The person or agent reading this in six months will not remember why it was written, will
not know what incident prompted it, and will not have been in the conversation.

Concretely:

- Name the failure the rule prevents. "Prevents the case where a deploy silently skips
  unchanged files" beats "ensures correct deploys."
- Use absolute dates, never relative ones.
- Spell out acronyms on first use, including internal ones.
- Give an example of the rule being applied, if the rule is at all subtle.

## Scope tightly

Broad instructions get violated and then ignored. An instruction that fires on every prompt
had better be genuinely universal, because a rule that is wrong 10% of the time trains the
reader to disregard it entirely — and that disregard spreads to neighboring rules.

Prefer several narrow rules with clear triggers over one broad rule with exceptions.

## Say what is forbidden, plainly

Prohibitions are the highest-value instructions because they prevent the expensive class of
error. Write them as prohibitions, not as preferences:

- "Never expose a development service on a production hostname" — clear
- "Development services should generally stay internal" — will be overridden by anyone
  with a deadline

Where a prohibition has a legitimate override, name the override explicitly and what
authorizes it. An unstated exception gets invented under pressure.

## Review triggers

Give any rule tied to a system a condition under which it should be re-examined: "revisit
if the deploy pipeline changes", "revisit when the auth provider is replaced."

Without this, instruction sets only ever grow. Nobody deletes a rule they are not sure
about, so obsolete rules accumulate until the set is untrustworthy in aggregate.

## Before adding one, ask

1. Does an existing instruction already cover this? Extend it rather than adding a near-duplicate.
2. Is this a rule, or is it a fact? Facts belong in documentation or a memory store.
3. Would an agent behave differently because of this? If no, do not add it.
4. Will this still be true in six months? If not, add the review trigger now.

## The failure this prevents

The characteristic end state of an undisciplined instruction set is not one bad rule. It is
**forty rules of unknown currency**, where the reader cannot distinguish the three that
would prevent a production incident from the thirty-seven that describe a system that no
longer exists.

At that point the set has negative value: it costs attention and delivers noise. Every rule
you add without a WHY and a review trigger moves the set closer to that state.
