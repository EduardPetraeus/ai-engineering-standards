# Testing Strategy

A decision tree for choosing the right test type. Every project should have a deliberate testing strategy — not just "write tests for everything."

---

## Decision Tree

```
Is the code you're testing...

├── Pure logic with no external dependencies?
│   └── UNIT TEST
│
├── Crossing a system boundary (DB, API, file system, queue)?
│   └── INTEGRATION TEST
│
├── A data pipeline or transformation?
│   └── DATA TEST (schema validation + row counts + value ranges)
│
├── A function where edge cases are hard to enumerate?
│   └── PROPERTY-BASED TEST (generate random inputs, assert invariants)
│
├── Already tested, but you want to verify test quality?
│   └── MUTATION TEST (inject bugs, verify tests catch them)
│
└── A user-facing workflow or multi-step process?
    └── END-TO-END TEST (simulate real usage)
```

---

## Test Types in Detail

### Unit Tests

**What:** Test a single function or class in isolation. No network, no database, no file system.

**When to use:**
- Business logic calculations
- Data transformations (parse, validate, format)
- Utility functions
- State machines

**Characteristics:**
- Fast (< 10ms per test)
- Deterministic (same input = same output, always)
- No setup/teardown of external resources
- Mock external dependencies

**Example:**
```python
def calculate_discount(price: float, tier: str) -> float:
    rates = {"bronze": 0.05, "silver": 0.10, "gold": 0.15}
    return price * rates.get(tier, 0.0)

def test_calculate_discount_gold_tier_returns_15_percent():
    result = calculate_discount(100.0, "gold")
    assert result == 15.0

def test_calculate_discount_unknown_tier_returns_zero():
    result = calculate_discount(100.0, "unknown")
    assert result == 0.0
```

### Integration Tests

**What:** Test that two or more components work together correctly across system boundaries.

**When to use:**
- Database queries return expected results
- API endpoints accept/return correct payloads
- File parsers handle real file formats
- Message queue producers/consumers connect properly

**Characteristics:**
- Slower (100ms–5s per test)
- May require Docker, test databases, or mock servers
- Test real I/O, not mocked I/O
- Run separately from unit tests (use markers)

**Example:**
```python
import pytest

@pytest.mark.integration
def test_user_repository_creates_and_retrieves_user(test_db):
    repo = UserRepository(test_db)
    repo.create(User(name="Alice", email="alice@example.com"))

    result = repo.get_by_email("alice@example.com")

    assert result is not None
    assert result.name == "Alice"
```

### Data Tests

**What:** Validate data pipeline outputs — schema correctness, row counts, value distributions, and freshness.

**When to use:**
- After ETL/ELT transformations
- On staging tables before promotion
- On dimension/fact tables in production
- Scheduled as part of pipeline runs

**Test categories:**
- **Schema tests:** Column exists, correct type, not null where expected
- **Row count tests:** Table is not empty, count within expected range
- **Value tests:** No negative amounts, dates within range, enums match expected values
- **Freshness tests:** Data updated within expected window
- **Uniqueness tests:** Primary keys are unique, no duplicate rows

**Example (dbt-style):**
```yaml
models:
  - name: fct_order
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: order_total
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
      - name: ordered_at
        tests:
          - not_null
          - dbt_utils.recency:
              datepart: day
              field: ordered_at
              interval: 1
```

### Property-Based Tests

**What:** Generate random inputs and assert that invariants always hold, instead of testing specific examples.

**When to use:**
- Serialization/deserialization roundtrips
- Mathematical operations (commutativity, associativity)
- Parsers (valid input always parses, invalid input never crashes)
- Encoding/decoding (encode then decode = original)

**Characteristics:**
- Discovers edge cases you would never write manually
- Uses libraries like Hypothesis (Python) or fast-check (JS)
- Slower than unit tests but finds more bugs per test

**Example:**
```python
from hypothesis import given, strategies as st

@given(st.floats(min_value=0, max_value=1_000_000, allow_nan=False))
def test_discount_never_exceeds_original_price(price):
    for tier in ["bronze", "silver", "gold"]:
        discount = calculate_discount(price, tier)
        assert 0 <= discount <= price
```

### Mutation Tests

**What:** Automatically modify your source code (mutants) and verify that your tests catch the changes. If a mutant survives (tests still pass), your tests have a gap.

**When to use:**
- After reaching coverage targets — to verify test quality, not just quantity
- On critical business logic
- Before declaring a module "well-tested"

**Tools:** mutmut (Python), Stryker (JS/TS), pitest (Java)

**Example run:**
```bash
mutmut run --paths-to-mutate=src/pricing.py --tests-dir=tests/
# Output: 23 mutants generated, 21 killed, 2 survived
# Investigate the 2 survivors — those are test gaps
```

### End-to-End Tests

**What:** Test the full user workflow from input to output, simulating real usage.

**When to use:**
- Critical user journeys (signup, checkout, data export)
- API contract validation
- CLI tool workflows

**Characteristics:**
- Slowest test type (seconds to minutes)
- Most brittle — breaks when UI or API changes
- Keep the count low: 5-15 E2E tests for most projects
- Run in CI, not on every commit

---

## Coverage Targets

| Layer | Target | Rationale |
|---|---|---|
| Application/business logic | 80% | Core value, must be reliable |
| Critical paths (payments, auth) | 90% | Failure = user impact or revenue loss |
| Utilities/helpers | 90% | Shared code, high reuse |
| API endpoints | 85% | Contract surface |
| Data pipelines | Schema + row count tests on every table | Data quality is non-negotiable |
| Infrastructure/config | No coverage target | Tested via integration/E2E |

---

## Test Pyramid

```
        ╱  E2E  ╲          Few (5-15)
       ╱----------╲
      ╱ Integration ╲      Some (20-50)
     ╱----------------╲
    ╱    Unit Tests     ╲   Many (100+)
   ╱--------------------╲
```

- **Unit tests** form the base: fast, cheap, many
- **Integration tests** in the middle: validate boundaries
- **E2E tests** at the top: few, expensive, high confidence

---

## When NOT to Test

- Generated code (protobuf stubs, ORM migrations)
- Simple configuration files
- One-off scripts that will be deleted
- Third-party library internals (trust their tests)
- Trivial getters/setters with no logic
