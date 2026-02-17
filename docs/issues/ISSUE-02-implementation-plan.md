# Feature Implementation Plan

**Overall Progress:** `0%`

## TLDR
Deliver a simple, working Postgres persistence foundation for Issue 2 by adding migrations, baseline DB access utilities, test coverage, and operator commands without expanding into crawler/search features.

## Critical Decisions
Key architectural/implementation choices made during exploration:
- Decision 1: Alembic + SQLAlchemy 2.x (sync) + psycopg - simplest reliable stack with strong migration support and low complexity.
- Decision 2: UUID generated in DB with `gen_random_uuid()` - keeps ID creation consistent and independent from application code.
- Decision 3: `TEXT` + `CHECK` constraints for enums - easier evolution for early-stage schema than PostgreSQL enum types.
- Decision 4: Minimal index set (`source`, `type`, `published_at`, `doc_themes.theme`) - supports planned filters and theme queries without premature indexing.

## Tasks:

- [ ] 🟥 **Step 1: Establish DB Toolchain and Configuration**
  - [ ] 🟥 Add DB/migration dependencies (SQLAlchemy, Alembic, psycopg).
  - [ ] 🟥 Initialize migration structure under `migrations/` and `migrations/versions/`.
  - [ ] 🟥 Define DB connection config contract from env vars (compatible with `.env.example`).

- [ ] 🟥 **Step 2: Create Baseline Schema Migration**
  - [ ] 🟥 Create migration to enable `pgcrypto` extension.
  - [ ] 🟥 Create `docs`, `themes`, and `doc_themes` tables with required columns.
  - [ ] 🟥 Enforce constraints: `UNIQUE (docs.url)`, `CHECK` constraints for `source` and `type`, PK/FK constraints.
  - [ ] 🟥 Add minimum indexes: `docs(source)`, `docs(type)`, `docs(published_at DESC)`, `doc_themes(theme)`.

- [ ] 🟥 **Step 3: Add Minimal DB Access Layer**
  - [ ] 🟥 Add engine/session lifecycle module for sync DB access.
  - [ ] 🟥 Add minimal access primitives needed for insert/select test coverage.
  - [ ] 🟥 Keep API health endpoint independent from DB checks (lightweight policy).

- [ ] 🟥 **Step 4: Add Migration and DB Operations Commands**
  - [ ] 🟥 Add `make migrate-up` mapped to `alembic upgrade head`.
  - [ ] 🟥 Add `make migrate-down` mapped to `alembic downgrade -1`.
  - [ ] 🟥 Add `make db-reset` for clean local DB iteration.

- [ ] 🟥 **Step 5: Add Tests and CI DB Verification**
  - [ ] 🟥 Add migration test from clean DB state (`migrate up` creates all tables/constraints).
  - [ ] 🟥 Add insert/select integration test against migrated schema.
  - [ ] 🟥 Update CI to run DB-backed tests with a Postgres service container.

- [ ] 🟥 **Step 6: Document Migration Conventions and Evidence**
  - [ ] 🟥 Document migration naming/versioning convention in process docs.
  - [ ] 🟥 Add Issue 2 closure evidence file with command outputs and CI link.
  - [ ] 🟥 Update `PLANS.md` status and close GitHub Issue 2 only after all criteria pass.

## Scope Guardrails

- Explicit non-goals and what must not change.
- No crawler/discovery implementation in this issue.
- No search, retrieval, themes, or gaps endpoint implementation in this issue.
- Keep `/health` lightweight and not DB-dependent.
- Constraints: time, performance, compatibility, security/compliance, hosting/runtime.
- Must stay aligned with GitHub Free guardrails (`docs/process/GITHUB_FREE_LIMITS.md`).
- Must use Postgres as source-of-truth schema runtime.
- Must keep migrations deterministic and repeatable from clean state.
- Rollout expectations: feature flag, phased rollout, migration expectations.
- No feature flag required.
- No phased rollout required.
- Include forward migration path and practical rollback support.

## Output Quality Checklist

- No implementation details beyond planning.
- No extra complexity or speculative scope.
- Status emojis applied consistently.
- Progress percentage matches top-level task states.
- Steps are concise and directly actionable.
