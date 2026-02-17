# AGENTS Rules

## Core Behavior

- Keep changes scoped to the active issue.
- Do not break the build or tests.
- Do not skip tests for changed behavior.
- Do not merge if contract/docs are stale.

## Required Per Issue

- Implement acceptance criteria from issue spec.
- Add or update tests (unit/integration as needed).
- Update `openapi.yaml` when API contracts change.
- Update `README.md` and/or process docs when workflows change.
- Add a short demo command in the PR description.

## Git Conventions

- Branch name: `codex/issue-<n>-<slug>`
- Commit style: small and logical (no giant mixed commits).
- PR title: `Issue <n>: <short summary>`

## Test Gate

Before opening or updating PR:

1. Run relevant tests locally.
2. Confirm no regression in previous issue behavior.
3. Confirm docs referenced by the issue are current.

## Source of Truth

Project scope and acceptance criteria are defined in:

- `JetFormBuilder_KnowledgeGPT_SPEC.md`
- `PLANS.md`
