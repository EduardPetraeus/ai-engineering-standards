# Commit Message Format

Based on [Conventional Commits](https://www.conventionalcommits.org/). Structured commit messages enable automated changelogs, semantic versioning, and clear history.

---

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Rules

- **First line:** max 72 characters
- **Type:** lowercase, from the allowed list below
- **Scope:** optional, lowercase, identifies the module or area
- **Description:** imperative mood ("add" not "added"), lowercase start, no period at end
- **Body:** explains **why**, not what (the diff shows what)
- **Footer:** breaking changes and issue references

---

## Types

| Type | Purpose | Triggers Version Bump |
|---|---|---|
| `feat` | New feature or capability | Minor (0.X.0) |
| `fix` | Bug fix | Patch (0.0.X) |
| `docs` | Documentation only changes | None |
| `test` | Adding or updating tests | None |
| `refactor` | Code change that neither fixes a bug nor adds a feature | None |
| `ci` | Changes to CI/CD configuration | None |
| `chore` | Maintenance tasks (deps, config, tooling) | None |
| `perf` | Performance improvement | Patch (0.0.X) |
| `style` | Formatting, whitespace (no code change) | None |
| `build` | Changes to build system or dependencies | None |
| `revert` | Reverts a previous commit | Depends on reverted type |

---

## Examples

### Simple Feature

```
feat(auth): add JWT token refresh endpoint
```

### Bug Fix with Body

```
fix(parser): handle empty CSV files without crashing

The CSV parser raised an IndexError when the input file had headers
but no data rows. Now returns an empty list instead.

Closes #127
```

### Breaking Change

```
feat(api)!: change user endpoint response format

The /api/users endpoint now returns a paginated response object
instead of a flat array. All API consumers must update their
parsing logic.

BREAKING CHANGE: GET /api/users response changed from array to
paginated object with { data: [], meta: { page, total } } structure.

Closes #89
```

### Refactor

```
refactor(pipeline): extract validation into separate module

Moved all input validation functions from pipeline.py into
validators.py to improve testability and reduce file size.
No behavior change.
```

### Documentation

```
docs(readme): add quick start section and architecture diagram
```

### Chore

```
chore(deps): upgrade pydantic from 2.5.0 to 2.6.1
```

### CI

```
ci(github-actions): add ruff linting step to PR checks
```

### Test

```
test(retry): add property-based tests for backoff calculation
```

### Revert

```
revert: feat(auth): add JWT token refresh endpoint

This reverts commit abc1234. The refresh endpoint caused session
conflicts in production. Reverting until root cause is identified.
```

---

## Scopes

Scopes are project-specific but should be consistent within a repo. Common patterns:

```
feat(auth): ...       # authentication module
fix(api): ...         # API layer
refactor(pipeline): ...  # data pipeline
test(models): ...     # model layer
ci(deploy): ...       # deployment pipeline
docs(readme): ...     # README file
chore(deps): ...      # dependencies
```

Define your project's scopes in the repo's `CLAUDE.md` or `CONTRIBUTING.md`.

---

## Multi-line Body

When the body is needed, separate it from the subject with a blank line. Wrap at 72 characters.

```
fix(export): prevent duplicate rows in CSV export

The export function was not deduplicating records when multiple
source tables contained overlapping date ranges. Added a
deduplication step using the composite key (user_id, event_date)
before writing to the output file.

The bug affected exports generated between 2025-01-15 and
2025-02-01. Historical exports should be regenerated.

Fixes #203
```

---

## Footer Conventions

| Footer | Purpose | Example |
|---|---|---|
| `Closes #N` | Auto-close an issue on merge | `Closes #127` |
| `Fixes #N` | Auto-close a bug issue on merge | `Fixes #203` |
| `Refs #N` | Reference without closing | `Refs #45` |
| `BREAKING CHANGE:` | Describe breaking change | `BREAKING CHANGE: API response format changed` |
| `Co-Authored-By:` | Credit co-authors | `Co-Authored-By: Name <email>` |

---

## What NOT to Do

```
# Too vague
fix: fix bug

# Past tense
feat(auth): added login endpoint

# Capitalized description
feat(api): Add new endpoint

# Period at end
fix(parser): handle null values.

# Way too long first line
feat(authentication): add JWT token refresh endpoint with automatic retry and configurable expiration timeout

# No type
update user service to handle edge cases

# Mixing concerns in one commit
feat(api): add user endpoint and fix CSV parser and update docs
```

---

## Commit Checklist

Before committing, verify:

- [ ] Type is correct (feat vs fix vs refactor)
- [ ] First line is under 72 characters
- [ ] Description uses imperative mood
- [ ] Body explains why (if non-obvious)
- [ ] Breaking changes are flagged with `!` and `BREAKING CHANGE:` footer
- [ ] Related issues are referenced in footer
- [ ] One logical change per commit
