# Coverage Requirements

Minimum test coverage targets by project layer. Coverage is a floor, not a ceiling — it tells you what is untested, not what is well-tested.

---

## Coverage Tiers

| Tier | Minimum Coverage | When to Apply |
|---|---|---|
| **Bronze** | 70% | Internal tools, scripts, prototypes |
| **Silver** | 80% | Production services, libraries |
| **Gold** | 90% | Critical paths, shared packages, public APIs |

---

## Coverage by Layer

| Layer | Minimum | Rationale |
|---|---|---|
| Business logic / domain | 80% | Core value of the application |
| Critical paths (auth, payments, data integrity) | 90% | Failures here = revenue loss or security breach |
| API endpoints | 85% | Contract surface between services |
| Utilities and helpers | 90% | Shared across the codebase, high reuse |
| Data pipelines | Schema + row count tests per table | Data quality is a separate concern |
| CLI commands | 75% | Test argument parsing + happy path |
| Configuration / infrastructure | No target | Validated via integration/E2E tests |
| Generated code | No target | Trust the generator |

---

## How to Measure

### Python: pytest-cov

```bash
# Run tests with coverage
pytest --cov=src --cov-report=term-missing --cov-report=html

# Fail CI if coverage drops below threshold
pytest --cov=src --cov-fail-under=80
```

### Configuration in pyproject.toml

```toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "tests/*",
    "scripts/*",
    "*/__pycache__/*",
    "*/migrations/*",
]

[tool.coverage.report]
show_missing = true
precision = 2
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if __name__ == .__main__.",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@overload",
]
```

### CI Integration (GitHub Actions)

```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=src --cov-report=xml --cov-fail-under=80

- name: Upload coverage report
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
```

---

## What Counts as Covered

### Covered (counts toward %)
- Lines executed during test runs
- Both branches of an if/else when `branch = true`
- Exception handling code that is triggered by tests
- Happy path AND error path

### Not Covered (excluded)
- Lines matching `exclude_lines` patterns
- Files in `omit` paths
- Type stubs and overloads
- `if TYPE_CHECKING:` blocks

### Does NOT Mean Well-Tested
- A line can be "covered" by a test that never asserts anything
- 100% coverage with no assertions = 0% useful coverage
- Use mutation testing to verify test quality, not just coverage quantity

---

## Branch Coverage

Always enable branch coverage (`branch = true`). Line coverage alone misses untested conditional branches.

```python
def get_status(score: int) -> str:
    if score >= 90:
        return "excellent"    # Branch 1
    return "needs improvement" # Branch 2

# This test gives 100% LINE coverage but only 50% BRANCH coverage:
def test_get_status_high_score():
    assert get_status(95) == "excellent"
    # Branch 2 is never tested!
```

---

## Ratchet Strategy

Never let coverage decrease. Use a ratchet approach:

1. Measure current coverage: `78.4%`
2. Set `fail_under = 78` in config
3. When coverage improves to `81.2%`, update to `fail_under = 81`
4. Never lower the threshold

This ensures coverage only moves in one direction over time.

---

## Exceptions

Some code is legitimately hard or pointless to test. Use `# pragma: no cover` sparingly and always with a comment explaining why:

```python
def main() -> None:  # pragma: no cover — entry point, tested via CLI integration tests
    app = create_app()
    app.run()
```

Track `pragma: no cover` usage. If a file has more than 3 pragmas, the code probably needs restructuring, not more pragmas.
