# JetFormBuilder Tutorials Knowledge GPT

System for crawling JetFormBuilder and Crocoblock content, indexing it in Postgres, and serving it through an API used by Custom GPT Actions.

## Project Status

Repository bootstrap is complete. Execution follows sequential issues defined in `PLANS.md`.

## Core Docs

- Scope and target architecture: `JetFormBuilder_KnowledgeGPT_SPEC.md`
- Execution plan: `PLANS.md`
- Team/agent rules: `AGENTS.md`
- Delivery workflow (issues, exploration, execution, testing, versions): `docs/process/WORKFLOW.md`
- GitHub setup and issue labels/board: `docs/process/GITHUB_SETUP.md`
- GitHub Free constraints and guardrails: `docs/process/GITHUB_FREE_LIMITS.md`
- Issue 1 GitHub delivery runbook: `docs/process/ISSUE_01_GITHUB_WORKFLOW.md`
- Migration conventions and commands: `docs/process/MIGRATIONS.md`
- API contract for GPT Actions: `openapi.yaml`
- Semantic versioning policy: `docs/process/VERSIONING.md`

## Quick Start (Git + GitHub)

1. Re-auth GitHub CLI:
   `gh auth login -h github.com`
2. Create public repo on GitHub (recommended for free-tier CI):
   `gh repo create JFB_docs_bot --public --source=. --remote=origin --push`
3. If private is required:
   use `--private` and follow `docs/process/GITHUB_FREE_LIMITS.md` strictly.

## Local Dev Bootstrap (Issue 1)

1. Install dependencies:
   `make install`
2. Start Postgres:
   `docker compose up -d db`
3. Start API:
   `make dev`
4. Validate health:
   `curl http://localhost:8000/health`
5. Run tests:
   `make test`
6. Run DB integration tests (starts local Postgres and enables destructive reset on local test DB only):
   `make test-db`
7. Run lint:
   `make lint`
8. Apply DB migrations:
   `make migrate-up`
9. Discover crawl candidate URLs from sitemaps:
   `make discover-urls`

Discovery output contract:

- Success emits JSON with `event=url_discovery_summary`, `candidate_count`, `processed_count`, and `counts_by_source_type`.
- Hard failures emit JSON with `event=url_discovery_failed` and return non-zero.

## Branching and Release

- Branch format: `codex/issue-<n>-<short-slug>`
- One issue per branch and PR.
- SemVer tags: `vMAJOR.MINOR.PATCH` (for example: `v0.1.0`)

## Testing Rule

Every issue PR must include:

- tests (unit/integration as applicable),
- passing local test evidence,
- updated docs if contract/behavior changed.

DB test safety defaults:

- `make test` keeps destructive DB integration tests disabled by default.
- `make test-db` enables `ALLOW_DESTRUCTIVE_TEST_DB_RESET=1`.
- DB integration tests run only when `TEST_DATABASE_URL` points to a local host and a database ending with `_test`.

Discovery env overrides:

- `JETFORMBUILDER_SITEMAP_URL` (default: `https://jetformbuilder.com/sitemap_index.xml`)
- `CROCOBLOCK_SITEMAP_URL` (default: `https://crocoblock.com/sitemap_index.xml`)
