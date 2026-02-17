---
name: issue-explorer
description: "Explore and clarify a feature/bug issue by grounding it in the current repository's goal, dependencies, and architecture. Use when the user wants investigation only (no implementation): identify mismatches/ambiguities, propose integration points, and produce a prioritized list of clarifying questions."
---

# Issue Exploration (No Implementation)

## Hard Rules

- Do not implement anything (no code changes, no refactors, no "quick fixes").
- Do not create commits/PRs.
- Do not run destructive commands.
- Prefer read-only inspection: `ls`, `rg`, `find`, opening files, and running the bundled repo context script.

## Inputs To Ask For (If Missing)

- The issue description (verbatim).
- Goal/outcome: what "done" means and how success is measured.
- Scope boundaries: explicit non-goals and what must not change.
- Constraints: time, performance, compatibility, security/compliance, hosting/runtime.
- Priority and rollout expectations: feature flag, phased rollout, migration expectations.

## Workflow

1. Restate the issue in your own words.
  - List explicit requirements.
  - List implicit assumptions you think the issue is making.
  - List success criteria and non-goals (even if inferred).

2. Ground yourself in the repo reality.
  - Identify the project's purpose and shape (README/docs if present).
  - Identify dependencies and runtime (Python/Node/etc).
  - Identify architecture: main modules, entry points, boundaries (API layer, data layer, jobs, UI).
  - Find similar/adjacent features to reuse or avoid duplicating.

Tip: Run `python3 skills/issue-explorer/scripts/repo_context.py` at repo root to get a quick snapshot.

3. Determine integration points (still no implementation).
  - Where would the feature logically live (which module/package/service)?
  - What existing interfaces are touched (routes, handlers, services, schemas, DB models, config)?
  - What new surfaces might be needed (new endpoint, new background task, new config/env var)?
  - What backward-compatibility/migration risks exist?

4. Identify mismatches and ambiguities.
  - Call out any place the issue conflicts with current code structure, naming, or capabilities.
  - Call out missing details that block a correct implementation.
  - Call out unclear ownership boundaries (which component should do what).

5. Produce a prioritized question list.
  - Ask questions that remove ambiguity fastest.
  - Prefer questions that are answerable and testable (acceptance criteria, examples, edge cases).

## Required Output: Issue Exploration Report

Produce a single Markdown report with these sections (keep it tight, but concrete):

1. **Issue Summary**
  - One paragraph summary in your own words.
  - Requirements (bullets).
  - Non-goals (bullets).

2. **Repo/Project Context**
  - Project purpose (quote file names you used, e.g. `README.md`).
  - Key dependencies and runtime (what you observed).
  - Current architecture map (bullets; optionally add a small Mermaid diagram if useful).

3. **Existing Related Code**
  - Files/dirs to read (with brief "why").
  - Similar features/patterns already present.

4. **Proposed Integration Plan (No Code)**
  - Where the change would go (modules/files by path if possible).
  - Expected new/changed interfaces (APIs, data models, config).
  - Risks/edge cases.

5. **Mismatches / Ambiguities**
  - Contradictions with current codebase or missing details.

6. **Questions To Resolve (Prioritized)**
  - P0 blocking questions.
  - P1 important questions.
  - P2 nice-to-have questions.

## If Repo Context Is Missing

If the repository is empty or lacks docs/dependency files, say so explicitly and focus on:

- The minimum info needed to start (questions).
- A suggested "project inventory" checklist the user can provide (README, deps files, directory tree, entry points).
