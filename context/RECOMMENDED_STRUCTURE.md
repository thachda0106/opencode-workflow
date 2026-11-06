# Recommended Package Structure — Platform Core

**Status:** Proposal — Pre-Implementation
**Replaces:** Single monolithic `core/` package (20 modules)
**Principle:** "Prefer smaller focused packages over a single massive shared core."

---

## Final Package Architecture

```
@platform/
├── foundation/          ← Zero dependencies. Used by EVERYTHING.
├── core/                ← Cross-cutting concerns. Used by MOST services.
├── messaging/           ← Messaging + workflow. Used by event-driven services.
├── persistence/         ← Data access. Used by database-backed services.
└── distributed/         ← Coordination. Used by distributed services.
```

**Five packages. Clear boundaries. Explicit dependencies.**

---

## Package 1: @platform/foundation

### Responsibility
The absolute minimum shared by every service. Zero external dependencies on other platform packages. Must not import any Node.js library beyond `node:async_hooks`, `node:crypto`, `node:buffer`.

### Contents

```
@platform/foundation/
├── errors/
│   ├── domain-error.ts          — abstract DomainError extends Error
│   ├── application-error.ts     — abstract ApplicationError
│   ├── infrastructure-error.ts  — abstract InfrastructureError
│   ├── validation-error.ts      — ValidationError with field-level details
│   ├── conflict-error.ts        — ConflictError for optimistic lock failures
│   ├── not-found-error.ts       — NotFoundError with entity type + id
│   ├── unauthorized-error.ts    — UnauthorizedError
│   ├── forbidden-error.ts       — ForbiddenError
│   ├── error-code.ts            — ErrorCode enum / string union
│   └── error-mapper.ts          — ErrorMapper interface (maps error → response shape)
│
├── contracts/
│   ├── domain/
│   │   ├── entity.ts            — abstract class Entity<TId>
│   │   ├── value-object.ts      — abstract class ValueObject
│   │   ├── aggregate-root.ts    — abstract class AggregateRoot<TId> extends Entity
│   │   ├── domain-event.ts      — abstract class DomainEvent
│   │   ├── repository.ts        — interface Repository<TAggregate, TId>
│   │   └── specification.ts     — interface Specification<T> (isSatisfiedBy + and/or/not)
│   └── application/
│       ├── command.ts            — interface Command<TResult = void>
│       ├── query.ts              — interface Query<TResult>
│       └── use-case.ts           — interface UseCase<TRequest, TResponse>
│
├── execution-context/
│   ├── execution-context.ts     — class ExecutionContext (AsyncLocalStorage wrapper)
│   ├── context-accessor.ts      — static accessor for current context
│   ├── context-keys.ts          — typed keys: requestId, correlationId, causationId, traceId, spanId, tenantId, userId, actorId, locale, baggage
│   └── context-propagator.ts    — interface for extracting/injecting context to headers
│
├── serialization/
│   ├── serializer.ts            — interface Serializer<T> { serialize, deserialize }
│   ├── content-type.ts          — ContentType enum (JSON, Avro, Protobuf)
│   └── serialization-error.ts   — error for deserialization failures
│
├── config/
│   ├── config-store.ts          — interface ConfigStore<T> { get(key): T }
│   ├── secret-provider.ts       — interface SecretProvider { getSecret(name): Promise<string> }
│   ├── config-schema.ts         — interface ConfigSchema<T> (typed config definition)
│   └── config-error.ts          — ConfigError for missing/invalid config
│
└── index.ts                     — barrel re-export
```

### Allowed Dependencies
- Node.js built-in modules only (`node:async_hooks`, `node:crypto`, `node:buffer`)
- **Must not** import from any `@platform/*` package
- **Must not** import from any third-party library (no `zod`, no `uuid`, no `lodash`)

### Forbidden Dependencies
```
@platform/foundation
  ✗ @platform/core
  ✗ @platform/messaging
  ✗ @platform/persistence
  ✗ @platform/distributed
  ✗ nestjs / express / fastify
  ✗ kafkajs / ioredis / prisma / typeorm
  ✗ zod / class-validator
```

### Extension Points
- `Serializer<T>` → implemented by JSON, Avro, Protobuf adapters
- `ConfigStore<T>` → implemented by env, AWS, Vault adapters
- `SecretProvider` → implemented by AWS Secrets Manager, Vault adapters
- `ErrorMapper` → implemented by framework-specific HTTP error mappers
- `ContextPropagator` → implemented by HTTP, gRPC, messaging adapters

---

## Package 2: @platform/core

### Responsibility
Cross-cutting concerns used by most services. Depends on `@platform/foundation`.

### Contents

```
@platform/core/
├── validation/
│   ├── schemas/                  — shared Zod schemas (email, UUID, pagination, etc.)
│   ├── refinements/              — custom Zod refinements (strong password, future date)
│   ├── validation-pipe.ts        — generic validation pipe (wraps Zod parse)
│   └── validation-error-factory.ts — maps ZodError → ValidationError
│
├── observability/
│   ├── logger.ts                 — interface ILogger (info, warn, error, debug, withContext)
│   ├── metrics.ts                — interface IMetrics (counter, gauge, histogram, timer)
│   ├── tracer.ts                 — interface ITracer (startSpan, inject, extract)
│   ├── health-check.ts           — interface IHealthCheck { liveness(), readiness() }
│   └── noop-implementations.ts   — NoOpLogger, NoOpMetrics, NoOpTracer, NoOpHealthCheck
│
├── security/
│   ├── crypto/                   — low-level crypto primitives
│   │   ├── password-hasher.ts    — interface PasswordHasher
│   │   ├── encryptor.ts          — interface Encryptor
│   │   └── random-generator.ts   — interface RandomGenerator (secure random tokens)
│   ├── token-provider.ts         — interface TokenProvider<TClaims>
│   └── authorization/
│       └── rbac.ts               — interface RbacChecker (hasPermission)
│
├── resilience/
│   ├── policy.ts                 — interface Policy
│   ├── policy-builder.ts         — PolicyBuilder with fluent API
│   ├── retry-policy.ts           — RetryPolicy (maxAttempts, backoff strategy, jitter)
│   ├── timeout-policy.ts         — TimeoutPolicy (mandatory timeout)
│   ├── circuit-breaker-policy.ts — CircuitBreaker (closed → open → half-open)
│   ├── bulkhead-policy.ts        — Bulkhead (max concurrency)
│   ├── rate-limiter-policy.ts    — RateLimiter (token bucket / sliding window)
│   └── policy-composer.ts        — Compose policies (retry + timeout + circuit breaker)
│
├── web/
│   ├── problem-details.ts        — RFC 7807 ProblemDetails type (plain TS, no framework)
│   ├── problem-details-factory.ts — Factory for common problems (notFound, validation, conflict)
│   ├── pagination.ts             — PaginationParams, PaginatedResult<T>
│   ├── cursor-pagination.ts      — CursorPagination with encode/decode
│   └── request-context.ts        — Middleware-agnostic request context extractor interface
│
├── tenancy/
│   ├── tenant-context.ts         — TenantId, TenantContext
│   ├── tenant-resolver.ts        — interface TenantResolver (resolve from request)
│   └── tenant-strategy.ts        — TenantStrategy enum + strategy-specific contracts
│
└── index.ts
```

### Allowed Dependencies
```
@platform/core
  → @platform/foundation (errors, contracts, execution-context, serialization, config)
  → zod (validation schemas — canonical choice, no wrapper abstraction)
  → uuid (ID generation)
```

### Forbidden Dependencies
```
@platform/core
  ✗ @platform/messaging
  ✗ @platform/persistence
  ✗ @platform/distributed
  ✗ nestjs / express / fastify
  ✗ kafkajs / ioredis / prisma / typeorm
```

### Design Decisions
- **Zod as canonical validation library.** No abstraction wrapper. Shared schemas live in this package. Services import them directly.
- **Security split into `crypto/` (low-level) and `token/` (application-level).** Crypto primitives have zero business knowledge. TokenProvider deals with claims.
- **Web module contains RFC 7807 types only.** No exception mapping to NestJS/Express — that lives in framework-specific adapters.
- **Resilience policies are framework-agnostic.** CircuitBreaker tracks failures via callbacks, not HTTP interceptors.

### Extension Points
- `ILogger` → Winston, Pino, CloudWatch adapters
- `IMetrics` → Prometheus, DataDog adapters
- `ITracer` → OpenTelemetry, Jaeger, X-Ray adapters
- `IHealthCheck` → service-specific liveness/readiness probes
- `PasswordHasher` → Argon2, BCrypt adapters
- `Encryptor` → AES-256-GCM, AWS KMS adapters
- `TokenProvider<TClaims>` → JWT, PASETO adapters
- `TenantResolver` → HTTP header, JWT claim, subdomain adapters

---

## Package 3: @platform/messaging

### Responsibility
All messaging concerns — producing, consuming, routing, and orchestrating business processes via events. Depends on `@platform/foundation` and `@platform/core`.

### Contents

```
@platform/messaging/
├── envelope/
│   ├── message-envelope.ts       — MessageEnvelope<T> with full metadata
│   ├── envelope-builder.ts       — Fluent builder for envelopes
│   └── envelope-validator.ts     — Schema validation for envelopes
│
├── producer/
│   ├── message-producer.ts       — interface MessageProducer { publish(envelope): Promise<void> }
│   ├── domain-event-publisher.ts — interface DomainEventPublisher (in-process dispatch)
│   └── integration-event-publisher.ts — interface IntegrationEventPublisher (durable publish)
│
├── consumer/
│   ├── message-consumer.ts       — interface MessageConsumer { subscribe(handler): void }
│   ├── message-handler.ts        — type MessageHandler<T> = (envelope: MessageEnvelope<T>) => Promise<void>
│   └── consumer-config.ts        — ConsumerConfig (concurrency, batching, retry)
│
├── outbox/
│   ├── outbox-store.ts           — interface OutboxStore { append, poll, markProcessed }
│   ├── outbox-message.ts         — OutboxMessage type (id, envelope, status, createdAt)
│   ├── outbox-poller.ts          — configurable poller with backoff
│   └── outbox-relay.ts           — coordinates poll → publish → mark sequence
│
├── inbox/
│   ├── inbox-store.ts            — interface InboxStore { exists, record, markProcessed }
│   ├── inbox-guard.ts            — wraps handler with idempotency check
│   └── deduplication-strategy.ts — configurable TTL-based dedup cleanup
│
├── routing/
│   ├── message-router.ts         — type-based message routing
│   ├── dead-letter.ts            — interface DeadLetterStore { send, replay, list }
│   └── retry-strategy.ts         — per-message-type retry config (maxAttempts, backoff, dlq)
│
├── versioning/
│   ├── schema-version.ts         — SchemaVersion utility
│   ├── schema-registry.ts        — interface SchemaRegistry { getSchema, validate, isCompatible }
│   └── version-migration.ts      — VersionMigration interface (upcast old → new)
│
├── workflow/
│   ├── state-machine/
│   │   ├── state.ts              — State<TState, TEvent>
│   │   ├── transition.ts         — Transition<From, To, Event>
│   │   ├── state-machine.ts      — interface StateMachine<TState, TEvent>
│   │   └── state-machine-builder.ts — Fluent builder for state machine definitions
│   ├── process-manager/
│   │   ├── process-manager.ts    — abstract class ProcessManager<TState>
│   │   └── process-repository.ts — interface ProcessRepository<T>
│   └── saga/
│       ├── saga-definition.ts    — SagaDefinition (steps, compensations)
│       ├── saga-coordinator.ts   — interface SagaCoordinator { execute(saga): Promise<SagaResult> }
│       ├── saga-step.ts          — SagaStep<TData> with execute + compensate
│       └── saga-result.ts        — SagaResult (completed, compensating, failed, compensated)
│
└── index.ts
```

### Allowed Dependencies
```
@platform/messaging
  → @platform/foundation (errors, contracts, execution-context, serialization, config)
  → @platform/core (observability, resilience — for retry policies only)
```

### Forbidden Dependencies
```
@platform/messaging
  ✗ @platform/persistence
  ✗ @platform/distributed
  ✗ kafkajs / amqplib / @aws-sdk/client-sqs
```

### Design Decisions
- **Outbox and Inbox are FIRST-CLASS messaging modules.** They are NOT persistence patterns even though they use storage. The outbox exists to bridge transactional DB writes with message publishing. It depends on a storage interface (OutboxStore) that adapters implement — it does NOT import persistence packages.
- **DomainEventPublisher vs IntegrationEventPublisher are separate interfaces.** Domain events are in-process, synchronous, and fire-and-forget. Integration events are durable, async, and have delivery guarantees. Conflating them into one `MessageBus` is the #1 messaging anti-pattern.
- **Dead letter and retry are first-class concepts.** Every message type has a retry strategy (max attempts, backoff type, DLQ destination). The consumer must know what to do with poison messages.
- **SchemaRegistry is a messaging concern.** Versioned schemas are how producers and consumers agree on message format. Without it, message evolution breaks consumers silently.

### Extension Points
- `MessageProducer` → Kafka, RabbitMQ, SQS adapters
- `MessageConsumer` → Kafka, RabbitMQ, SQS adapters
- `OutboxStore` → PostgreSQL, MongoDB adapters
- `InboxStore` → PostgreSQL, MongoDB, Redis adapters
- `DeadLetterStore` → S3, database, dedicated Kafka topic adapters
- `SchemaRegistry` → Confluent Schema Registry, AWS Glue adapters
- `StateMachine` → XState, custom FSM adapters (interface allows swap)
- `SagaCoordinator` → Temporal, Camunda adapters (interface allows swap)

---

## Package 4: @platform/persistence

### Responsibility
Data access abstractions. Depends on `@platform/foundation` and `@platform/core`.

### Contents

```
@platform/persistence/
├── transaction/
│   ├── transaction-manager.ts    — interface TransactionManager { execute<T>(fn, options): Promise<T> }
│   ├── transaction-options.ts    — TransactionOptions (isolation level, timeout, readOnly)
│   └── transaction-context.ts    — TransactionContext (propagated via execution context)
│
├── unit-of-work/
│   ├── unit-of-work.ts           — interface UnitOfWork { registerNew, registerDirty, registerDeleted, commit, rollback }
│   └── unit-of-work-factory.ts   — interface UnitOfWorkFactory { create(): UnitOfWork }
│
├── specification/
│   ├── specification.ts          — interface Specification<T> (re-exported from foundation)
│   ├── composite-specification.ts — AndSpecification, OrSpecification, NotSpecification
│   └── specification-builder.ts  — Fluent builder for common compositions
│
├── optimistic-lock/
│   ├── version.ts                — Version type (monotonic number)
│   ├── concurrency-token.ts      — ConcurrencyToken (opaque token for CAS)
│   └── optimistic-lock-error.ts  — OptimisticLockError (extends ConflictError)
│
├── repository/
│   ├── repository.ts             — interface Repository<TAggregate, TId> (re-export from foundation)
│   ├── paginated-repository.ts   — interface PaginatedRepository<T> extends Repository
│   └── repository-registry.ts    — optional registry for repository factory lookup
│
└── index.ts
```

### Allowed Dependencies
```
@platform/persistence
  → @platform/foundation (errors, contracts, execution-context, serialization)
  → @platform/core (observability — for transaction logging/metrics)
```

### Forbidden Dependencies
```
@platform/persistence
  ✗ @platform/messaging
  ✗ @platform/distributed
  ✗ prisma / typeorm / sequelize / knex
  ✗ pg / mysql2 / mongodb
```

### Design Decisions
- **No Outbox/Inbox.** These are messaging patterns, moved to `@platform/messaging`. Persistence provides the storage interfaces, messaging uses them — but persistence does NOT import messaging.
- **TransactionManager is generic.** It supports both SQL transactions (`BEGIN/COMMIT/ROLLBACK`) and NoSQL transactions (MongoDB sessions). The `options` type is extensible but never leaks ORM-specific types.
- **Specification pattern is pure predicate composition.** No SQL generation, no query builder integration. Services compose specifications and pass them to repository implementations, which translate them to database queries.
- **UnitOfWork tracks entity state changes.** It is NOT a database transaction — it's a change tracker that feeds into a transaction. TransactionManager wraps UnitOfWork.

### Extension Points
- `TransactionManager` → Prisma, TypeORM, Knex, MongoDB adapters
- `UnitOfWorkFactory` → Prisma, TypeORM, MikroORM adapters
- `Repository<T>` → concrete repository implementations per service
- `Specification<T>` → service-specific business rule specifications

---

## Package 5: @platform/distributed

### Responsibility
Distributed systems coordination patterns. Depends on `@platform/foundation` and `@platform/core`.

### Contents

```
@platform/distributed/
├── lock/
│   ├── distributed-lock.ts       — interface DistributedLock { acquire(key, ttl, options): Promise<LockHandle> }
│   ├── lock-handle.ts            — LockHandle { release(), renew(), isExpired(), fencingToken }
│   └── lock-options.ts           — LockOptions (mandatory timeout, retry policy)
│
├── lease/
│   ├── lease.ts                  — interface Lease { acquire, renew, release, onExpired }
│   └── lease-manager.ts          — interface LeaseManager { createLease(resource, ttl): Lease }
│
├── fencing-token/
│   ├── fencing-token.ts          — FencingToken (monotonic number, included in every write)
│   └── fencing-token-provider.ts — interface FencingTokenProvider { nextToken(): FencingToken }
│
├── leader-election/
│   ├── leader-elector.ts         — interface LeaderElector { campaign, resign, isLeader, onLeadershipChange }
│   └── leadership-callback.ts    — LeadershipCallbacks (onElected, onOusted)
│
├── idempotency/
│   ├── idempotency-key.ts        — IdempotencyKey type (string with optional TTL)
│   ├── idempotency-store.ts      — interface IdempotencyStore { save, exists, getResult, remove }
│   └── idempotency-guard.ts      — wraps any operation with idempotency (check → execute → store result)
│
├── cache/
│   ├── cache-store.ts            — interface CacheStore { get, set, delete, exists, invalidate, getOrSet }
│   ├── cache-key-strategy.ts     — CacheKeyStrategy (key generation pattern)
│   ├── cache-options.ts          — CacheOptions (TTL, stampede protection, serialization)
│   └── cache-stampede-guard.ts   — Stampede protection (single-flight for getOrSet)
│
├── consistency/
│   ├── compare-and-swap.ts        — CAS operation contract
│   ├── etag.ts                    — ETag generation and validation
│   └── conflict-resolution.ts     — ConflictResolutionStrategy interface
│
├── scheduler/
│   ├── scheduler.ts              — interface Scheduler { schedule, cancel, list }
│   ├── job.ts                     — Job<TData> definition (schedule, payload, idempotency key)
│   ├── distributed-job.ts         — DistributedJob extends Job (ensures single execution across instances)
│   └── job-store.ts              — interface JobStore { save, load, markComplete, listPending }
│
├── feature-flags/
│   ├── feature-flag-provider.ts  — interface FeatureFlagProvider { isEnabled, getValue, onUpdate }
│   ├── feature-flag.ts           — FeatureFlag type (key, defaultValue, rules)
│   └── flag-evaluation-context.ts — EvaluationContext (userId, tenantId, attributes)
│
└── index.ts
```

### Allowed Dependencies
```
@platform/distributed
  → @platform/foundation (errors, execution-context, serialization, config)
  → @platform/core (observability — for lock/cache metrics, resilience — for retry/timeout policies)
```

### Forbidden Dependencies
```
@platform/distributed
  ✗ @platform/messaging
  ✗ @platform/persistence
  ✗ ioredis / redis
  ✗ zookeeper / consul
  ✗ launchdarkly / openfeature SDKs
```

### Design Decisions
- **DistributedLock.acquire() requires a mandatory timeout at the type level.** `acquire(key: string, ttl: number, options: LockOptions): Promise<LockHandle>` — `ttl` is NOT optional. A lock without a TTL is a production outage waiting for a GC pause.
- **FencingToken is a first-class concept.** Every lock handle includes a fencing token (monotonic integer). Every write to a shared resource includes the fencing token. The resource rejects writes with stale tokens. This prevents the "stale lock holder" problem definitively.
- **CacheStore.getOrSet() MUST document stampede protection behavior.** The interface contract must specify whether concurrent getOrSet calls for the same key result in one or multiple executions. The default implementation provides single-flight protection.
- **Scheduler distinguishes at-most-once from at-least-once.** `DistributedJob` guarantees exactly-one execution across instances (via distributed lock). `Job` makes no such guarantee.
- **Feature flags could live in @platform/core.** They're placed here because they solve a distributed configuration propagation problem. A thin re-export from @platform/core is recommended for ergonomics.

### Extension Points
- `DistributedLock` → Redis (Redlock), PostgreSQL (advisory locks), ZooKeeper, Consul adapters
- `LeaderElector` → ZooKeeper, Consul, Kubernetes Lease adapters
- `FencingTokenProvider` → Redis INCR, PostgreSQL sequence adapters
- `IdempotencyStore` → Redis, PostgreSQL, DynamoDB adapters
- `CacheStore` → Redis, Memcached, in-memory (testing) adapters
- `Scheduler` → BullMQ, node-cron, AWS EventBridge adapters
- `FeatureFlagProvider` → LaunchDarkly, OpenFeature, local config adapters

---

## Dependency Graph

```
                    ┌─────────────────────────┐
                    │  @platform/foundation    │
                    │  (zero dependencies)     │
                    └───────────┬─────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
   │ @platform/core │  │@platform/      │  │@platform/      │
   │                │  │messaging       │  │persistence     │
   └───────┬────────┘  └───────┬────────┘  └───────┬────────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │ @platform/distributed    │
                    └─────────────────────────┘
```

**Key rules:**
- `@platform/foundation` has **zero internal dependencies**
- `@platform/core`, `@platform/messaging`, and `@platform/persistence` depend **only** on `@platform/foundation`
- `@platform/distributed` depends on `@platform/foundation` **and** `@platform/core`
- **No package depends on a sibling** — `@platform/messaging` does NOT import `@platform/persistence`
- Cross-package communication happens through interfaces defined in `@platform/foundation`

### Dependency Inversion for Outbox/Inbox

The outbox pattern requires storage but is a messaging concern. Resolution:
1. `@platform/foundation` defines `OutboxStore` and `InboxStore` interfaces
2. `@platform/messaging` uses these interfaces (depends on foundation, not persistence)
3. Adapters (e.g., `@platform/adapters/postgres-outbox`) implement `OutboxStore` using PostgreSQL
4. Adapters are injected at runtime — no compile-time coupling

```
@platform/foundation       defines OutboxStore (interface)
        ↑
        │ implements
        │
@platform/adapters/        implements OutboxStore with PostgreSQL
postgres-outbox/

@platform/messaging        uses OutboxStore (depends on foundation only)
```

---

## Ownership Boundaries

| Package | Owner Team | Review Required | Breaking Change Policy |
|---------|-----------|----------------|----------------------|
| foundation | Platform Architecture | 3 approvers | 6-month deprecation period, semver major |
| core | Platform Architecture | 2 approvers | 3-month deprecation period, semver major |
| messaging | Platform Architecture | 2 approvers | 3-month deprecation period, semver major |
| persistence | Platform Architecture | 2 approvers | 3-month deprecation period, semver major |
| distributed | Platform Architecture | 2 approvers | 3-month deprecation period, semver major |
| adapters/* | Feature Teams | 1 platform approver | Adapter-specific |

---

## Evolution Strategy

### Phase 1: Foundation (Month 1-2)
Ship `@platform/foundation` first. Without errors, contracts, execution context, serialization, and config — nothing else can be built. Every service can adopt foundation immediately with zero risk (it has no dependencies).

### Phase 2: Core (Month 2-3)
Ship `@platform/core`. Services adopt logging, metrics, tracing, health checks, and validation schemas. Resilience policies are optional — services opt in.

### Phase 3: Messaging + Persistence (Month 3-5)
Ship in parallel. These are independent packages. Services adopt the package relevant to their role (message consumers adopt messaging, database services adopt persistence, some adopt both).

### Phase 4: Distributed (Month 5-6)
Ship last. Built on stable foundation + core. Services adopt lock, cache, idempotency, and feature flags as needed.

### Backward Compatibility
- `@platform/foundation` v1 is supported for 12 months after v2 release
- All other packages: 6 months
- Adapters must support at least 2 major versions of their platform package
- Deprecation notices via `@deprecated` JSDoc tags + runtime warnings in non-production
