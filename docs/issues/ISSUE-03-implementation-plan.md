# Feature Implementation Plan

**Overall Progress:** `83%`

## TLDR
Implement Issue 3 by adding a sitemap-first URL discovery pipeline that stores crawl candidates in a dedicated queue table, classifies URLs with a safe fallback, and reports source/type discovery counts for predictable handoff to Issue 4.

## Critical Decisions
Key architectural/implementation choices made during exploration:
- Decision 1: Use a dedicated `discovered_urls` queue table (not `docs`) - `docs` requires parsed content fields and is not suitable for discovery-only records.
- Decision 2: Discovery acceptance target is "discover all available URLs," with success requiring at least 50 URLs per source when that source exposes enough URLs - keeps validation realistic and measurable.
- Decision 3: Classify URL type using deterministic URL-pattern rules with `unknown` fallback - ensures stable behavior before full HTML parsing in Issue 4.
- Decision 4: Keep Issue 3 sitemap-first only, with optional fallback explicitly deferred unless required by acceptance during execution - prevents scope creep into crawler implementation.

## Tasks:

- [x] 🟩 **Step 1: Define Discovery Data Contract and Migration**
  - [x] 🟩 Add migration for `discovered_urls` queue table with uniqueness and crawl-state fields.
  - [x] 🟩 Add/update SQLAlchemy models for discovery records and enum/check constraints aligned with existing conventions.
  - [x] 🟩 Add minimal indexes required for queue reads and idempotent inserts.

- [x] 🟩 **Step 2: Build Sitemap Discovery Module**
  - [x] 🟩 Implement sitemap index and sitemap URL parsing flow for both sources.
  - [x] 🟩 Normalize and deduplicate URLs before persistence.
  - [x] 🟩 Implement deterministic source/type classification with `unknown` fallback.

- [x] 🟩 **Step 3: Persist Discovery Results for Crawl Runs**
  - [x] 🟩 Add repository functions for idempotent enqueue/upsert of discovered URLs.
  - [x] 🟩 Store metadata needed by Issue 4 handoff (source, type, discovered timestamp, status).
  - [x] 🟩 Ensure repeated discovery runs do not create duplicates.

- [x] 🟩 **Step 4: Add Execution Command and Discovery Logging**
  - [x] 🟩 Add a dedicated make/script command to run URL discovery.
  - [x] 🟩 Emit structured summary counts by source and type.
  - [x] 🟩 Return a clear non-zero status when discovery fails hard.

- [x] 🟩 **Step 5: Add Tests for Parsing, Classification, and Persistence**
  - [x] 🟩 Add unit tests with mocked sitemap XML for parser behavior.
  - [x] 🟩 Add unit tests for URL type classification and normalization edge cases.
  - [x] 🟩 Add integration test for DB persistence idempotency and count reporting contract.

- [ ] 🟨 **Step 6: Validate Acceptance and Update Documentation**
  - [x] 🟩 Run lint/tests and capture command evidence for Issue 3 closure.
  - [x] 🟩 Document discovery command usage and expected output in process/readme docs.
  - [ ] 🟨 Update issue closure evidence with CI links and acceptance verification.

## Scope Guardrails

- Explicit non-goals and what must not change.
- No HTML fetch/content extraction (Issue 4 scope).
- No theme extraction or gap logic (Issue 5/8 scope).
- No search/retrieval API implementation changes (Issue 6/7 scope).
- Keep existing DB safety patterns intact (`_test` guardrails and destructive reset controls).
- Constraints: time, performance, compatibility, security/compliance, hosting/runtime.
- Keep dependencies lightweight and aligned with existing Python stack.
- Discovery should be deterministic and idempotent.
- Maintain compatibility with current Postgres + Alembic workflow.
- Rollout expectations: feature flag, phased rollout, migration expectations.
- No feature flag required for Issue 3.
- No phased rollout required.
- Include forward migration path and safe rollback support for schema changes.

## Output Quality Checklist

- No implementation details beyond planning.
- No extra complexity or speculative scope.
- Status emojis applied consistently.
- Progress percentage matches top-level task states.
- Steps are concise and directly actionable.
