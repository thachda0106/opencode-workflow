---
name: map-critical-paths
description: Rank changed or existing code paths by ownership risk so review effort goes where consequences are real. Use after implementation, before merging, or when onboarding to an unfamiliar module — not for whole-repo audits.
metadata:
  layer: knowledge
  stage: post-implementation
---


# Skill: map-critical-paths

Produce a ranked, evidence-backed list of the code paths that deserve the engineer's own
attention. The output is a decision aid, not documentation: it answers *"where would being
wrong hurt most, and where do I start reading?"*

## When to use

- After a multi-file implementation (T2, or T1 touching a shared path).
- Before merging anything where a silent failure is plausible.
- When taking ownership of an existing module you did not write.
- Not for: style review, test coverage reports, whole-repo architecture surveys
  (use `analyze-project-structure`).

## Procedure

### 1. Scope

Pick exactly one scope and say it:

| Scope | Source |
|-------|--------|
| Changed code | `git diff --name-status origin/main...HEAD` (or `HEAD` if uncommitted) |
| One module | directory the user named |
| One flow | entry point the user named — trace with `trace-execution-flow` first |

### 2. Enumerate candidate paths

A **path** is one trigger → one terminal effect. Examples: `POST /orders → order row + outbox event`,
`payment webhook → ledger update + email`, `cron sweep → stale session delete`.

Aim for 3–8 paths. If you find more than 8, group by entry point and rank the groups.
Do **not** create a path for: pure DTO/type files, controller method-signature mapping,
config values, CSS, test fixtures, generated code.

### 3. Score each path

Nine dimensions, 0/1/2 each. Score only what you can point at in the code — a score without a
`file:line` is a guess and must be marked `?`.

| # | Dimension | 0 | 1 | 2 |
|---|-----------|---|---|---|
| 1 | Business consequence | cosmetic/internal | feature degraded | money, access, legal, data loss |
| 2 | Transaction boundary | none | single write | multi-write / multi-table / outbox |
| 3 | Concurrency | single-threaded by construction | possible overlap | genuinely concurrent or queued |
| 4 | Authorization | no identity involved | role check only | object-level ownership / tenancy |
| 5 | External I/O | none | one dependency | 2+ dependencies or non-idempotent calls |
| 6 | Data consistency | read-only | additive write | update/delete, derived state, idempotency needed |
| 7 | Error propagation | throws to framework handler | caught and mapped | swallowed, retried, or compensated |
| 8 | Performance sensitivity | O(1)-ish | O(n) over bounded n | unbounded n, N+1, hot path |
| 9 | State complexity | stateless | one flag/status | multi-state machine or partial-failure states |

**Promotion rule:** if dimension 2, 3, 4, or 6 scores 2, the path is **Tier A** regardless of total.
Consequence-dense surfaces do not average out.

```
Tier A: sum ≥ 10  or  promotion rule hit
Tier B: sum 5–9
Tier C: sum ≤ 4
```

### 4. For each Tier A and B path, capture four things

1. **Debug entry point** — the exact file:line where you would put the first breakpoint or log.
2. **Invariant** — the one sentence that must stay true (e.g. "order.total == sum(items) before
   the outbox row is written").
3. **Manual verification step** — the concrete command/query a human can run to prove it holds
   (a `psql` query, a curl, a specific test).
4. **What breaks silently** — the failure that leaves no error: missing event, stale cache,
   double charge, orphan row.

### 4a. Flow and review priority

The ranking decides how much visual and review effort each path deserves. Do not apply the same
depth everywhere.

| Tier | Implementation flows | Review depth | Stress pass | Ownership |
|------|---------------------|--------------|-------------|-----------|
| **A** | Mandatory flowchart + sequence/state as applicable | All dimensions, hand-trace, concurrency, rollback | Mandatory | Level 3 |
| **B** | Flowchart if it materially clarifies behavior | Correctness, bugs, security, architecture, tests | If write/state/external | Level 2 |
| **C** | None | Correctness and conventions | Lightweight | Level 1 |

Every Tier A path must appear in `.ai/work/<slug>/implementation-flows.md` and in the feature's
`full-flow.md`. If a Tier A path cannot be represented, state why and record the gap.

### 5. Output

Table, ranked by tier then sum:

```
| # | Path | Entry | Score | Tier | Dominant risk | Debug entry | Manual check |
```

Below the table, one line per Tier A path:

```
<path> — invariant: <...> · silent failure: <...> · verify: <command>
```

### 6. Persist

Merge into `.ai/knowledge/critical-paths.md`:

- Existing path still valid → leave it.
- Path changed → update its row in place, do not append a second row.
- Path removed → mark `(removed YYYY-MM-DD)`, keep one release cycle.
- Add one line to `.ai/knowledge/index.md` if the file is new.

## Worked example (NestJS + PostgreSQL)

Changed: `src/orders/**`, `src/payments/webhook.controller.ts`.

```
| # | Path                            | Entry                                   | Score | Tier | Dominant risk        | Debug entry                              | Manual check                              |
| 1 | gateway webhook → ledger + order | payments/webhook.controller.ts:41       | 15    | A    | duplicate settlement | webhook.controller.ts:63 (idempotency key) | replay same event id twice → 1 ledger row |
| 2 | checkout → order + outbox        | orders/order.service.ts:112             | 13    | A    | partial commit       | order.service.ts:131 (tx begin)          | kill app mid-tx → 0 orders, 0 events      |
| 3 | GET /orders/:id                  | orders/order.controller.ts:22           | 6     | B    | object-level authz   | order.service.ts:44                      | fetch another tenant's id → 404           |
```

Tier A #2: invariant `order.outbox_event written iff order row committed` · silent failure
`order created, event lost → fulfillment never runs` · verify `select count(*) from outbox where
aggregate_id = '<id>'` after a forced rollback.

## Decision rules

- Unreadable region → mark the dimension `?` and add one line to "What I could not score".
  Never invent a score to fill the table.
- Two paths with identical scores → rank by business consequence, then by concurrency.
- Boilerplate CRUD with no authz and no state → Tier C even if it is 200 lines. Volume is not risk.
- If every path is Tier A, the scoring was too generous. Re-read dimensions 1, 2, 6.

## Non-goals

- Fixing anything, or opening findings as review comments (that is `review-implemented-files`).
- Benchmarking. "Performance sensitive" is a judgement from shape (unbounded loops, N+1),
  not a measurement.
- Exhaustive security audit.
- Explaining how each path works — that is `transfer-implementation-knowledge`.
