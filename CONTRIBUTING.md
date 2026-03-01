# Contributing to AI Engineering Standards

Thank you for your interest in contributing to the AI Engineering Standards
project. This document explains how to set up a development environment,
add new standards, and submit changes.

## Development Setup

### Prerequisites

- Python 3.11 or later
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/EduardPetraeus/ai-engineering-standards.git
cd ai-engineering-standards

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Verify installation
ai-standards validate .
python -m pytest tests/ -v
```

### Development Commands

```bash
# Run tests with coverage
make test

# Run linter
make lint

# Auto-format code
make format

# Clean build artifacts
make clean
```

## How to Add a New Standard

### 1. Choose the Right Location

Standards are organized by domain:

| Directory          | Content                       |
|--------------------|-------------------------------|
| `architecture/`   | ADR templates, architecture docs |
| `code-style/`     | Language-specific style guides |
| `documentation/`  | Doc formats, templates        |
| `error-handling/`  | Exception patterns, logging   |
| `git/`            | Commit formats, workflow       |
| `naming/`         | Naming conventions             |
| `review/`         | Code review checklists         |
| `security/`       | Security standards, scanning   |
| `testing/`        | Test strategy, coverage        |
| `agentic/`        | AI agent behavior standards    |

### 2. Write the Standard

- Use kebab-case for file names (e.g., `retry-policy.md`)
- Include practical examples, not just rules
- Reference related standards with relative links
- Keep standards actionable — every rule should be verifiable

### 3. Add a Validator Check (if applicable)

If the standard can be checked programmatically:

1. Add a check function in `src/ai_standards/checks.py`
2. Add tests in `tests/test_checks.py`
3. Register the check in `ALL_CHECKS`
4. Update the CLI documentation

### 4. Update Documentation

- Update README.md if a new top-level section was added
- Add a CHANGELOG entry under "Unreleased"

## Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/add-<standard-name>
   ```

2. **Make your changes** following the conventions in CLAUDE.md

3. **Run quality checks**:
   ```bash
   make lint
   make test
   ai-standards validate .
   ```

4. **Commit with conventional commit messages**:
   ```bash
   git commit -m "feat(standards): add retry policy for HTTP clients"
   ```

5. **Push and create a PR**:
   ```bash
   git push -u origin feature/add-<standard-name>
   gh pr create --title "feat: add retry policy" --body "..."
   ```

6. **PR requirements**:
   - All CI checks pass
   - At least one approval
   - No unresolved comments
   - Conventional commit message on squash-merge

## Code Style

- Python: Follow ruff configuration in `pyproject.toml`
- Markdown: One sentence per line (for clean diffs)
- YAML: 2-space indentation
- All content in English

## Reporting Issues

Use GitHub Issues for:
- Bug reports (include steps to reproduce)
- Feature requests (describe the use case)
- Standard proposals (draft the standard content)

Label your issues appropriately:
- `type:bug` — something is broken
- `type:feature` — new capability
- `type:docs` — documentation improvement
- `type:chore` — maintenance task

## Code of Conduct

This project follows the Contributor Covenant v2.1. See
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.
