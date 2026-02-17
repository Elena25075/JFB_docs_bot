# Feature Implementation Plan

**Overall Progress:** `100%`

## TLDR
Deliver a simple, working Postgres persistence foundation for Issue 2 by adding migrations, baseline DB access utilities, test coverage, and operator commands without expanding into crawler/search features.

## Critical Decisions
Key architectural/implementation choices made during exploration:
- Decision 1: Alembic + SQLAlchemy 2.x (sync) + psycopg - simplest reliable stack with strong migration support and low complexity.
- Decision 2: UUID generated in DB with `gen_random_uuid()` - keeps ID creation consistent and independent from application code.
- Decision 3: `TEXT` + `CHECK` constraints for enums - easier evolution for early-stage schema than PostgreSQL enum types.
- Decision 4: Minimal index set (`source`, `type`, `published_at`, `doc_themes.theme`) - supports planned filters and theme queries without premature indexing.

## Tasks:

- [x] 🟩 **Step 1: Establish DB Toolchain and Configuration**
  - [x] 🟩 Add DB/migration dependencies (SQLAlchemy, Alembic, psycopg).
  - [x] 🟩 Initialize migration structure under `migrations/` and `migrations/versions/`.
  - [x] 🟩 Define DB connection config contract from env vars (compatible with `.env.example`).

- [x] 🟩 **Step 2: Create Baseline Schema Migration**
  - [x] 🟩 Create migration to enable `pgcrypto` extension.
  - [x] 🟩 Create `docs`, `themes`, and `doc_themes` tables with required columns.
  - [x] 🟩 Enforce constraints: `UNIQUE (docs.url)`, `CHECK` constraints for `source` and `type`, PK/FK constraints.
  - [x] 🟩 Add minimum indexes: `docs(source)`, `docs(type)`, `docs(published_at DESC)`, `doc_themes(theme)`.

- [x] 🟩 **Step 3: Add Minimal DB Access Layer**
  - [x] 🟩 Add engine/session lifecycle module for sync DB access.
  - [x] 🟩 Add minimal access primitives needed for insert/select test coverage.
  - [x] 🟩 Keep API health endpoint independent from DB checks (lightweight policy).

- [x] 🟩 **Step 4: Add Migration and DB Operations Commands**
  - [x] 🟩 Add `make migrate-up` mapped to `alembic upgrade head`.
  - [x] 🟩 Add `make migrate-down` mapped to `alembic downgrade -1`.
  - [x] 🟩 Add `make db-reset` for clean local DB iteration.

- [x] 🟩 **Step 5: Add Tests and CI DB Verification**
  - [x] 🟩 Add migration test from clean DB state (`migrate up` creates all tables/constraints).
  - [x] 🟩 Add insert/select integration test against migrated schema.
  - [x] 🟩 Update CI to run DB-backed tests with a Postgres service container.

- [x] 🟩 **Step 6: Document Migration Conventions and Evidence**
  - [x] 🟩 Document migration naming/versioning convention in process docs.
  - [x] 🟩 Add Issue 2 closure evidence file with command outputs and CI link.
  - [x] 🟩 Update `PLANS.md` status and close GitHub Issue 2 only after all criteria pass.

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
