# Issue Creation, Exploration, Execution, Testing, and Versioning

## 1) Issue Creation (GitHub)

Use GitHub Issues with templates in `.github/ISSUE_TEMPLATE/`.

Required fields:

- problem statement,
- expected outcome,
- acceptance criteria,
- out-of-scope,
- test plan.

Issue labels:

- `type:feature`, `type:bug`, `type:chore`
- `area:crawler`, `area:api`, `area:db`, `area:themes`, `area:docs`
- `priority:p0`, `priority:p1`, `priority:p2`

## 2) Issue Exploration (Before Coding)

Create an exploration note:

- file path: `docs/issues/ISSUE-XX-exploration.md`
- include:
  - requirements,
  - current repo context,
  - integration points,
  - risks,
  - blocking questions.

Do not code until blockers are resolved.

## 3) Execution Workflow

1. Create branch from `main`: `codex/issue-<n>-<slug>`
2. Implement only the active issue scope.
3. Keep commits focused.
4. Update docs/contracts if behavior changes.
5. Open PR linked to the issue.

## 4) Testing Workflow

Minimum required checks per issue:

- unit tests for logic/parsing rules,
- integration tests for DB/API behavior when applicable,
- smoke checks for service health when applicable.

Record in PR:

- exact command(s) run,
- test results,
- known limitations.

Recommended commands:

- baseline local checks: `make lint && make test`
- DB integration checks (local test DB reset enabled): `make test-db`
- sitemap discovery execution: `make discover-urls`

DB integration safety gates:

- requires `ALLOW_DESTRUCTIVE_TEST_DB_RESET=1`,
- requires `TEST_DATABASE_URL` host in `localhost`, `127.0.0.1`, or `::1`,
- requires `TEST_DATABASE_URL` database name to end with `_test`.

Discovery command behavior:

- Success prints a JSON summary event: `url_discovery_summary`.
- Failure prints a JSON error event: `url_discovery_failed` and exits non-zero.

## 5) Issue Closure Workflow

Before closing an issue:

1. Create `docs/issues/ISSUE-XX-closure-evidence.md`.
2. Fill it using `docs/issues/ISSUE_CLOSURE_EVIDENCE_TEMPLATE.md`.
3. Verify each acceptance criterion with concrete evidence.
4. Link PR(s), commits, and CI run URL.
5. Close the GitHub issue only after evidence is complete.

## 6) File and Version Locations

Core planning and policy:

- `JetFormBuilder_KnowledgeGPT_SPEC.md`
- `PLANS.md`
- `AGENTS.md`
- `README.md`

API contract:

- `openapi.yaml`

Issue exploration records:

- `docs/issues/ISSUE-XX-exploration.md`
- `docs/issues/ISSUE-XX-closure-evidence.md`

Database schema versions:

- `migrations/versions/`

Tests:

- `tests/unit/`
- `tests/integration/`
- `tests/fixtures/`
- `docs/process/MIGRATIONS.md`

## 7) Release and SemVer

Follow Semantic Versioning (`MAJOR.MINOR.PATCH`):

- `PATCH`: bug fixes and non-breaking internal improvements.
- `MINOR`: backward-compatible new features.
- `MAJOR`: breaking API/schema/workflow changes.

Tag format:

- `vMAJOR.MINOR.PATCH` (example `v0.1.0`).

Version command example:

- `git tag -a v0.1.0 -m "Bootstrap and schema foundation"`
