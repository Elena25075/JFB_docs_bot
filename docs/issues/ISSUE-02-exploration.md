# Issue Exploration Report: Issue 2 (DB schema + migrations)

## 1. Issue Summary

Issue 2 establishes the first durable persistence layer for the project: create schema and migration workflow for `docs`, `themes`, and `doc_themes`, add a minimal DB access layer, and validate via migration and insert/select tests.

Requirements:

- Add migration tooling and baseline migrations.
- Create tables: `docs`, `themes`, `doc_themes`.
- Enforce unique URL in `docs`.
- Add minimal DB access layer for future issues.
- Add migration and insert/select tests.

Non-goals:

- No crawler/discovery logic (Issue 3+).
- No search/doc retrieval/themes API implementation (Issue 6+).
- Keep `/health` lightweight (no DB dependency in Issue 2).

## 2. Repo/Project Context

Project purpose observed in:

- `README.md`
- `JetFormBuilder_KnowledgeGPT_SPEC.md`
- `PLANS.md`

Key dependencies/runtime:

- Python 3.11+
- FastAPI + Uvicorn
- Pytest + Ruff
- Local Postgres via Docker Compose
- No DB/migration toolchain yet

Current architecture map:

- API entrypoint: `app/main.py`
- DB runtime container: `docker-compose.yml`
- Env contract: `.env.example`
- CI/test gate: `.github/workflows/ci.yml`
- Migration location reserved: `migrations/versions/`

## 3. Existing Related Code

Files/dirs to read:

- `JetFormBuilder_KnowledgeGPT_SPEC.md` - canonical table and acceptance requirements.
- `docs/issues/ISSUE-02-db-schema.md` - active issue scope.
- `docker-compose.yml` - DB runtime target for migrations.
- `.env.example` - DB connection variables.
- `pyproject.toml` - dependency surface to extend for DB/migrations.
- `.github/workflows/ci.yml` - where DB checks must run.
- `Makefile` - place for `migrate up/down` and reset helpers.

Similar patterns already present:

- Script/Make-driven developer workflow and CI checks from Issue 1.

## 4. Proposed Integration Plan (No Code)

Selected decisions for simplest working setup:

- Migration stack: **Alembic + SQLAlchemy 2.x (sync) + psycopg**.
- DB access layer: simple SQLAlchemy session/repository baseline (sync), no async yet.
- Migration command contract:
  - `make migrate-up` => `alembic upgrade head`
  - `make migrate-down` => `alembic downgrade -1`
- DB reset helper (requested): `make db-reset` for clean local state.
- ID generation (requested): generated in DB via `gen_random_uuid()` (`pgcrypto` extension).
- Enum strategy (chosen): use **TEXT + CHECK constraints** for `source` and `type` to keep migrations simple and flexible in early versions.

Minimum index set beyond `UNIQUE (url)`:

- `idx_docs_source` on `docs(source)`
- `idx_docs_type` on `docs(type)`
- `idx_docs_published_at` on `docs(published_at DESC)`
- `idx_doc_themes_theme` on `doc_themes(theme)`

Rationale:

- Supports planned filters (`source`, `type`, date windows) and theme-gap queries.
- Keeps index set small and low-maintenance for v1.
- FTS-specific indexes can be added in Issue 6 when search behavior is implemented.

## 5. Mismatches / Ambiguities

Resolved:

- Tooling choice was ambiguous; now fixed to Alembic + SQLAlchemy + psycopg.
- ID generation now fixed to DB-side UUID generation.
- Enum strategy and baseline index strategy now defined.

Remaining to confirm during implementation:

- Exact CI approach for DB integration tests (GitHub Actions service container vs split local-only checks). Recommendation: use service container so CI verifies migrations end-to-end.

## 6. Questions To Resolve (Prioritized)

P0:

- None remaining for scope definition.

P1:

- Confirm CI DB service shape (single Postgres service in same workflow job).

P2:

- None. Migration naming/versioning conventions and DB reset helper are now explicit scope items.
