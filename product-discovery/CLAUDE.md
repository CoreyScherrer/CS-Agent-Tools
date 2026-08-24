# Running this framework

Instructions for Claude when working inside a Masterful Product Swashbuckling project.

## Before anything

Read `protocol/evidence.md` and `protocol/assumptions.md` before writing any artifact.
They are short and they are the point of the framework. Skills reference them rather than
restating them, so a skill read without the protocol is missing its rules.

## The rule that matters most

**Never write a number you cannot source.**

Not a volume, not a duration, not a user count, not a percentage, not a cost. If the
evidence base does not establish it and the person did not tell you, it is an assumption
with an ID and a validation path — or it does not appear.

This is not a style preference. A plausible invented number in a PRD becomes organizational
fact: it gets quoted in planning, inherited by people who were not in the room, and
defended by people who assume someone verified it. It is the highest-damage thing an AI
can do to a product process, and it happens silently.

When you catch yourself about to write "approximately" or "roughly" in front of a figure
nobody gave you — stop. That is the tell.

## Working order

1. Check whether `corpus.yaml` is filled in. If not, that is the first conversation.
2. Do not interview the person about things the corpus answers. Mine first, then ask about
   gaps. This is the whole reason MINE precedes DISCOVER.
3. Write artifacts to disk, never to chat. Chat output does not survive the session, does
   not diff, and cannot be linted.
4. Lint before presenting — **both** scripts:

       python3 scripts/lint-artifact.py <project-dir>
       python3 scripts/lint-evidence.py <project-dir>

   The evidence lint is the one that checks the files everything else rests on. Run it
   after every mining session, not just at the end.
5. Run `critique-artifact` before anything moves to `reviewed`. Both `reviewed` and
   `final` require a `last_critique` date.

## Facilitation

Per `protocol/facilitation.md`: one question at a time, numbered options with an escape,
stage gates where the person confirms before proceeding.

Default to context-dump mode when a corpus exists. Asking a person to answer questions
their own documents already answer is the failure mode this framework was built to avoid.

## Stage gates

At each gate report: artifacts written (paths), findings added (count), assumptions
registered (with high-impact ones named), and what the next stage needs that you do not
have.

A **high**-impact open assumption blocks advancement past DEFINE — not before. Expect to
accumulate them in FRAME and MINE; that is the framework working, and they become the
DISCOVER agenda. `lint-evidence.py` reports them at every stage so the gate never ambushes
you at stage 4.

**You may not accept a risk on someone's behalf.** If the gate blocks and no person has
accepted, stop and report which assumptions block, and what each would take to validate.
That report is the required output, not a failure to finish.

## Tone

The framework has a swashbuckling name. The artifacts it produces are sober professional
documents that will be read by people who did not choose the name and may not find it
charming. Keep the theme in the framework's own voice — README, command names, docs — and
out of the deliverables.

## What not to do

- Do not copy content from third-party skill libraries into this repo. Frameworks are cited
  to their originators; text here is original. See the attribution note in README.
- Do not put employer-specific, project-specific, or personal-infrastructure references in
  `skills/`, `protocol/`, or `scripts/`. Those must stay portable enough to hand to another
  team unchanged. Project specifics live in the project directory.
- Do not leave placeholders in anything that leaves your hands. A placeholder reads as
  complete and is not; a stated gap reads as honest. The linter fails on the former.
