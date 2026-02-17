# Semantic Versioning Policy

This project uses Semantic Versioning:

- `MAJOR`: breaking changes to API contract, database behavior, or required workflows.
- `MINOR`: backward-compatible features.
- `PATCH`: backward-compatible fixes and improvements.

## Tag Format

- `vMAJOR.MINOR.PATCH`
- Examples: `v0.1.0`, `v0.2.1`, `v1.0.0`

## Pre-1.0 Guidance

Before `v1.0.0`, breaking changes may still happen while architecture stabilizes, but releases must still use SemVer format and changelog notes.

## Release Checklist

1. `PLANS.md` updated for completed issues.
2. Tests passing.
3. API docs (`openapi.yaml`) updated if needed.
4. `README.md` updated for operational changes.
5. Create tag:
   - `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
6. Push tag:
   - `git push origin vX.Y.Z`
