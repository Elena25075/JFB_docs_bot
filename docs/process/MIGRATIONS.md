# Migration Conventions

This project uses Alembic migrations in:

- `migrations/versions/`

## Naming and Versioning Rules

- File name format:
  - `YYYYMMDD_NNNN_<short_slug>.py`
  - Example: `20260217_0001_initial_schema.py`
- Alembic revision id format:
  - `YYYYMMDD_NNNN`
  - Example: `20260217_0001`
- Each migration must include both `upgrade()` and `downgrade()`.
- Keep each migration scoped to one logical schema change set.

## Required Commands

- Apply latest migration:
  - `make migrate-up`
- Roll back one revision:
  - `make migrate-down`
- Reset local DB and reapply migrations:
  - `make db-reset`

## Safety Rules

- Never edit already-applied migration files.
- Add new migration files for incremental changes.
- Keep schema constraints explicit in migrations (PK/FK/UNIQUE/CHECK/indexes).
