---
name: create-plan
description: "Create a concise implementation plan document from prior exploration and issue capture. Use when the user wants planning only (no coding yet), with modular minimal steps, emoji task statuses, and dynamic overall progress tracking."
---

# Plan Creation Stage

## Hard Rules

- Do not implement code or make code changes.
- Produce only a clear markdown plan document.
- Do not add extra scope beyond explicitly clarified details.
- Keep steps minimal, modular, and aligned to existing codebase structure.
- Prefer bullet points over long paragraphs.

## Inputs To Use

- Use the full prior exchange in the thread.
- Use confirmed decisions from exploration and issue capture.
- If critical detail is missing, ask at most 1 focused clarification question.

## Status System

Use only these statuses:

- `🟩 Done`
- `🟨 In Progress`
- `🟥 To Do`

Task checkbox mapping:

- `- [x] 🟩` for complete
- `- [ ] 🟨` for active
- `- [ ] 🟥` for not started

## Progress Calculation

- Add `Overall Progress` at the top.
- Compute percentage from top-level steps only:
  - `Progress = (Done top-level steps / Total top-level steps) * 100`
- Round to the nearest whole percent.
- Keep this value updated whenever statuses change.

## Planning Rules

- Keep the plan elegant and concise.
- Use only necessary steps to deliver the clarified outcome.
- Ensure each step can be executed independently without ambiguity.
- Keep integration seamless with existing architecture and conventions.
- Include only realistic tasks that follow from confirmed scope.

## Required Output Template

Use this exact structure:

# Feature Implementation Plan

**Overall Progress:** `0%`

## TLDR
Short summary of what we're building and why.

## Critical Decisions
Key architectural/implementation choices made during exploration:
- Decision 1: [choice] - [brief rationale]
- Decision 2: [choice] - [brief rationale]

## Tasks:

- [ ] 🟥 **Step 1: [Name]**
  - [ ] 🟥 Subtask 1
  - [ ] 🟥 Subtask 2

- [ ] 🟥 **Step 2: [Name]**
  - [ ] 🟥 Subtask 1
  - [ ] 🟥 Subtask 2

## Scope Guardrails

- Explicit non-goals and what must not change.
- Constraints: time, performance, compatibility, security/compliance, hosting/runtime.
- Rollout expectations: feature flag, phased rollout, migration expectations.

## Output Quality Checklist

- No implementation details beyond planning.
- No extra complexity or speculative scope.
- Status emojis applied consistently.
- Progress percentage matches top-level task states.
- Steps are concise and directly actionable.

