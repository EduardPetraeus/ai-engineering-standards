# Docstring Format

Google-style docstrings for all Python code. Required for all public functions, classes, and modules.

---

## Format

```python
def function_name(param1: type, param2: type) -> return_type:
    """One-line summary of what the function does.

    Optional longer description if the one-liner isn't enough.
    Keep it concise — if you need more than 3-4 lines, the function
    might be doing too much.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter. If the description
            is long, indent continuation lines by 4 spaces.

    Returns:
        Description of the return value. For complex return types,
        describe the structure.

    Raises:
        ValueError: When param1 is negative.
        NotFoundError: When the requested resource doesn't exist.
    """
```

---

## Sections

| Section | Required | When to Include |
|---|---|---|
| One-line summary | Always | Every public function/class |
| Extended description | When needed | Complex logic, non-obvious behavior |
| Args | When function has parameters | Skip for no-arg functions |
| Returns | When function returns a value | Skip for None/void returns |
| Raises | When function raises exceptions | Only document intentional raises |

---

## Examples

### Simple Function

```python
def calculate_discount(price: float, rate: float) -> float:
    """Calculate the discount amount for a given price and rate.

    Args:
        price: Original price in the transaction currency.
        rate: Discount rate as a decimal (e.g., 0.15 for 15%).

    Returns:
        The discount amount, always non-negative.

    Raises:
        ValueError: When price is negative or rate is not between 0 and 1.
    """
    if price < 0:
        raise ValueError(f"Price must be non-negative, got {price}")
    if not 0 <= rate <= 1:
        raise ValueError(f"Rate must be between 0 and 1, got {rate}")
    return price * rate
```

### Function with Complex Return Type

```python
def parse_csv_file(file_path: str, delimiter: str = ",") -> list[dict[str, str]]:
    """Parse a CSV file into a list of dictionaries.

    Each row becomes a dictionary with column headers as keys.
    Empty files return an empty list. Headers are stripped of
    leading/trailing whitespace.

    Args:
        file_path: Absolute path to the CSV file.
        delimiter: Column separator character. Defaults to comma.

    Returns:
        A list of dictionaries where each dictionary represents one row.
        Keys are column headers, values are string cell contents.
        Example: [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]

    Raises:
        FileNotFoundError: When file_path does not exist.
        ValidationError: When the file has no header row.
    """
```

### Class

```python
class UserRepository:
    """Handles persistence operations for User entities.

    Provides CRUD operations backed by a SQL database. All methods
    are synchronous and use connection pooling internally.

    Args:
        connection_string: Database connection URL.
        pool_size: Maximum number of concurrent connections. Defaults to 5.

    Example:
        repo = UserRepository("postgresql://localhost:5432/app")
        user = repo.get_by_email("alice@example.com")
    """

    def __init__(self, connection_string: str, pool_size: int = 5) -> None:
        self._pool = create_pool(connection_string, pool_size)

    def get_by_email(self, email: str) -> User | None:
        """Fetch a user by their email address.

        Performs a case-insensitive lookup.

        Args:
            email: The email address to search for.

        Returns:
            The matching User object, or None if no user has this email.
        """
```

### Method with No Args or Return

```python
def close(self) -> None:
    """Release all database connections in the pool."""
```

### Generator Function

```python
def stream_records(file_path: str, batch_size: int = 1000) -> Iterator[list[dict]]:
    """Stream records from a large file in batches.

    Reads the file lazily to avoid loading the entire dataset into memory.
    Each yielded batch contains up to batch_size records.

    Args:
        file_path: Path to the data file.
        batch_size: Number of records per batch.

    Yields:
        Lists of record dictionaries, each list containing up to
        batch_size items.

    Raises:
        FileNotFoundError: When file_path does not exist.
    """
```

---

## When Docstrings Are Required

| Element | Docstring Required? |
|---|---|
| Public function | Yes |
| Public class | Yes |
| Public method | Yes |
| Module (top of file) | Yes, if module has non-obvious purpose |
| Private function (`_func`) | Recommended for complex ones |
| Private method (`_method`) | Recommended for complex ones |
| Dunder methods (`__init__`) | Yes, if init has parameters |
| Test functions | No (test name should be self-documenting) |
| Simple properties | No (if the name is self-explanatory) |

---

## Common Mistakes

```python
# WRONG: Restates the function name
def get_user(user_id: str) -> User:
    """Get a user."""  # Adds zero information

# CORRECT: Adds useful context
def get_user(user_id: str) -> User:
    """Fetch a user from the database by their unique ID.

    Args:
        user_id: The UUID of the user to retrieve.

    Returns:
        The User object with all profile fields populated.

    Raises:
        NotFoundError: When no user exists with this ID.
    """
```

```python
# WRONG: Documents implementation, not behavior
def calculate_tax(amount: float) -> float:
    """Multiplies amount by 0.25 and returns the result."""

# CORRECT: Documents behavior and meaning
def calculate_tax(amount: float) -> float:
    """Calculate Danish VAT (moms) for a given amount.

    Args:
        amount: The pre-tax amount in DKK.

    Returns:
        The VAT amount at the standard 25% rate.
    """
```

```python
# WRONG: Args descriptions are just the type repeated
def send_email(to: str, subject: str, body: str) -> bool:
    """Send an email.

    Args:
        to: A string.
        subject: A string.
        body: A string.
    """

# CORRECT: Args descriptions explain semantics
def send_email(to: str, subject: str, body: str) -> bool:
    """Send a transactional email via the configured SMTP provider.

    Args:
        to: Recipient email address. Must be a valid email format.
        subject: Email subject line. Max 200 characters.
        body: Email body in plain text. HTML is not supported.

    Returns:
        True if the email was accepted by the SMTP server.

    Raises:
        ValidationError: When the email address format is invalid.
        ExternalServiceError: When the SMTP server is unreachable.
    """
```
