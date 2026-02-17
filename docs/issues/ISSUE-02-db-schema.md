## DB Schema + Migrations (Issue 2)
**Type:** feature
**Priority:** high
**Effort:** medium

### TL;DR
- Add first database schema and migration workflow for `docs`, `themes`, and `doc_themes`, with a working DB access layer and tests.
- Use the simplest production-viable stack: Alembic + SQLAlchemy + Postgres.

### Current State
- Issue 1 bootstrap is complete with FastAPI, local Postgres in Docker, and CI lint/test gates.
- There are no DB tables, migration files, or DB access abstractions yet.

### Expected Outcome
- The project can run migrations to create required tables and enforce URL uniqueness for docs.
- A baseline DB access layer exists (SQLAlchemy or lightweight SQL) ready for crawler and API issues.
- **Done means:**
- Migration tooling is added and `migrate up` creates `docs`, `themes`, and `doc_themes`.
- `docs.url` uniqueness is enforced at DB level.
- A minimal DB access layer is implemented and usable by future issues.
- Migration and insert/select tests pass locally and in CI.
- Migration naming/versioning conventions are documented.
- A local DB reset helper command is available.
- **Success is measured by:**
- Running migrations from a clean Postgres instance succeeds consistently.
- Test coverage confirms schema creation and round-trip insert/select behavior.

### Relevant Files
- `JetFormBuilder_KnowledgeGPT_SPEC.md` - source of truth for required tables and acceptance criteria.
- `docker-compose.yml` - local Postgres target for migration execution and verification.
- `app/main.py` - API entrypoint where DB integration hooks will be introduced.

### Notes/Risks
- **Non-goals / must not change:**
- Do not implement URL discovery/crawling logic (Issue 3+).
- Do not implement search, retrieval, themes, or gap APIs (Issues 6+).
- Keep `/health` lightweight (no DB dependency in Issue 2 unless explicitly approved).
- **Constraints:**
- Must remain compatible with GitHub Free guardrails (`docs/process/GITHUB_FREE_LIMITS.md`).
- Must use Postgres as the source-of-truth schema runtime.
- Migration process must be deterministic and repeatable from clean DB state.
- IDs must be generated in DB.
- Keep enum handling simple and migration-friendly.
- **Rollout expectations:**
- No feature flag needed.
- No phased rollout needed.
- Include a migration path (`up`, and rollback strategy where practical) for safe iterative schema changes.

## Implementation Decisions (Resolved During Exploration)

- Migration stack: Alembic + SQLAlchemy 2.x (sync) + psycopg.
- ID generation: DB-side UUID (`gen_random_uuid()` with `pgcrypto`).
- Enum strategy: `TEXT` columns with `CHECK` constraints for `source` and `type`.
- Minimum indexes beyond `UNIQUE (url)`:
  - `docs(source)`
  - `docs(type)`
  - `docs(published_at DESC)`
  - `doc_themes(theme)`
- Required helper commands:
  - `make migrate-up`
  - `make migrate-down`
  - `make db-reset`
