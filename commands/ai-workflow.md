---
description: Master workflow — risk-tiered lifecycle from classification to verified, understood delivery
---

# AI Workflow — Classify → Investigate → Plan → Implement → Verify → Transfer

This is the default lifecycle for non-trivial work. Effort scales with risk, not with the
number of files touched. The tier table and its rules live in `AGENTS.md`; this file is the
execution sequence.

> The old three-gate model (SCRATCHPAD → PLAN → TASKS, three hard stops for every task) is
> retired for day-to-day work. It survives only where a phase document genuinely warrants it:
> `/build-minimum-system`, `/build-large-system`, `/design-platform-core`.

---

## 0 · CLASSIFY

Print one line before anything else:

```
Tier: T2 — trigger: transaction boundary (src/orders/order.service.ts)
```

Triggers are objective. If you cannot name one from the AGENTS.md table, the task is T1.

Also decide now, and say it:

- **Scope lock**: which directories/files are in play. Anything outside them is out of scope.
- **Re-tier point**: what would force a re-classification (schema change appears, authz found).

---

## 1 · INVESTIGATE

No code, no plan text yet.

1. Trace the existing path end to end:
   `analyze-project-structure` for layout, `trace-execution-flow` for the specific path,
   `locate-code-patterns` for "how is this already done elsewhere".
2. Find the pattern to follow. Name the file you are copying the shape from. A new pattern in an
   established codebase needs a reason.
3. Read the invariants: what must remain true after this change (counts, totals, state transitions,
   tenant isolation).
4. Write down what you could not determine. Unresolved unknowns become plan risks, not silent guesses.

**T0** → skip to Phase 4.

---

## 2 · PLAN

**T1** — inline in the reply, ≤6 lines: files · shape of each change · verification command.

**T2** — artifact at `.ai/knowledge/plans/<slug>.md`, ≤40 lines:

```markdown
# <feature> — plan
Tier: T2 · trigger: <...>
Objective: <one sentence>
Invariants that must hold: <1-3 bullets>
Approach: <the design, 3-6 lines>
Rejected alternative: <what and why not>
Files: <path — change>
Steps: <ordered, verifiable each>
Failure modes: <what the design does when X fails>
Verification: <commands + scenarios>
Non-goals: <explicit>
```

Then **STOP**:

```
Plan ready at .ai/knowledge/plans/<slug>.md
Trade-off taken: <one line>. Rejected: <one line>.
Approve to implement, or tell me what to change.
```

No implementation code in this phase. No second artifact (no separate TASKS file — the plan's
step list is the task list).

---

## 3 · IMPLEMENT

Follow the approved plan. During implementation:

- Match existing code shape exactly; a reviewer should not be able to tell who wrote it.
- One step at a time, in plan order. Do not reorder silently.
- If reality contradicts the plan: **stop**, three lines on what changed, wait for my word.
- If the change grows past the plan (new file outside scope, new dependency, destructive step):
  stop before doing it.

Commit hygiene: no unrelated files, no formatting sweeps, no dependency bumps.

---

## 4 · VERIFY

Run what exists, in this order, and quote results:

```bash
# whichever of these the project actually has
npm run typecheck        # or: npx tsc --noEmit
npm run lint
npm test -- <pattern>
npm run build
```

| Tier | Minimum |
|------|---------|
| T0 | typecheck + build |
| T1 | + targeted tests |
| T2 | + full suite, + `stress-test-implementation` pass |

A failing check is reported, not explained away. A check that could not run is reported as
`not run`, never as `passed`.

---

## 5 · TRANSFER

| Tier | Output |
|------|--------|
| T0 | one line in chat: what changed |
| T1 | 6–10 line note → `.ai/knowledge/features/<slug>.md` |
| T2 | `transfer-implementation-knowledge` report + chat summary (≤15 lines) |

T2 also offers — once — `/ownership-check`.

---

## Completion block (mandatory, all tiers)

```
VERIFIED:      <command> → <result>
TESTED:        <scenario asserted>
ASSUMED:       <reasoned, not executed>
UNTESTED RISK: <highest-impact unexercised thing>
```

If a line has nothing to report, write `none` — an empty line reads as an omission.

---

## Why the gates changed

| Old model | Cost | New model |
|-----------|------|-----------|
| 3 hard stops before any code, at every size | 3 round-trips for a 2-file change; the gates become rubber stamps and stop carrying signal | 1 stop at T2 only |
| SCRATCHPAD + PLAN + TASKS as three artifacts | three documents that mostly restate each other | one plan artifact holding invariants, steps, failure modes |
| Review separate from understanding | review passes, understanding does not transfer | Phase 5 is the default exit, not an optional extra |

The invariant that survives: **the risky decision is approved by a human before code exists.**
