# Context File Patterns

Patterns for managing context in agentic development projects. Context
files bridge the gap between stateless AI sessions and the continuous
state of a software project.

## The Context Hierarchy

Context flows from global to specific. Each level can override the one
above it:

```
~/.claude/CLAUDE.md          (Level 0: Global user defaults)
    |
<repo>/CLAUDE.md             (Level 1: Repo constitution)
    |
<repo>/src/CLAUDE.md         (Level 2: Subsystem overrides)
    |
<repo>/CONTEXT.md            (Level 3: Dynamic project state)
    |
~/.claude/memory/*.md        (Level 4: Cross-session persistence)
```

### Level 0: Global CLAUDE.md

User-wide preferences that apply to all repositories. Keep this minimal:
language preferences, communication style, identity context. Anything
project-specific belongs at Level 1.

### Level 1: Repo CLAUDE.md

The constitution for a specific project. Contains conventions, session
protocols, security rules, and quality standards. This is the most
important context file and is described in detail in `claude-md-template.md`.

### Level 2: Subsystem CLAUDE.md

Optional overrides for specific directories. Use sparingly — only when
a subsystem has genuinely different rules (e.g., a frontend directory
in a mostly-backend repo).

### Level 3: CONTEXT.md

Dynamic project state that changes frequently. Unlike CLAUDE.md (which
changes rarely), CONTEXT.md tracks what is happening right now.

### Level 4: Memory Files

Cross-session persistence for patterns, learnings, and decisions that
span multiple projects.

## CLAUDE.md as Constitution

CLAUDE.md is a *constitution*, not a *to-do list*. It defines the rules
of engagement, not the current tasks. Key characteristics:

- **Stable**: Changes infrequently (once per milestone, not per session)
- **Prescriptive**: States what agents must and must not do
- **Verified**: Changes go through PR review
- **Versioned**: Tracked in git alongside code

## CONTEXT.md for Project State

CONTEXT.md captures the *current state* of a project. It answers
questions like:

- What was recently completed?
- What is the current focus?
- What decisions were made and why?
- What blockers exist?

### Template

```markdown
# CONTEXT.md — <project-name>

Last updated: <date>

## Current State
- Version: <current version>
- Branch: <active branch>
- Focus: <what is being worked on>

## Recent Decisions
- <date>: <decision and rationale>

## Architecture Notes
- <key architectural patterns or constraints>

## Known Issues
- <blockers or technical debt items>

## Next Steps
- <prioritized list of upcoming work>
```

### Update Protocol

- Update at the end of meaningful sessions (not every minor change)
- The agent proposes updates; the human approves
- Keep it under 100 lines — if it grows, archive old sections

## Memory Files for Cross-Session Persistence

Memory files live in `~/.claude/memory/` and persist information that
spans multiple projects and sessions. Examples:

- `profile.md` — user background, goals, preferences
- `stack.md` — tech stack, architecture principles
- `products.md` — active products and pipeline
- `MEMORY.md` — auto-captured learnings from sessions

### When to Write Memory

Write to memory when:
- A pattern was discovered that will save time in future sessions
- A non-obvious decision was made that might be questioned later
- A workflow optimization was found
- A tool configuration was tuned after experimentation

Do not write to memory:
- Session-specific debugging steps
- Information already captured in CONTEXT.md or CLAUDE.md
- Temporary workarounds that will be resolved soon

## Builder-Brain Pattern

For prolific builders managing multiple projects, a dedicated context
repository provides a centralized "brain":

```
builder-brain/
  hot/
    always-loaded.md    # Identity, preferences, communication style
  cold/
    agentic-framework.md    # Loaded on trigger keywords
    context-architecture.md
    update-protocol.md
  INDEX.md              # Active projects overview
  builder-brain-master.md  # Full reference (hot + cold combined)
```

### Hot vs Cold Memory

- **Hot memory** is loaded at session start, every time. Keep it small
  (under 100 lines). Contains identity, preferences, and active project
  index.
- **Cold memory** is loaded on demand when trigger keywords appear.
  Contains detailed frameworks, protocols, and reference material that
  is not needed every session.

### Session Protocol with Builder-Brain

1. Read `hot/always-loaded.md` (identity and preferences)
2. Read `INDEX.md` (which project is active)
3. Navigate to the active project
4. Read that project's CONTEXT.md
5. Begin work

This protocol ensures the agent has full context in 4 file reads,
regardless of which project is being worked on.

## Anti-Patterns

### Monolithic Context

Putting everything in one giant CLAUDE.md. After 200 lines, agents
struggle to prioritize information. Split into CLAUDE.md (rules) and
CONTEXT.md (state).

### Stale Context

CONTEXT.md that references completed work or outdated decisions. Worse
than no context — it actively misleads. Set a reminder to review context
files monthly.

### Duplicated Context

The same information in CLAUDE.md, CONTEXT.md, and memory files. When
it gets updated in one place but not others, agents get conflicting
instructions. Single source of truth, always.

### Over-Documentation

Writing detailed memory entries for every session. Memory should capture
*insights*, not *activities*. If a future agent would not benefit from
the information, do not write it.
