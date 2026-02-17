---
name: review-skill
description: "Perform comprehensive but concise code review focused on logging, error handling, TypeScript quality, production readiness, React/hooks correctness, performance, security, and architecture alignment. Use when the user asks for a review and expects severity-ranked findings with file:line references and summary counts."
---

# Code Review Task

Perform comprehensive code review. Be thorough but concise.

## Review Rules

- Prioritize findings over summaries.
- Include concrete file and line references for each issue.
- Keep recommendations actionable and minimal.
- Do not implement fixes unless explicitly requested.

## Check For

### Logging

- No `console.log` statements.
- Use proper logger with context.

### Error Handling

- Async flows use try/catch where needed.
- Centralized handlers are used consistently.
- Error messages are actionable and informative.

### TypeScript

- No `any` types unless strictly justified.
- Proper interfaces/types are used.
- No `@ts-ignore`.

### Production Readiness

- No debug statements.
- No TODO/FIXME leftovers in production paths.
- No hardcoded secrets or credentials.

### React/Hooks

- Effects include cleanup when required.
- Dependencies are complete and correct.
- No infinite render/effect loops.

### Performance

- No avoidable re-renders.
- Expensive computations are memoized when appropriate.

### Security

- Authentication and authorization are enforced.
- Inputs are validated and sanitized.
- Row-level security policies are in place where required.

### Architecture

- Follows existing patterns and conventions.
- Code is placed in the correct directory/layer.

## Output Format

### ✅ Looks Good
- [Item 1]
- [Item 2]

### ⚠️ Issues Found
- **[Severity]** [File:line] - [Issue description]
  - Fix: [Suggested fix]

### 📊 Summary
- Files reviewed: X
- Critical issues: X
- Warnings: X

## Severity Levels

- **CRITICAL** - Security, data loss, crashes
- **HIGH** - Bugs, performance issues, bad UX
- **MEDIUM** - Code quality, maintainability
- **LOW** - Style, minor improvements

## Completion Criteria

- All requested checks are covered.
- Each issue includes severity + file:line + fix guidance.
- Summary counts match listed findings.

