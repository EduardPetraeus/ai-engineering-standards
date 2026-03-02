# STATUS — V2 Workstream 2

## Branch
`feature/v2`

## Summary
Added four new content-aware validation checks to the `ai-standards validate` CLI, moving beyond file-existence checks into AST-based code analysis and content parsing.

## Changes

### New Checks (src/ai_standards/checks.py)

| Check | Description |
|---|---|
| **Naming conventions** | AST-based: verifies functions/variables use `snake_case`, classes use `PascalCase`. Reports file, line number, and offending name. Skips `.venv`, `__pycache__`, etc. |
| **Commit message format** | Validates Conventional Commits pattern (`type(scope): description`). Checks first line <= 72 chars. Supports all standard types + breaking change `!` indicator. |
| **CLAUDE.md sections** | Verifies CLAUDE.md contains required sections: Identity, Scope, Boundaries. Case-insensitive heading matching at any level (h1-h6). |
| **Docstring presence** | AST-based: verifies all public functions (not starting with `_`) have docstrings. Checks both top-level functions and class methods. |

### Updated Files

| File | Change |
|---|---|
| `src/ai_standards/checks.py` | +4 new check functions, +3 repo-level wrappers, ALL_CHECKS expanded from 8 to 11 |
| `tests/test_v2_checks.py` | 43 new tests across 8 test classes |
| `tests/conftest.py` | Updated `compliant_repo` fixture with CLAUDE.md sections |
| `tests/test_cli.py` | Updated check count assertions (8 -> 11) |
| `README.md` | Added Validator CLI documentation section |

## Test Results
- **71 tests passing** (28 existing + 43 new)
- Ruff check: clean
- Ruff format: clean

## Test Counts by Check

| Check | Tests |
|---|---|
| Naming conventions | 13 (10 file-level + 3 repo-level) |
| Commit messages | 11 |
| CLAUDE.md sections | 9 (6 file-level + 3 repo-level) |
| Docstring presence | 10 (7 file-level + 3 repo-level) |

## Acceptance Criteria

- [x] `ai-standards validate .` catches camelCase function names
- [x] `ai-standards validate .` catches missing docstrings
- [x] `check_commit_message()` catches malformed commit messages
- [x] `ai-standards validate .` catches CLAUDE.md without required sections
- [x] Each check has >= 3 tests
- [x] All 28 existing tests still pass
- [x] Ruff clean (check + format)
