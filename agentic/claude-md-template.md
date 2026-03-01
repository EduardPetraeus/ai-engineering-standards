# CLAUDE.md Template

A CLAUDE.md file is the constitution for AI agent behavior in a repository.
It is the single source of truth that governs what agents can and cannot do.

This template provides a complete, production-ready structure. Copy it into
your repo root and customize each section.

---

## Template

```markdown
# CLAUDE.md — <project-name>

This file governs all AI agent sessions in this repository.
Hierarchy: ai-governance-framework > this CLAUDE.md > session context.

## project_context

<!-- What is this project? Keep it to 3-5 lines. Agents need fast orientation. -->

- Repo: <repo-name>
- Purpose: <one-line description>
- License: <MIT / Apache-2.0 / proprietary>
- Status: <version or phase>
- Stack: <primary languages and frameworks>

## conventions

<!-- Non-negotiable rules for all code and content in this repo. -->

- All code, comments, docstrings, and documentation in English
- File names: kebab-case for markdown, snake_case for Python modules
- Python style: snake_case functions/variables, PascalCase classes
- Configs use standard tool formats (ruff.toml, pyproject.toml)
- Every function must have a docstring
- Type hints on all public function signatures
- No print() in library code — use logging

## session_protocol

<!-- Step-by-step instructions for agent behavior at each phase. -->

### start

1. Read this CLAUDE.md first
2. Read CONTEXT.md if it exists (project state and decisions)
3. Confirm scope with the user before making changes
4. Check git status — do not start work on a dirty tree unless instructed

### during

- Commit frequently with descriptive messages (conventional commits)
- Run lint and tests before every commit
- Ask before creating new files — prefer editing existing ones
- Stay within the agreed scope — do not refactor unrelated code
- Use existing patterns in the codebase, do not introduce new ones without approval

### end

- Run full test suite and lint
- Summarize what was done and what remains
- Update CONTEXT.md if project state changed
- Do not push to remote unless explicitly asked

## security_protocol

<!-- Hard boundaries that must never be crossed. -->

- Never commit secrets, API keys, or credentials
- Never read or modify files outside this repository without explicit permission
- Never run destructive git commands (force push, reset --hard) without approval
- Never install packages not listed in dependencies without asking
- Flag any file that looks like it contains PII

## quality_standards

<!-- Minimum quality bar for all contributions. -->

- All new code must have tests (target: 80% coverage)
- All tests must pass before committing
- Ruff lint must pass with zero errors
- No TODO comments without a linked issue
- Documentation must be updated alongside code changes

## framework_references

<!-- Links to the governance and standards ecosystem. -->

- Governance: ai-governance-framework (constitution hierarchy)
- Standards: ai-engineering-standards (coding conventions)
- Task management: ai-project-management (YAML task engine)
- Templates: ai-project-templates (scaffolder)
```

---

## Usage Notes

### Placement

CLAUDE.md must live in the repository root. Claude Code automatically reads
this file at session start. No additional configuration is needed.

### Size Guidelines

Keep CLAUDE.md under 200 lines. If it grows beyond that, extract detailed
standards into separate files and reference them:

```markdown
## conventions
- See `docs/coding-standards.md` for full Python style guide
- See `docs/api-guidelines.md` for REST API conventions
```

### Inheritance

CLAUDE.md files form a hierarchy:

1. **Global CLAUDE.md** (`~/.claude/CLAUDE.md`) — user-wide defaults
2. **Repo CLAUDE.md** (`<repo>/CLAUDE.md`) — project-specific rules
3. **Directory CLAUDE.md** (`<repo>/src/CLAUDE.md`) — subsystem overrides

Lower levels override higher levels. Keep global rules minimal and put
project-specific details in the repo-level file.

### Agent-Agnostic Compatibility

For teams using multiple AI tools, create symlinks:

```bash
ln -s CLAUDE.md AGENTS.md
ln -s CLAUDE.md .cursorrules
ln -s CLAUDE.md .windsurfrules
```

CLAUDE.md remains the master file. Symlinks ensure other tools pick up
the same instructions. See `agents-md-template.md` for details.

### Versioning

Track CLAUDE.md in git. Changes to the constitution should go through
the same PR review process as code changes. This ensures the team agrees
on agent behavior rules.

### Anti-Patterns

- **Too vague**: "Write good code" gives agents no actionable guidance
- **Too strict**: Micromanaging every decision slows agents down
- **Outdated**: A CLAUDE.md that references deprecated tools is worse than none
- **Duplicated**: Do not copy standards inline — reference the canonical source
