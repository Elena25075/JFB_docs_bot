# GitHub Setup Instructions (Free Account)

## 1) Authenticate and Create Remote

```bash
gh auth login -h github.com
gh repo create JFB_docs_bot --public --source=. --remote=origin --push
```

If private visibility is required:

```bash
gh repo create JFB_docs_bot --private --source=. --remote=origin --push
```

## 2) Enable Standard Workflow Surface

Use:

- GitHub Issues (intake and tracking)
- Pull Requests (code review and merge gate)
- GitHub Project board (kanban for issue progression)

Recommended board columns:

1. Backlog
2. Ready
3. In Progress
4. In Review
5. Done

## 3) Labels to Create

```bash
gh label create "type:feature" --color 1d76db || true
gh label create "type:bug" --color d73a4a || true
gh label create "type:chore" --color cfd3d7 || true
gh label create "area:crawler" --color 5319e7 || true
gh label create "area:api" --color 0e8a16 || true
gh label create "area:db" --color fbca04 || true
gh label create "area:themes" --color 006b75 || true
gh label create "area:docs" --color 0052cc || true
gh label create "priority:p0" --color b60205 || true
gh label create "priority:p1" --color d93f0b || true
gh label create "priority:p2" --color fbca04 || true
```

## 4) Create Issues 1-12

Create each issue from `PLANS.md`, one issue per spec item, and include:

- acceptance criteria,
- non-goals,
- test plan.

Issue 1 body template:

- `docs/issues/ISSUE-01-bootstrap.md`

## 5) Branch and PR Rules

- Branch format: `codex/issue-<n>-<slug>`
- One issue per branch
- One PR linked to one issue
- Required checks: CI + local tests evidence in PR template

## 6) Release and Versions

- Use tags: `vMAJOR.MINOR.PATCH`
- Suggested milestone tags:
  - `v0.1.0` after Issues 1-3
  - `v0.2.0` after Issues 4-5
  - `v0.3.0` after Issues 6-8
  - `v0.4.0` after Issues 9-10
  - `v1.0.0` after Issues 11-12

## 7) First Issue Delivery

Use:

- `docs/process/ISSUE_01_GITHUB_WORKFLOW.md`
