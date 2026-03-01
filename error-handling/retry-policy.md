# Retry Policy

Standard retry behavior for transient failures. Prevents cascading failures while giving temporary issues time to resolve.

---

## Default Configuration

| Parameter | Value | Rationale |
|---|---|---|
| Base delay | 1 second | Short enough to be responsive |
| Backoff factor | 2 | Exponential: 1s → 2s → 4s → 8s → ... |
| Max delay | 60 seconds | Cap to prevent absurdly long waits |
| Max retries | 3 | Total of 4 attempts (1 initial + 3 retries) |
| Jitter | ±25% random | Prevents thundering herd |

### Delay Sequence (with factor=2, max=60s)

| Attempt | Base Delay | With Jitter (±25%) |
|---|---|---|
| 1 (initial) | immediate | immediate |
| 2 (retry 1) | 1s | 0.75s–1.25s |
| 3 (retry 2) | 2s | 1.50s–2.50s |
| 4 (retry 3) | 4s | 3.00s–5.00s |

Total worst-case wait: ~8.75s before final failure.

---

## What to Retry

### Retry (Transient Errors)

| Error Type | Example | Why Retry |
|---|---|---|
| Timeout | Connection/read timeout | Network blip, server overloaded temporarily |
| HTTP 429 | Too Many Requests | Rate limit, will clear after backoff |
| HTTP 503 | Service Unavailable | Server restarting or temporarily overloaded |
| HTTP 502 | Bad Gateway | Upstream temporarily down |
| Connection refused | TCP connection failed | Service restarting |
| DNS resolution failure | Temporary DNS issue | DNS propagation, temporary outage |

### Never Retry (Permanent Errors)

| Error Type | Example | Why Not |
|---|---|---|
| HTTP 400 | Bad Request | Your input is wrong, fix it |
| HTTP 401 | Unauthorized | Credentials are invalid |
| HTTP 403 | Forbidden | No permission, retrying won't help |
| HTTP 404 | Not Found | Resource doesn't exist |
| HTTP 405 | Method Not Allowed | Wrong HTTP method |
| HTTP 409 | Conflict | State conflict, needs resolution |
| HTTP 422 | Unprocessable Entity | Validation failure |
| Any other 4xx | Client error | Problem is on our side |

### Special Case: HTTP 429

Always retry 429 responses, but **respect the `Retry-After` header** if present:

```python
if response.status_code == 429:
    retry_after = int(response.headers.get("Retry-After", default_delay))
    await asyncio.sleep(retry_after)
```

---

## Python Implementation

```python
import random
import time
import logging
from functools import wraps
from typing import TypeVar, Callable, Any

logger = logging.getLogger(__name__)

T = TypeVar("T")

TRANSIENT_STATUS_CODES = {429, 502, 503, 504}


class RetryExhaustedError(Exception):
    """All retry attempts have been exhausted."""

    def __init__(self, attempts: int, last_error: Exception):
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"Failed after {attempts} attempts: {last_error}")


def retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 60.0,
    jitter: float = 0.25,
    retryable_exceptions: tuple[type[Exception], ...] = (TimeoutError, ConnectionError),
) -> Callable:
    """Decorator that retries a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts.
        base_delay: Initial delay in seconds before first retry.
        backoff_factor: Multiplier applied to delay after each retry.
        max_delay: Maximum delay in seconds (cap).
        jitter: Random jitter factor (0.25 = ±25%).
        retryable_exceptions: Tuple of exception types that trigger a retry.

    Returns:
        Decorated function with retry behavior.

    Raises:
        RetryExhaustedError: When all retries are exhausted.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None

            for attempt in range(1, max_retries + 2):  # +2 for initial + retries
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt > max_retries:
                        break

                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (backoff_factor ** (attempt - 1)), max_delay)

                    # Add jitter
                    jitter_range = delay * jitter
                    delay = delay + random.uniform(-jitter_range, jitter_range)
                    delay = max(0, delay)

                    logger.warning(
                        "Retrying after transient error",
                        extra={
                            "context": {
                                "function": func.__name__,
                                "attempt": attempt,
                                "max_retries": max_retries,
                                "delay_seconds": round(delay, 2),
                                "error_type": type(e).__name__,
                                "error_message": str(e),
                            }
                        },
                    )

                    time.sleep(delay)

            raise RetryExhaustedError(max_retries + 1, last_exception)

        return wrapper

    return decorator
```

### Usage

```python
@retry(max_retries=3, retryable_exceptions=(TimeoutError, ConnectionError))
def fetch_user_data(user_id: str) -> dict:
    response = requests.get(
        f"https://api.example.com/users/{user_id}",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
```

---

## Circuit Breaker

When a service is consistently failing, stop retrying and fail fast. This prevents wasting resources on a dead service and gives it time to recover.

### Configuration

| Parameter | Value | Rationale |
|---|---|---|
| Failure threshold | 5 consecutive failures | Service is likely down, not just flaky |
| Recovery timeout | 60 seconds | Wait before trying again |
| Half-open requests | 1 | Test with a single request before fully opening |

### States

```
CLOSED ──(failure threshold reached)──► OPEN
  ▲                                       │
  │                                       │ (recovery timeout expires)
  │                                       ▼
  └────(success)──── HALF-OPEN ──(failure)──► OPEN
```

- **CLOSED:** Normal operation. Requests pass through. Failures are counted.
- **OPEN:** All requests fail immediately without calling the service. Timer starts.
- **HALF-OPEN:** After the recovery timeout, one request is allowed through. Success → CLOSED. Failure → OPEN.

### Implementation

```python
import time
import threading
from enum import Enum


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Circuit breaker that stops calling a failing service.

    Args:
        failure_threshold: Number of consecutive failures before opening.
        recovery_timeout: Seconds to wait before trying again.
    """

    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._lock = threading.Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            if self._state == CircuitState.OPEN and self._last_failure_time:
                if time.time() - self._last_failure_time >= self.recovery_timeout:
                    self._state = CircuitState.HALF_OPEN
            return self._state

    def record_success(self) -> None:
        with self._lock:
            self._failure_count = 0
            self._state = CircuitState.CLOSED

    def record_failure(self) -> None:
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            if self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                logger.error(
                    "Circuit breaker opened",
                    extra={
                        "context": {
                            "failure_count": self._failure_count,
                            "threshold": self.failure_threshold,
                        }
                    },
                )

    def allow_request(self) -> bool:
        current_state = self.state
        if current_state == CircuitState.CLOSED:
            return True
        if current_state == CircuitState.HALF_OPEN:
            return True
        return False


class CircuitOpenError(Exception):
    """Raised when the circuit breaker is open and requests are blocked."""

    pass
```

### Usage with Retry

```python
payment_circuit = CircuitBreaker(failure_threshold=5, recovery_timeout=60)


@retry(max_retries=3, retryable_exceptions=(TimeoutError, ConnectionError))
def charge_payment(order_id: str, amount: float) -> dict:
    if not payment_circuit.allow_request():
        raise CircuitOpenError("Payment service circuit breaker is open")

    try:
        result = payment_gateway.charge(order_id, amount)
        payment_circuit.record_success()
        return result
    except (TimeoutError, ConnectionError) as e:
        payment_circuit.record_failure()
        raise
```

---

## Decision Table

| Scenario | Retry? | Circuit Break? |
|---|---|---|
| Single timeout | Yes | No (count failure) |
| HTTP 429 with Retry-After | Yes (use header) | No |
| HTTP 503 | Yes | No (count failure) |
| 5 consecutive timeouts | No (circuit open) | Yes |
| HTTP 400 | No | No (don't count) |
| HTTP 401 | No | No (don't count) |
| Network unreachable | Yes | No (count failure) |
| DNS failure | Yes | No (count failure) |
| SSL certificate error | No | No (configuration issue) |
