# Approved Dependencies

A registry of vetted packages approved for use in projects. Before adding a new dependency, check this list. If the package is not listed, it needs a review.

---

## Approval Criteria

Before approving a new dependency:

1. **License compatible** — Must be MIT, BSD, Apache 2.0, or ISC (no GPL for library code)
2. **Actively maintained** — Commit in the last 6 months, issues triaged
3. **No known critical CVEs** — Check `pip-audit` or `safety` output
4. **Widely adopted** — Prefer packages with 1000+ GitHub stars or significant download counts
5. **Minimal transitive dependencies** — Fewer indirect deps = smaller attack surface

---

## Approved Packages

### Core / Runtime

| Package | Approved Version | License | Last Audit | Notes |
|---|---|---|---|---|
| pydantic | >=2.6.0,<3.0.0 | MIT | 2025-06-01 | Data validation and settings. Always use v2. |
| requests | >=2.31.0,<3.0.0 | Apache 2.0 | 2025-06-01 | HTTP client. Use httpx for async. |
| httpx | >=0.27.0,<1.0.0 | BSD-3 | 2025-06-01 | Async HTTP client. Preferred over aiohttp. |
| fastapi | >=0.109.0,<1.0.0 | MIT | 2025-06-01 | Web framework. Pair with uvicorn. |
| uvicorn | >=0.27.0,<1.0.0 | BSD-3 | 2025-06-01 | ASGI server for FastAPI. |
| sqlalchemy | >=2.0.0,<3.0.0 | MIT | 2025-06-01 | ORM and database toolkit. Always use v2 style. |
| alembic | >=1.13.0,<2.0.0 | MIT | 2025-06-01 | Database migrations for SQLAlchemy. |
| pyyaml | >=6.0.1,<7.0.0 | MIT | 2025-06-01 | YAML parsing. Always use safe_load(). |
| python-dotenv | >=1.0.0,<2.0.0 | BSD-3 | 2025-06-01 | Load .env files. Dev only where possible. |
| click | >=8.1.0,<9.0.0 | BSD-3 | 2025-06-01 | CLI framework. |
| rich | >=13.7.0,<14.0.0 | MIT | 2025-06-01 | Terminal formatting and progress bars. |
| tenacity | >=8.2.0,<9.0.0 | Apache 2.0 | 2025-06-01 | Retry library. Alternative to custom retry logic. |
| structlog | >=24.1.0,<25.0.0 | Apache 2.0 | 2025-06-01 | Structured logging. |

### Data Processing

| Package | Approved Version | License | Last Audit | Notes |
|---|---|---|---|---|
| pandas | >=2.2.0,<3.0.0 | BSD-3 | 2025-06-01 | Tabular data. Use polars for large datasets. |
| polars | >=0.20.0,<1.0.0 | MIT | 2025-06-01 | High-performance DataFrames. Preferred for new projects. |
| duckdb | >=0.10.0,<1.0.0 | MIT | 2025-06-01 | In-process SQL analytics. |
| pyarrow | >=15.0.0,<16.0.0 | Apache 2.0 | 2025-06-01 | Columnar data format. Required by pandas/polars. |
| dbt-core | >=1.7.0,<2.0.0 | Apache 2.0 | 2025-06-01 | Data transformation framework. |
| jinja2 | >=3.1.0,<4.0.0 | BSD-3 | 2025-06-01 | Template engine. Used by dbt internally. |

### Testing

| Package | Approved Version | License | Last Audit | Notes |
|---|---|---|---|---|
| pytest | >=8.0.0,<9.0.0 | MIT | 2025-06-01 | Test framework. Always use pytest, never unittest. |
| pytest-cov | >=4.1.0,<5.0.0 | MIT | 2025-06-01 | Coverage plugin for pytest. |
| pytest-asyncio | >=0.23.0,<1.0.0 | Apache 2.0 | 2025-06-01 | Async test support. |
| pytest-mock | >=3.12.0,<4.0.0 | MIT | 2025-06-01 | Mock/patch helpers. |
| hypothesis | >=6.98.0,<7.0.0 | MPL 2.0 | 2025-06-01 | Property-based testing. |
| responses | >=0.25.0,<1.0.0 | Apache 2.0 | 2025-06-01 | Mock HTTP responses for requests lib. |
| respx | >=0.20.0,<1.0.0 | BSD-3 | 2025-06-01 | Mock HTTP responses for httpx. |
| faker | >=22.0.0,<23.0.0 | MIT | 2025-06-01 | Generate realistic test data. |
| mutmut | >=2.4.0,<3.0.0 | ISC | 2025-06-01 | Mutation testing. |

### Development Tools

| Package | Approved Version | License | Last Audit | Notes |
|---|---|---|---|---|
| ruff | >=0.2.0,<1.0.0 | MIT | 2025-06-01 | Linter + formatter. Replaces flake8, isort, black. |
| mypy | >=1.8.0,<2.0.0 | MIT | 2025-06-01 | Static type checker. |
| pre-commit | >=3.6.0,<4.0.0 | MIT | 2025-06-01 | Git hook framework. |
| pip-audit | >=2.7.0,<3.0.0 | Apache 2.0 | 2025-06-01 | Vulnerability scanning for pip packages. |
| detect-secrets | >=1.4.0,<2.0.0 | Apache 2.0 | 2025-06-01 | Secret detection in code. |

### AI / LLM

| Package | Approved Version | License | Last Audit | Notes |
|---|---|---|---|---|
| anthropic | >=0.18.0,<1.0.0 | MIT | 2025-06-01 | Claude API client. |
| openai | >=1.12.0,<2.0.0 | Apache 2.0 | 2025-06-01 | OpenAI API client. |
| tiktoken | >=0.6.0,<1.0.0 | MIT | 2025-06-01 | Token counting for OpenAI models. |

---

## Packages Requiring Extra Scrutiny

These packages are approved but need careful usage:

| Package | Risk | Mitigation |
|---|---|---|
| `pyyaml` | Unsafe load can execute arbitrary code | Always use `yaml.safe_load()`, never `yaml.load()` |
| `jinja2` | Template injection if user input is templated | Never template user-provided strings |
| `requests` | SSRF if URL comes from user input | Validate and allowlist external URLs |
| `sqlalchemy` | SQL injection via `text()` with string concat | Always use parameterized queries |
| `subprocess` | Command injection | Never use `shell=True` with user input |

---

## Rejected Packages

| Package | Reason | Alternative |
|---|---|---|
| `flask` | Prefer FastAPI for new projects (async, type hints, OpenAPI) | `fastapi` |
| `unittest` | Verbose, less ergonomic than pytest | `pytest` |
| `flake8` | Replaced by ruff (faster, more rules) | `ruff` |
| `black` | Replaced by ruff format | `ruff` |
| `isort` | Replaced by ruff's I rules | `ruff` |
| `aiohttp` | Less ergonomic than httpx | `httpx` |
| `nose` | Unmaintained | `pytest` |

---

## Adding a New Dependency

1. Check this list first — is it already approved?
2. If not listed, open a PR with:
   - Package name, version, license
   - Why it's needed (what problem it solves)
   - Alternatives considered
   - `pip-audit` output showing no known vulnerabilities
3. Add to the appropriate table above after approval
4. Update `last_audit` date

## Audit Process

```bash
# Check for known vulnerabilities
pip-audit --requirement requirements.txt

# Check licenses
pip-licenses --format=table --with-urls

# Check for outdated packages
pip list --outdated
```
