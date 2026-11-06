---
name: transfer-implementation-knowledge
description: Produce an Engineering Knowledge Report after implementation — what changed, why, how it works, what can break, where to debug, and the 1-3 details you must understand yourself. Use when a T2 change is complete, or when the engineer asks what they need to know about a change.
metadata:
  layer: knowledge
  stage: post-implementation
---


# Skill: transfer-implementation-knowledge

Convert an implementation into understanding. The report is written **from the diff and the
code**, not from the plan — plans describe intent, the report must describe what is actually
on disk.

## When to use

- After any T2 implementation, before declaring the task done.
- After a T1 change when it introduced a new pattern, dependency, or failure mode.
- On request: "explain what you just built", "what do I need to understand here".

Not for: line-by-line code walkthroughs, API reference docs, or tutorials on the framework.

## Inputs

1. The diff: `git diff HEAD` or `git diff origin/main...HEAD` — the authoritative source.
2. The entry points the diff touches (read the full function, not just the hunk).
3. The existing `.ai/knowledge/` for this area — update, do not duplicate.
4. Test output actually observed in this session.

## Report structure (fixed — 9 sections)

Write to `.ai/knowledge/features/<slug>.md`. Every section is mandatory; keep total ≤120 lines.

### 1. What changed
One table. No prose.

```
| File | Change | Why |
|------|--------|-----|
| src/orders/order.service.ts:112 | new tx wrapping order+outbox insert | prevent partial commit |
```

### 2. Why it changed this way
The constraint that forced the shape. Name the alternative you rejected and the one sentence
reason. If there was no alternative worth considering, say "no meaningful alternative".

### 3. How it works
The path, as a numbered chain with file:line at each hop. Start at the trigger, end at the
durable effect (row written, event published, response sent). One line per hop, max 10 hops.
If a hop is a library call that does something non-obvious, name what it does in 5 words.

### 4. Components that interact
Only real couplings: what calls in, what it calls out, what shares state. Table:

```
| Component | Direction | Contract | Breaks if |
```

### 5. Technical decisions worth knowing
Each decision: chosen · rejected · what it costs. Only decisions a future maintainer could
reverse by accident. If a "decision" is just following an existing pattern, say
"followed existing pattern in <file>" — that is useful information.

### 6. Assumptions this relies on
Numbered list. Each must be falsifiable: "the upstream service always sends `event_id`" is
useful; "the system is reliable" is not. Mark each `verified` / `assumed`.

### 7. What can go wrong in production
3–6 concrete failures. Each: trigger → symptom → first check. No generic risks.

```
- Double settlement: gateway retries the webhook after our 30s timeout → two ledger rows →
  check `select event_id, count(*) from ledger group by 1 having count(*) > 1`
```

### 8. Where debugging begins
The exact starting point. Not "check the logs".

```
| Symptom | Start at | Then |
| order stuck in PENDING | order.service.ts:131 (tx boundary) | `select * from outbox where aggregate_id = ...` |
```

### 9. What you should understand more deeply
**1–3 items, maximum.** This is the highest-value section and the easiest to ruin by being
generous. Each item:

```
- <specific mechanism, named>: why it matters (one line) ·
  the question you should be able to answer without looking ·
  read: <file:line range>
```

Selection rule — pick from, in priority order:
1. any path `map-critical-paths` scored Tier A,
2. the one place the implementation was not obvious to write,
3. the one place a future change is most likely to break silently.

Never include: framework boilerplate, DTO shapes, config wiring, anything a competent engineer
would infer from the file name.

## Chat output

≤15 lines. Fixed shape:

```
Changed: <n> files, <one-phrase summary>
Path: <trigger> → <effect> (via <n> hops)
Understand: <1-3 items, name only>
Watch: <top production failure>
Debug: <start point>
Verified: <...> · Assumed: <...>
Full report: .ai/knowledge/features/<slug>.md
```

Do not paste the report into chat. Do not narrate the sections one by one.

## Rules

- **Evidence over memory.** Every file:line must be checked against disk at write time. A stale
  line number is worse than no line number.
- **No forward references.** If §3 uses a term defined in §5, define it inline first.
- **Concrete numbers.** Real event ids, real table names, real timeouts. No `foo`, no `example.com`.
- **Update, don't append.** If a report for this feature exists, revise it; add a `Revised:`
  date line at the top.
- **Length is a feature.** If the report exceeds 120 lines, the feature was too large or the
  report is repeating the code. Cut §1 and §4 first.
- **Say what you did not verify.** §6 and §7 must contain at least one `assumed` item or you
  did not look hard enough.

## After writing

Append one line to `.ai/knowledge/index.md`:

```
features/<slug>.md · YYYY-MM-DD · <one-phrase purpose>
```

Then offer — once, not repeatedly — the `verify-ownership` check.

## Non-goals

- Restating the plan (`plans/<slug>.md` already exists).
- Teaching the framework. If the reader needs NestJS fundamentals, link the docs once.
- Review findings. Correctness verdicts belong to `review-implemented-files`; this report can
  describe a flaw but must not grade the code.
