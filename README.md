# ai-engineering-standards

Machine-readable coding conventions for agentic development. Standards that AI agents can parse, enforce, and follow — not just humans.

## Why This Exists

AI coding agents interpret rules literally. Ambiguous guidelines produce inconsistent code. This repo provides **concrete, example-driven standards** that both humans and AI agents can follow without interpretation gaps.

## Quick Start

1. Clone or reference this repo
2. Copy the configs you need into your project's `.engineering/` directory
3. Add a reference in your project's `CLAUDE.md`:
   ```
   ## engineering_standards
   - Source: ~/Github repos/ai-engineering-standards
   - Active: naming, code-style/python, testing, git
   ```
4. Run linters with the provided configs

## Directory Structure

```
ai-engineering-standards/
├── CLAUDE.md                        # Agent governance for this repo
├── README.md                        # This file
├── LICENSE                          # MIT
├── naming/
│   └── naming-conventions.md        # Python, SQL, files, YAML, git branches
├── code-style/
│   ├── python/
│   │   ├── ruff.toml                # Ruff linter configuration
│   │   └── pyproject.toml           # Black + mypy + pytest config
│   └── sql/
│       └── sql-conventions.md       # SQL formatting and style rules
├── testing/
│   ├── testing-strategy.md          # Decision tree for test types
│   ├── coverage-requirements.md     # Coverage targets by layer
│   └── test-naming.md              # Test function naming pattern
├── git/
│   ├── workflow.md                  # Feature branch workflow
│   ├── commit-message-format.md     # Conventional Commits spec
│   └── pr-template.md              # Pull request template
├── review/
│   ├── agent-review-checklist.md    # What AI agents check
│   └── human-review-checklist.md    # What humans check
├── error-handling/
│   ├── logging-format.md            # Structured JSON logging
│   ├── exception-patterns.md        # Custom exception hierarchy
│   └── retry-policy.md             # Exponential backoff + circuit breaker
├── documentation/
│   ├── docstring-format.md          # Google-style docstrings
│   ├── readme-template.md           # README structure template
│   └── changelog-format.md          # Keep a Changelog format
├── security/
│   ├── security-standards.md        # Security rules + OWASP mapping
│   ├── secret-scanning-config.yaml  # Pre-commit secret detection
│   └── approved-dependencies.md     # Vetted package registry
├── architecture/
│   ├── adr-template.md              # Architecture Decision Record template
│   └── architecture-md-template.md  # Architecture doc template
└── docs/
    ├── PHILOSOPHY.md                # Why standards matter for AI agents
    └── ADOPTION.md                  # Step-by-step adoption guide
```

## Agentic Engineering OS

This repo is part of the **Agentic Engineering OS** — a modular ecosystem for building software with AI agents.

| Repo | Purpose | Status |
|---|---|---|
| [ai-governance-framework](https://github.com/EduardPetraeus/ai-governance-framework) | Constitution, guardrails, agent roles, CI/CD governance | v0.3.0 — active |
| [ai-engineering-standards](https://github.com/EduardPetraeus/ai-engineering-standards) | Code conventions, testing, git workflow (this repo) | v0.1.0 — active |
| [ai-project-management](https://github.com/EduardPetraeus/ai-project-management) | YAML-based task engine, milestones, progress tracking | Scaffolding |
| [ai-project-templates](https://github.com/EduardPetraeus/ai-project-templates) | Cookiecutter scaffolder for new projects | Scaffolding |
| [agentic-engineering](https://github.com/EduardPetraeus/agentic-engineering) | Umbrella docs, content marketing, ecosystem overview | Scaffolding |

## How to Adopt

### Minimal (copy configs)
```bash
mkdir -p .engineering
cp ai-engineering-standards/code-style/python/ruff.toml .engineering/
cp ai-engineering-standards/code-style/python/pyproject.toml .engineering/
```

### Standard (reference in CLAUDE.md)
Add to your project's `CLAUDE.md`:
```markdown
## engineering_standards
- Source: ~/Github repos/ai-engineering-standards
- Active sections: naming, code-style/python, testing, git, error-handling
- Override: line-length = 120 (project-specific)
```

### Full (pre-commit + CI)
1. Copy linter configs to `.engineering/`
2. Reference standards in `CLAUDE.md`
3. Set up pre-commit hooks with the provided secret-scanning config
4. Add linter checks to CI pipeline
5. Adopt incrementally — don't rewrite existing code all at once

## License

MIT
