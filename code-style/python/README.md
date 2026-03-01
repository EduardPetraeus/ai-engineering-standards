# Python Code Style — Pre-commit & Tooling

This directory contains the standard Python tooling configuration for all projects in this ecosystem.

## Files

| File | Purpose |
|---|---|
| [`.pre-commit-config.yaml`](.pre-commit-config.yaml) | Pre-commit hook definitions with pinned versions |
| [`ruff.toml`](ruff.toml) | Ruff linter and formatter configuration |
| [`pyproject.toml`](pyproject.toml) | Python project config (mypy, pytest, black) |

## What's Included and Why

The pre-commit configuration enforces code quality automatically before each commit:

| Hook | Source | Purpose |
|---|---|---|
| **ruff** | `astral-sh/ruff-pre-commit` | Linting — catches bugs, enforces style, sorts imports |
| **ruff-format** | `astral-sh/ruff-pre-commit` | Formatting — consistent code style (replaces black) |
| **mypy** | `pre-commit/mirrors-mypy` | Type checking — catches type errors before runtime |
| **trailing-whitespace** | `pre-commit/pre-commit-hooks` | Removes trailing whitespace from all files |
| **end-of-file-fixer** | `pre-commit/pre-commit-hooks` | Ensures files end with a single newline |
| **check-yaml** | `pre-commit/pre-commit-hooks` | Validates YAML syntax |
| **check-json** | `pre-commit/pre-commit-hooks` | Validates JSON syntax |
| **detect-secrets** | `Yelp/detect-secrets` | Prevents accidental secret/credential commits |

All hooks use **pinned versions** (`rev:`) to ensure reproducible builds across environments.

## Installation

### 1. Copy config to your project

Copy `.pre-commit-config.yaml` to your project root:

```bash
cp code-style/python/.pre-commit-config.yaml /path/to/your-project/.pre-commit-config.yaml
```

### 2. Install pre-commit

```bash
pip install pre-commit
```

### 3. Activate hooks

```bash
cd /path/to/your-project
pre-commit install
```

This registers the hooks with git so they run automatically on every `git commit`.

### 4. Initialize detect-secrets baseline

```bash
detect-secrets scan > .secrets.baseline
```

## Running Manually

Run all hooks against all files (useful for CI or first-time setup):

```bash
pre-commit run --all-files
```

Run a specific hook:

```bash
pre-commit run ruff --all-files
pre-commit run mypy --all-files
pre-commit run detect-secrets --all-files
```

Update all hooks to their latest pinned versions:

```bash
pre-commit autoupdate
```

> **Note:** After `autoupdate`, review the version changes and test before committing.

## Customization

### Adjusting the Ruff config path

By default, the hooks reference `.engineering/ruff.toml`. If your project stores the config elsewhere, update the `args` in `.pre-commit-config.yaml`:

```yaml
hooks:
  - id: ruff
    args: [--fix, --config, path/to/your/ruff.toml]
  - id: ruff-format
    args: [--config, path/to/your/ruff.toml]
```

See [`ruff.toml`](ruff.toml) in this directory for the standard linter configuration.

### Adding mypy dependencies

If your project uses typed libraries (e.g., `pydantic`, `sqlalchemy`), add their stubs:

```yaml
hooks:
  - id: mypy
    additional_dependencies:
      - pydantic
      - sqlalchemy-stubs
      - types-requests
```

See [`pyproject.toml`](pyproject.toml) for the standard mypy settings.

### Adding or removing hooks

To add a new hook, append a new entry under `repos:` with a pinned `rev:`. Example:

```yaml
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.3
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]
```

To remove a hook, delete its entry from the YAML file and run `pre-commit install` again.

### Skipping hooks temporarily

Skip a specific hook for a single commit (use sparingly):

```bash
SKIP=mypy git commit -m "wip: temporary skip"
```

## Related Configuration

- [`ruff.toml`](ruff.toml) — Full Ruff linter/formatter rules (target Python 3.11, 100-char line length)
- [`pyproject.toml`](pyproject.toml) — mypy strict mode, pytest config, coverage settings
- [`../../security/secret-scanning-config.yaml`](../../security/secret-scanning-config.yaml) — Secret scanning patterns
