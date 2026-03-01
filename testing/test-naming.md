# Test Naming Convention

Consistent test names make failures self-documenting. A failing test name should tell you what broke without reading the test body.

---

## Pattern

```
test_{function_name}_{scenario}_{expected_result}
```

| Part | Description | Example |
|---|---|---|
| `test_` | Required pytest prefix | `test_` |
| `{function_name}` | The function or method being tested | `parse_csv` |
| `{scenario}` | The specific input or condition | `empty_file` |
| `{expected_result}` | What should happen | `returns_empty_list` |

---

## Examples

### Good Names

```python
# Function: parse_csv
def test_parse_csv_empty_file_returns_empty_list():
    ...

def test_parse_csv_single_row_returns_one_record():
    ...

def test_parse_csv_missing_header_raises_value_error():
    ...

def test_parse_csv_unicode_characters_preserves_encoding():
    ...

# Function: calculate_score
def test_calculate_score_all_correct_returns_100():
    ...

def test_calculate_score_negative_input_raises_value_error():
    ...

def test_calculate_score_empty_answers_returns_zero():
    ...

# Function: authenticate_user
def test_authenticate_user_valid_credentials_returns_token():
    ...

def test_authenticate_user_expired_password_raises_auth_error():
    ...

def test_authenticate_user_locked_account_raises_account_locked_error():
    ...

# Method: UserRepository.get_by_email
def test_get_by_email_existing_user_returns_user():
    ...

def test_get_by_email_unknown_email_returns_none():
    ...

def test_get_by_email_case_insensitive_matches_correctly():
    ...
```

### Bad Names

```python
# Too vague — what does "works" mean?
def test_parse_csv_works():
    ...

# No scenario — which case is this testing?
def test_calculate_score():
    ...

# Describes implementation, not behavior
def test_authenticate_calls_database_and_checks_hash():
    ...

# Test number instead of description
def test_parse_csv_1():
    ...

# Missing expected result
def test_calculate_score_negative_input():
    ...
```

---

## Class-Based Tests

When testing a class, use a test class to group related tests:

```python
class TestUserService:
    def test_create_user_valid_input_returns_user_id(self):
        ...

    def test_create_user_duplicate_email_raises_conflict_error(self):
        ...

    def test_delete_user_existing_user_returns_true(self):
        ...

    def test_delete_user_nonexistent_user_raises_not_found_error(self):
        ...
```

Class name pattern: `Test{ClassName}` — PascalCase, no underscores.

---

## Parametrized Tests

For tests with multiple inputs that share the same logic, use `pytest.mark.parametrize`. The test name should describe the general behavior:

```python
@pytest.mark.parametrize(
    "tier, expected_rate",
    [
        ("bronze", 0.05),
        ("silver", 0.10),
        ("gold", 0.15),
    ],
)
def test_get_discount_rate_returns_correct_rate_for_tier(tier, expected_rate):
    assert get_discount_rate(tier) == expected_rate
```

---

## Fixture Naming

Fixtures describe what they provide, not how they create it:

```python
# CORRECT — describes what it is
@pytest.fixture
def active_user():
    return User(name="Alice", email="alice@test.com", is_active=True)

@pytest.fixture
def empty_database(test_db):
    test_db.clear_all()
    return test_db

@pytest.fixture
def authenticated_client(test_client, active_user):
    test_client.login(active_user)
    return test_client
```

```python
# WRONG — describes implementation
@pytest.fixture
def setup_user():
    ...

@pytest.fixture
def db_fixture():
    ...
```

---

## File Naming

Test files mirror the source file they test:

| Source File | Test File |
|---|---|
| `src/data_loader.py` | `tests/test_data_loader.py` |
| `src/services/user_service.py` | `tests/services/test_user_service.py` |
| `src/utils/csv_parser.py` | `tests/utils/test_csv_parser.py` |

Pattern: `test_{source_filename}.py`

---

## Summary

| Element | Convention | Example |
|---|---|---|
| Test function | `test_{func}_{scenario}_{expected}` | `test_parse_csv_empty_file_returns_empty_list` |
| Test class | `Test{ClassName}` | `TestUserService` |
| Test file | `test_{source_file}.py` | `test_data_loader.py` |
| Fixture | Describes what it provides | `active_user`, `empty_database` |
| Parametrized | General behavior name | `test_get_rate_returns_correct_rate_for_tier` |
