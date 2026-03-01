# Git Workflow

Feature branch workflow with PR-based merging. Simple, linear, and compatible with both solo development and team collaboration.

---

## Core Rules

1. **Never commit directly to `main`**
2. **Always branch from the latest `main`**
3. **All changes go through pull requests**
4. **Delete branches after merge**

---

## Branch Lifecycle

```
main ──────────────────────────────────────────────────────────►
       │                           ▲
       │ git checkout -b           │ PR merge
       │ feature/add-retry-logic   │ (squash)
       ▼                           │
       ●───●───●───●───●──────────┘
       feature/add-retry-logic
```

### Step-by-step

```bash
# 1. Start from latest main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/add-retry-logic

# 3. Work in small commits
git add src/retry.py
git commit -m "feat(retry): add exponential backoff with jitter"

git add tests/test_retry.py
git commit -m "test(retry): add unit tests for backoff calculation"

# 4. Push and create PR
git push -u origin feature/add-retry-logic
gh pr create --title "feat: add retry logic with exponential backoff"

# 5. After PR is approved and merged, clean up
git checkout main
git pull origin main
git branch -d feature/add-retry-logic
```

---

## Branch Naming

See [naming-conventions.md](../naming/naming-conventions.md#git-branches) for full details.

Format: `{type}/{short-description}`

| Type | Purpose |
|---|---|
| `feature/` | New functionality |
| `fix/` | Bug fix |
| `docs/` | Documentation only |
| `refactor/` | Code improvement, no behavior change |
| `test/` | Adding or updating tests |
| `ci/` | CI/CD pipeline changes |
| `chore/` | Maintenance, deps, config |

---

## Merge Strategy

| Situation | Strategy | Why |
|---|---|---|
| Feature branch → main | **Squash merge** | Clean history, one commit per feature |
| Release branch → main | **Merge commit** | Preserve release history |
| Hotfix → main | **Squash merge** | Single atomic fix |

### Squash Merge (default)

Combines all branch commits into a single commit on main. Use for feature branches.

```bash
# Via GitHub UI: "Squash and merge"
# Via CLI:
gh pr merge --squash
```

The squash commit message should follow [Conventional Commits](commit-message-format.md):
```
feat(retry): add exponential backoff with jitter (#42)
```

### Merge Commit (releases)

Preserves the full branch history. Use for release branches.

```bash
gh pr merge --merge
```

---

## Working with PRs

### Before Creating a PR

```bash
# Ensure your branch is up to date with main
git fetch origin main
git rebase origin/main

# Run linters and tests locally
ruff check .
pytest

# Push
git push origin feature/your-branch
```

### PR Requirements

- Title follows Conventional Commits format
- Description explains what and why (use the [PR template](pr-template.md))
- All CI checks pass
- At least one review (if working with a team)
- No merge conflicts

### Reviewing a PR

```bash
# Check out the PR locally
gh pr checkout 42

# Run tests
pytest

# Leave review
gh pr review 42 --approve
# or
gh pr review 42 --request-changes --body "Issue with error handling in retry.py"
```

---

## Handling Conflicts

```bash
# Option 1: Rebase onto latest main (preferred — clean history)
git fetch origin main
git rebase origin/main
# Resolve conflicts, then:
git rebase --continue
git push --force-with-lease

# Option 2: Merge main into branch (when rebase is too complex)
git fetch origin main
git merge origin/main
# Resolve conflicts, then:
git push
```

Always use `--force-with-lease` instead of `--force` when pushing after a rebase. It prevents overwriting others' work.

---

## Commit Frequency

- Commit early, commit often on feature branches
- Each commit should compile/run (no broken intermediate states)
- Squash merge will clean up the history when merging to main

---

## Protected Branches

Configure `main` as a protected branch:

- Require pull request reviews before merging
- Require status checks to pass (linting, tests)
- Require branches to be up to date before merging
- Do not allow force pushes
- Do not allow deletions

---

## Stale Branches

- Branches older than 30 days without activity should be reviewed
- Delete merged branches immediately after merge
- Archive (tag then delete) long-running branches that are paused

```bash
# List merged branches that can be deleted
git branch --merged main | grep -v main

# Delete all merged branches
git branch --merged main | grep -v main | xargs git branch -d
```
