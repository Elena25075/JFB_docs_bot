---
name: create-issue
description: "Capture an in-progress development problem and produce a complete issue ticket fast. Use when the user wants quick issue intake (2-3 targeted questions), codebase file discovery limited to 3 files, and a structured output with title, labels, TL;DR, current vs expected state, done criteria, success metrics, non-goals, constraints, and rollout expectations."
---

# Create Issue (Fast Intake)

## Hard Rules

- Do not implement or fix code.
- Keep the exchange under 2 minutes.
- Ask 2-3 targeted questions total. Ask fewer if enough details already exist.
- Use bullet points over long paragraphs.
- Keep code context to a maximum of 3 files.
- Default labels when missing: `Priority=normal`, `Effort=medium`.
- Allowed type values: `bug`, `feature`, `improvement`.

## Required Input

- Capture the issue description verbatim first.
- If the issue description is missing, ask for a one-sentence problem statement.

## Question Strategy (Ask Only Missing Essentials)

- Question 1 (classification + goal):
  - "Is this a bug, feature, or improvement, and what should be true when done?"
- Question 2 (scope + constraints):
  - "What must not change, and what constraints apply (time, performance, compatibility, security/compliance, hosting/runtime)?"
- Question 3 (rollout + risk):
  - "Do you need a feature flag, phased rollout, or migration plan, and is there any priority override?"

If the user already provided parts of the above, do not re-ask them. Keep total questions <= 3.

## File Discovery Workflow (Max 3 Files)

- Extract 3-8 concrete keywords from the issue and answers.
- Search quickly with `rg`:
  - `rg -n -S "<keyword1>|<keyword2>|<keyword3>" .`
  - `rg --files | rg "<module|domain|feature-term>"`
- Select up to 3 files with highest relevance and include one reason per file.
- Prefer this order when possible: entrypoint -> core logic -> tests/config.
- If nothing relevant is found, write `- (none found in current repo)`.

Optional helper:
- `python3 skills/create-issue/scripts/find_relevant_files.py --query "<issue text>" --root .`

## Output Construction

- Build a clear, action-oriented title.
- Include:
  - Type, Priority, Effort labels.
  - TL;DR.
  - Current State.
  - Expected Outcome with:
    - Definition of done.
    - Success metrics.
  - Relevant Files (max 3).
  - Notes/Risks with:
    - Non-goals / must not change.
    - Constraints.
    - Rollout expectations (feature flag, phased rollout, migration).
- Keep bullets short and concrete.

## Output Format

Use this exact structure:

## [Title]
**Type:** bug | feature | improvement
**Priority:** low | normal | high | critical
**Effort:** small | medium | large

### TL;DR
- ...

### Current State
- ...

### Expected Outcome
- ...
- **Done means:**
- **Success is measured by:**

### Relevant Files
- `path/to/file` - reason
- `path/to/file` - reason
- `path/to/file` - reason

### Notes/Risks
- **Non-goals / must not change:**
- **Constraints:**
- **Rollout expectations:**

## Fallback When Context Is Missing

- If the repo is empty or inaccessible, still produce the issue from provided text.
- Set `Relevant Files` to `(none found in current repo)`.
- Ask one extra follow-up only if a blocker remains and still keep total questions <= 3.

