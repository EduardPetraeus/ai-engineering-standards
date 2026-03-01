# Human Review Checklist

What humans should check that AI agents miss. These require judgment, context, and understanding of the bigger picture.

---

## Architecture Fit

- [ ] **Does this change belong here?** — Is this the right module/service/layer for this logic?
- [ ] **Separation of concerns** — Is business logic mixed with infrastructure? Is presentation leaking into the domain?
- [ ] **Dependency direction** — Do dependencies point inward (domain has no external deps)? Or is the domain importing from API/infra layers?
- [ ] **Abstraction level** — Is this the right level of abstraction? Too generic (over-engineered)? Too specific (will need rewriting soon)?
- [ ] **Consistency with existing patterns** — Does this follow the same patterns used elsewhere in the codebase, or does it introduce a new way of doing the same thing?

## Business Logic Correctness

- [ ] **Does it solve the actual problem?** — Not just "does the code work" but "does it do what the user/stakeholder needs?"
- [ ] **Edge cases in business context** — What happens on weekends? Across timezones? With currencies that have 3 decimal places? During a leap year?
- [ ] **Data semantics** — Is `created_at` a server timestamp or client timestamp? Is `amount` gross or net? Is `count` inclusive or exclusive?
- [ ] **Backward compatibility** — Will existing data, APIs, or integrations break?
- [ ] **Regulatory/compliance implications** — Does this change affect data retention, GDPR, financial reporting, or audit trails?

## Design and Maintainability

- [ ] **Would a new team member understand this?** — Could someone unfamiliar with the context read this code and understand the intent?
- [ ] **Is there a simpler way?** — Is the solution proportional to the problem? Could a 5-line change do what 50 lines are doing?
- [ ] **Future maintenance burden** — Will this be painful to change in 6 months? Does it create tight coupling that limits future options?
- [ ] **Magic numbers and hidden assumptions** — Are there implicit assumptions about data size, timing, ordering, or environment?
- [ ] **Error messages for operators** — When this fails at 3 AM, will the error message help someone fix it without reading the source?

## Performance at Scale

- [ ] **Volume assumptions** — Does this work with 10 rows AND 10 million rows? What happens at 100x current load?
- [ ] **Memory footprint** — Does this load entire datasets into memory? Could it stream instead?
- [ ] **Database impact** — Will new queries cause table scans? Are indexes needed? Will this lock tables under concurrent access?
- [ ] **Network calls** — Are external API calls in the hot path? What's the timeout and retry behavior?
- [ ] **Caching trade-offs** — Is caching appropriate here? What's the invalidation strategy? Is stale data acceptable?

## UX and User Impact

- [ ] **Error experience** — What does the user see when this fails? A helpful message or a stack trace?
- [ ] **Loading states** — If this is slow, does the UI show progress or does it look frozen?
- [ ] **Data loss risk** — Could the user lose work? Is there a confirmation step for destructive actions?
- [ ] **Accessibility** — Can this be used by people with different abilities, screen readers, keyboard-only navigation?
- [ ] **Localization** — Are there hardcoded strings that should be translatable? Date/number formats that are locale-specific?

## Team and Organizational Context

- [ ] **Conventions not captured in rules** — Does this follow the team's unwritten agreements? (e.g., "we always use factory functions here", "this module is being deprecated")
- [ ] **Ownership boundaries** — Does this change touch code owned by another team? Should they be notified?
- [ ] **Migration plan** — If this changes a shared interface, is there a plan for migrating existing consumers?
- [ ] **Feature flags** — Should this be behind a feature flag for safe rollout?
- [ ] **Documentation updates** — Do READMEs, wikis, runbooks, or API docs need updating?

## Security (Human Judgment Layer)

- [ ] **Authorization logic** — Are permission checks correct for all roles? Can a regular user access admin-only data?
- [ ] **Trust boundaries** — Is external input trusted when it shouldn't be? Are internal service-to-service calls authenticated?
- [ ] **Timing attacks** — Is there constant-time comparison for secrets? Can response timing leak information?
- [ ] **Race conditions** — Could concurrent requests cause inconsistent state? Is there proper locking?

## Data and Observability

- [ ] **Logging is useful** — Are log messages at the right level? Would they help debug a production incident?
- [ ] **Metrics and alerts** — Should this change have new metrics? Will existing alerts still be valid?
- [ ] **Audit trail** — For sensitive operations, is there a record of who did what and when?
- [ ] **Rollback plan** — If this deployment fails, can we roll back safely? Is the database migration reversible?

---

## When to Invest More Review Time

Spend more time reviewing when the change involves:

- **Money** — payment processing, billing, pricing logic
- **Access control** — authentication, authorization, permissions
- **Data pipelines** — transformations that affect downstream consumers
- **Shared libraries** — code used by multiple services
- **Infrastructure** — deployment, configuration, secrets management
- **Schema changes** — database migrations, API contracts

---

## Summary: Agent vs Human Review

| Agent Checks (Automated) | Human Checks (Judgment) |
|---|---|
| Syntax and formatting | Architecture fit |
| Naming conventions | Business logic correctness |
| Security patterns (regex) | Performance at scale |
| Test existence and coverage | UX implications |
| Import organization | Team conventions |
| Dead code detection | Organizational context |
| Type hint completeness | Authorization logic |
| Documentation presence | Rollback safety |
