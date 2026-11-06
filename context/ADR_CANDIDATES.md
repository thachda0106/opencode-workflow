# Architecture Decision Record Candidates — Platform Core

**Status:** Candidate list — must be written before implementation begins.
**ADR Format:** Title → Status → Context → Decision → Consequences → Alternatives Considered

---

## Mandatory ADRs (Must Be Written Before Package Design)

### ADR-001: Package Boundary Strategy
**Context:** The platform could be one monolithic `core/` package or split into focused packages.
**Decision to Make:** How many packages? What are the boundaries?
**Key Trade-Off:** Fewer packages = simpler dependency management but higher coupling. More packages = looser coupling but more version management overhead.
**Proposed:** 5 packages (foundation, core, messaging, persistence, distributed)

### ADR-002: Zero-Dependency Foundation Package
**Context:** `@platform/foundation` must have zero external dependencies.
**Decision to Make:** Are `uuid`, `zod`, or `luxon` allowed if wrapped behind interfaces?
**Key Trade-Off:** Zero dependencies ensures no transitive dependency conflicts, but forces re-implementation of basic utilities (GUID generation, date handling).
**Proposed:** Foundation may import `node:*` built-ins only. Wrap `crypto.randomUUID()` for IDs. No wrapper abstractions for basic utilities — use plain functions.

### ADR-003: Validation Library Standardization
**Context:** The validation module must choose between wrapper abstraction or canonical library.
**Decision to Make:** Abstract validation behind an interface (supports Zod, class-validator, Joi) OR standardize on one library (Zod)?
**Key Trade-Off:** Abstraction = flexibility but leaky indirection. Standardization = simplicity but lock-in.
**Proposed:** Standardize on Zod. No wrapper. Shared schemas in `@platform/core/validation/schemas/`. If org consensus changes, migrate schemas — not the abstraction layer.

### ADR-004: Execution Context Propagation Strategy
**Context:** Execution context must propagate across async boundaries, HTTP calls, and message brokers.
**Decision to Make:** `AsyncLocalStorage` for in-process + explicit header propagation for out-of-process? Or full W3C TraceContext?
**Key Trade-Off:** `AsyncLocalStorage` is Node.js-native, zero-overhead, but fragile across certain async patterns. W3C TraceContext is universal but heavier.
**Proposed:** `AsyncLocalStorage` for in-process. W3C `traceparent`/`tracestate` headers for cross-process. ContextPropagator interface for framework-specific injection/extraction.

### ADR-005: Outbox Pattern Implementation Strategy
**Context:** Outbox bridges transactional database writes with message publishing.
**Decision to Make:** Polling-based outbox (SELECT + DELETE) OR transaction log tailing (CDC/debezium) OR application-level dual write with retry?
**Key Trade-Off:** Polling is simple but has latency (poll interval). CDC is real-time but requires infrastructure (Debezium). Dual write is fragile (no atomicity).
**Proposed:** Polling-based outbox as the core abstraction (simple, infrastructure-agnostic). CDC adapter available for high-throughput services. Dual write explicitly documented as anti-pattern.

### ADR-006: Event Envelope Metadata Design
**Context:** Every message carries metadata for routing, tracing, and deduplication.
**Decision to Make:** What fields are mandatory vs optional? Should envelope include schema version? Should envelope include encryption metadata?
**Key Trade-Off:** More metadata = larger messages, higher serialization cost. Less metadata = harder to debug, trace, and deduplicate.
**Proposed:** Mandatory fields: `messageId`, `messageType`, `schemaVersion`, `occurredAt`, `correlationId`, `traceId`, `payload`. Optional: `causationId`, `tenantId`, `userId`, `compression`, `encryption`. Rationale documented per field.

### ADR-007: Fencing Token Strategy
**Context:** Distributed locks without fencing tokens are vulnerable to the "stale lock holder" problem.
**Decision to Make:** Monotonic integer (Redis INCR) vs hybrid logical clock vs ZK zxid?
**Key Trade-Off:** Monotonic integer is simplest but requires a strongly consistent counter. HLC works without coordination but is more complex. ZK zxid requires ZooKeeper.
**Proposed:** `FencingTokenProvider` interface. Default implementation: monotonic integer from a strongly consistent store (Redis INCR or PostgreSQL sequence). Alternative: HLC implementation for ZooKeeper/Consul-free deployments.

### ADR-008: Saga Compensation Strategy
**Context:** Sagas undo partial work when a step fails, but compensation can also fail.
**Decision to Make:** Forward recovery (retry until success) vs backward recovery (compensate and stop) vs mixed strategy?
**Key Trade-Off:** Forward recovery is simpler but can block indefinitely. Backward recovery is complete but compensation failures cascade. Mixed is flexible but more complex.
**Proposed:** Mixed strategy. Default: backward recovery with compensation. Configurable: forward recovery for idempotent steps. Compensation failures go to dead letter for manual intervention. Saga state is persisted for observability.

### ADR-009: Cache Invalidation Strategy
**Context:** Cache invalidation is one of the hardest problems in distributed systems.
**Decision to Make:** TTL-only (simplest) vs write-through (consistent) vs write-behind (fast) vs cache-aside (flexible)?
**Key Trade-Off:** TTL-only serves stale data. Write-through is consistent but slow. Write-behind is fast but can lose data. Cache-aside is flexible but puts burden on application code.
**Proposed:** `CacheStore` interface supports all strategies. Default implementation: cache-aside with configurable TTL. Write-through and write-behind as optional strategies with documented trade-offs.

### ADR-010: Error Model Design
**Context:** A unified error taxonomy is needed across all services.
**Decision to Make:** Inheritance hierarchy (extends Error) vs discriminated union (type + kind) vs error codes only?
**Key Trade-Off:** Inheritance is familiar but fragile (instanceof breaks across package versions). Discriminated unions are robust but unidiomatic in TypeScript error handling. Error codes only lose structural information.
**Proposed:** Hybrid: abstract base classes (`DomainError extends Error`) for structural grouping + `code` property (string union) for machine-readable identification + HTTP status mapping via `ErrorMapper` interface. instanceof checks discouraged — use `error.code` for control flow.

### ADR-011: Idempotency Key Scope and TTL
**Context:** Idempotency prevents duplicate processing, but keys must expire to avoid unbounded storage.
**Decision to Make:** What is the default TTL? How are keys scoped (per-service, per-user, global)?
**Key Trade-Off:** Short TTL = smaller storage but risk of reprocessing. Long TTL = safer but larger storage cost. Global scope = simpler but collision risk. Scoped = safer but more complex.
**Proposed:** Default TTL: 24 hours (covers most retry windows). Key scoping: `{service}:{entity}:{operation}:{clientSuppliedKey}`. Storage: use existing database (no new infrastructure). Cleanup: scheduled job for expired keys.

### ADR-012: Schema Registry Responsibility
**Context:** Message schemas evolve over time. Producers and consumers must agree on schema versions.
**Decision to Make:** Centralized schema registry (Confluent) vs decentralized (schema in code) vs hybrid (registry for integration events, code for domain events)?
**Key Trade-Off:** Centralized registry provides governance but adds infrastructure dependency. Decentralized is simpler but risks incompatible changes. Hybrid is practical but adds complexity.
**Proposed:** `SchemaRegistry` interface in `@platform/messaging`. Default: decentralized for domain events (schema in code, validated at build time). Centralized for integration events (Confluent Schema Registry, AWS Glue — adapter-implemented). Compatibility checks: BACKWARD, FORWARD, FULL.

### ADR-013: Monorepo vs Multi-Repo for Platform Packages
**Context:** Five platform packages need coordinated development and versioning.
**Decision to Make:** Single monorepo (pnpm workspaces) vs separate repos per package?
**Key Trade-Off:** Monorepo = atomic commits across packages, easier refactoring. Multi-repo = independent CI/CD, clearer ownership, but harder cross-package changes.
**Proposed:** Monorepo with pnpm workspaces for platform packages. Services consume packages via npm registry (not workspace references). Platform packages are developed together but released independently.

### ADR-014: Testing Strategy for Platform Packages
**Context:** Platform packages are consumed by 20+ services. Bugs in platform packages affect all services.
**Decision to Make:** What test pyramid applies? Contract testing vs integration testing priority?
**Key Trade-Off:** Comprehensive testing = slower releases but higher confidence. Light testing = faster iteration but higher risk.
**Proposed:** Per package: unit tests ≥ 90% coverage, integration tests for adapter interfaces, contract tests for all public APIs, property-based tests for serialization/validation. Every adapter ships with a test suite that validates it against the contract.

### ADR-015: Deprecation and Migration Policy
**Context:** Platform packages will evolve. Breaking changes must not force all services to migrate simultaneously.
**Decision to Make:** How long is the deprecation window? What migration tooling is provided?
**Key Trade-Off:** Long deprecation = safe but slow. Short deprecation = fast evolution but risky.
**Proposed:** Foundation: 12-month deprecation (zero-dependency makes this safe). All others: 6 months. Codemods provided for mechanical migrations (renamed interfaces, moved modules). `@deprecated` JSDoc + runtime warnings in non-production. Migration guide per breaking change.

---

## Optional ADRs (Write If Applicable)

### ADR-016: Event Sourcing Support
**Context:** Some services may need event sourcing (full audit trail, temporal queries).
**Decision:** Should `@platform/foundation` include `EventStore` and `EventSourcedAggregate` contracts?
**Status:** DEFER. Add to foundation only when 3+ services need it. Premature abstraction without concrete use cases.

### ADR-017: GraphQL vs REST API Contracts
**Context:** The web module provides REST pagination. Should it also provide GraphQL relay connections?
**Decision:** Add `@platform/web/graphql/` with Relay-compliant pagination?
**Status:** DEFER. REST pagination first (80% use case). GraphQL pagination as extension when GraphQL adoption reaches critical mass.

### ADR-018: gRPC Support
**Context:** Some inter-service communication may use gRPC instead of REST/messaging.
**Decision:** Should platform packages include gRPC middleware contracts?
**Status:** DEFER. REST + messaging covers 90%+ of communication patterns. gRPC support as adapter package if needed.

### ADR-019: Multi-Region Support
**Context:** The organization may expand to multiple regions.
**Decision:** Should distributed packages include region-aware primitives (CRDT, multi-leader, geo-routing)?
**Status:** DEFER. Single-region first. Multi-region patterns are v2 — they require real production experience before abstracting.

### ADR-020: Observability Pipeline
**Context:** Logs, metrics, and traces need to be collected, aggregated, and stored.
**Decision:** Should platform define observability pipeline contracts (collector, aggregator, storage)?
**Status:** KEEP SIMPLE. Platform defines `ILogger`, `IMetrics`, `ITracer`. Collection/aggregation/storage is infrastructure — adapters handle OpenTelemetry collector, Prometheus, Grafana, etc. Platform does NOT define pipeline contracts.

---

## ADR Template

All ADRs follow this structure:

```markdown
# ADR-NNN: Title

**Status:** Proposed | Accepted | Deprecated | Superseded

**Date:** YYYY-MM-DD

**Context:**
What is the issue? What forces are at play? What constraints exist?

**Decision:**
What will we do? Be specific. Include code-level details where relevant.

**Consequences:**
What becomes easier? What becomes harder? What risks are introduced?

**Alternatives Considered:**
What other options were evaluated? Why were they rejected?
```
