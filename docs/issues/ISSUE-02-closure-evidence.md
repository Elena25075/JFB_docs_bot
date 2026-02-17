# Issue Closure Evidence

## Issue

- Issue number: 2
- Title: DB schema + migrations
- PR(s): N/A (implemented on repository mainline for this phase)
- Commit(s): `6f4980f`, `86f070e`, `202484d`, `d2f6684`, `ff19d17`, `24502f2`, `d4366e5`, `ad7c169`, `43645af`, `f841e62`
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
  - Evidence: `Makefile` includes `migrate-up`, `migrate-down`, `db-reset`, and `test-db`.
- [x] Local DB safety and deterministic test/migration behavior hardened.
  - Evidence: localhost-only destructive reset guard, bounded Postgres readiness retries, fail-fast DB integration setup errors, deterministic `db-reset` migration target URLs, and IPv6-safe URL builder with tests.

## Post-Closure Hardening Changes

- `86f070e`: added TEST DB safety guardrails and removed redundant migration setup in tests.
- `202484d`: fixed migration URL precedence and strengthened DB relation verification coverage.
- `d2f6684`: aligned local test DB defaults and session typing.
- `ff19d17`: added explicit destructive reset toggle and Postgres readiness wait improvements.
- `24502f2`: hardened `db-reset` local-only behavior and documented DB integration workflow.
- `d4366e5`: corrected test DB migration environment usage and made DB integration setup fail fast with actionable errors.
- `ad7c169`: bounded readiness waits and encoded generated DB URLs.
- `43645af`: removed ambient DB URL override behavior from local `db-reset`.
- `f841e62`: fixed IPv6 host handling in DB URL builder and added unit coverage.

## Commands Run

```bash
python3 -m ruff check app migrations
python3 -m alembic upgrade head --sql > /tmp/issue2_upgrade.sql
./scripts/lint.sh
./scripts/test.sh
make -n migrate-up migrate-down db-reset test-db
```

## Results

- Lint: passed.
- Tests:
  - local default run: `5 passed, 2 skipped` (DB integration gated unless destructive reset is explicitly enabled)
  - CI run: DB-backed checks passed
- Integration/smoke: DB migration + repository integration tests passed in CI, including latest hardening patches.
- CI run URLs:
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22107897270
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22108643660
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22108818208
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22109007399
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22109159637
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22109382311
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22109612655
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22109750092
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22109842584
  - https://github.com/Elena25075/JFB_docs_bot/actions/runs/22109931748

## Risks / Follow-ups

- Known limitations: local sandbox could not reach Dockerized Postgres reliably, so DB tests were skipped in this environment.
- Deferred work: crawler/data ingestion starts in Issue 3.
- Next issue dependency: Issue 3 (URL discovery) depends on this schema baseline.

## Closure Decision

- [x] Close issue now
- [ ] Keep issue open
- Reason: acceptance criteria are implemented and validated with green DB-backed CI.
