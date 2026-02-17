# GitHub Free Constraints and How To Avoid Paid Overages

Verified against GitHub Docs on 2026-02-17.

## Recommended Account Strategy

- Use a **public repository** unless private visibility is required.
- For this project, run most validation locally and keep GitHub Actions minimal.
- Do not add a payment method if you want a hard stop at free quotas.

## Constraints That Can Exceed Free Plan Limits

1. GitHub Actions (private repos):
   - GitHub Free includes **2,000 minutes/month** and **500 MB** artifact storage.
   - Standard runners in **public repos** are free.
   - macOS and Windows runners consume minutes faster (multipliers).
   - Actions cache has separate size/eviction constraints (keep cache usage minimal).
2. GitHub Packages (private packages):
   - GitHub Free includes **500 MB storage** and **1 GB/month data transfer**.
   - Storage is shared with Actions artifacts/caches.
3. Git LFS:
   - GitHub Free includes **10 GiB storage** and **10 GiB/month bandwidth**.
4. Codespaces (personal account):
   - GitHub Free includes **120 core-hours/month** and **15 GB-month storage**.
5. Large files/repo health:
   - GitHub blocks files larger than **100 MiB**.
   - Repo size and structure limits can degrade performance if exceeded.

## Constraint Checklist For Every PR

- Is CI still Linux-only (`ubuntu-latest`)?
- Was matrix expansion avoided?
- Were artifact uploads avoided?
- Are there any files over 25 MiB?
- Is any large dataset/binary being introduced?
- Is this still safe to keep as a public repo?

## Guardrails To Stay Within Free Limits

## A) Actions Guardrails

- Keep CI lightweight:
  - Linux runner only (`ubuntu-latest`),
  - single Python version until needed,
  - run on PR + `main` push only.
- Avoid artifact uploads by default.
- Cancel stale CI runs with concurrency.
- Prefer local test runs during heavy development.
- Do not use larger runners.

## B) Packages Guardrails

- Do not publish private packages for this project.
- If packages are needed, prefer public package visibility.
- Avoid storing build outputs in Packages.

## C) LFS Guardrails

- Avoid LFS unless absolutely necessary.
- Keep fixture files small text samples, not large binaries.
- Store large datasets outside GitHub (external object storage).

## D) Codespaces Guardrails

- Default to local development.
- If Codespaces is used:
  - stop/delete idle codespaces,
  - use smallest machine size,
  - avoid long-running background tasks.

## E) Repository Hygiene Guardrails

- Reject files > 25 MiB in PR review.
- Never commit generated assets or database dumps.
- Keep test fixtures minimal.

## Budget/Spending Safety

- Keep account without payment method for hard usage block at quota.
- If payment method is ever added, set product budgets to 0 or strict caps immediately.

## Team Rules For This Repo

- Public repo by default.
- Minimal CI workflow only.
- No private packages.
- No large binaries in Git.

## References

- [GitHub Actions billing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
- [GitHub Packages billing](https://docs.github.com/en/billing/concepts/product-billing/github-packages)
- [Git LFS billing](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage)
- [GitHub Codespaces billing](https://docs.github.com/billing/managing-billing-for-github-codespaces/about-billing-for-codespaces)
- [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits)
- [Collaborator access on GitHub Free](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration)
