---
description: Create a feature module through the engineering-ownership lifecycle — mode routing, gated artifacts, implementation flows, verification, knowledge package
agent: feature-builder
subtask: false
---

# Create Feature

Add a module/component that looks like it was always there. Effort and gates scale with
consequence. The mode table and gate rules live in `AGENTS.md`.

## 0 · CLASSIFY

Feature to build: **$ARGUMENTS** (if empty, ask for the feature name and stop).

```
Mode: Standard (T1) — trigger: new feature path in orders module, 5 files, no critical surface
Scope lock: src/orders/**; not touching payments.
Re-tier point: a schema change or authz rule appears.
```

T2 triggers are in `AGENTS.md` (a new table is T2; a new authz rule is T2; an endpoint that moves
money is T2). Say which mode and why.

## 1 · INVESTIGATE — Standard and Full

Write `.ai/work/<slug>/scratchpad.md`.

- Ask only what changes the design. Default set, drop any the request already answers:
  1. Entity fields and the invariants they must satisfy.
  2. Endpoints or interface, and who is allowed to call them.
  3. Relationships with existing modules — read or write, cascade behavior.
  4. What must not break: existing callers, existing rows, existing clients.
- Find the reference implementation:
  - `analyze-project-structure` for module layout and naming.
  - `locate-code-patterns` for a sibling module with the same shape.
  - Name it: "Following `src/billing/**` — same layering, same DTO/validation style."
- No new pattern without a stated reason. No new abstraction for a single use.

**GATE 1 — WAIT.** Present findings, evidence, assumptions, risks, scope. Require explicit
`APPROVE GATE 1`.

## 2 · PLAN — Standard and Full

Write `.ai/work/<slug>/plan.md`.

Every plan states: invariants with IDs, migration strategy (if schema changes), transaction
boundaries, failure modes, security, rollback, verification, non-goals, acceptance criteria, and
the rejected alternative.

**GATE 2 — WAIT.** Present decisions and trade-offs. Require explicit `APPROVE GATE 2`. Freeze
the plan baseline.

## 3 · TASKS — Standard and Full

Write `.ai/work/<slug>/tasks.md`. Layer order, so each task is independently checkable:

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
- Every task references the plan decision or invariant it implements.

**GATE 3 — WAIT.** Present tasks, dependencies, order, risk. Require explicit `APPROVE GATE 3`.

## 4 · IMPLEMENTATION FLOWS — Standard and Full

Mandatory for Full. Mandatory for Standard when the feature alters runtime behavior; use a compact
flow (one flowchart plus the primary failure path). Skip only for a pure refactor/rename with
identical behavior, and state why.

Load `design-implementation-flows` and write `.ai/work/<slug>/implementation-flows.md`. No source
changes before it exists. If flows contradict the plan or expose a new decision, return to Gate 2.

## 5 · BUILD

Implement in task order. No silent reordering.

## 6 · TEST + VERIFY

- Unit tests: service rules, including one failure path per rule.
- Integration test: the endpoint against the real database (or the project's standard substitute).
- Run: typecheck · lint · targeted tests · full suite.
- Full mode: load `stress-test-implementation` and reconcile the implementation flows.

## 7 · REVIEW

- Standard: final summary with verification evidence, deviations, updated flows, remaining risks.
- Full: write `.ai/work/<slug>/review.md` and wait for `APPROVE GATE 4`.
- If Standard deviates from the plan or risk escalates, promote to Full and run Gate 4.

## 8 · KNOWLEDGE

- Standard: `.ai/knowledge/features/<slug>/README.md` + `full-flow.md`.
- Full: all four package files.
- Use `transfer-implementation-knowledge`; update `.ai/knowledge/index.md`.

End with the completion block from `/ai-workflow`.

## Definition of done

- [ ] Mode and trigger stated; re-tier point stated
- [ ] Gates 1–3 approved for Standard; Gates 1–4 for Full
- [ ] Implementation flows exist before code when behavior changes
- [ ] Matches the reference module's shape; no invented pattern
- [ ] Invariants from §1 hold and are asserted by a test
- [ ] Migration is backward compatible (or the incompatibility is stated explicitly)
- [ ] Failure modes answered with evidence labels
- [ ] Knowledge package written; `.ai/knowledge/index.md` updated
