# Agent Review Checklist

What AI code review agents should check automatically. These are objective, rule-based checks that don't require human judgment.

---

## Syntax and Formatting

- [ ] **No syntax errors** — code parses without errors
- [ ] **Linter passes** — ruff/flake8 reports zero violations
- [ ] **Formatter applied** — black/ruff format shows no changes needed
- [ ] **Import order** — isort-compliant (stdlib → third-party → local)
- [ ] **Line length** — within configured limit (100 chars default)
- [ ] **Trailing whitespace** — none
- [ ] **File ends with newline** — yes

## Naming Conventions

- [ ] **Variables and functions** — `snake_case`
- [ ] **Classes** — `PascalCase`
- [ ] **Constants** — `UPPER_SNAKE_CASE`
- [ ] **Files** — `snake_case.py` for Python, `kebab-case.md` for docs
- [ ] **Test functions** — follow `test_{function}_{scenario}_{expected}` pattern
- [ ] **No single-letter variables** — except `i`, `j`, `k` in loops, `e` in except, `f` in file handling
- [ ] **No abbreviations** — use `customer` not `cust`, `transaction` not `txn` (unless domain-standard)

## Security

- [ ] **No hardcoded secrets** — no API keys, passwords, tokens, or connection strings in code
- [ ] **No .env files committed** — `.env` is in `.gitignore`
- [ ] **No private keys** — no `-----BEGIN.*PRIVATE KEY-----` patterns
- [ ] **Parameterized queries** — no string concatenation or f-strings in SQL queries
- [ ] **No `eval()` or `exec()`** — unless explicitly justified with a comment
- [ ] **Input validation** — user input is validated before use
- [ ] **No sensitive data in logs** — no PII, passwords, or tokens in log messages
- [ ] **Dependencies pinned** — no unpinned versions in requirements files

### Secret Patterns to Scan

```regex
# AWS keys
AKIA[0-9A-Z]{16}
# Generic API key assignments
(?i)(api[_-]?key|api[_-]?secret|access[_-]?token)\s*[=:]\s*["'][^"']{8,}["']
# Private keys
-----BEGIN\s+(RSA|DSA|EC|OPENSSH)\s+PRIVATE\s+KEY-----
# Connection strings
(?i)(postgresql|mysql|mongodb|redis):\/\/[^:]+:[^@]+@
# JWT tokens
eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}
```

## Test Coverage

- [ ] **New code has tests** — every new function/class has at least one test
- [ ] **Test files exist** — `test_{module}.py` exists for every `{module}.py`
- [ ] **Coverage not decreased** — PR does not lower overall coverage percentage
- [ ] **Edge cases tested** — empty input, null/None, boundary values
- [ ] **Error paths tested** — exceptions are raised and caught correctly

## Import Organization

- [ ] **No unused imports** — every import is referenced in the file
- [ ] **No circular imports** — modules don't import each other
- [ ] **No wildcard imports** — no `from module import *`
- [ ] **Standard grouping** — stdlib, then third-party, then local (blank line between groups)

```python
# CORRECT
import os
import sys
from pathlib import Path

import requests
from pydantic import BaseModel

from src.models import User
from src.utils import validate_email
```

## Dead Code

- [ ] **No commented-out code** — delete it, git has history
- [ ] **No unreachable code** — nothing after unconditional return/raise
- [ ] **No unused variables** — every assigned variable is read
- [ ] **No unused functions** — every defined function is called (or exported)
- [ ] **No TODO/FIXME without issue reference** — `TODO(#123)` is OK, bare `TODO` is not

## Documentation

- [ ] **Public functions have docstrings** — Google-style format
- [ ] **Docstrings match implementation** — Args/Returns/Raises are accurate
- [ ] **No outdated comments** — comments match the current code behavior
- [ ] **Complex logic explained** — non-obvious algorithms have comments

## Error Handling

- [ ] **No bare `except:`** — always catch specific exceptions
- [ ] **No silent swallowing** — no empty `except` blocks without logging
- [ ] **Custom exceptions used** — not raising generic `Exception`
- [ ] **Error messages are descriptive** — include context (what failed, what was expected)
- [ ] **Resources cleaned up** — files, connections, etc. use context managers or finally blocks

## Type Hints

- [ ] **Public functions have type hints** — parameters and return type annotated
- [ ] **No `Any` without justification** — `Any` type should have a comment explaining why
- [ ] **mypy passes** — zero type errors in strict mode

## Performance (Basic)

- [ ] **No N+1 queries** — database queries inside loops
- [ ] **No unbounded collections** — lists/dicts that grow without limit
- [ ] **No synchronous I/O in async context** — blocking calls in async functions
- [ ] **No unnecessary copies** — deep copying large objects without reason

---

## Agent Review Output Format

When an AI agent runs this checklist, it should produce structured output:

```json
{
  "status": "pass | fail | warning",
  "checks": [
    {
      "category": "security",
      "check": "no_hardcoded_secrets",
      "status": "pass",
      "details": null
    },
    {
      "category": "naming",
      "check": "snake_case_functions",
      "status": "fail",
      "details": "Function 'CalculateTotal' in src/billing.py:42 should be 'calculate_total'"
    }
  ],
  "summary": {
    "total": 30,
    "passed": 28,
    "failed": 1,
    "warnings": 1
  }
}
```
