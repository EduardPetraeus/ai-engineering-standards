# Security Standards

Security rules for all applications. These are non-negotiable baselines — not aspirational goals.

---

## Core Rules

### 1. No Hardcoded Secrets

Never put secrets in source code. Not in variables, not in comments, not in "temporary" debug code.

```python
# WRONG — secrets in code
API_KEY = "sk-live-abc123def456"
DATABASE_URL = "postgresql://admin:password123@prod-db:5432/app"

# CORRECT — secrets from environment
import os
API_KEY = os.environ["API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]

# CORRECT — secrets from a secret manager
from app.config import get_secret
API_KEY = get_secret("api-key")
```

**Where secrets belong:**
- Environment variables (`.env` file locally, secrets manager in prod)
- Cloud secret managers (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- CI/CD secret stores (GitHub Secrets, GitLab CI Variables)

**Where secrets never belong:**
- Source code files
- Configuration files committed to git
- Log messages
- Error messages returned to clients
- Comments

### 2. Pinned Dependencies

Always pin exact versions. Unpinned dependencies can introduce breaking changes or vulnerabilities silently.

```
# WRONG — unpinned
requests
pydantic>=2.0
fastapi

# CORRECT — pinned
requests==2.31.0
pydantic==2.6.1
fastapi==0.109.2
```

For libraries (published packages), use compatible ranges in `pyproject.toml`:
```toml
[project]
dependencies = [
    "requests>=2.31.0,<3.0.0",
    "pydantic>=2.6.0,<3.0.0",
]
```

For applications (deployed services), use exact pins in `requirements.txt`.

### 3. Input Validation at Boundaries

Validate all external input at the point of entry. Never trust data from users, APIs, files, or databases.

```python
from pydantic import BaseModel, Field, EmailStr


class CreateUserRequest(BaseModel):
    """Validates user creation input at the API boundary."""

    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    age: int = Field(ge=0, le=150)
```

Validate at:
- API endpoints (request bodies, query params, headers)
- File uploads (type, size, content)
- Database reads (schemas can drift)
- External API responses (don't trust third parties)
- Environment variables at startup (fail fast if invalid)

### 4. Parameterized Queries

Never build SQL queries with string concatenation or f-strings. Always use parameterized queries.

```python
# WRONG — SQL injection vulnerability
query = f"SELECT * FROM users WHERE email = '{email}'"
cursor.execute(query)

# WRONG — still injectable
query = "SELECT * FROM users WHERE email = '%s'" % email
cursor.execute(query)

# CORRECT — parameterized query
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))

# CORRECT — ORM with parameter binding
user = session.query(User).filter(User.email == email).first()
```

### 5. Least Privilege

Every component should have the minimum permissions needed to do its job.

- Database users: read-only unless writes are needed
- API keys: scoped to specific operations
- File system: read-only unless writes are needed
- Network: only allow necessary outbound connections
- IAM roles: no wildcards (`*`) in production

### 6. No PII in Logs

Never log personally identifiable information. Log IDs and references instead.

```python
# WRONG — PII in logs
logger.info(f"User registered: {user.email}, name: {user.name}")

# CORRECT — log IDs, not PII
logger.info("User registered", extra={"context": {"user_id": user.id}})
```

PII includes: names, emails, phone numbers, addresses, IP addresses, SSN/CPR numbers, credit card numbers, dates of birth.

### 7. HTTPS Only

All network communication must use TLS encryption.

- No HTTP endpoints in production (redirect to HTTPS)
- Verify TLS certificates on outbound requests (never `verify=False` in production)
- Use TLS 1.2 or higher
- HSTS headers on all responses

```python
# WRONG — disabled TLS verification
response = requests.get(url, verify=False)

# CORRECT
response = requests.get(url)  # verify=True is the default
```

### 8. CORS Restricted

Cross-Origin Resource Sharing must be explicitly configured with specific origins.

```python
# WRONG — allows everything
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# CORRECT — specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com", "https://admin.example.com"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
)
```

---

## OWASP Top 10 Mapping

How these standards map to the [OWASP Top 10 (2021)](https://owasp.org/Top10/):

| OWASP Category | Our Standard | Implementation |
|---|---|---|
| A01: Broken Access Control | Least Privilege | Role-based access, endpoint authorization |
| A02: Cryptographic Failures | HTTPS Only, No Hardcoded Secrets | TLS everywhere, secrets in vault |
| A03: Injection | Parameterized Queries, Input Validation | No string concat in SQL, Pydantic validation |
| A04: Insecure Design | Input Validation at Boundaries | Validate all external input, fail closed |
| A05: Security Misconfiguration | CORS Restricted, Pinned Dependencies | Explicit CORS, locked versions |
| A06: Vulnerable Components | Pinned Dependencies, Approved Dependencies | Version pinning, regular audit |
| A07: Authentication Failures | No Hardcoded Secrets | Secrets in vault, rotate regularly |
| A08: Data Integrity Failures | Pinned Dependencies | Verify package integrity, lockfiles |
| A09: Logging Failures | No PII in Logs, Structured Logging | JSON logging with context, no PII |
| A10: SSRF | Input Validation | Validate URLs, allowlist external hosts |

---

## Dependency Audit Schedule

| Frequency | Action |
|---|---|
| Every PR | Dependabot/Renovate checks for known vulnerabilities |
| Weekly | Automated dependency update PRs |
| Monthly | Manual review of dependency audit report |
| Quarterly | Full security review of all dependencies |

---

## Secret Rotation

| Secret Type | Rotation Frequency | Method |
|---|---|---|
| API keys | Every 90 days | Automated via secret manager |
| Database passwords | Every 90 days | Automated rotation |
| JWT signing keys | Every 30 days | Key versioning with overlap |
| Service account tokens | Every 180 days | CI/CD pipeline update |
| TLS certificates | Before expiry (auto-renew) | Let's Encrypt or cloud provider |

---

## Security Headers

Every HTTP response should include:

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

---

## Checklist for Every PR

- [ ] No hardcoded secrets (scan with detect-secrets)
- [ ] Input validated at entry points
- [ ] SQL uses parameterized queries
- [ ] No PII in log messages
- [ ] Dependencies pinned to exact versions
- [ ] TLS verification not disabled
- [ ] CORS configured with specific origins
- [ ] Error messages don't leak internal details to clients
