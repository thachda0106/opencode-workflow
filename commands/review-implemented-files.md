---
description: Review implemented changes as a Principal Engineer — correctness, security, architecture, performance, error handling, tests — with evidence labels and a merge verdict
agent: code-reviewer
subtask: false
---

# Review Implemented Files

Review changes produced by any agent. Read-only: find problems, do not fix them.
No approval gates — a review is analysis, not a mutation. Produce the review in one pass.

## 1. Load

Scope override: **$ARGUMENTS** (empty = the uncommitted diff).

```bash
git diff --name-status            # uncommitted
git diff --stat HEAD~1            # last commit
git log --oneline -5
```

Read every changed file in full. Read `.ai/knowledge/plans/*.md` if a plan exists for this change —
the plan defines intended behaviour, and a mismatch is a finding, not an opinion.

## 2. Depth by risk

Load `map-critical-paths` and rank the changed paths. Then:

| Tier | Review depth |
|------|--------------|
| A | every dimension below, plus a hand-trace of the main path, plus a concurrency and rollback question |
| B | dimensions 1–4 and 7 |
| C | skim for correctness and convention violations only |

Do not run the full checklist over boilerplate. Say which paths you reviewed at which depth.

## 3. Dimensions

1. **Correctness** — matches plan? logic errors? off-by-one, null/undefined, type mismatch?
   boundary conditions (empty, zero, max, single item)? state transitions complete?
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
7. **Tests** — do they assert behaviour or implementation? failure paths covered? asserts on
   real values, not on mocks echoing themselves? would they fail if the feature broke?

## 4. Evidence labels

Every finding carries one:

```
CONFIRMED   reproduced by reading the exact code path, file:line cited
LIKELY      pattern strongly suggests it, but depends on runtime config or caller behaviour
QUESTION    needs the author's intent before it is a finding
```

A finding without a `file:line` is not a finding. Do not pad the list.

## 5. Severity

| Level | Meaning |
|-------|---------|
| **MUST_FIX** | bug, security hole, data corruption, invariant violation, broken migration |
| **SHOULD_FIX** | architecture violation, missing error handling, performance risk, missing failure-path test |
| **OPTIONAL** | readability, naming, test structure |

## 6. Verdict

```
APPROVED               no MUST_FIX, no SHOULD_FIX
APPROVED_WITH_COMMENTS no MUST_FIX, SHOULD_FIX tracked
CHANGES_REQUESTED      any MUST_FIX
```

Green tests do not upgrade the verdict. Say which behaviour is covered by tests and which is
merely assumed — that distinction is the most valuable thing a review can state.

## 7. Output

Write `review-implementation.md` at repo root (or `docs/reviews/<date>-<slug>.md` if the repo
keeps reviews):

```markdown
# Review — <change>
Tier: <A/B/C per path> · Scope: <n> files
Verdict: <...>

## Findings
| # | Sev | Evidence | File:line | Finding | Why it matters |
|---|-----|----------|-----------|---------|----------------|

## What tests actually cover
<scenario → test name>

## What is assumed, not verified
<list>

## Questions for the author
<list>
```

Chat output: ≤12 lines — verdict, counts by severity, the 1–3 findings that matter, the top
assumption. Do not paste the report.

## Rules

- Report, never fix. If asked to fix, that is a separate task with its own tier.
- Never restate the diff. The author knows what they wrote.
- No style opinions unless the project has a written rule about them.
- If the change is too large to review meaningfully (>400 changed lines), say so and propose a
  split — reviewing it superficially is worse than refusing.
