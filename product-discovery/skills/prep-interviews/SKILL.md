---
name: prep-interviews
description: Plan interviews that only cover what the corpus could not answer. Use after gaps are identified, before talking to anyone.
stage: 3
inputs: [artifacts/3-gaps.md, artifacts/1-stakeholders.md]
outputs: [artifacts/3-interview-plan.md]
depth: quick | standard | deep
---

# Prep Interviews

## Purpose

Plan conversations that earn the time they cost.

By the time this skill runs, mining has already answered most factual questions and the gap
list has stripped out everything resolvable another way. What remains is what only a person
can provide: motivation, experience, tradeoffs, what they do when the system fails, and the
reasons behind choices that look irrational from outside.

Interviewing for facts a document already contains is the fastest way to teach stakeholders
that talking to you is not worth it.

## When To Use

- After `identify-gaps`, for the gaps classified as requiring conversation
- Before any user or stakeholder interview

## When Not To Use

- Before mining and gap identification. An interview plan written first will be full of
  questions the corpus answers.
- For single-fact questions — those are a message, not an interview.

## Process

Follow `protocol/facilitation.md`.

**1. Take only the interview-classified gaps.** If a question is not on that list, it does
not go in the plan. This constraint is the point.

**2. Group by person, then decide who is actually necessary.** Three well-chosen
conversations beat eight obligatory ones. Prefer people who do the work over people who
manage it — and where both matter, interview them separately. People describe their process
differently in front of their manager.

**3. Write questions that ask about the past, not the future.** "Walk me through the last
time you needed this" produces evidence. "Would you use a dashboard?" produces speculation
that sounds like data and is worthless. Past behavior is observable; future intention is
not.

**4. Ask for specifics, not generalities.** "How often does that happen?" gets an estimate.
"When did it last happen?" gets an incident you can follow. Specific memories are reliable;
frequency self-reports are not.

**5. Prepare for what the corpus suggested but could not confirm.** Where mining surfaced a
conflict or a suspicious workaround, plan how to raise it without leading. Show the artifact
and ask what it is for, rather than asking whether your interpretation is correct.

**6. Plan for disconfirmation.** For each thing you believe, write the question that would
reveal it to be wrong. Interviews that only seek confirmation reliably provide it.

**7. Decide what you will not ask.** Questions that are really solution pitches, questions
whose answers you would ignore, and anything already answered. Writing the exclusions keeps
the conversation short and the goodwill intact.

**8. Plan the capture.** Who takes notes, whether it is recorded, how findings will enter
the evidence base. Interview evidence that never gets recorded is the most common way
discovery effort evaporates.

## Output Contract

**Path:** `artifacts/3-interview-plan.md`

**Required sections:**
- `# Interview Plan`
- `## Who And Why` — each person, the gaps they can close, why them specifically
- `## Questions By Person` — grouped; each question tied to a gap ID
- `## Disconfirming Questions` — what would reveal our current beliefs to be wrong
- `## Artifacts To Show` — what to put in front of them, and how to raise it neutrally
- `## Not Asking` — deliberate exclusions and why
- `## Capture Plan` — notes, recording, how findings reach the evidence base
- `## Provenance` — per `protocol/artifact-standards.md`

**Frontmatter:** `artifact: interview-plan`, `stage: 3`.

## Evidence Requirements

Per `protocol/evidence.md`.

**Must cite:** every question references the gap ID or assumption ID it addresses. A
question with no provenance is one you invented, and it is usually the one that wastes the
interview.

**Must cite or mark as assumption:** claims about what a person knows or does — these
determine who you interview and are frequently wrong.

## Pitfalls

**Pitfall 1 — Asking what the corpus answered.**
*Symptom:* Questions about documented process or stated volumes. *Consequence:* Wasted
time, and the interviewee concludes you did not read what they sent.
*Fix:* Gap list only. If it is not a gap, it is not a question.

**Pitfall 2 — Hypothetical questions.**
*Symptom:* "Would you…", "Do you think you'd…". *Consequence:* Speculation recorded as
evidence, and people are systematically poor at predicting their own behavior.
*Fix:* Ask about the last actual occurrence.

**Pitfall 3 — Leading with your interpretation.**
*Symptom:* "So the problem is the category mapping, right?" *Consequence:* Agreement that
confirms nothing, because most people accommodate a confident framing.
*Fix:* Show the artifact, ask what it does, stay quiet.

**Pitfall 4 — Interviewing only managers.**
*Symptom:* The plan covers people who describe work rather than do it.
*Consequence:* You learn the official process, which frequently differs from the real one.
*Fix:* Interview practitioners; separately.

**Pitfall 5 — No capture plan.**
*Symptom:* Notes taken ad hoc, findings never recorded. *Consequence:* The most expensive
evidence you gather never reaches the evidence base. *Fix:* Decide in advance.

## References

**Related skills:** `identify-gaps` (stage 3), `synthesize-research` (stage 3),
`map-stakeholders` (stage 1)

**Protocol:** `protocol/evidence.md`, `protocol/facilitation.md`

**External frameworks:** Asking about past behavior rather than future intention follows
Rob Fitzpatrick, *The Mom Test* (2013). Interview structure and continuous-interviewing
cadence follow Teresa Torres, *Continuous Discovery Habits* (2021). Contextual observation
of practitioners follows Beyer and Holtzblatt, *Contextual Design* (1997).
