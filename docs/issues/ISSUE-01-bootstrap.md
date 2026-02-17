## Summary

Bootstrap the project with FastAPI skeleton, local Postgres via Docker Compose, and basic developer scripts.

## Scope

- Create FastAPI app with `/health`.
- Add dependency management for runtime + dev tools.
- Add Docker Compose for Postgres.
- Add scripts: `dev`, `test`, `lint`.
- Add smoke test for `/health`.

## Acceptance Criteria

- [ ] `docker compose up -d db` starts Postgres.
- [ ] `make dev` starts API locally.
- [ ] `GET /health` returns 200 with `{\"status\":\"ok\"}`.
- [ ] `make lint` passes.
- [ ] `make test` passes.

## Non-goals

- DB schema/migrations (Issue 2).
- Crawling logic (Issue 3+).
- Search/theme APIs (Issue 6+).

## Test Plan

- Unit test: `tests/unit/test_health.py`
- Integration smoke test: `tests/integration/test_health_smoke.py`
- CI workflow: lint + tests
