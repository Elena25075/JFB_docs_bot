# Issue Closure Evidence

## Issue

- Issue number: 3
- Title: URL discovery (sitemaps-first)
- PR(s): N/A (implemented on repository mainline for this phase)
- Commit(s): `7bfb06a`
- Date: 2026-02-18

## Acceptance Criteria Verification

- [x] Discover URLs from sitemap indexes where available.
  - Evidence: `app/discovery/sitemap.py` implements sitemap index + nested sitemap traversal (`sitemapindex` and `urlset` handling).
- [x] Store discovered URLs for crawl run.
  - Evidence: `migrations/versions/20260218_0002_discovered_urls_queue.py` adds `discovered_urls`; `app/db/repository.py` adds idempotent enqueue/upsert and pending queue reads.
- [x] Fetches N URLs per source.
  - Evidence: multi-source discovery behavior covered by `tests/unit/test_sitemap_discovery.py::test_discover_url_candidates_collects_rows_per_configured_source`; command entrypoint supports both configured sources.
- [x] Logs discovered counts by type/source.
  - Evidence: `app/discovery/run.py` emits JSON `url_discovery_summary` with `counts_by_source_type`.
- [x] Mock sitemap parsing test.
  - Evidence: parser and normalization tests in `tests/unit/test_sitemap_discovery.py`.

## Commands Run

```bash
./scripts/lint.sh
./scripts/test.sh
python3 -m pytest tests/unit/test_sitemap_discovery.py tests/unit/test_db_config.py
python3 -m ruff check app tests
python3 -m alembic upgrade head --sql > /tmp/issue3_step1_upgrade.sql
make -n discover-urls
JETFORMBUILDER_SITEMAP_URL=http://127.0.0.1:1/sitemap.xml CROCOBLOCK_SITEMAP_URL=http://127.0.0.1:1/sitemap.xml make discover-urls
```

## Results

- Lint: passed.
- Tests: `10 passed, 3 skipped` on `./scripts/test.sh`; sitemap/db-config unit subset `8 passed`.
- Integration/smoke:
  - Discovery queue migration renders in offline SQL migration output.
  - Discovery command failure path returns non-zero and emits `url_discovery_failed` JSON.
- CI run URL: https://github.com/Elena25075/JFB_docs_bot/actions/runs/22132800385

## Risks / Follow-ups

- Known limitations: local sandbox cannot access external sitemap hosts, so live sitemap fetch validation was not executed locally.
- Deferred work: HTML fetch/content extraction remains in Issue 4.
- Next issue dependency: Issue 4 consumes `discovered_urls` queue for crawl execution.

## Closure Decision

- [x] Close issue now
- [ ] Keep issue open
- Reason: Issue 3 deliverables are implemented with migration-backed persistence, discovery command contract, and test coverage.
