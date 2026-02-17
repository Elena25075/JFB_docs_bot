# JetFormBuilder Tutorials Knowledge GPT — Specification (Codex Execution)

## 1) Goal
Build a system that **fetches and indexes all JetFormBuilder + Crocoblock tutorials/blog posts**, then powers a **Custom GPT** that can:
- Recommend relevant tutorials/posts for a question
- Answer questions based on the indexed content
- Report **new themes** (recent topic clusters), **past themes**, and **gaps** (topics users ask for but content is missing or thin)

## 2) Scope

### In-scope
- Public content from:
  - `jetformbuilder.com` (tutorials, docs, blog posts)
  - `crocoblock.com` (JetFormBuilder-related tutorials/blog/KB; optionally all Crocoblock content but tagged)
- A backend service that provides:
  - search results + short descriptions
  - full doc retrieval
  - theme aggregation
  - gap detection
- A Custom GPT configured with **Actions** calling the backend via an **OpenAPI schema**

### Out of scope (v1)
- Authenticated/private docs behind login
- Perfect long-form quoting/citation extraction (store text; answer briefly and link sources)
- Multi-language workflows (can be added later)

## 3) High-level Architecture

### Components
1) **Crawler/Indexer**
- Discovers URLs (prefer sitemaps/robots; fallback to WP REST where available)
- Fetches HTML
- Extracts: title, date, type, tags/categories, short_description, main_text, headings
- De-duplicates and updates via `content_hash`

2) **Storage**
- Postgres (local Docker or hosted)
- Tables for docs + extracted metadata + theme labels

3) **API**
- `GET /v1/docs/search`
- `GET /v1/docs/get`
- `GET /v1/themes/list`
- `GET /v1/themes/gaps`
- Serves **OpenAPI 3.1** spec for GPT Actions

4) **Custom GPT**
- Uses Actions to call the API
- Instruction policy: “never invent docs; always cite URLs returned by API”

### Authentication
- Prefer **API key auth** between GPT Action ↔ API.

## 4) Data Model (Postgres)

### Table: `docs`
- `id` (uuid, pk)
- `url` (text, unique)
- `source` (enum: `jetformbuilder`, `crocoblock`)
- `type` (enum: `tutorial`, `blog`, `kb`, `docs`, `unknown`)
- `title` (text)
- `published_at` (date/timestamp nullable)
- `tags` (text[])
- `categories` (text[])
- `short_description` (text)
- `content_text` (text)
- `headings` (text[])
- `content_hash` (text)
- `last_crawled_at` (timestamp)
- `http_status` (int)
- `language` (text default `en`)

### Table: `themes`
- `theme` (text, pk)
- `description` (text)
- `updated_at` (timestamp)

### Table: `doc_themes`
- `doc_id` (uuid fk -> docs)
- `theme` (text fk -> themes)
- primary key `(doc_id, theme)`

## 5) Theme Detection + Gap Detection (v1 Logic)

### Theme detection (v1)
Hybrid approach:
- Start with tags/categories as candidate themes
- Add keyword themes using keyphrase extraction from headings + first paragraphs
- Normalize via synonyms mapping (e.g., `"file upload" ~ "uploads"`, `"frontend submission" ~ "post submit"`)
- Save 1–5 themes per doc

### Gap detection (v1)
Compute metrics per theme:
- `tutorial_count`, `blog_count`, `last_seen`, `recent_count_90d`

Flag gaps:
- **blog_theme_missing_tutorial**: `blog_count ≥ 3 AND tutorial_count ≤ 1`
- **new_feature_low_coverage**: `recent_count_90d` high but `tutorial_count` low
- **tutorial_theme_missing_reference_article** (optional): `tutorial_count ≥ 3 AND blog_count == 0`

Return gaps with evidence URLs (top docs in that theme).

## 6) API Contract (must match GPT Actions)

### Endpoint: Search
`GET /v1/docs/search?q=&source=&type=&after=&before=&limit=`

Returns list with:
- `title, url, date, source, type, short_description, tags, themes`

### Endpoint: Get doc
`GET /v1/docs/get?url=`

Returns:
- `title, url, date, source, type, content_text, headings, tags, themes`

### Endpoint: Themes list
`GET /v1/themes/list?after=&before=&min_docs=`

Returns:
- `theme, doc_count, last_seen`

### Endpoint: Theme gaps
`GET /v1/themes/gaps?after=&before=&gap_type=`

Returns:
- `theme, reason, evidence_urls[]`

## 7) Quality + Testing Requirements

### Unit tests
- HTML parsing: title/date extraction, main content extraction
- Short description generation rules
- Theme normalization mapping

### Integration tests
- Crawl 5 known URLs end-to-end → stored in DB
- API search returns expected fields + stable ranking

### “GPT Evaluation Set” (manual)
At least 10 questions to verify:
1. “How do I create a front-end post submission form with JetFormBuilder?”
2. “What tutorials mention conditional logic + calculations?”
3. “What’s new in the last 60 days about JetFormBuilder?”
4. “What themes are missing tutorials but discussed in the blog?”
5. “Show me tutorials about Stripe/PayPal payments in forms.”
6. “Any content about PDF generation or email attachments?”
7. “What do we have on file upload + drag-and-drop addon?”
8. “Common gaps around dynamic data + JetEngine integration?”
9. “How do I build multi-step forms?”
10. “Do we have anything about form spam protection?”

## 8) Deployment (v1)
- API deployed on a container host or serverless (if compatible)
- Postgres hosted
- Scheduled crawler job:
  - daily incremental crawl
  - weekly full sitemap refresh
- Logs/monitoring:
  - crawl success rate
  - HTTP error distribution
  - doc count over time

## 9) Codex Execution Workflow

### Repo setup files
- `PLANS.md` (Codex execution plan, updated as work proceeds)
- `AGENTS.md` (agent rules: run tests, keep changes scoped, never break build)
- `openapi.yaml` (Actions schema)
- `README.md` (local dev + deploy steps)

### Definition of Done (DoD) for every issue
- Code implemented
- Tests added/updated and passing
- API docs updated (OpenAPI + README if needed)
- Small demo command/script showing it works

## 10) Issue Breakdown (execute sequentially)

### Issue 1 — Bootstrap repo + local dev environment
**Deliverables**
- FastAPI project skeleton (default) + dependency management
- Docker compose for Postgres
- Scripts: `dev`, `test`, `lint`

**Acceptance criteria**
- `docker compose up` starts DB
- API starts locally
- `/health` returns OK

**Tests**
- smoke test for `/health`

---

### Issue 2 — DB schema + migrations
**Deliverables**
- SQL migrations for `docs`, `themes`, `doc_themes`
- DB access layer (SQLAlchemy or lightweight SQL)

**Acceptance criteria**
- `migrate up` creates tables
- Unique URL constraint enforced

**Tests**
- migration test + insert/select test

---

### Issue 3 — URL discovery (sitemaps-first)
**Deliverables**
- Discover URLs from sitemap indexes where available
- Store discovered URLs for crawl run

**Acceptance criteria**
- Fetches N URLs per source
- Logs discovered counts by type/source

**Tests**
- mock sitemap parsing test

---

### Issue 4 — Crawler: fetch + parse content
**Deliverables**
- HTML fetcher with retry + backoff + user-agent
- Content extractor:
  - title, date, main text, headings
  - short_description (excerpt/meta/first sentences)
- `content_hash`
- Upsert into DB

**Acceptance criteria**
- Crawls at least 50 docs without crashing
- Updates changed pages without duplicates

**Tests**
- parser unit tests using HTML fixtures

---

### Issue 5 — Theme extraction + normalization
**Deliverables**
- Theme extraction pipeline (tags/categories + keyphrases)
- Normalization map + stopword filters
- Persist to `themes` + `doc_themes`

**Acceptance criteria**
- Each doc has 1–5 themes
- Themes not exploding with near-duplicates

**Tests**
- deterministic theme extraction tests on fixtures

---

### Issue 6 — Search API (ranking + filters)
**Deliverables**
- `GET /v1/docs/search` supports:
  - q, source, type, after/before, limit
- Ranking:
  - Postgres full-text search preferred (FTS)

**Acceptance criteria**
- Query returns relevant docs with required fields
- Filters work

**Tests**
- integration test: seed docs → search assertions

---

### Issue 7 — Doc retrieval API
**Deliverables**
- `GET /v1/docs/get?url=` returns full doc payload

**Acceptance criteria**
- Valid URL returns doc
- Unknown URL returns 404

**Tests**
- retrieval integration test

---

### Issue 8 — Theme listing + gaps API
**Deliverables**
- `GET /v1/themes/list`
- `GET /v1/themes/gaps` implementing v1 gap logic

**Acceptance criteria**
- Themes list returns counts + last_seen
- Gaps endpoint returns explainable results + evidence

**Tests**
- seed dataset → known gap expectations

---

### Issue 9 — OpenAPI schema for GPT Actions + hardening
**Deliverables**
- `openapi.yaml` for all endpoints
- API key auth middleware
- Basic rate limiting + request logging

**Acceptance criteria**
- Schema imports into GPT Actions
- Requests without API key rejected (except `/health`)

**Tests**
- auth tests (401 vs 200)

---

### Issue 10 — Custom GPT configuration package
**Deliverables**
- `GPT_INSTRUCTIONS.md` (copy/paste into GPT Builder)
- `EVAL_QUESTIONS.md`
- Actions testing checklist

**Acceptance criteria**
- A human can configure GPT in <30 minutes
- GPT always uses Actions for content lookups

---

### Issue 11 — Deployment pipeline
**Deliverables**
- Production config (env vars, DB URL, API key)
- Deploy instructions for chosen host
- Scheduled crawler job instructions (cron / platform scheduler)

**Acceptance criteria**
- Public API reachable
- Daily crawl runs and updates DB
- Logs visible

---

### Issue 12 — Post-deploy verification
**Deliverables**
- Run `EVAL_QUESTIONS.md` against the Custom GPT
- Fix top 3 failure modes (ranking, extraction, theme noise)

**Acceptance criteria**
- 10/10 eval questions return relevant links + short descriptions
- “gaps” output is reasonable and evidence-backed
