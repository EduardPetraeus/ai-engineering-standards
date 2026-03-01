# AGENTS.md Pattern

## What Is AGENTS.md?

AGENTS.md is an agent-agnostic alias for CLAUDE.md. It serves the same
purpose — governing AI agent behavior in a repository — but uses a
tool-neutral filename.

The pattern exists because different AI coding tools look for different
configuration files:

| Tool          | Config file       |
|---------------|-------------------|
| Claude Code   | CLAUDE.md         |
| Cursor        | .cursorrules      |
| Windsurf      | .windsurfrules    |
| Generic       | AGENTS.md         |

Maintaining separate files with the same content creates drift. The
solution: one master file with symlinks.

## Implementation

### Symlink Approach (Recommended)

Keep CLAUDE.md as the single source of truth. Create symlinks for
other tools:

```bash
# In repo root
ln -s CLAUDE.md AGENTS.md
ln -s CLAUDE.md .cursorrules
ln -s CLAUDE.md .windsurfrules
```

Commit the symlinks to git. They resolve correctly on all platforms
that support symbolic links (Linux, macOS, Windows with developer mode).

### Verification

```bash
# Verify symlinks point to CLAUDE.md
ls -la AGENTS.md .cursorrules .windsurfrules
# Should show: AGENTS.md -> CLAUDE.md
```

### Scaffolder Integration

The ai-project-templates scaffolder creates these symlinks automatically
when generating a new project. The `scaffold.py` command accepts a
`--agent-aliases` flag to control which symlinks are created.

## When to Use a Separate File

In most cases, symlinks are sufficient. Use a separate AGENTS.md only when:

1. **Tool-specific instructions differ materially**: One tool needs
   different session protocols than another (rare in practice).

2. **Team uses a tool that cannot follow symlinks**: Some Windows CI
   environments may not resolve symlinks. In this case, use a post-checkout
   git hook to copy the file.

3. **Public repos targeting non-Claude users**: If the primary audience
   uses Cursor or Windsurf, naming the master file AGENTS.md and
   symlinking CLAUDE.md to it may be more intuitive.

## Content Guidelines

Whether the file is called CLAUDE.md or AGENTS.md, the content structure
should follow the template in `claude-md-template.md`. The key sections are:

- **project_context** — orientation for the agent
- **conventions** — coding and documentation rules
- **session_protocol** — start/during/end behavior
- **security_protocol** — hard boundaries
- **quality_standards** — minimum quality bar
- **framework_references** — links to governance ecosystem

## Relationship to Other Config Files

AGENTS.md / CLAUDE.md governs *agent behavior*. It is not a replacement for:

- **pyproject.toml** — build system and tool configuration
- **ruff.toml** — linter rules
- **.pre-commit-config.yaml** — git hook configuration
- **.editorconfig** — editor formatting preferences

These files configure tools. CLAUDE.md configures the agent that uses those
tools. Both are needed.

## Migration Guide

If your repo already has a .cursorrules or .windsurfrules file:

1. Audit the existing content — extract anything agent-universal
2. Create CLAUDE.md with the universal content
3. Replace .cursorrules/.windsurfrules with symlinks to CLAUDE.md
4. If tool-specific content remains, add it as a commented section
   at the bottom of CLAUDE.md with a clear header

```markdown
<!-- Cursor-specific: uncomment if using Cursor -->
<!-- ## cursor_overrides -->
<!-- - Use TypeScript for new files -->
```

## Best Practices

- **One master, many symlinks**: Never edit the symlinks directly
- **Track in git**: Symlinks should be committed, not gitignored
- **Review changes**: CLAUDE.md changes go through PR review like code
- **Keep it current**: Outdated agent instructions cause more harm than
  no instructions at all
- **Test with multiple tools**: Verify your CLAUDE.md works correctly
  when read by different AI assistants
