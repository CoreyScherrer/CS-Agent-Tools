# Facilitation Protocol

How skills in this framework talk to the person running them. Every interactive skill
references this file rather than restating it.

## Entry modes

At the start of any skill, offer three ways in:

1. **Guided** — one question at a time, full depth
2. **Context dump** — the person pastes what they have; the skill extracts what it can
   and asks only about genuine gaps
3. **Best guess** — the skill drafts from available evidence and flags every guess

Mode 2 is the default when a corpus exists, and it is the mode that makes this framework
faster than a template. Do not ask a person a question the corpus already answers. Mine
first, then ask about the gaps. Nothing burns stakeholder patience faster than being
interviewed about something you wrote down last quarter.

Mode 3 always produces assumption ledger entries for every guess. A best-guess artifact
that does not carry visible assumption markers is a failure, not a shortcut.

## One question at a time

Never bundle. A person answering four questions at once answers the first well and the
rest carelessly. Ask one, listen, let the answer shape the next.

Prefer numbered options when the answer space is knowable — they are faster to answer
than open prompts and they surface possibilities the person had not considered. Always
include an escape:

    1. Weekly
    2. Monthly
    3. Ad hoc, on request
    4. Something else (describe)

Accept `1,3` and `1 and 3` for multi-select.

## Progress

Show position in longer sequences: `Framing 3/6`. People tolerate a long process when
they can see its shape. They abandon one that feels unbounded.

## Stage gates

Between stages, stop. Summarize what was produced, what is still open, and what the next
stage will do. The person confirms before proceeding.

This is the human gate, and it is not ceremony — it is where a wrong turn gets caught for
the cost of one conversation instead of three artifacts.

At each gate, report:
- Artifacts written this stage (paths)
- New findings added to the evidence base (count)
- New assumptions registered, with any high-impact ones named explicitly
- What the next stage needs that you do not yet have

## Running non-interactively

This framework will often run without a person available to answer turn by turn — from a
context dump, in a batch job, or inside a subagent. That is a legitimate mode, not a
degraded one, but it changes what you must do.

When there is nobody to ask:

- **Default to context-dump mode.** Extract everything the corpus and the brief support.
- **Do not silently guess the rest.** Every gap becomes an assumption ledger entry with a
  real `how_to_validate`. This is the whole substitute for asking.
- **Do not simulate the person's answers.** Inventing what a stakeholder would probably say
  and proceeding as if they said it is the worst available failure — it manufactures
  consent and buries the fact that nobody was consulted.
- **Do not self-accept a blocking gate.** If a high-impact assumption blocks DEFINE, stop
  and report it. Claude does not accept risk on someone's behalf.
- **Report the questions you would have asked**, in priority order, at the end. That list is
  a deliverable — it is the agenda for the first conversation with a real person.

An artifact produced non-interactively must say so in Provenance, so a reader knows which
gaps are unexplored versus explored-and-empty.

## Interruption

The person can stop, redirect, or jump stages at any point. Do not insist on sequence when
they have a reason to break it. Note in the artifact frontmatter when a stage was skipped
or run shallow, so the gap is visible later rather than invisible.

## Tone

Plain and direct. This framework has a swashbuckling name; the artifacts it produces are
sober professional documents that will be read by people who did not choose the name. Keep
the theme in the framework's voice — README, command names, docs — and out of the
deliverables.
