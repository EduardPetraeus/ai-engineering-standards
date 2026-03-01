# Philosophy: Why Standards Matter for AI Agents

This document explains the design principles behind these engineering standards and why they are structured the way they are.

---

## The Core Problem

AI coding agents parse rules literally. When a human reads "use consistent naming," they interpret it based on experience, context, and team norms. When an AI agent reads it, it gets:

- **No concrete pattern** — what does "consistent" mean?
- **No examples** — what does correct look like?
- **No exceptions** — are there cases where the rule doesn't apply?

The result: inconsistent code. Different agents (or the same agent on different days) will make different choices. Every ambiguous guideline becomes a coin flip.

---

## Design Principles

### 1. Machine-Readable Over Prose

Prose describes intent. Configurations enforce it. Always provide both.

```
BAD:  "Use a modern Python linting tool with reasonable defaults"
GOOD: ruff.toml with explicit rule selection and per-file-ignores
```

A linter config is unambiguous. A paragraph about "reasonable defaults" is a prompt for improvisation.

### 2. Examples Over Descriptions

Every rule must include concrete examples of correct AND incorrect usage. Examples are the ground truth that both humans and AI agents can pattern-match against.

```
BAD:  "Functions should use snake_case"
GOOD: "Functions should use snake_case"
      CORRECT: calculate_monthly_revenue()
      CORRECT: fetch_user_by_email()
      WRONG:   CalculateRevenue()
      WRONG:   fetchuser()
```

Three correct examples and two incorrect examples eliminate most ambiguity. A rule without examples is a suggestion.

### 3. Constraints Over Guidelines

A constraint says "never do X" or "always do Y." A guideline says "prefer X over Y when possible." AI agents handle constraints well and handle guidelines poorly.

```
BAD (guideline):  "Prefer CTEs over subqueries when it improves readability"
GOOD (constraint): "Use CTEs. Do not use subqueries. Exception: correlated subqueries in WHERE clauses."
```

Guidelines require judgment. Constraints require compliance. AI agents are good at compliance.

### 4. Explicit Exceptions Over Implicit Flexibility

When a rule has exceptions, list them. If the exception list is empty, the rule is absolute.

```
BAD:  "No SELECT * (but it's fine sometimes)"
GOOD: "No SELECT * in production code. Exceptions:
       1. Inside a CTE that feeds into an explicit column list
       2. In ad-hoc exploratory queries (never committed)"
```

### 5. Composable Over Monolithic

Standards are organized as independent modules:
- `naming/` — naming rules only
- `code-style/python/` — Python linter configs only
- `testing/` — testing strategy only
- `git/` — git workflow only

A project can adopt `naming/` + `testing/` without touching `security/`. Each module is self-contained. No module requires another module to function.

### 6. Defaults With Override Mechanisms

Every standard has a sensible default. Projects can override specific values without forking the entire standard.

```markdown
## engineering_standards
- Source: ~/Github repos/ai-engineering-standards
- Active sections: naming, code-style/python, testing, git
- Override: line-length = 120 (default is 100)
```

The override is explicit and visible. The agent knows which standard applies and where the project diverges.

---

## Why Not Just Use a Linter?

Linters enforce syntax rules. Standards cover:

| Concern | Linter Can Enforce | Standards Cover |
|---|---|---|
| Line length | Yes | Yes |
| Import order | Yes | Yes |
| Naming conventions | Partially | Yes, with full examples |
| Git workflow | No | Yes |
| Commit messages | No | Yes |
| Test strategy | No | Yes |
| Error handling patterns | No | Yes |
| Security practices | Partially | Yes |
| Architecture decisions | No | Yes |
| Documentation format | No | Yes |

Linters are a subset. Standards are the superset. Use both.

---

## How AI Agents Consume These Standards

### In CLAUDE.md

```markdown
## engineering_standards
- Source: ~/Github repos/ai-engineering-standards
- Active: naming, code-style/python, testing, git, error-handling
```

The agent reads the referenced files at session start and applies them throughout the session.

### In Code Review

The agent uses the [agent review checklist](../review/agent-review-checklist.md) as a structured verification pass. Each check is binary (pass/fail), not subjective.

### In Code Generation

When generating new code, the agent uses:
1. **Naming conventions** — to name files, functions, classes, variables
2. **Code style configs** — to format and lint the output
3. **Docstring format** — to document public interfaces
4. **Error handling patterns** — to structure try/except blocks
5. **Test naming** — to generate properly named test functions

---

## The Hierarchy

```
ai-governance-framework          # WHO can do what (roles, guardrails)
    ↓
ai-engineering-standards         # HOW to do it (conventions, patterns)
    ↓
Project CLAUDE.md                # WHAT to do (project-specific rules + overrides)
```

Governance defines the boundaries. Standards define the craft. The project defines the context.

---

## Guiding Maxim

> If an AI agent would need to ask a clarifying question to follow the rule, the rule is not specific enough.

Every standard in this repo should pass this test. If it doesn't, it needs more examples, more constraints, or more explicit exceptions.
