# ADR Template

Architecture Decision Records capture significant design decisions. Use this template for any decision that affects the system's structure, technology choices, or development practices.

---

## Template

Copy the template below into a new file: `docs/adr/ADR-NNN-short-title.md`

```markdown
# ADR-NNN: Title of Decision

## Status

**Proposed** | Accepted | Deprecated | Superseded by [ADR-NNN](link)

## Date

YYYY-MM-DD

## Context

What is the issue that we're seeing that is motivating this decision or change?

Describe the forces at play:
- Technical constraints
- Business requirements
- Team capabilities
- Timeline pressure
- Quality attributes (performance, security, maintainability)

Be specific. Include numbers where possible (e.g., "current response time is 2.3s, target is <500ms").

## Decision

What is the change that we're proposing and/or doing?

State the decision clearly in 1-2 sentences, then elaborate on the details:
- What will we build/adopt/change?
- How will it work at a high level?
- What are the key design choices within this decision?

## Consequences

What becomes easier or more difficult to do because of this change?

### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Trade-off 2

### Neutral
- Side effect that is neither positive nor negative

## Alternatives Considered

### Alternative 1: Name
- **Description:** Brief description
- **Pros:** What's good about it
- **Cons:** Why we didn't choose it

### Alternative 2: Name
- **Description:** Brief description
- **Pros:** What's good about it
- **Cons:** Why we didn't choose it
```

---

## Example

```markdown
# ADR-001: Use PostgreSQL as Primary Database

## Status

Accepted

## Date

2025-05-15

## Context

We need a primary database for the user management service. Requirements:
- ACID transactions for user data integrity
- JSON support for flexible metadata storage
- Full-text search for user directory
- Expected scale: 500K users, 50 req/s reads, 5 req/s writes
- Team has experience with PostgreSQL and MySQL

## Decision

Use PostgreSQL 16 as the primary database, hosted on AWS RDS.

Key choices:
- RDS Multi-AZ for high availability
- db.r6g.large instance (2 vCPU, 16GB RAM) initially
- JSONB columns for user metadata (not a separate document store)
- pg_trgm extension for fuzzy text search

## Consequences

### Positive
- JSONB gives us schema flexibility without a separate NoSQL database
- Team already knows PostgreSQL — no learning curve
- RDS handles backups, patching, and failover
- Full-text search avoids needing Elasticsearch for basic search

### Negative
- RDS costs more than self-managed (~$200/month for Multi-AZ)
- Vendor lock-in to AWS for managed database features
- JSONB queries are slower than dedicated document stores for deep nesting

### Neutral
- Need to manage database migrations with Alembic
- Connection pooling required (PgBouncer or SQLAlchemy pool)

## Alternatives Considered

### Alternative 1: MySQL 8 on RDS
- **Description:** MySQL with JSON support on AWS RDS
- **Pros:** Simpler replication, slightly lower cost
- **Cons:** JSON support less mature than PostgreSQL's JSONB, no native full-text search trigrams

### Alternative 2: MongoDB Atlas
- **Description:** Document database for flexible schema
- **Pros:** Native JSON, horizontal scaling, flexible schema
- **Cons:** No ACID transactions across collections, team has no MongoDB experience, separate service to manage

### Alternative 3: DynamoDB
- **Description:** AWS serverless NoSQL
- **Pros:** Zero management, pay-per-request, infinite scale
- **Cons:** Complex query patterns, no JOIN support, team unfamiliar, difficult to run locally
```

---

## When to Write an ADR

Write an ADR when:
- Choosing a database, framework, or major library
- Designing a new service or component boundary
- Changing deployment architecture
- Adopting a new practice or workflow
- Making a trade-off that future team members will question

Don't write an ADR for:
- Choosing between two equivalent libraries (just pick one)
- Standard patterns already documented in engineering standards
- Bug fixes or minor refactoring

---

## ADR Lifecycle

1. **Proposed** — Written and open for discussion
2. **Accepted** — Team agrees, implementation begins
3. **Deprecated** — No longer applicable (technology retired)
4. **Superseded** — Replaced by a newer ADR (link to it)

Never delete ADRs. They are a historical record. Mark them as Deprecated or Superseded instead.

---

## File Organization

```
docs/
└── adr/
    ├── ADR-001-postgresql-primary-database.md
    ├── ADR-002-fastapi-web-framework.md
    ├── ADR-003-medallion-data-architecture.md
    └── ADR-004-github-actions-ci-cd.md
```

Number sequentially. Never reuse numbers.
