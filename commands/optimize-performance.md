---
description: Identify and fix performance bottlenecks with evidence-based analysis
agent: performance-optimizer
subtask: false
---

# Optimize Performance

> **Modes and gates**: follow the mode table in `AGENTS.md`. Lightweight runs with no stops;
> Standard uses Gates 1–3; Full uses Gates 1–4. Work artifacts live under `.ai/work/<slug>/`.

Identify and fix performance bottlenecks using evidence-based analysis.

---

## 1 · INVESTIGATE — Profiling

**No code changes in this phase. Investigation only.**

1. Identify the problem:
   - What is slow? (specific endpoint, operation, page load)
   - How slow? (current vs. expected latency/throughput)
   - Since when? (regression or longstanding issue)
2. Profile and measure:
   - Trace execution flow for the slow path
   - Identify the bottleneck stage (DB query, computation, I/O, network)
   - Gather evidence (query logs, execution time, memory usage)
3. Diagnose root cause:
   - **Database**: N+1 queries, missing indexes, full table scans, unoptimized joins
   - **Computation**: O(n²) algorithms, unnecessary iterations, blocking operations
   - **I/O**: Synchronous file operations, unbatched network calls
   - **Memory**: Memory leaks, excessive object creation, missing cleanup
   - **Concurrency**: Blocking main thread, incorrect async patterns
4. Write all findings into `.ai/work/<slug>/plan.md`

---

## 2 · PLAN — Optimization Strategy

1. Define optimization strategy:
   - Specific bottleneck to fix (one at a time)
   - Proposed solution (prefer simple: add index, batch queries)
   - Before/after expected metrics
   - Risk of regression
2. Write into `.ai/work/<slug>/plan.md`

---

## 3 · STEPS — Optimization Steps

1. Break the optimization into ordered steps:
   - [ ] Step 1: Description + files to change
   - [ ] Step 2: Description + files to change
   - [ ] Step N: Add benchmark / regression test
2. Write into `.ai/work/<slug>/plan.md`

---

## 4 · IMPLEMENT

- Fix the specific bottleneck identified
- Prefer simple solutions over complex ones
- Do NOT optimize areas without evidence of problems

---

## 5 · VERIFICATION

After optimization:
- Measure the optimized path
- Compare before/after metrics
- Run regression tests

## Critical Rules

- **No evidence = no optimization**
- **Measure first, optimize second**
- **One bottleneck at a time**
- **Verify improvement with data**
