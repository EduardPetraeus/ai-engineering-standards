# Exception Patterns

A consistent exception hierarchy and handling strategy. Every application should define its own exceptions that map to failure modes — not use generic `Exception` everywhere.

---

## Custom Exception Hierarchy

```
AppError (base — all application exceptions inherit from this)
├── ValidationError          — input doesn't meet requirements
├── NotFoundError            — requested resource doesn't exist
├── AuthorizationError       — user lacks permission
├── AuthenticationError      — identity cannot be verified
├── ConflictError            — resource state conflict (duplicate, version mismatch)
├── ExternalServiceError     — third-party API/service failed
│   ├── TimeoutError         — external call timed out
│   └── RateLimitError       — external rate limit hit
└── ConfigurationError       — missing or invalid configuration
```

### Implementation

```python
class AppError(Exception):
    """Base exception for all application errors.

    All custom exceptions inherit from this. Allows catching all
    application-level errors with a single except clause when needed.
    """

    def __init__(self, message: str, code: str | None = None, context: dict | None = None):
        self.message = message
        self.code = code or self.__class__.__name__
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.context:
            ctx = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"[{self.code}] {self.message} ({ctx})"
        return f"[{self.code}] {self.message}"


class ValidationError(AppError):
    """Input data failed validation rules."""

    def __init__(self, message: str, field: str | None = None, **kwargs):
        context = kwargs.pop("context", {})
        if field:
            context["field"] = field
        super().__init__(message, context=context, **kwargs)


class NotFoundError(AppError):
    """Requested resource does not exist."""

    def __init__(self, resource: str, identifier: str, **kwargs):
        context = {"resource": resource, "identifier": identifier}
        message = f"{resource} not found: {identifier}"
        super().__init__(message, context=context, **kwargs)


class AuthorizationError(AppError):
    """User does not have permission to perform this action."""

    pass


class AuthenticationError(AppError):
    """User identity could not be verified."""

    pass


class ConflictError(AppError):
    """Resource state conflict (e.g., duplicate entry, version mismatch)."""

    pass


class ExternalServiceError(AppError):
    """A third-party service or API call failed."""

    def __init__(self, service: str, message: str, status_code: int | None = None, **kwargs):
        context = kwargs.pop("context", {})
        context["service"] = service
        if status_code:
            context["status_code"] = status_code
        super().__init__(message, context=context, **kwargs)


class TimeoutError(ExternalServiceError):
    """External service call timed out."""

    pass


class RateLimitError(ExternalServiceError):
    """External service rate limit exceeded."""

    def __init__(self, service: str, retry_after: int | None = None, **kwargs):
        context = kwargs.pop("context", {})
        if retry_after:
            context["retry_after_seconds"] = retry_after
        super().__init__(service, "Rate limit exceeded", context=context, **kwargs)


class ConfigurationError(AppError):
    """Required configuration is missing or invalid."""

    pass
```

---

## Exception Handling Rules

### Rule 1: Never Catch Bare `Exception`

```python
# WRONG — catches everything including KeyboardInterrupt, SystemExit
try:
    process_data(data)
except Exception:
    pass

# CORRECT — catch specific exceptions
try:
    process_data(data)
except ValidationError as e:
    logger.warning("Invalid data", extra={"context": e.context})
    return ErrorResponse(status=400, message=str(e))
except ExternalServiceError as e:
    logger.error("Service failure", extra={"context": e.context}, exc_info=True)
    return ErrorResponse(status=502, message="Upstream service unavailable")
```

### Rule 2: Never Swallow Exceptions Silently

```python
# WRONG — exception disappears, bugs become invisible
try:
    send_notification(user_id, message)
except Exception:
    pass

# CORRECT — at minimum, log it
try:
    send_notification(user_id, message)
except ExternalServiceError as e:
    logger.error(
        "Failed to send notification",
        extra={"context": {"user_id": user_id, "error": str(e)}},
        exc_info=True,
    )
    # Notification failure is non-critical, continue without re-raising
```

### Rule 3: Always Log with Context

```python
# WRONG — useless error message
except Exception as e:
    logger.error("Something went wrong")

# CORRECT — include what, where, and relevant IDs
except PaymentError as e:
    logger.error(
        "Payment processing failed",
        extra={
            "context": {
                "order_id": order.id,
                "amount": order.total,
                "payment_method": order.payment_method_type,
                "error_code": e.code,
            }
        },
        exc_info=True,
    )
```

### Rule 4: Re-raise When You Cannot Handle

```python
# If you can't meaningfully recover, don't catch — or catch, log, and re-raise
def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise ConfigurationError(
            f"Configuration file not found: {path}",
            context={"path": path},
        )
    except yaml.YAMLError as e:
        raise ConfigurationError(
            f"Invalid YAML in configuration file: {path}",
            context={"path": path, "parse_error": str(e)},
        )
```

### Rule 5: Use Custom Exceptions, Not Built-in Ones

```python
# WRONG — generic exception gives no semantic meaning
if not user:
    raise ValueError("User not found")

# CORRECT — custom exception maps to a failure mode
if not user:
    raise NotFoundError("User", user_id)
```

### Rule 6: Handle at the Right Level

```python
# LOW LEVEL — translates infrastructure error to domain error
def get_user(user_id: str) -> User:
    try:
        row = db.query("SELECT * FROM users WHERE id = %s", user_id)
    except DatabaseError as e:
        raise ExternalServiceError("database", f"Query failed: {e}")

    if not row:
        raise NotFoundError("User", user_id)
    return User.from_row(row)

# HIGH LEVEL — maps domain errors to HTTP responses
@app.get("/users/{user_id}")
def get_user_endpoint(user_id: str):
    try:
        user = get_user(user_id)
        return user.to_response()
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    except ExternalServiceError:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
```

---

## Mapping Exceptions to HTTP Status Codes

| Exception | HTTP Status | Response |
|---|---|---|
| `ValidationError` | 400 Bad Request | Include field-level error details |
| `AuthenticationError` | 401 Unauthorized | Generic message (don't leak auth details) |
| `AuthorizationError` | 403 Forbidden | Generic message |
| `NotFoundError` | 404 Not Found | Resource type and ID |
| `ConflictError` | 409 Conflict | Describe the conflict |
| `RateLimitError` | 429 Too Many Requests | Include Retry-After header |
| `ExternalServiceError` | 502 Bad Gateway | Generic upstream error |
| `TimeoutError` | 504 Gateway Timeout | Generic timeout message |
| `AppError` (fallback) | 500 Internal Server Error | Generic error, log details server-side |

---

## Context Managers for Cleanup

Always use context managers or `try/finally` for resource cleanup:

```python
# CORRECT — context manager ensures cleanup
def process_file(path: str) -> list[dict]:
    with open(path) as f:
        return parse_csv(f)

# CORRECT — finally for non-context-manager resources
def process_with_connection() -> None:
    conn = get_connection()
    try:
        conn.execute(query)
        conn.commit()
    except DatabaseError:
        conn.rollback()
        raise
    finally:
        conn.close()
```

---

## Anti-Patterns

```python
# Anti-pattern 1: Catching and returning None
def get_user(user_id):
    try:
        return db.get(user_id)
    except Exception:
        return None  # Caller has no idea why it failed

# Anti-pattern 2: Exception as control flow
try:
    value = my_dict[key]
except KeyError:
    value = default  # Use my_dict.get(key, default) instead

# Anti-pattern 3: Logging and re-raising the same exception repeatedly
def layer_1():
    try:
        layer_2()
    except AppError as e:
        logger.error("Error in layer 1")  # Logged again!
        raise

# Anti-pattern 4: Catching too broadly at a low level
def parse_input(data):
    try:
        return json.loads(data)
    except Exception:  # Catches MemoryError, KeyboardInterrupt, etc.
        return {}
```
