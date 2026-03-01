# Naming Conventions

Machine-readable naming rules for all code, files, and infrastructure. Each rule includes concrete examples so AI agents can pattern-match without ambiguity.

---

## Python

### Variables and Functions: `snake_case`

```python
# CORRECT
user_count = 42
total_revenue = 15000.50
is_active = True

def calculate_monthly_revenue(start_date, end_date):
    ...

def fetch_user_by_email(email_address):
    ...

def validate_input_schema(raw_data, expected_schema):
    ...
```

```python
# WRONG
userCount = 42          # camelCase
TotalRevenue = 15000    # PascalCase
isactive = True         # missing underscore

def CalculateRevenue():  # PascalCase
    ...

def fetchuser():         # missing underscore
    ...
```

### Classes: `PascalCase`

```python
# CORRECT
class DataPipeline:
    ...

class UserAuthenticationService:
    ...

class HttpResponseHandler:
    ...

class CsvFileParser:
    ...
```

```python
# WRONG
class data_pipeline:       # snake_case
class userAuthService:     # camelCase
class HTTPResponseHandler: # Acronym not title-cased (use Http)
```

### Constants: `UPPER_SNAKE_CASE`

```python
# CORRECT
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT_SECONDS = 30
DATABASE_URL = "postgresql://localhost:5432/app"
API_VERSION = "v2"
BATCH_SIZE = 1000
```

```python
# WRONG
maxRetryCount = 3       # camelCase
default_timeout = 30    # snake_case (looks like a variable)
Batch_Size = 1000       # Mixed case
```

### Private Members: Leading Underscore

```python
# CORRECT
class UserService:
    def __init__(self):
        self._connection_pool = None    # internal, not part of public API
        self._cache = {}

    def _validate_token(self, token):   # internal helper
        ...

    def get_user(self, user_id):        # public API
        ...
```

### Module Names: `snake_case`

```python
# CORRECT
import data_loader
import user_service
import csv_parser

# WRONG
import DataLoader
import user-service    # kebab-case is invalid Python
import csvparser       # missing underscore
```

---

## Files

### Documentation Files: `kebab-case.md`

```
# CORRECT
naming-conventions.md
testing-strategy.md
commit-message-format.md
sql-conventions.md
pr-template.md
```

```
# WRONG
naming_conventions.md   # snake_case
NamingConventions.md    # PascalCase
namingconventions.md    # no separator
```

### Python Files: `snake_case.py`

```
# CORRECT
data_loader.py
user_service.py
test_data_loader.py
csv_file_parser.py
```

```
# WRONG
data-loader.py          # kebab-case (invalid import)
DataLoader.py           # PascalCase
dataloader.py           # no separator
```

### Configuration Files: Standard Tool Names

```
# CORRECT — use the tool's expected filename
ruff.toml
pyproject.toml
.pre-commit-config.yaml
docker-compose.yml
Makefile
```

### Directory Names: `kebab-case`

```
# CORRECT
code-style/
error-handling/
test-fixtures/
data-models/

# WRONG
code_style/             # snake_case
codeStyle/              # camelCase
CodeStyle/              # PascalCase
```

---

## SQL

### Identifiers: `snake_case`

```sql
-- CORRECT
SELECT
    user_id,
    first_name,
    created_at,
    total_order_amount
FROM orders

-- WRONG
SELECT
    userId,             -- camelCase
    FirstName,          -- PascalCase
    CREATED_AT,         -- UPPER_CASE (reserved for keywords)
    totalorderamount    -- no separator
FROM orders
```

### Table Prefixes by Layer

| Prefix | Layer | Purpose | Example |
|---|---|---|---|
| `stg_` | Staging | Raw ingestion, minimal transformation | `stg_salesforce_contacts` |
| `int_` | Intermediate | Joins, business logic, not final | `int_orders_enriched` |
| `dim_` | Dimension | Descriptive entity tables | `dim_customer` |
| `fct_` | Fact | Event/transaction tables | `fct_order_line_item` |
| `vw_` | View | Computed views for consumers | `vw_monthly_revenue` |
| `rpt_` | Report | Aggregated for BI/dashboards | `rpt_weekly_sales_summary` |

```sql
-- CORRECT
CREATE TABLE stg_stripe_payments AS ...
CREATE TABLE dim_product AS ...
CREATE TABLE fct_page_views AS ...
CREATE VIEW vw_active_subscriptions AS ...

-- WRONG
CREATE TABLE stripe_payments AS ...       -- no layer prefix
CREATE TABLE DimProduct AS ...            -- PascalCase
CREATE TABLE fact_page_views AS ...       -- "fact_" not "fct_"
```

### Schema Names: `snake_case`

```sql
-- CORRECT
CREATE SCHEMA raw_data;
CREATE SCHEMA business_logic;
CREATE SCHEMA reporting;

-- WRONG
CREATE SCHEMA RawData;
CREATE SCHEMA business-logic;   -- kebab-case invalid in SQL
```

---

## YAML

### Keys: `kebab-case`

```yaml
# CORRECT
project-name: ai-engineering-standards
max-retry-count: 3
database-url: postgresql://localhost:5432/app
enable-caching: true
log-level: info

nested-config:
  connection-timeout: 30
  max-pool-size: 10
```

```yaml
# WRONG
projectName: ai-engineering-standards     # camelCase
max_retry_count: 3                        # snake_case
DATABASE_URL: postgresql://...            # UPPER_CASE
EnableCaching: true                       # PascalCase
```

### Exception: Tool-specific YAML

When a tool requires specific key formats (e.g., GitHub Actions, Docker Compose), follow the tool's convention:

```yaml
# GitHub Actions — uses kebab-case AND specific keywords
on:
  pull_request:           # GitHub's own convention
    branches: [main]
runs-on: ubuntu-latest    # kebab-case (GitHub convention)
```

---

## Git Branches

### Format: `{type}/{short-description}`

| Type | Purpose | Example |
|---|---|---|
| `feature/` | New functionality | `feature/user-authentication` |
| `fix/` | Bug fix | `fix/csv-parser-null-handling` |
| `docs/` | Documentation only | `docs/update-api-reference` |
| `refactor/` | Code improvement, no behavior change | `refactor/extract-validation-logic` |
| `test/` | Adding or updating tests | `test/add-integration-tests-payments` |
| `ci/` | CI/CD pipeline changes | `ci/add-ruff-linting-step` |
| `chore/` | Maintenance, deps, config | `chore/upgrade-pydantic-v2` |

```
# CORRECT
feature/add-retry-logic
fix/handle-empty-csv-input
docs/add-naming-conventions
refactor/simplify-auth-middleware
test/coverage-data-loader
ci/github-actions-cache
chore/pin-dependency-versions

# WRONG
add-retry-logic              # no type prefix
feature/Add_Retry_Logic      # mixed case, underscores
feature/add retry logic      # spaces
FEATURE/add-retry-logic      # uppercase type
bugfix/csv-parser            # use fix/, not bugfix/
```

### Branch Name Rules

- Use lowercase only
- Use hyphens to separate words in the description
- Keep descriptions short (2-5 words)
- Include ticket/issue number when available: `feature/123-user-auth`
- Never use special characters except hyphens and forward slash

---

## Summary Table

| Context | Convention | Example |
|---|---|---|
| Python variable | `snake_case` | `user_count` |
| Python function | `snake_case` | `calculate_total()` |
| Python class | `PascalCase` | `DataPipeline` |
| Python constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Python file | `snake_case.py` | `data_loader.py` |
| Doc file | `kebab-case.md` | `naming-conventions.md` |
| Directory | `kebab-case` | `error-handling/` |
| SQL identifier | `snake_case` | `order_amount` |
| SQL table | `prefix_snake_case` | `fct_order_line_item` |
| YAML key | `kebab-case` | `max-retry-count` |
| Git branch | `type/kebab-case` | `feature/add-auth` |
