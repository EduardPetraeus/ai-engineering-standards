# Status — ai-engineering-standards

Last updated: 2026-03-01

## Completed Tasks

### TASK-001: Pre-commit hook config for Python projects

**Status:** Done
**Completed:** 2026-03-01

Added `code-style/python/.pre-commit-config.yaml` with pinned versions for:
- Ruff linting and formatting (v0.9.7)
- mypy type checking (v1.15.0)
- Pre-commit hooks for whitespace, YAML, JSON (v5.0.0)
- detect-secrets for credential scanning (v1.5.0)

Added `code-style/python/README.md` documenting installation, manual usage, and customization.

### TASK-002: Databricks/Spark coding standards

**Status:** Done
**Completed:** 2026-03-01

Added `code-style/databricks/databricks-conventions.md` covering:
1. Notebook vs script conventions (naming, structure, max cells)
2. Unity Catalog naming (three-level namespace, environment catalogs, domain schemas)
3. Medallion layer rules (bronze/silver/gold with specific requirements)
4. DLT patterns (decorators, expectations as guard rails, pipeline naming)
5. SQL warehouse best practices (type selection, cost tagging, sizing, timeouts)
6. Spark DataFrame style guide (`.transform()`, `F.col()`, aliasing, `collect()` rules)

Cross-references to `../python/ruff.toml` and `../sql/sql-conventions.md` included.

## Repository Structure

```
code-style/
  python/
    .pre-commit-config.yaml  (NEW — TASK-001)
    README.md                (NEW — TASK-001)
    ruff.toml
    pyproject.toml
  sql/
    sql-conventions.md
  databricks/
    databricks-conventions.md  (NEW — TASK-002)
```
