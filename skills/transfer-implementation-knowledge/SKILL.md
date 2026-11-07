---
name: transfer-implementation-knowledge
description: Produce a durable per-feature knowledge package after implementation — README, visual full-flow, architecture, and decisions — so another engineer can understand, debug, and own the feature without the chat transcript.
metadata:
  layer: knowledge
  stage: post-implementation
---

# Skill: transfer-implementation-knowledge

Convert an implementation into understanding. Write from the diff, the code, and the verified
flows — not from the plan. Plans describe intent; the package must describe what is actually on
disk.

## When to use

- After any Full Engineering change, before declaring it complete.
- After a Standard change when behavior, boundaries, or failure modes changed.
- On request: "explain what you just built", "what do I need to understand here".

Not for: line-by-line code walkthroughs, API reference docs, framework tutorials, or grading the
implementation.

## Inputs

1. The diff: `git diff HEAD` or `git diff origin/main...HEAD` — authoritative.
2. `.ai/work/<slug>/plan.md` and `tasks.md` — approved decisions and task mapping.
3. `.ai/work/<slug>/implementation-flows.md` — pre-code design and deviations.
4. The entry points the diff touches; read the full function, not just the hunk.
5. Test output actually observed in this session.
6. Existing `.ai/knowledge/features/<slug>/` — update, never duplicate.

## Output package

```
.ai/knowledge/features/<slug>/
  README.md
  full-flow.md
  architecture.md
  decisions.md
```

| File | Contents | Budget |
|------|----------|--------|
| `README.md` | What/why, actors, triggers, outcomes, main components, entry points, source links | ≤60 lines |
| `full-flow.md` | Complete visual lifecycle: flowcharts, sequence diagrams, critical decisions, source mapping, debugging guide, ownership checklist | ≤200 lines |
| `architecture.md` | Boundaries, dependencies, patterns, data ownership, integration points | ≤100 lines |
| `decisions.md` | Decisions, alternatives, reasons, trade-offs, limitations | ≤100 lines |

- **Standard:** `README.md` + `full-flow.md`; fold architecture/decisions in when small.
- **Full:** all four mandatory.
- **Pure refactor/rename with identical behavior:** short note, no forced diagram; state why.

If the package exceeds its budget, the feature is too large or the file is restating the code.
Split the feature or cut duplication.

## `full-flow.md` — mandatory content

### A. Feature overview

Business purpose, actors, trigger conditions, expected outcomes. Two or three sentences; no
framework history.

### B. Full execution flow

A Mermaid flowchart of the complete lifecycle: trigger → entry point → validation → business
logic → persistence/external calls → response/effect. Include alternative and error paths, not
just the happy path.

### C. Sequence diagrams

Where applicable: frontend/backend, internal services, database operations, external
integrations, asynchronous events, error handling.

### D. Critical decision points

Conditions, business rules, state transitions, transaction boundaries, retry behavior, failure
handling. This is the Level 3 section: explain what a maintainer must understand to avoid
breaking the system silently.

### E. Source code mapping

| Step | File:line | Class/function | Responsibility | Task |
|------|-----------|----------------|----------------|------|

Every important step references real code. A stale line number is worse than no line number.

### F. Production debugging guide

| Symptom | Start at | Then |
|---------|----------|------|

Where to put the first breakpoint or log, which failure points matter, how errors propagate, what
to inspect when behavior differs from expectations. No "check the logs".

### G. Engineering ownership checklist

- **Verified facts:** what was observed or executed.
- **Assumptions:** what is reasoned but not exercised.
- **Untested behavior:** what nobody has run.
- **Remaining risks:** the highest-impact gaps.

For each item, name the file:line range to read and the question the engineer should be able to
answer without looking.

## Labelling and truth rules

- `[V]` verified existing behavior with `file:line`.
- `[P]` planned behavior with task ID.
- `[?]` unknown; add it to open questions.
- `VERIFIED` / `TESTED` / `ASSUMED` / `GAP` labels apply to claims in prose and tables.
- Never invent behavior to complete a diagram. Unknown is a valid, useful state.
- Mermaid source stays inside Markdown so it remains editable and version-controlled.
- Distinguish existing behavior from behavior introduced by this change.

## Chat output

≤15 lines. Fixed shape:

```
Changed: <n> files, <one-phrase summary>
Path: <trigger> → <effect> (via <n> hops)
Understand: <1-3 items, name only>
Watch: <top production failure>
Debug: <start point>
Verified: <...> · Assumed: <...>
Knowledge: .ai/knowledge/features/<slug>/
```

Do not paste the package into chat. Do not narrate every section.

## Update rules

- Read `.ai/knowledge/index.md` first. If a package or legacy report exists, update it.
- Legacy `.ai/knowledge/features/<slug>.md`: either update it or migrate it to a package; never
  maintain both.
- Update `full-flow.md` in the same change that alters execution behavior.
- Append one line to `.ai/knowledge/index.md`:
  `features/<slug>/README.md · YYYY-MM-DD · <one-phrase purpose>`.
- Offer the `verify-ownership` check once, not repeatedly.

## Non-goals

- Restating the plan or the implementation tasks.
- Teaching the framework.
- Review verdicts. Describe a flaw if it matters, but do not grade the code.
- Replacing `stress-test-implementation`; the package records its findings, it does not replace
  the failure-mode pass.
