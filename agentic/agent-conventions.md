# Agent Conventions

Rules and expectations for how AI agents should behave when working in
repositories governed by the AI Engineering Standards.

## Session Start Protocol

When an agent begins a session in any repository:

1. **Read CLAUDE.md** — This is mandatory. Do not proceed without reading
   the repo's constitution file.
2. **Read CONTEXT.md** — If present, this contains project state, recent
   decisions, and active work items.
3. **Check git status** — Understand the current branch, uncommitted changes,
   and recent commits before making any modifications.
4. **Confirm scope** — Verify what the user wants accomplished. Do not assume.
   A brief "I will do X and Y, does that cover it?" saves time.

## Tool Usage Rules

### File Operations

- **Prefer editing over creating**: Always check if an existing file can be
  modified before creating a new one.
- **Never create documentation files unless asked**: READMEs, markdown docs,
  and similar files should only be created on explicit request.
- **Use absolute paths**: When referencing files in output, always use
  absolute paths so the user can navigate directly.
- **Read before writing**: Always read a file before attempting to edit it.
  Blind edits based on assumptions cause errors.

### Git Operations

- **Commit frequently**: Small, focused commits with conventional commit
  messages (feat:, fix:, chore:, docs:, test:, refactor:).
- **Never force push**: Force pushing destroys history. Always prefer
  creating new commits over amending.
- **Never skip hooks**: Pre-commit hooks exist for a reason. If a hook
  fails, fix the underlying issue.
- **Branch discipline**: Work on feature branches. Never commit directly
  to main unless explicitly instructed.
- **Do not push unless asked**: Local commits are safe. Pushing affects
  the team. Wait for explicit permission.

### Search and Navigation

- **Use specialized tools**: Prefer grep/glob tools over shell commands
  for searching. They provide better output formatting.
- **Start broad, narrow down**: When investigating, search broadly first,
  then focus on specific files.
- **Check multiple locations**: Do not assume a pattern only exists in one
  place. Search the entire codebase.

## Error Handling

- **Surface errors immediately**: Do not silently retry or work around
  errors. Show the error, explain it, and propose a fix.
- **Diagnose root causes**: Do not put band-aids on symptoms. If a test
  fails, understand why before changing it.
- **Preserve failing states**: If something is broken, do not hide it by
  deleting the test or disabling the check.

## Scope Discipline

- **Stay in scope**: If the user asks to fix a bug, fix that bug. Do not
  refactor the entire module.
- **Flag adjacent issues**: If you notice problems outside the current
  scope, mention them but do not fix them unless asked.
- **No unsolicited improvements**: Renaming variables, reformatting code,
  or adding type hints outside the current task creates noise in diffs.
- **Ask before expanding**: If the fix naturally requires touching more
  files than expected, check with the user first.

## Commit Etiquette

### Message Format

```
<type>(<scope>): <description>

<optional body>

Co-Authored-By: <agent-name> <email>
```

### Types

- `feat` — new feature or capability
- `fix` — bug fix
- `docs` — documentation only
- `test` — adding or updating tests
- `chore` — maintenance (deps, CI, configs)
- `refactor` — code restructuring without behavior change

### Rules

- One logical change per commit
- Description in imperative mood ("add feature" not "added feature")
- Body explains *why*, not *what* (the diff shows what)
- Always include Co-Authored-By when an AI agent contributed

## Handover Protocol

When a session ends or work is paused:

1. **Summarize work done**: List what was completed, what was tested,
   and what remains.
2. **Update CONTEXT.md**: If project state changed meaningfully, update
   the context file so the next session (human or agent) can resume.
3. **List open questions**: If decisions were deferred, document them
   explicitly.
4. **Clean state**: Ensure the repo is in a clean, buildable state.
   Do not leave half-finished changes uncommitted.

## Memory Management

### Within a Session

- Track decisions made during the session
- Reference earlier context rather than re-reading files
- If the conversation is long, proactively summarize key decisions

### Across Sessions

- **CONTEXT.md** captures project state (what is done, what is next)
- **CLAUDE.md** captures rules (how to behave)
- **Memory files** (~/.claude/memory/) persist cross-session learnings
- Do not rely on session memory for important decisions — write them down

### What to Capture

Capture information that would save time in a future session:
- Architecture decisions and their rationale
- Non-obvious patterns in the codebase
- Known limitations or workarounds
- Test strategies that worked (or failed)

Do not capture:
- Temporary debugging steps
- Conversation-specific context
- Information already in the codebase
