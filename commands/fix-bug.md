---
description: Systematically diagnose and fix bugs through the engineering-ownership lifecycle — mode routing, root-cause evidence, gated fix plan, verification
agent: bug-hunter
subtask: false
---

# Fix Bug

Diagnose first; fix only after the cause is evidence-backed. The mode table and gate rules live in
`AGENTS.md`.

## 0 · CLASSIFY

Bug to diagnose: **$ARGUMENTS** (if empty, ask for the symptom and stop).

```
Mode: Standard (T1) — trigger: one module, 4 files, no critical surface
Scope lock: src/orders/**; not touching payments.
Re-tier point: the fix needs a migration or touches authz.
```

- Lightweight (T0): ≤2 files, localized, no critical surface → direct fix, verify, one-line note.
- Standard (T1): one module, 2–6 files → Gates 1–3.
- Full (T2): authz, money, transaction, migration, concurrency, external contract, >6 files, or
  >1 module → Gates 1–4.

## 1 · INVESTIGATE

No code changes in this phase.

1. Read the bug description/error message carefully.
2. Identify affected functionality and reproduction steps.
3. Check whether it is a regression (`git blame` / `git log`).
4. Use the stack trace to find the source, or trace forward from the entry point.
5. Search for relevant code patterns and related modules/layers.
6. Diagnose the root cause — categorize it:
   - Request lifecycle: middleware, guards, interceptors.
   - Dependency injection: missing providers, circular dependencies.
   - Database/ORM: query errors, mapping, migration problems.
   - Types: mismatches, null/undefined, incorrect assertions.
   - Async: unhandled promises, race conditions.
   - Validation: missing or incorrect checks.
   - API/data: wrong endpoint, format, or error handling.
7. Separate observation from hypothesis. Cite `file:line` for observations.
8. Write findings to `.ai/work/<slug>/scratchpad.md`: symptom, evidence, root cause, impact,
   assumptions, open questions, alternatives considered.

**Lightweight:** use a short inline investigation; no artifact. If the cause is not evidence-backed,
promote to Standard.

**GATE 1 — Standard/Full.** Present findings, evidence, assumptions, risks, scope. Require
`APPROVE GATE 1`.

## 2 · PLAN

Write `.ai/work/<slug>/plan.md`: minimal change, side effects, edge cases, files, risk of breaking
other features, verification strategy, rollback, rejected alternative, non-goals, acceptance
criteria.

**GATE 2 — Standard/Full.** Present decisions and trade-offs. Require `APPROVE GATE 2`.

## 3 · TASKS

Write `.ai/work/<slug>/tasks.md`: ordered fix steps, regression test, acceptance criteria,
verification command, risk, plan-decision reference. Every step is independently checkable.

**GATE 3 — Standard/Full.** Present tasks, dependencies, order, risk. Require `APPROVE GATE 3`.

## 4 · IMPLEMENTATION FLOWS

Mandatory for Full. Mandatory for Standard when the fix changes runtime behavior; use a compact
flow showing the failing path before the fix and the corrected path after it. Skip only for a pure
rename or non-behavioral change, and state why.

Load `design-implementation-flows` and write `.ai/work/<slug>/implementation-flows.md`. No source
changes before it exists.

## 5 · IMPLEMENT

- Make targeted changes only.
- Match existing code style and patterns.
- Add a regression test that fails before the fix and passes after it.
- Update callers if a signature changes.
- No unrelated refactoring, formatting sweeps, or dependency bumps.

## 6 · VERIFY

- Reproduce the original bug scenario; confirm it is fixed.
- Run the regression test.
- Run targeted tests, then the project's typecheck/lint/build.
- Full mode: full suite + `stress-test-implementation`.
- Report `not run` for anything that could not run; never report it as passed.

## 7 · REVIEW AND KNOWLEDGE

- Standard: final summary with verification evidence, deviations, remaining risks.
- Full: write `.ai/work/<slug>/review.md`; wait for `APPROVE GATE 4`.
- Standard knowledge: `.ai/knowledge/features/<slug>/README.md` + `full-flow.md` when behavior
  changed; otherwise a short note.
- Full knowledge: all four package files.
- Add a gotcha to `.ai/knowledge/gotchas.md` if diagnosis took >15 minutes.

End with the completion block from `/ai-workflow`.
