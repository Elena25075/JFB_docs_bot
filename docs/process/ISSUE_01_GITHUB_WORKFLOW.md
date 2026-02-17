# Issue 01 GitHub Delivery Workflow

Goal: deliver **Issue 1 - Bootstrap repo + local dev environment** to GitHub with tests and CI.

## Preconditions

- `gh` installed and authenticated:
  - `gh auth login -h github.com`
- Work from repo root:
  - `/Users/elenakartoshkina/Documents/JFB_docs_bot`

## 1) Create/Push Repository

Recommended free-tier-safe option:

```bash
gh repo create JFB_docs_bot --public --source=. --remote=origin --push
```

## 2) Create Labels (one-time)

```bash
gh label create "type:feature" --color 1d76db || true
gh label create "area:api" --color 0e8a16 || true
gh label create "priority:p0" --color b60205 || true
```

## 3) Create Issue 1

```bash
gh issue create \
  --title "Issue 1: Bootstrap repo + local dev environment" \
  --label "type:feature" \
  --label "area:api" \
  --label "priority:p0" \
  --body-file docs/issues/ISSUE-01-bootstrap.md
```

## 4) Branch and Implement

```bash
git checkout -b codex/issue-1-bootstrap-local-dev
```

## 5) Local Validation

```bash
make install
make lint
make test
docker compose up -d db
```

Expectations:

- API starts: `make dev`
- Health endpoint returns 200:
  - `curl http://localhost:8000/health`
- DB container is healthy:
  - `docker compose ps`

## 6) Commit and PR

```bash
git add .
git commit -m "Issue 1: bootstrap FastAPI, Postgres compose, scripts, smoke test"
git push -u origin codex/issue-1-bootstrap-local-dev
gh pr create --fill --title "Issue 1: Bootstrap repo + local dev environment"
```

## 7) Merge and Tag

After CI passes and review is done:

```bash
gh pr merge --squash --delete-branch
git checkout main
git pull
git tag -a v0.1.0 -m "Issue 1 bootstrap complete"
git push origin v0.1.0
```

## Free-tier Notes

- Keep CI on Linux only.
- Do not upload large artifacts.
- Prefer local heavy testing.
