# Architecture Document Template

Every project should have an `ARCHITECTURE.md` that describes the system's structure. This is the first file an engineer reads to understand how things fit together.

---

## Template

Copy the template below into your project root as `ARCHITECTURE.md`.

```markdown
# Architecture

## Overview

1-2 paragraph description of what this system does, who uses it, and what problem it solves. Include the deployment model (single service, microservices, serverless, etc.).

**Key characteristics:**
- [e.g., Real-time data processing]
- [e.g., Multi-tenant SaaS]
- [e.g., Event-driven architecture]

## Components

```
┌─────────────────────────────────────────────────┐
│                    Clients                        │
│          (Web App, CLI, Mobile)                   │
└──────────────────┬──────────────────────────────┘
                   │ HTTPS
                   ▼
┌─────────────────────────────────────────────────┐
│              API Gateway / Load Balancer          │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Service  │ │ Service  │ │ Service  │
   │    A     │ │    B     │ │    C     │
   └────┬─────┘ └────┬─────┘ └────┬─────┘
        │             │            │
        ▼             ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │   DB A  │  │   DB B  │  │  Queue  │
   └─────────┘  └─────────┘  └─────────┘
```

### Component Descriptions

| Component | Responsibility | Tech Stack | Owner |
|---|---|---|---|
| Service A | User management, authentication | FastAPI, PostgreSQL | Team Alpha |
| Service B | Order processing, payments | FastAPI, PostgreSQL | Team Beta |
| Service C | Notification delivery | Worker, Redis | Team Alpha |
| Queue | Async job processing | Redis / RabbitMQ | Platform |

## Data Flow

Describe the primary data flows through the system. Use numbered steps for complex flows.

### Flow 1: User Places an Order

1. Client sends POST /api/orders to API Gateway
2. API Gateway routes to Service B
3. Service B validates the order and writes to DB B
4. Service B publishes `order.created` event to Queue
5. Service C consumes the event and sends confirmation email
6. Service A updates user's order history

### Flow 2: Data Pipeline (if applicable)

```
Source Systems → Bronze (raw) → Silver (cleaned) → Gold (aggregated) → BI Dashboard
```

## Key Decisions

Link to Architecture Decision Records for significant choices.

| Decision | ADR | Date |
|---|---|---|
| PostgreSQL as primary database | [ADR-001](docs/adr/ADR-001-postgresql-primary-database.md) | 2025-05-15 |
| FastAPI web framework | [ADR-002](docs/adr/ADR-002-fastapi-web-framework.md) | 2025-05-15 |
| Event-driven communication | [ADR-003](docs/adr/ADR-003-event-driven-architecture.md) | 2025-06-01 |

## Dependencies

### External Services

| Service | Purpose | SLA | Fallback |
|---|---|---|---|
| Stripe | Payment processing | 99.99% | Queue and retry |
| SendGrid | Email delivery | 99.95% | Fallback to SES |
| Auth0 | Authentication | 99.99% | Cached tokens |

### Internal Dependencies

| This Service | Depends On | Communication |
|---|---|---|
| Service B | Service A | REST API (sync) |
| Service C | Service B | Event queue (async) |
| Service A | Database A | Direct connection |

## Deployment

### Environments

| Environment | Purpose | URL | Infrastructure |
|---|---|---|---|
| Development | Local development | localhost:8000 | Docker Compose |
| Staging | Pre-production testing | staging.example.com | AWS ECS |
| Production | Live users | api.example.com | AWS ECS (Multi-AZ) |

### Infrastructure

```
AWS Region: eu-west-1
├── VPC
│   ├── Public Subnet
│   │   └── ALB (Application Load Balancer)
│   └── Private Subnet
│       ├── ECS Cluster (Fargate)
│       │   ├── Service A (2 tasks)
│       │   ├── Service B (3 tasks)
│       │   └── Service C (2 tasks)
│       ├── RDS PostgreSQL (Multi-AZ)
│       └── ElastiCache Redis
└── Route 53 (DNS)
```

## Security Considerations

- All traffic encrypted in transit (TLS 1.2+)
- Secrets stored in AWS Secrets Manager
- IAM roles follow least privilege
- Database access restricted to private subnet
- API authentication via JWT tokens
- Rate limiting: 100 req/min per client
- PII encrypted at rest

See [security-standards.md](link) for full security requirements.

## Monitoring and Observability

| Signal | Tool | Alert Threshold |
|---|---|---|
| Metrics | CloudWatch / Datadog | p99 latency > 1s |
| Logs | CloudWatch Logs / ELK | ERROR rate > 1% |
| Traces | X-Ray / Jaeger | Trace error rate > 0.5% |
| Uptime | Synthetic monitoring | < 99.9% over 5 min |
```

---

## Usage Notes

- Keep the architecture doc up to date — if the diagram doesn't match reality, it's worse than no diagram
- Use ASCII diagrams for version control friendliness (avoid images that can't be diffed)
- Link to ADRs for "why" questions — the architecture doc shows "what", ADRs explain "why"
- Review the architecture doc quarterly or when a major component changes
