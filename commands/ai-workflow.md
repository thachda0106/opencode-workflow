---
description: Master engineering-ownership workflow — classify, investigate, plan, approve, task, design flows, implement, verify, review, transfer knowledge
---

# AI Workflow — Engineering Ownership Lifecycle

This is the default lifecycle for non-trivial work. Effort scales with consequence, not with the
number of files touched. The mode table, gates, artifact paths, and evidence labels live in
`AGENTS.md`; this file is the execution sequence.

```
CLASSIFY
  → INVESTIGATE → scratchpad.md → GATE 1
  → PLAN        → plan.md       → GATE 2
  → TASKS       → tasks.md      → GATE 3
  → FLOWS       → implementation-flows.md
  → IMPLEMENT → VERIFY
  → GATE 4 (Full; Standard on deviation) → KNOWLEDGE → COMPLETE
```

Lightweight (T0) short-circuits to IMPLEMENT → VERIFY → one-line note.

---

## 0 · CLASSIFY

Print one line before anything else:

```
Mode: Full Engineering (T2) — trigger: transaction boundary (src/orders/order.service.ts:112)
Scope lock: src/orders/**, src/coupons/**; not touching payments.
Re-tier point: a schema change or authz rule appears.
```

Triggers are objective. If you cannot name one from the T2 column in `AGENTS.md`, the task is
Standard (T1). If it is ≤2 files with no critical surface and no new public interface, it is
Lightweight (T0).

Say which mode and why. Re-classify when scope grows; do not silently expand.

---

## 1 · INVESTIGATE — Standard and Full

No code, no plan text yet.

1. Trace the existing path end to end:
   `analyze-project-structure` for layout, `trace-execution-flow` for the specific path,
   `locate-code-patterns` for "how is this already done elsewhere".
2. Find the pattern to follow. Name the file you are copying the shape from. A new pattern in an
   established codebase needs a reason.
3. Separate observations from hypotheses. Observations cite `file:line`; hypotheses are marked
   as such.
4. Record what you could not determine. Unresolved unknowns become plan risks, not silent guesses.
5. Write `.ai/work/<slug>/scratchpad.md` using `prompts/templates/scratchpad.md`.

**GATE 1 — WAIT.** Present findings, evidence, assumptions, risks, and scope. Do not continue
until the human explicitly approves with `APPROVE GATE 1` or an unambiguous equivalent.

---

## 2 · PLAN — Standard and Full

Write `.ai/work/<slug>/plan.md` using `prompts/templates/plan.md`.

Required: objective · scope · invariants (with IDs) · findings summary · architecture decisions
(with IDs) · alternatives rejected · trade-offs · impacted components · failure modes · security
· rollback · verification strategy · non-goals · acceptance criteria.

**GATE 2 — WAIT.** Present decisions, alternatives, trade-offs, invariants, and verification.
Do not continue until explicit `APPROVE GATE 2`. Freeze the plan baseline. Any later change to an
approved decision requires a delta and re-approval.

---

## 3 · TASKS — Standard and Full

Write `.ai/work/<slug>/tasks.md` using `prompts/templates/tasks.md`.

Every task: ID · objective · status · dependencies · impacted files · implementation instructions
· acceptance criteria · verification steps · risk classification · plan-decision reference.

Tasks must be reviewable independently where possible. If a task cannot be verified alone, split
it. Every task maps to an approved plan decision or invariant.

**GATE 3 — WAIT.** Present tasks, dependencies, order, and risk levels. Do not continue until
explicit `APPROVE GATE 3`. Gate 3 authorizes implementation-flow generation, not source changes.

---

## 4 · IMPLEMENTATION FLOWS — Standard and Full

Mandatory for Full. Mandatory for Standard when the change alters runtime behavior; use a compact
flow (one flowchart plus the primary failure path). Skip only for a pure refactor/rename with
identical behavior, and state why.

Load `design-implementation-flows` and write `.ai/work/<slug>/implementation-flows.md`.
No source changes before this file exists.

If the flows expose a new decision or contradict the approved plan, stop and return to GATE 2. If
they expose a new task, stop and return to GATE 3.

---

## 5 · IMPLEMENT

Follow the approved plan and task order. During implementation:

- Match existing code shape exactly; a reviewer should not be able to tell who wrote it.
- One task at a time, in order. Do not reorder silently.
- If reality contradicts the plan: **stop**, state the delta in three lines, wait for my word.
- If the change grows past the plan (new file outside scope, new dependency, destructive step):
  stop before doing it.
- Commit hygiene: no unrelated files, no formatting sweeps, no dependency bumps.

---

## 6 · VERIFY

Run what exists, in this order, and quote results:

```bash
# whichever of these the project actually has
npm run typecheck        # or: npx tsc --noEmit
npm run lint
npm test -- <pattern>
npm run build
```

| Mode | Minimum |
|------|---------|
| Lightweight | typecheck + build |
| Standard | + targeted tests |
| Full | + full suite, + `stress-test-implementation` pass |

A failing check is reported, not explained away. A check that could not run is reported as
`not run`, never as `passed`.

---

## 7 · REVIEW

**Full:** write `.ai/work/<slug>/review.md` and present Gate 4: results, verification evidence,
deviations, updated flows, remaining risks, knowledge links. Wait for explicit `APPROVE GATE 4`.

**Standard:** present a final summary. If a deviation occurred or risk escalated, promote to Full
and run Gate 4.

**Lightweight:** one-line summary.

---

## 8 · KNOWLEDGE

| Mode | Output |
|------|--------|
| Lightweight | one line in chat: what changed |
| Standard | `.ai/knowledge/features/<slug>/README.md` + `full-flow.md` |
| Full | `README.md` + `full-flow.md` + `architecture.md` + `decisions.md` |

Load `transfer-implementation-knowledge`. Update `.ai/knowledge/index.md` once. Full mode also
offers `/ownership-check` once.

---

## 9 · CONTEXT RECOVERY

When resuming:

1. Read `.ai/work/<slug>/scratchpad.md`, `plan.md`, `tasks.md`, `implementation-flows.md`,
   `review.md` in that order.
2. Read the feature package `README.md` and `full-flow.md` if they exist.
3. Inspect `git status`, `git diff`, `git log`.
4. Verify completed tasks against acceptance criteria and actual code/tests. Never trust status
   without evidence.
5. Identify the last verified checkpoint, check approved decisions, and resume. If a decision
   changed, re-gate.

---

## Completion block (mandatory, all modes)

```
VERIFIED:      <command> → <result>
TESTED:        <scenario asserted>
ASSUMED:       <reasoned, not executed>
UNTESTED RISK: <highest-impact unexercised thing>
```

If a line has nothing to report, write `none` — an empty line reads as an omission.

---

## Why the gates exist

| Old failure | Cost | New rule |
|-------------|------|----------|
| 45 gates on every task | gates became rubber stamps | Lightweight has 0; Standard 3; Full 4 |
| Investigation and decisions in one file | hypotheses became decisions | `scratchpad.md` and `plan.md` are separate, separately approved |
| No execution contract | tasks drifted from the plan | `tasks.md` maps every task to a plan decision |
| Code before system understanding | developer read code to learn the design | `implementation-flows.md` exists before code |
| Review without a failure model | green tests were treated as proof | evidence labels + stress pass + Gate 4 |

The invariant: **the risky decision is approved by a human before code exists, and the final
behavior is reviewed before the change is called complete.**
