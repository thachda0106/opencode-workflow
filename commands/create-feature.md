---
description: Create a feature module — risk-tiered, following existing architecture, with post-implementation knowledge transfer
agent: feature-builder
subtask: false
---

# Create Feature

Add a module/component that looks like it was always there. Gates scale with risk.

## 0 · CLASSIFY

Feature to build: **$ARGUMENTS** (if empty, ask for the feature name and stop).

```
Tier: T1 — new feature path in orders module, 5 files, no critical surface
```

Print the tier. T2 triggers are in `AGENTS.md` (a new table is T2; a new authz rule is T2;
a new endpoint that moves money is T2).

## 1 · REQUIREMENTS + PATTERN

Ask only what changes the design. Default set, drop any the request already answers:

1. Entity fields and the invariants they must satisfy.
2. Endpoints or interface, and who is allowed to call them.
3. Relationships with existing modules — read or write, cascade behaviour.
4. What must not break: existing callers, existing rows, existing clients.

Then find the reference implementation:

- `analyze-project-structure` for module layout and naming.
- `locate-code-patterns` for a sibling module with the same shape.
- Name it: "Following `src/billing/**` — same layering, same DTO/validation style."

No new pattern without a stated reason. No new abstraction for a single use.

## 2 · PLAN

**T1** — inline, ≤6 lines: files · layering · verification.

**T2** — plan artifact per `/ai-workflow` Phase 2, then **STOP for approval**.

Every plan states: migration strategy (if schema changes), transaction boundaries, and what
happens to in-flight data.

## 3 · BUILD

Layer order, so each step is independently checkable:

1. Model/entity + migration
2. DTOs / schemas + validation at the trust boundary
3. Repository / data access
4. Service (business rules, transaction boundary, state transitions)
5. Controller / handler (thin: map input, call service, map errors)
6. Module wiring + registration
7. Tests

Rules:
- Controllers contain no business rules. If a branch is about the domain, it belongs in the service.
- Transactions wrap exactly the invariant — not the HTTP call, not the validation.
- Errors: framework-standard exception types, mapped once, no stack traces to clients.
- No repository call outside the service layer unless the existing codebase already does it that way.

## 4 · TEST + VERIFY

- Unit tests: service rules, including one failure path per rule.
- Integration test: the endpoint against the real database (or the project's standard substitute).
- Run: typecheck · lint · targeted tests · full suite.

## 5 · FAILURE PASS — T2, or any write path

Load `stress-test-implementation`. At minimum answer: transaction boundary, concurrency on the
same row, retry safety, migration compatibility during a rolling deploy, object-level authorization.

## 6 · KNOWLEDGE

- T1: 6–10 line note → `.ai/knowledge/features/<slug>.md` (what · why · non-obvious detail ·
  debug entry point).
- T2: full `transfer-implementation-knowledge` report + `map-critical-paths` ranking.

End with the completion block from `/ai-workflow`.

## Definition of done

- [ ] Matches the reference module's shape; no invented pattern
- [ ] Invariants from §1 hold and are asserted by a test
- [ ] Migration is backward compatible (or the incompatibility is stated explicitly)
- [ ] Failure modes answered with evidence labels
- [ ] Knowledge note written; `.ai/knowledge/index.md` updated
