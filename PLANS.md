# Execution Plan

Source: `JetFormBuilder_KnowledgeGPT_SPEC.md`

## Workflow Rules

- Execute issues in sequence from 1 to 12 unless explicitly re-prioritized.
- Each issue has:
  - one branch (`codex/issue-<n>-<slug>`),
  - one PR,
  - tests,
  - documentation updates.
- Keep status updated in this file.

## Issue Tracker

1. [x] Issue 1 - Bootstrap repo + local dev environment
2. [x] Issue 2 - DB schema + migrations
3. [x] Issue 3 - URL discovery (sitemaps-first)
4. [ ] Issue 4 - Crawler fetch + parse content
5. [ ] Issue 5 - Theme extraction + normalization
6. [ ] Issue 6 - Search API (ranking + filters)
7. [ ] Issue 7 - Doc retrieval API
8. [ ] Issue 8 - Theme listing + gaps API
9. [ ] Issue 9 - OpenAPI schema + auth + hardening
10. [ ] Issue 10 - Custom GPT configuration package
11. [ ] Issue 11 - Deployment pipeline
12. [ ] Issue 12 - Post-deploy verification

## Current Status

- 2026-02-17: Issue 1 completed (FastAPI `/health`, Postgres compose, scripts, tests, CI, GitHub issue created and tracked).
- 2026-02-17: Issue 2 completed (migrations, DB layer, DB tests, CI validation, docs and conventions).
- 2026-02-17: Issue 2 hardening updates completed (safe local `db-reset`, deterministic migration URLs, bounded DB readiness waits, fail-fast DB integration setup, encoded/IPv6-safe DB URL generation, and added unit coverage).
- 2026-02-18: Issue 3 completed (sitemap-first discovery module, `discovered_urls` queue schema, discovery command/logging contract, and discovery test coverage).

## Release Milestones

- `v0.1.0`: Issues 1-3 complete
- `v0.2.0`: Issues 4-5 complete
- `v0.3.0`: Issues 6-8 complete
- `v0.4.0`: Issues 9-10 complete
- `v1.0.0`: Issues 11-12 complete and evaluation passed
