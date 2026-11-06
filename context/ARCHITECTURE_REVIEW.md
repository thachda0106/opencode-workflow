# Architecture Review — Platform Core Package

**Date:** 2026-06-10
**Reviewer:** Principal Platform Architect
**Status:** Critical Review — Pre-Implementation

---

## Executive Summary

**Verdict: Do NOT implement as designed. Restructure before proceeding.**

The current proposal describes a **God Core Package** — a single monolithic `core/` package containing 20 diverse modules spanning DDD primitives, infrastructure abstractions, distributed systems toolkits, application patterns, web/HTTP concerns, and cross-cutting utilities. This is not a "shared core." It is a nascent platform framework waiting to become a maintenance nightmare.

### Primary Finding

A single package with 20 modules creates an **unbounded dependency surface**. Every service must depend on the entire package even if it only needs 3 modules. Every change to any module — even one a service doesn't use — forces a version bump and coordinated rollout across all 20+ services. This is the exact opposite of microservice autonomy.

### Recommendation

Split into **5 focused, independently versioned packages** with strict dependency rules. Each package has a clear purpose, narrow API surface, and explicit ownership boundaries.

---

## 1. Scope Analysis — What Is This Actually?

The current design is **three distinct things masquerading as one**:

| Identity | Modules | Description |
|----------|---------|-------------|
| **Shared Core** | errors, contracts, execution-context, serialization | Truly shared primitives used by every service |
| **Infrastructure Abstraction Layer** | messaging, persistence, cache, distributed, scheduler, feature-flags | Contracts that infrastructure adapters implement |
| **Application Framework** | workflow, resilience, web, tenancy, security, idempotency, consistency, validation, observability, config | Patterns and utilities consumed at the service/application layer |

**Diagnosis:** Mixing all three into a single package violates the Single Responsibility Principle at the package level. It guarantees that:

1. A service needing only DDD primitives pulls in messaging, caching, workflows, and web modules.
2. A change to the web module (e.g., pagination format) forces all services to update — even message-only consumers.
3. The package grows unboundedly because "just one more module" has no gate.

---

## 2. Module-by-Module Assessment

### Legend
- ✅ **Keep** — belongs in shared platform
- 🔀 **Move** — belongs in a different package
- ❌ **Remove** — does not belong in any shared package
- ⚠️ **Redesign** — concept is valid but current scope is wrong

### Detailed Assessment

#### ✅ errors/
**Keep in @platform/foundation**
- Standard error taxonomy needed by every service
- Zero external dependencies
- **Risk:** Error model must not become framework-specific (no NestJS HttpException dependency)

#### ✅ contracts/ (DDD primitives only)
**Keep in @platform/foundation — but split domain vs application**
- `Entity`, `ValueObject`, `AggregateRoot`, `DomainEvent` → `contracts/domain/`
- `Repository`, `Specification` → `contracts/domain/` (interfaces only)
- `Command`, `Query`, `UseCase` → `contracts/application/`
- **Risk:** `DomainService` abstraction is a leak — it has no invariant behavior to share and belongs in individual services

#### ✅ execution-context/
**Keep in @platform/foundation**
- Essential cross-cutting primitive
- `AsyncLocalStorage` is Node.js-native — no framework coupling
- **Risk:** Must not grow beyond context propagation. Lint: no business logic, no HTTP middleware, no database access.

#### ✅ serialization/
**Keep in @platform/foundation**
- `Serializer<T>` interface with zero dependencies
- Enables message serialization, event encoding, config parsing
- **Risk:** Must remain purely an interface. No JSON.parse defaults, no schema registry coupling.

#### ✅ config/
**Keep in @platform/foundation — but contracts only**
- Typed config interfaces: `ConfigStore`, `SecretProvider`
- Implementation adapters live in `@platform/adapters/*`
- **Risk:** Must not import `dotenv`, AWS SDK, or Vault SDK

#### ⚠️ validation/
**Keep in @platform/core — redesign**
- Current scope: "abstraction layer for Zod, class-validator"
- **Problem:** A validation abstraction that hides Zod is a leaky abstraction. Zod IS the schema language — wrapping it adds indirection without value.
- **Recommendation:** Standardize on one validation library per platform (e.g., Zod as the canonical choice). The "abstraction" becomes a set of **shared schemas and custom refinements**, not a wrapper.

#### ✅ observability/
**Keep in @platform/core**
- `ILogger`, `IMetrics`, `ITracer`, `IHealthCheck` — well-scoped
- OpenTelemetry compatibility is the correct target
- **Missing:** `IHealthCheck` needs explicit `liveness()` vs `readiness()` distinction

#### ⚠️ resilience/
**Move to @platform/core — redesign scope**
- `Policy`, `PolicyBuilder`, Retry, Timeout, CircuitBreaker, Bulkhead, RateLimiter
- **Problem:** These are application-level concerns, not infrastructure contracts. But they ARE cross-cutting and valuable to share.
- **Risk:** CircuitBreaker must not couple to any HTTP library (no `axios`, `fetch` imports). RateLimiter must not couple to Redis.

#### 🔀 persistence/transaction/
**Move to @platform/persistence**
- `TransactionManager` interface — correctly scoped
- **Risk:** Must support both SQL transactions AND NoSQL "transactions" (MongoDB sessions). Interface must be generic enough for both.

#### 🔀 persistence/unit-of-work/
**Move to @platform/persistence**
- `UnitOfWork` with `execute<T>(callback, options): Promise<T>` — well-designed
- **Risk:** `options` type must not leak ORM-specific concepts (no Prisma transaction options, no TypeORM entity manager)

#### 🔀 persistence/specification/
**Move to @platform/persistence**
- Composable specifications — valuable pattern
- **Risk:** Must remain pure predicate composition. No SQL generation, no Prisma query building.

#### 🔀 persistence/outbox/ + persistence/inbox/
**Move to @platform/messaging**
- **Critical finding:** Outbox and Inbox are **messaging patterns**, not persistence patterns. They exist to bridge the gap between transactional storage and message brokers. Placing them in `persistence/` is a category error.
- Outbox: atomic write of business state + outgoing events → messaging concern
- Inbox: idempotent processing of incoming events → messaging concern
- **Risk:** If left in persistence, the persistence package gains a dependency on messaging concepts.

#### 🔀 persistence/optimistic-lock/
**Move to @platform/persistence**
- Version-based concurrency — correctly scoped

#### 🔀 messaging/ (all sub-modules)
**Move to @platform/messaging**
- `MessageProducer`, `MessageConsumer`, `MessageBus` — correctly scoped
- Domain Events vs Integration Events separation is correct
- `MessageEnvelope<T>` — well-designed metadata schema
- **Missing:** No dead letter strategy. No message versioning. No retry policy per message type. These MUST be first-class concepts.

#### 🔀 distributed/ (all sub-modules)
**Move to @platform/distributed**
- `DistributedLock`, `Lease`, `LeaderElection`, `FencingToken` — correctly scoped
- Stale lock holder problem and fencing token solution are essential to document
- **Missing:** No circuit breaker integration for lock acquisition failures. A distributed lock that blocks indefinitely is a production outage.

#### 🔀 cache/
**Move to @platform/distributed**
- `CacheStore` with get/set/delete/exists/invalidate/getOrSet — correctly scoped
- Cache key strategy is an essential addition
- **Missing:** Cache invalidation strategy patterns (write-through, write-behind, TTL-based). "There are only two hard things in Computer Science: cache invalidation and naming things."

#### ⚠️ security/
**Keep in @platform/core — redesign**
- `PasswordHasher`, `Encryptor`, `TokenProvider`
- **Problem:** `PasswordHasher` and `Encryptor` are low-level crypto primitives. `TokenProvider` is an application-level auth concern. Mixing them is wrong.
- **Recommendation:** Split into `crypto/` (hashing, encryption — zero business knowledge) and keep `TokenProvider` in core. Remove JWT-specific assumptions from TokenProvider — it should be a generic token contract.

#### 🔀 idempotency/
**Move to @platform/distributed**
- `IdempotencyKey`, `IdempotencyStore`, `IdempotencyPolicy`
- **Correct assessment:** Idempotency is fundamentally a distributed systems concern (exactly-once semantics across network boundaries)

#### ⚠️ consistency/
**Split across packages**
- `Version`, `ConcurrencyToken` → `@platform/persistence` (optimistic concurrency primitives)
- `CompareAndSwap`, `ETag`, `ConflictResolution` → `@platform/distributed` (distributed consistency patterns)
- **Problem:** Two different consistency domains conflated into one module

#### 🔀 tenancy/
**Move to @platform/core**
- `TenantContext`, `TenantResolver`, `TenantStrategy`
- Correctly scoped as a cross-cutting concern
- **Risk:** TenantStrategy must not assume PostgreSQL schemas. Shared-database-per-tenant approach needs different primitives than database-per-tenant.

#### 🔀 workflow/state-machine/
**Move to @platform/messaging**
- `State`, `Transition` — state machine primitives
- **Finding:** State machines are most commonly used in sagas and process managers, which are messaging patterns. A generic state machine CAN live in foundation, but its primary consumer is messaging workflows.

#### 🔀 workflow/process-manager/ + workflow/saga/
**Move to @platform/messaging**
- `ProcessManager`, `SagaCoordinator`
- **Correct:** These are messaging-orchestrated patterns. A saga without messaging is not a saga — it's a local transaction.
- **Missing:** Saga compensation strategy must be explicit. "How do you undo step 3 when step 7 fails?" is the fundamental saga question.

#### 🔀 scheduler/
**Move to @platform/distributed**
- `Job`, `Scheduler`, `DistributedJob`
- Correctly scoped as a distributed coordination concern
- **Risk:** Scheduler must distinguish between at-most-once and at-least-once execution guarantees

#### 🔀 feature-flags/
**Move to @platform/distributed**
- `FeatureFlagProvider`
- **Controversial:** Feature flags could also live in @platform/core since they're consumed at the application layer. However, they fundamentally solve a distributed configuration propagation problem (flags must reach all service instances consistently).
- **Recommendation:** Place in @platform/distributed but expose a thin re-export from @platform/core for ergonomics.

#### ✅ errors/ (re-confirmed)
**Keep in @platform/foundation**
- `DomainError`, `ApplicationError`, `InfrastructureError`, `ValidationError`, `ConflictError`, `NotFoundError`, `UnauthorizedError`, `ForbiddenError`
- `ErrorCode`, `ErrorMapper`
- **Missing:** `ErrorMapper` needs a clear contract for HTTP status code mapping. Must not import NestJS or Express types.

#### 🔀 web/
**Move to @platform/core**
- Problem Details (RFC 7807), Exception Mapping, Pagination, Cursor Pagination, Request Context Integration
- **Correct scope:** These are HTTP-facing concerns. Services that are pure message consumers don't need them.
- **Risk:** ProblemDetails must not import framework-specific exception types. RFC 7807 is a JSON format — it should be a plain object, not an Express/NestJS exception.

---

## 3. DDD Review

### Missing DDD Building Blocks

| Concept | Status | Recommendation |
|---------|--------|----------------|
| Entity | ✅ Present | Keep as abstract base class with `id` and `equals()` |
| AggregateRoot | ✅ Present | Keep with domain event collection pattern |
| ValueObject | ✅ Present | Keep with structural equality |
| DomainEvent | ✅ Present | Keep with `occurredAt`, `aggregateId` |
| Repository | ✅ Present | Keep as interface only — implementation in services |
| Specification | ✅ Present | Keep as composable predicate pattern |
| DomainService | ⚠️ Present | **Remove.** No shared behavior to justify. Services implement their own. |
| Command | ✅ Present | Keep as marker interface |
| Query | ✅ Present | Keep as marker interface |
| UseCase | ✅ Present | Keep as `execute(request): Promise<response>` contract |
| IntegrationEvent | ✅ Present | **Move to @platform/messaging** |
| Domain Event Publisher | ❌ Missing | Interface for publishing domain events within a bounded context |
| Event Store | ❌ Missing | Interface for event sourcing (optional but important for CQRS) |

### Separation of domain/ and application/

The current `contracts/` module mixes domain contracts and application contracts:

```
Current (WRONG):
contracts/
  AggregateRoot, Entity, ValueObject, DomainService, Repository, Specification
  Command, Query, Event, DomainEvent, IntegrationEvent, UseCase

Recommended (CORRECT):
contracts/
  domain/
    Entity, ValueObject, AggregateRoot, DomainEvent, Repository, Specification
  application/
    Command, Query, UseCase
```

**Rationale:** Domain contracts represent the **what** (business rules). Application contracts represent the **how** (use case orchestration). Services import domain contracts into their domain layer and application contracts into their application layer. Mixing them blurs the Clean Architecture dependency rule (domain must not depend on application).

### What belongs in shared core vs. services

**Shared core provides:**
- Abstract base classes (Entity, ValueObject, AggregateRoot)
- Interfaces (Repository, Specification)
- Base types (DomainEvent, Command, Query, UseCase)

**Services provide:**
- Concrete entities (User, Order, Product)
- Concrete value objects (Email, Money, Address)
- Concrete repositories (UserRepository, OrderRepository)
- Concrete use cases (CreateOrderUseCase, RegisterUserUseCase)
- Domain services (PricingService, InventoryService)

---

## 4. Distributed Systems Review

### Pattern Coverage

| Pattern | Status | Notes |
|---------|--------|-------|
| Outbox | ✅ Present | Atomic event persistence + reliable publishing |
| Inbox | ✅ Present | Idempotent consumer + duplicate detection |
| Saga | ✅ Present | SagaCoordinator with compensation |
| Process Manager | ✅ Present | Stateful orchestration |
| Idempotency | ✅ Present | IdempotencyKey + IdempotencyStore |
| Distributed Lock | ✅ Present | Lock + fencing token |
| Lease Lock | ✅ Present | Time-bounded lock with renewal |
| Fencing Token | ✅ Present | Monotonic token for stale lock prevention |
| Event Envelope | ✅ Present | Standardized metadata envelope |
| Message Versioning | ❌ Missing | **Critical gap.** Without versioning, evolving message schemas breaks consumers. |
| Deduplication | ⚠️ Partial | Inbox handles dedup, but no explicit dedup strategy for non-inbox consumers |
| Retry Strategy | ❌ Missing | **Critical gap.** Resilience module has retry, but messaging-specific retry (backoff per message type, dead letter after N attempts) is absent |
| Dead Letter Handling | ❌ Missing | **Critical gap.** Failed messages must have a defined destination and replay mechanism |
| Consistency Boundaries | ⚠️ Partial | Consistency module has CompareAndSwap/ETag, but no aggregate-level consistency boundary definition |
| Event Ordering | ❌ Missing | Ordering guarantees (partition key design, sequence numbers) not addressed |
| Backpressure | ❌ Missing | Consumer backpressure strategy not defined |
| Schema Registry | ❌ Missing | Centralized schema management for Avro/Protobuf not addressed |

### Dangerous Abstractions Identified

1. **`MessageBus` as a single interface**: A unified bus that handles both domain events and integration events is a leaky abstraction. Domain events are intra-service, synchronous, and in-process. Integration events are inter-service, asynchronous, and durable. They need different contracts.

2. **`DistributedLock` without timeout**: Every `acquire()` call must have a mandatory timeout or the interface is dangerous. A lock that blocks indefinitely is a production outage waiting for a GC pause.

3. **`CacheStore` without stampede protection**: `getOrSet` must document whether it protects against cache stampede (thundering herd). If it doesn't, it's not production-ready.

4. **`SagaCoordinator` without idempotency**: A saga step that executes twice due to retry must be safe. The coordinator must enforce idempotency per step.

---

## 5. Dependency Governance

Per-module dependency rules for the current (flawed) structure — identifies the problems that drive the restructured recommendation.

### Allowed Dependencies (current structure)

```
errors/           → (nothing — leaf module)
serialization/    → (nothing — leaf module)
contracts/        → errors/
execution-context/ → (nothing — Node.js built-in only)
config/           → errors/, serialization/
validation/       → errors/
observability/    → errors/, execution-context/
resilience/       → errors/
security/         → errors/
persistence/      → errors/, contracts/, serialization/
messaging/        → errors/, contracts/, serialization/, execution-context/
distributed/      → errors/, serialization/
cache/            → errors/, serialization/
idempotency/      → errors/, serialization/
consistency/      → errors/, contracts/
tenancy/          → errors/, execution-context/
workflow/         → errors/, contracts/, messaging/
scheduler/        → errors/, serialization/
feature-flags/    → errors/
web/              → errors/, serialization/, execution-context/
```

### Forbidden Dependencies (current structure)

```
messaging/       ✗ persistence/     — Outbox bridges these; dependency must be inverted
messaging/       ✗ cache/           — Message dedup might use cache, but must be behind interface
persistence/     ✗ messaging/       — Outbox writes to DB; must not know about Kafka
resilience/      ✗ distributed/     — Circuit breaker must not know about Redis locks
web/             ✗ resilience/      — HTTP retry must not couple to circuit breaker
observability/   ✗ messaging/       — Traces must not know about Kafka topics
workflow/        ✗ persistence/     — Saga state must not couple to database schema
```

### Circular Dependency Risks

The biggest risk is **messaging ↔ persistence**:
- `messaging/outbox` writes to the database (needs persistence)
- `persistence/` wants to emit domain events (needs messaging)
- **Resolution:** Extract outbox/inbox to a separate module that depends on both, or use dependency inversion (persistence emits events through a callback, not by importing messaging).

---

## 6. Non-Functional Requirements Per Module

| Module | Scalability | Failure Mode | Recovery | Performance | Observability | Security |
|--------|------------|--------------|----------|-------------|---------------|----------|
| execution-context | Must not allocate per-request — use AsyncLocalStorage | Context loss on uncaught exception | Regenerate from incoming headers | Sub-microsecond access | Trace all context propagation | Never log secrets from context |
| messaging/outbox | Outbox table must be partitioned by time | Outbox poller misses messages | Message ID-based dedup on replay | Batch polling > single-row poll | Track outbox lag as metric | Encrypt payload if contains PII |
| messaging/inbox | Inbox table grows unboundedly | Duplicate event crashes consumer | Idempotency by messageId | Index on messageId for O(1) lookup | Track duplicate rate | — |
| distributed/lock | Lock contention under high concurrency | Lock holder crashes without release | Fencing token + TTL-based auto-release | Lock acquisition < 10ms p99 | Lock wait time histogram | — |
| distributed/fencing-token | Monotonic token generation bottleneck | Token generation fails | Fallback to TTL-only locks | Token generation < 5ms | Token generation latency | — |
| cache/ | Cache cluster must scale horizontally | Cache miss storm → DB overload | Circuit breaker on cache → fallback to stale data | get/set < 1ms p99 | Cache hit rate, miss latency | Never cache unencrypted PII |
| workflow/saga | Saga state storage must be partitionable | Saga step fails mid-execution | Compensation + idempotent retry | Step timeout < configurable SLA | Saga completion rate, step latency | — |
| web/ | Pagination must use cursor-based (not offset) | Deep pagination degrades DB | — | Cursor decode < 1ms | Pagination depth histogram | Validate cursor tokens against tampering |

---

## 7. Anti-Patterns Identified

### 1. God Package (CRITICAL)
**Location:** Entire `core/` package
**Issue:** 20 modules in a single package. Every service depends on the entire monolith.
**Fix:** Split into 5 focused packages.

### 2. Leaky Abstraction — MessageBus
**Location:** `messaging/` module
**Issue:** A single `MessageBus` interface handling both in-process domain events and durable integration events forces the same contract on fundamentally different communication patterns.
**Fix:** Separate `DomainEventPublisher` (in-process) from `IntegrationEventPublisher` (durable, async).

### 3. Infrastructure Leakage Risk — Resilience
**Location:** `resilience/` module
**Issue:** CircuitBreaker, Bulkhead, and RateLimiter are described as "inspired by Polly" (a .NET library). This risks importing .NET-specific patterns into a TypeScript codebase.
**Fix:** No Polly import or reference. Design from first principles for TypeScript/Node.js.

### 4. DDD Violation — Outbox in Persistence
**Location:** `persistence/outbox/` and `persistence/inbox/`
**Issue:** Outbox and Inbox are messaging patterns, not persistence patterns. A persistence module should not know about message brokers.
**Fix:** Move to messaging package.

### 5. Framework Coupling Risk — Web
**Location:** `web/` module
**Issue:** "Exception Mapping" and "Request Context Integration" are framework-sensitive concepts. Mapping NestJS exceptions vs Express exceptions vs Fastify exceptions requires different code.
**Fix:** Define RFC 7807 problem details as plain TypeScript types. Leave Exception Mapping to framework-specific adapters.

### 6. Circular Dependency Risk — Messaging ↔ Persistence
**Location:** Outbox pattern
**Issue:** Outbox writes to DB (needs persistence) but persistence wants to emit events (needs messaging). Bidirectional dependency.
**Fix:** Dependency Inversion — persistence exposes an `onCommit` hook that messaging plugs into.

### 7. Theoretical Completeness Over Practicality
**Location:** Entire design
**Issue:** The design includes modules for leader election, fencing tokens, state machines, process managers, sagas, and distributed jobs. Most services at an org with 20+ microservices will use maybe 5-8 of these. The rest is dead weight.
**Fix:** Each package should list which modules are "Tier 1" (needed by 80%+ of services) vs "Tier 2" (needed by <20%). Tier 2 modules can be separate optional packages.

---

## 8. Risk Register

| ID | Risk | Severity | Likelihood | Mitigation |
|----|------|----------|------------|------------|
| R1 | God Package: single package grows unboundedly, every change forces all-service rollout | CRITICAL | Certain | Split into 5 packages now |
| R2 | Messaging↔Persistence circular dependency emerges during implementation | HIGH | Likely | Dependency inversion via hooks/callbacks |
| R3 | Framework leakage: web/resilience/validation modules import NestJS/Express types | HIGH | Likely | Strict lint rules per package; architecture fitness functions |
| R4 | Over-abstraction: validation wrapper around Zod adds complexity without value | MEDIUM | Likely | Choose Zod as canonical; provide shared schemas, not abstraction |
| R5 | Saga implementation couples to message broker semantics | MEDIUM | Possible | Saga depends on messaging contracts, not Kafka/RabbitMQ specifics |
| R6 | Cache stampede: getOrSet without thundering herd protection causes DB overload | HIGH | Possible | Document and enforce stampede protection in CacheStore contract |
| R7 | DistributedLock without mandatory timeout causes production outages | CRITICAL | Possible | `acquire()` must require timeout parameter at type level |
| R8 | Message versioning omitted → breaking schema changes break consumers | HIGH | Certain | Add MessageVersion to envelope; add SchemaRegistry contract |
| R9 | Execution context leaks across async boundaries (AsyncLocalStorage edge cases) | MEDIUM | Possible | Comprehensive async boundary tests |
| R10 | Tenant data leakage: shared-database strategy exposes cross-tenant data | CRITICAL | Possible | Tenant isolation tests; row-level security guidance |

---

## 9. Trade-Off Analysis

| Decision | Option A (Current) | Option B (Recommended) | Trade-Off |
|----------|-------------------|----------------------|-----------|
| Package count | 1 monolithic package | 5 focused packages | More packages = more version management, but safer evolution |
| Validation | Abstract wrapper around Zod/class-validator | Adopt Zod as canonical, share schemas | Less flexibility, dramatically simpler, removes leaky abstraction |
| Outbox location | persistence/outbox/ | messaging/outbox/ | Moving to messaging prevents circular dependency but feels unintuitive to DB-focused devs |
| Workflow location | top-level workflow/ | messaging/workflow/ | Sagas ARE messaging patterns, but workflow module might feel like it deserves independence |
| Feature flags location | standalone feature-flags/ | distributed/feature-flags/ | Less discoverable but more architecturally correct |
| MessageBus | Single unified interface | Separate DomainEventPublisher + IntegrationEventPublisher | Two interfaces = more code, but correct separation of concerns |
| Schema Registry | Not included | Add as contract | Adds scope but essential for Avro/Protobuf evolution |

---

## 10. Final Assessment

The current design demonstrates strong architectural knowledge — the individual module specifications are well-reasoned and the infrastructure-agnostic discipline is correct. However, the **packaging strategy** is critically flawed. A single `core/` package containing 20 modules is a God Package that will:

1. Force unnecessary dependency upgrades across all services
2. Accumulate coupling between unrelated modules over time
3. Become impossible to deprecate or remove modules from
4. Create a single point of architectural contention across teams

**The fix is not to redesign the modules — it's to repackage them.** The modules themselves are largely correct. The organization is wrong.

Proceed to RECOMMENDED_STRUCTURE.md for the concrete proposal.
