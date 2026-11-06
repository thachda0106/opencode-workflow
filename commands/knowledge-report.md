---
description: Post-implementation knowledge transfer — risk-ranked paths, engineering knowledge report, optional failure-mode pass
agent: build
---

# /knowledge-report

Run knowledge transfer for the current change. Do not re-plan, do not modify code.

## 1. Scope

```
git diff --name-status HEAD
```

If the working tree is clean, ask one question: "Branch diff against which base?" and stop.
If `$ARGUMENTS` names a module or feature, use it as scope instead.

Classify the change using the tier table in AGENTS.md. Print the tier line.

## 2. Rank

Load and follow `map-critical-paths`.

- Produce the ranked table for the changed paths only.
- Merge into `.ai/knowledge/critical-paths.md`.

## 3. Report

Load and follow `transfer-implementation-knowledge`.

- Write `.ai/knowledge/features/<slug>.md`.
- Print the ≤15-line chat summary. Do not paste the report.

## 4. Failure modes (conditional)

If the change is T2, or touches a write path / consumer / webhook / migration, load and follow
`stress-test-implementation`. Append its table under `## Production risks` in the same feature
report. Skip when the change is a read-only path or a pure rename — say that you skipped it and why.

## 5. Hand-off

Print exactly:

```
Knowledge: .ai/knowledge/features/<slug>.md
Ranked paths: <n> (Tier A: <n>)
Production risks: <n> gaps, <n> assumed
Next: /ownership-check <slug>   (optional — 5 questions, ~10 min)
```

Update `.ai/knowledge/index.md` once. Then stop. No follow-up suggestions unless asked.
