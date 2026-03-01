# Adoption Guide

How to adopt these engineering standards in your project. Start small, expand incrementally.

---

## Step 1: Copy Linter Configs

Copy the machine-enforceable configs to your project. Use `.engineering/` as the standard directory.

```bash
# Create the directory
mkdir -p .engineering

# Copy Python linter and formatter config
cp ~/Github\ repos/ai-engineering-standards/code-style/python/ruff.toml .engineering/
cp ~/Github\ repos/ai-engineering-standards/code-style/python/pyproject.toml .engineering/

# Or symlink if you want automatic updates
ln -s ~/Github\ repos/ai-engineering-standards/code-style/python/ruff.toml .engineering/ruff.toml
```

Configure your tools to use these files:

```bash
# Ruff: point to the config
ruff check . --config .engineering/ruff.toml

# Or move configs to project root (some tools require root-level config)
cp .engineering/pyproject.toml ./pyproject.toml
```

---

## Step 2: Add Standards Reference to CLAUDE.md

Add a section to your project's `CLAUDE.md` that tells AI agents which standards apply.

```markdown
## engineering_standards
- Source: ~/Github repos/ai-engineering-standards
- Active sections:
  - naming/naming-conventions.md
  - code-style/python/
  - testing/testing-strategy.md
  - testing/test-naming.md
  - git/commit-message-format.md
  - git/workflow.md
  - error-handling/exception-patterns.md
  - error-handling/logging-format.md
  - documentation/docstring-format.md
- Overrides:
  - line-length: 120 (default is 100)
  - coverage target: 85% (default is 80%)
```

This tells the agent:
- Where to find the standards
- Which sections are active (don't enforce sections you haven't adopted)
- Where your project deviates from defaults

---

## Step 3: Set Up Pre-commit Hooks

Install pre-commit and use the secret scanning config as a starting point.

```bash
# Install pre-commit
pip install pre-commit

# Copy the pre-commit config
cp ~/Github\ repos/ai-engineering-standards/security/secret-scanning-config.yaml .pre-commit-config.yaml

# Install the hooks
pre-commit install

# Run against all existing files (first time only)
pre-commit run --all-files
```

Add additional hooks for your linter:

```yaml
# Add to .pre-commit-config.yaml
repos:
  # ... existing hooks from secret-scanning-config.yaml ...

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.2
    hooks:
      - id: ruff
        args: [--config, .engineering/ruff.toml, --fix]
      - id: ruff-format
        args: [--config, .engineering/ruff.toml]
```

---

## Step 4: Run Linters on Existing Code

Don't try to fix everything at once. Use a phased approach.

### Phase 1: Baseline (Week 1)

Run the linter and count existing violations:

```bash
# Count violations by rule
ruff check . --config .engineering/ruff.toml --statistics

# Auto-fix safe issues
ruff check . --config .engineering/ruff.toml --fix
```

Commit the auto-fixes in a single commit:
```
chore(lint): apply ruff auto-fixes to existing codebase
```

### Phase 2: New Code Only (Weeks 2-4)

Add the linter to CI but only block on new violations, not existing ones:

```yaml
# GitHub Actions — only check changed files
- name: Lint changed files
  run: |
    git diff --name-only origin/main...HEAD -- '*.py' | xargs ruff check --config .engineering/ruff.toml
```

### Phase 3: Full Enforcement (Month 2+)

Once the team is comfortable, enable full enforcement:

```yaml
# GitHub Actions — check all files
- name: Lint
  run: ruff check . --config .engineering/ruff.toml

- name: Type check
  run: mypy src/
```

---

## Step 5: Adopt Incrementally

Don't adopt all standards at once. Recommended order:

| Priority | Standard | Why First |
|---|---|---|
| 1 | `code-style/python/ruff.toml` | Automated, immediate impact, auto-fixable |
| 2 | `naming/naming-conventions.md` | Consistency from day one, easy to follow |
| 3 | `git/commit-message-format.md` | Clean history, enables automation |
| 4 | `testing/test-naming.md` | Quick win for test readability |
| 5 | `error-handling/exception-patterns.md` | Improves debugging and error handling |
| 6 | `documentation/docstring-format.md` | Better AI-generated documentation |
| 7 | `security/security-standards.md` | Security baseline |
| 8 | `testing/testing-strategy.md` | Strategic test coverage |
| 9 | `architecture/adr-template.md` | Decision documentation |
| 10 | Everything else | Full adoption |

---

## Project-Specific Overrides

Projects can override any default. Document overrides explicitly in `CLAUDE.md`.

### Override Examples

```markdown
## engineering_standards_overrides

### Line length
- Default: 100
- This project: 120
- Reason: Data pipeline code has long column lists

### Coverage target
- Default: 80%
- This project: 90%
- Reason: Payment processing, high reliability requirement

### SQL prefix convention
- Default: stg_, dim_, fct_, vw_
- This project: raw_, clean_, mart_, view_
- Reason: Existing convention from dbt project, migration too costly

### Test naming
- Default: test_{function}_{scenario}_{expected}
- This project: test_{function}_{scenario} (without expected suffix)
- Reason: Team preference, adopted before standards were available
```

---

## Measuring Adoption

Track adoption metrics to see progress:

```bash
# Linter violations over time
ruff check . --config .engineering/ruff.toml --statistics 2>&1 | tail -20

# Test coverage
pytest --cov=src --cov-report=term-missing | grep TOTAL

# Commit message compliance (check last 50 commits)
git log --oneline -50 | grep -cE '^[a-f0-9]+ (feat|fix|docs|test|refactor|ci|chore|perf|style|build|revert)'
```

### Adoption Scorecard

| Standard | Metric | Target | Current |
|---|---|---|---|
| Linting | Zero ruff violations | 0 | ___ |
| Type checking | Zero mypy errors | 0 | ___ |
| Test coverage | Coverage percentage | 80% | ___% |
| Commit format | % conventional commits | 100% | ___% |
| Secret scanning | Pre-commit hooks installed | Yes | ___ |
| Docstrings | % public functions documented | 90% | ___% |

---

## Common Pitfalls

### "Let's fix everything first"
Don't. Adopt incrementally. A 500-file formatting PR is impossible to review and will cause merge conflicts.

### "We'll override most of the rules"
If you override more than 20% of the rules, you don't need standards — you need your own config. Fork and customize.

### "The team hasn't bought in"
Start with auto-fixable linter rules. They require zero behavioral change. Once the team sees clean diffs and consistent code, the harder standards become easier to adopt.

### "Our codebase is too old/messy"
Use the phased approach (Step 4). New code follows standards immediately. Old code gets cleaned up gradually. There is no "too messy to start."

### "AI agents don't read our standards"
Add the reference to `CLAUDE.md`. AI agents read what they're told to read. No reference = no awareness.
