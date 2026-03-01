# Logging Format

Structured JSON logging for all applications. Machine-parseable, searchable, and compatible with log aggregation tools (ELK, Datadog, CloudWatch).

---

## Required Fields

Every log entry must include:

| Field | Type | Description | Example |
|---|---|---|---|
| `timestamp` | ISO 8601 string | When the event occurred | `"2025-06-15T14:30:22.451Z"` |
| `level` | string | Log severity | `"INFO"` |
| `message` | string | Human-readable description | `"User login successful"` |
| `module` | string | Source module/file | `"auth.service"` |
| `function` | string | Source function name | `"authenticate_user"` |

## Optional Context Fields

| Field | Type | Description |
|---|---|---|
| `context` | object | Structured data relevant to the event |
| `request_id` | string | Correlation ID for request tracing |
| `user_id` | string | Who triggered the event (never log PII) |
| `duration_ms` | number | Operation duration in milliseconds |
| `error` | object | Error details (type, message, traceback) |
| `environment` | string | dev / staging / production |
| `service` | string | Service name in multi-service setups |

---

## Example Log Entries

### Successful Operation

```json
{
  "timestamp": "2025-06-15T14:30:22.451Z",
  "level": "INFO",
  "message": "Order processed successfully",
  "module": "orders.service",
  "function": "process_order",
  "context": {
    "order_id": "ord_abc123",
    "item_count": 3,
    "total_amount": 149.99
  },
  "request_id": "req_xyz789",
  "duration_ms": 234
}
```

### Error

```json
{
  "timestamp": "2025-06-15T14:30:25.102Z",
  "level": "ERROR",
  "message": "Failed to charge payment method",
  "module": "payments.gateway",
  "function": "charge_card",
  "context": {
    "order_id": "ord_abc456",
    "payment_method": "card_ending_4242",
    "attempt": 2
  },
  "error": {
    "type": "ExternalServiceError",
    "message": "Payment gateway returned 503",
    "traceback": "Traceback (most recent call last):\n  File ..."
  },
  "request_id": "req_xyz790",
  "duration_ms": 5023
}
```

### Warning

```json
{
  "timestamp": "2025-06-15T14:30:30.889Z",
  "level": "WARNING",
  "message": "Rate limit approaching threshold",
  "module": "api.middleware",
  "function": "check_rate_limit",
  "context": {
    "current_rate": 85,
    "limit": 100,
    "window_seconds": 60,
    "client_id": "client_abc"
  }
}
```

---

## Log Levels

| Level | When to Use | Examples |
|---|---|---|
| `DEBUG` | Development only. Detailed internal state. Never in production. | Variable values, SQL queries, cache hits/misses |
| `INFO` | Happy path events. Things that should happen. | Request completed, job started, user logged in |
| `WARNING` | Recoverable issues. Something unexpected but handled. | Rate limit approaching, deprecated API called, retry triggered |
| `ERROR` | Failures that need attention. Something broke for a user. | Payment failed, database query timeout, external API returned 500 |
| `CRITICAL` | System is down or data integrity is at risk. Page someone. | Database unreachable, disk full, data corruption detected |

### Level Selection Rules

1. If the system handled it without user impact → `WARNING`
2. If a user experienced a failure → `ERROR`
3. If multiple users are affected or data is at risk → `CRITICAL`
4. If everything worked as expected → `INFO`
5. If it's only useful during debugging → `DEBUG`

---

## Python Configuration

### Using logging.config.dictConfig

```python
import logging
import logging.config
import json
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Formats log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }

        # Add exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["error"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        # Add extra context fields
        if hasattr(record, "context"):
            log_entry["context"] = record.context

        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id

        if hasattr(record, "duration_ms"):
            log_entry["duration_ms"] = record.duration_ms

        return json.dumps(log_entry, default=str)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": JsonFormatter,
        },
        "simple": {
            "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "app.log",
            "maxBytes": 10_485_760,  # 10 MB
            "backupCount": 5,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "app": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "app.debug": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


# Initialize at application startup
logging.config.dictConfig(LOGGING_CONFIG)
```

### Usage in Application Code

```python
import logging

logger = logging.getLogger("app.orders")


def process_order(order_id: str) -> None:
    logger.info(
        "Processing order",
        extra={
            "context": {"order_id": order_id},
            "request_id": get_current_request_id(),
        },
    )

    try:
        result = execute_order(order_id)
        logger.info(
            "Order processed successfully",
            extra={
                "context": {"order_id": order_id, "total": result.total},
                "duration_ms": result.duration_ms,
            },
        )
    except PaymentError as e:
        logger.error(
            "Payment failed for order",
            extra={
                "context": {"order_id": order_id, "error_code": e.code},
            },
            exc_info=True,
        )
        raise
```

---

## Rules

1. **Never log PII** — no emails, names, addresses, phone numbers, SSNs in logs
2. **Never log secrets** — no API keys, passwords, tokens, connection strings
3. **Always include context** — bare "Error occurred" is useless. Include IDs, counts, durations
4. **Use structured fields** — don't embed data in the message string, put it in `context`
5. **Log at boundaries** — log when entering/exiting significant operations, not every internal step
6. **One event per log line** — don't log multi-line strings (except in tracebacks)
7. **Use correlation IDs** — `request_id` lets you trace a single request across all log entries
