---
description: Review implemented changes and Gate 4 evidence — correctness, security, architecture, performance, error handling, tests, plan/task/flow compliance, with evidence labels and a merge verdict
agent: code-reviewer
subtask: false
---

# Review Implemented Files

Review changes produced by any agent. Read-only: find problems, do not fix them. A review is
analysis, not a mutation, so there are no approval gates before producing it.

## 1. Load

Scope override: **$ARGUMENTS** (empty = the uncommitted diff).

```bash
git diff --name-status            # uncommitted
git diff --stat HEAD~1            # last commit
git log --oneline -5
```

Read every changed file in full. Read the change's planning artifacts:

- `.ai/work/<slug>/plan.md` — approved decisions and invariants.
- `.ai/work/<slug>/tasks.md` — execution contract.
- `.ai/work/<slug>/implementation-flows.md` — intended behavior.
- `.ai/knowledge/features/<slug>/full-flow.md` if it already exists.

A mismatch between the approved plan/tasks/flows and the code is a finding, not an opinion.

## 2. Depth by risk

Load `map-critical-paths` and rank the changed paths. Then:

| Tier | Review depth |
|------|--------------|
| A | Every dimension below, plus a hand-trace of the main path, plus concurrency and rollback questions, plus flow reconciliation |
| B | Dimensions 1–4 and 7, plus flow reconciliation if a flow exists |
| C | Skim for correctness and convention violations only |

Do not run the full checklist over boilerplate. Say which paths you reviewed at which depth.

## 3. Dimensions

1. **Correctness** — matches approved decisions and invariants? logic errors? off-by-one,
   null/undefined, type mismatch? boundary conditions (empty, zero, max, single item)? state
   transitions complete?
2. **Bugs** — races on shared rows, locks taken in different orders, resource leaks (connections,
   file handles, listeners), unbounded loops, unhandled rejections, missing cleanup on throw.
3. **Security** — trust-boundary input validated? injection (SQL/command/template)? authz checked
   at object level, not just role? secrets in code or logs? path traversal? mass-assignment?
4. **Architecture** — follows existing patterns (name the pattern file)? layer violations
   (domain logic in controller, repository in controller)? circular imports? new abstraction
   justified, or abstraction for one caller?
5. **Performance** — N+1 queries, missing index for a new predicate, unbounded `findMany`,
   work inside a loop that belongs outside, sync I/O on a hot path.
6. **Error handling** — exceptions caught at the right level (not swallowed)? mapped to correct
   status codes? user-safe messages? transaction rolled back on error? retry-safe?
7. **Tests** — do they assert behavior or implementation? failure paths covered? asserts on real
   values, not on mocks echoing themselves? would they fail if the feature broke?
8. **Plan/task/flow compliance** — every approved task is implemented or explicitly deferred; the
   implementation flow matches the code; deviations are recorded; diagrams are updated.

## 4. Flow reconciliation

For every Tier A path:

1. Compare the actual code with `implementation-flows.md` and `full-flow.md`.
2. Change `[P]` to `[V]` only with evidence.
3. Record deviations: planned → actual → reason.
4. A Tier A path with no diagram, or a diagram that contradicts the code, is a finding.

## 5. Evidence labels

Every finding carries one:

```
CONFIRMED   reproduced by reading the exact code path, file:line cited
LIKELY      pattern strongly suggests it, but depends on runtime config or caller behaviour
QUESTION    needs the author's intent before it is a finding
```

A finding without a `file:line` is not a finding. Do not pad the list.

## 6. Severity

| Level | Meaning |
|-------|---------|
| **MUST_FIX** | bug, security hole, data corruption, invariant violation, broken migration, plan decision violated |
| **SHOULD_FIX** | architecture violation, missing error handling, performance risk, missing failure-path test, stale flow |
| **OPTIONAL** | readability, naming, test structure |

## 7. Verdict

```
APPROVED               no MUST_FIX, no SHOULD_FIX
APPROVED_WITH_COMMENTS no MUST_FIX, SHOULD_FIX tracked
CHANGES_REQUESTED      any MUST_FIX
```

Green tests do not upgrade the verdict. Say which behavior is covered by tests and which is merely
assumed — that distinction is the most valuable thing a review can state.

## 8. Output

Write `.ai/work/<slug>/review.md` for a gated change; otherwise write
`review-implementation.md` at repo root (or `docs/reviews/<date>-<slug>.md` if the repo keeps
reviews).

```markdown
# Review — <change>
Mode: <Lightweight/Standard/Full> · Tier: <A/B/C per path> · Scope: <n> files
Verdict: <...>

## Findings
| # | Sev | Evidence | File:line | Finding | Why it matters |
|---|-----|----------|-----------|---------|----------------|

## Plan/task/flow compliance
| Item | Status | Evidence |
|------|--------|----------|

## Deviations
| Planned | Actual | Reason | Approved? |
|---------|--------|--------|-----------|

## What tests actually cover
<scenario → test name>

## What is assumed, not verified
<list>

## Remaining risks
<list>

## Questions for the author
<list>
```

Chat output: ≤12 lines — verdict, counts by severity, the 1–3 findings that matter, the top
assumption. Do not paste the report.

## 9. Gate 4 hand-off

For Full work, the review is the evidence for Gate 4. Present:

- Verdict and findings.
- Verification commands actually run and their results.
- Deviations and whether they were approved.
- Updated implementation flows and knowledge links.
- Remaining risks.

Wait for explicit `APPROVE GATE 4` before marking the workflow complete.

## Rules

- Report, never fix. If asked to fix, that is a separate task with its own mode and gates.
- Never restate the diff. The author knows what they wrote.
- No style opinions unless the project has a written rule about them.
- If the change is too large to review meaningfully (>400 changed lines), say so and propose a
  split — reviewing it superficially is worse than refusing.
