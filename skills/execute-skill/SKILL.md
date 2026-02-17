---
name: execute-skill
description: "Implement work exactly from an approved markdown plan without adding scope. Use when it is time to build: execute planned steps in order, follow existing codebase patterns, write minimal modular code with clear documentation, and update plan step statuses plus overall progress dynamically."
---

# Execute Plan In Full

## Hard Rules

- Implement precisely what the plan defines. Do not add extra scope.
- Do not redesign architecture unless the plan explicitly requires it.
- Keep code elegant, minimal, modular, and consistent with existing patterns.
- Follow existing conventions: naming, structure, error handling, logging, and tests.
- Add clear inline comments/docstrings where behavior is non-obvious.
- Keep comments useful and specific; avoid obvious commentary.

## Inputs

- Approved plan markdown document.
- Relevant repository context and conventions.
- Any constraints or non-goals captured during issue exploration/planning.

If the plan is missing or ambiguous, ask focused clarifying questions before coding.

## Execution Workflow

1. Read the plan document and identify:
- Ordered top-level steps.
- Definition of done and constraints.
- Any rollout/migration notes.

2. Start execution step-by-step:
- Mark current step as `🟨 In Progress` before editing.
- Implement only that step's scope.
- Verify locally (targeted tests/checks relevant to the step).
- Mark the step `🟩 Done` when complete and verified.

3. Keep plan tracking live:
- Recompute and update `**Overall Progress:**` after each status change.
- Use top-level steps only for progress percentage.

4. Continue until all planned steps are complete:
- Ensure no planned item remains unaddressed.
- If blocked, record blocker in plan notes and stop adding unrelated work.

## Status and Progress Rules

Use only these statuses in plan tasks:

- `🟩 Done` -> `- [x] 🟩`
- `🟨 In Progress` -> `- [ ] 🟨`
- `🟥 To Do` -> `- [ ] 🟥`

Progress formula:

- `Progress = (Done top-level steps / Total top-level steps) * 100`
- Round to nearest whole percent.

## Coding Standards During Execution

- Respect repository architecture boundaries.
- Prefer small, composable functions/modules over monolithic changes.
- Reuse existing helpers/utilities before introducing new abstractions.
- Keep public interface changes intentional and minimal.
- Update tests/docs only where required by the planned change.

## Plan Tracking Update Pattern

For each step transition:

1. Set current step to `🟨 In Progress`.
2. Save code changes for that step.
3. Run targeted validation.
4. Set step to `🟩 Done`.
5. Update `**Overall Progress:**`.

Optional helper:

- `python3 skills/execute-skill/scripts/update_plan_progress.py --file <plan.md>`

## Output Expectations

- Implemented code matching planned scope.
- Updated plan markdown with accurate statuses and progress.
- Brief execution summary listing:
  - Completed steps.
  - Validation performed.
  - Any blockers or deferred items (only if explicitly justified by plan constraints).

