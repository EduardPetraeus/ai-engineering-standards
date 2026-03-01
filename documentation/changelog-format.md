# Changelog Format

Based on [Keep a Changelog](https://keepachangelog.com/). A human-readable log of notable changes for each version.

---

## Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New feature or capability

### Changed
- Modification to existing functionality

## [0.2.0] - 2025-06-15

### Added
- User authentication with JWT tokens
- Rate limiting middleware (100 req/min per client)

### Changed
- API response format now includes pagination metadata

### Fixed
- CSV parser no longer crashes on empty files (#127)

### Security
- Upgraded requests from 2.28.0 to 2.31.0 (CVE-2023-32681)

## [0.1.0] - 2025-05-01

### Added
- Initial project structure
- Basic CRUD endpoints for users
- PostgreSQL database integration
- Docker Compose for local development
- CI pipeline with linting and tests
```

---

## Sections

| Section | When to Use | Example |
|---|---|---|
| **Added** | New features, capabilities, endpoints | "Add CSV export for reports" |
| **Changed** | Modifications to existing behavior | "Change default timeout from 30s to 60s" |
| **Deprecated** | Features that will be removed in a future version | "Deprecate /api/v1/users endpoint (use /api/v2/users)" |
| **Removed** | Features that have been removed | "Remove legacy XML import support" |
| **Fixed** | Bug fixes | "Fix duplicate rows in monthly report export (#203)" |
| **Security** | Vulnerability patches, dependency updates for CVEs | "Upgrade pyyaml to 6.0.1 (CVE-2023-XXXXX)" |

---

## Rules

### Version Headers

- Format: `## [X.Y.Z] - YYYY-MM-DD`
- Use [Semantic Versioning](https://semver.org/):
  - **Major (X):** Breaking changes
  - **Minor (Y):** New features, backward compatible
  - **Patch (Z):** Bug fixes, backward compatible
- Date format: ISO 8601 (`YYYY-MM-DD`)

### Unreleased Section

Always keep an `## [Unreleased]` section at the top for changes not yet in a release:

```markdown
## [Unreleased]

### Added
- Webhook support for order events

### Fixed
- Memory leak in connection pool under high load
```

When releasing, move Unreleased items to the new version section and create a fresh empty Unreleased section.

### Writing Style

- Start each entry with a **verb** in imperative mood: Add, Change, Fix, Remove, Deprecate, Upgrade
- Reference issue/PR numbers: `(#127)`, `(PR #42)`
- Be specific: "Fix CSV parser crash on empty files" not "Fix bug"
- One entry per logical change (don't combine unrelated changes)

### What NOT to Include

- Internal refactoring that doesn't affect users
- Dependency updates that don't fix vulnerabilities
- CI/CD changes
- Code formatting changes
- Test additions (unless they represent a new testing capability)

---

## Example Entries

### Good Entries

```markdown
### Added
- Add exponential backoff retry for external API calls (max 3 retries)
- Add structured JSON logging with request correlation IDs
- Add health check endpoint at /api/health (#89)

### Changed
- Change user search to be case-insensitive (#156)
- Increase default connection pool size from 5 to 10

### Deprecated
- Deprecate `GET /api/v1/reports` — use `GET /api/v2/reports` instead (removal in v1.0.0)

### Removed
- Remove support for Python 3.9 (minimum is now 3.11)

### Fixed
- Fix race condition in concurrent order processing (#203)
- Fix incorrect tax calculation for zero-amount orders (#211)
- Fix memory leak when processing large CSV files (>1GB)

### Security
- Upgrade cryptography from 41.0.0 to 42.0.0 (CVE-2024-XXXXX)
- Add CSRF protection to all form endpoints
- Remove PII from application logs
```

### Bad Entries

```markdown
# Too vague
- Fix bug
- Update code
- Improvements

# Implementation details (users don't care)
- Refactor UserService to use repository pattern
- Add type hints to utils module
- Update GitHub Actions workflow

# Past tense (use imperative)
- Added new feature
- Fixed the parser
- Changed the config
```

---

## Automation

Generate changelog entries from conventional commit messages:

```bash
# Using git-cliff or similar tool
git cliff --unreleased --prepend CHANGELOG.md

# Or manually from git log
git log --oneline v0.1.0..HEAD --format="- %s"
```

Map commit types to changelog sections:

| Commit Type | Changelog Section |
|---|---|
| `feat` | Added |
| `fix` | Fixed |
| `docs` | (skip — unless user-facing) |
| `refactor` | (skip) |
| `perf` | Changed |
| `test` | (skip) |
| `ci` | (skip) |
| `chore` | (skip — unless dependency security update) |

---

## File Location

The changelog file should be:
- Named `CHANGELOG.md`
- Located in the project root
- Included in the git repository (not generated at build time)
