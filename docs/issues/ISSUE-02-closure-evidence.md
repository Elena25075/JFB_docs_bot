# Issue Closure Evidence

## Issue

- Issue number: 2
- Title: DB schema + migrations
- PR(s): N/A (implemented on repository mainline for this phase)
- Commit(s): pending final Issue 2 commit
- Date: 2026-02-17

## Acceptance Criteria Verification

- [x] `migrate up` creates tables.
  - Evidence: baseline migration file `migrations/versions/20260217_0001_initial_schema.py` created; offline migration generation succeeds (`python3 -m alembic upgrade head --sql`).
- [x] Unique URL constraint enforced.
  - Evidence: migration creates `uq_docs_url` on `docs(url)`; migration integration test checks constraint name and column.
- [x] DB access layer implemented.
  - Evidence: `app/db/config.py`, `app/db/session.py`, `app/db/models.py`, and `app/db/repository.py` added.
- [x] Migration and insert/select tests added.
  - Evidence: `tests/integration/test_db_migrations.py` and `tests/integration/test_db_repository.py`.
- [x] Migration commands and reset helper added.
  - Evidence: `Makefile` includes `migrate-up`, `migrate-down`, `db-reset`.

## Commands Run

```bash
python3 -m ruff check app migrations
python3 -m alembic upgrade head --sql > /tmp/issue2_upgrade.sql
./scripts/lint.sh
./scripts/test.sh
make -n migrate-up migrate-down db-reset
```

## Results

- Lint: passed.
- Tests: passed with DB tests skipped locally when Postgres is unreachable (`2 passed, 2 skipped`).
- Integration/smoke: health and unit tests pass locally; DB integration tests are configured and require reachable Postgres.
- CI run URL: pending final push of Issue 2 implementation changes.

## Risks / Follow-ups

- Known limitations: local sandbox could not reach Dockerized Postgres reliably, so DB tests were skipped in this environment.
- Deferred work: crawler/data ingestion starts in Issue 3.
- Next issue dependency: Issue 3 (URL discovery) depends on this schema baseline.

## Closure Decision

- [ ] Close issue now
- [x] Keep issue open
- Reason: wait for CI run on final Issue 2 push and confirm DB-backed checks in GitHub before closure.
