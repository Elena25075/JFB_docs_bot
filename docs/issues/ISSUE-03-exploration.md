# Issue Exploration Report: Issue 3 (URL discovery, sitemaps-first)

## 1. Issue Summary

Issue 3 should add a first discovery stage that collects candidate content URLs from source sitemaps (JetFormBuilder and Crocoblock), stores those discovered URLs for later crawl execution, and reports discovery counts grouped by source and content type.

Requirements:

- Discover URLs from sitemap indexes where available.
- Cover both sources: `jetformbuilder.com` and `crocoblock.com`.
- Persist discovered URLs for crawl execution.
- Produce discovery counts by `source` and `type`.
- Add at least one mock sitemap parsing test.

Implicit assumptions:

- Public sitemap endpoints are reachable and sufficient for initial URL coverage.
- URL-to-type classification can be inferred during discovery (before full page parsing).
- Discovery output should be consumable by Issue 4 crawler without redesign.

Success criteria (from spec + inferred):

- Discovery run returns a non-zero URL set for each configured source.
- Discovery persistence is deterministic/idempotent for repeated runs.
- Logs/metrics show count totals by source and type.

Non-goals:

- No HTML fetch/extraction (Issue 4).
- No theme extraction/gap logic (Issue 5+ and Issue 8).
- No search or retrieval API changes (Issue 6+ and Issue 7).

## 2. Repo/Project Context

Project purpose observed in:

- `README.md`
- `JetFormBuilder_KnowledgeGPT_SPEC.md`
- `PLANS.md`

Key dependencies/runtime observed:

- Python 3.11+
- FastAPI + Uvicorn
- SQLAlchemy + Alembic + psycopg
- Pytest + Ruff
- Postgres via Docker Compose
- No crawler/discovery module exists yet

Current architecture map:

- API entrypoint: `app/main.py`
- DB models/repository/session: `app/db/`
- Schema management: `migrations/` + `alembic.ini`
- Commands/workflow: `Makefile`, `scripts/*.sh`
- Tests: `tests/unit/`, `tests/integration/`

## 3. Existing Related Code

Files/dirs to read next (and why):

- `JetFormBuilder_KnowledgeGPT_SPEC.md`: canonical Issue 3 deliverables/acceptance.
- `PLANS.md`: confirms Issue 3 is the next active issue.
- `app/db/models.py`: current schema constraints and what can/cannot store discovery output.
- `app/db/repository.py`: existing DB access pattern to extend.
- `migrations/versions/20260217_0001_initial_schema.py`: baseline schema and migration conventions.
- `tests/integration/conftest.py`: DB test safety model to follow for new integration tests.
- `Makefile`: command surface where discovery execution target should be added.

Similar/adjacent patterns already present:

- DB-safe integration test gating (`ALLOW_DESTRUCTIVE_TEST_DB_RESET`) and local safety checks.
- Clear make-target workflow for developer operations.
- Single-service architecture with explicit migration-backed data model changes.

## 4. Proposed Integration Plan (No Code)

Where changes should logically go:

- New discovery module under `app/` (for example `app/discovery/`) for sitemap fetch/parse/classify flow.
- New DB persistence layer under `app/db/` for discovered URL writes/reads.
- New migration file under `migrations/versions/` if a dedicated discovery queue table is introduced.
- New unit tests for sitemap parsing/classification under `tests/unit/`.
- Optional integration test for persistence/idempotency under `tests/integration/`.
- New command in `Makefile` to run discovery locally/CI (for example `make discover-urls`).

Expected interfaces/surfaces:

- Input configuration for source sitemap roots (likely env vars, currently missing in `.env.example`).
- Discovery function/service returning normalized URL records with `source` and provisional `type`.
- Persistence contract for "discovered, pending crawl" URLs.
- Logging contract: summary counts by source/type at end of run.

Risks/edge cases:

- Nested sitemap indexes and `.gz` sitemap files.
- Duplicate URLs across sitemap partitions.
- URL normalization/canonicalization (trailing slash, query params, fragments).
- Crocoblock sitemap breadth may include non-JetFormBuilder pages; scope filtering required.
- Type classification from URL patterns may be ambiguous for some pages.

## 5. Mismatches / Ambiguities

- Current `docs` table is not a good discovery queue target: `title` is non-null and assumes parsed content exists (`app/db/models.py`), but Issue 3 only discovers URLs.
- "Store discovered URLs for crawl run" does not specify storage shape:
  - dedicated queue table,
  - or partial rows in `docs`,
  - or file-based transient storage.
- Acceptance criterion "Fetches N URLs per source" does not define `N` or behavior when source sitemap has fewer than `N`.
- "Logs discovered counts by type/source" does not define authoritative type mapping at discovery stage.
- Sitemaps-first wording implies fallback behavior may be deferred, but fallback scope (robots.txt, WP REST) is not explicitly included in Issue 3 acceptance.

## 6. Questions To Resolve (Prioritized)

P0 (blocking):

- Should Issue 3 introduce a dedicated `discovered_urls` (or crawl queue) table instead of writing into `docs`?
- What exact minimum `N` per source should be required for acceptance, and how to handle cases where source provides fewer URLs?
- What is the required URL type classification rule in discovery (strict mapping rules vs `unknown` fallback)?

P1 (important):

- What URL filtering rules should apply for Crocoblock to keep JetFormBuilder relevance?
- Should discovery runs be idempotent by URL only, or by `(url, discovered_at/run_id)` for historical tracking?
- Should Issue 3 include only sitemap index parsing, or also direct sitemap files and `.gz` handling in scope?

P2 (nice-to-have):

- Should discovery output include crawl priority hints for Issue 4 (e.g., tutorials first, recency boosts)?
- Do we want per-run metrics persisted in DB now, or only structured logs in Issue 3?
