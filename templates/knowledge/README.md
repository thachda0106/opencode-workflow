# `.ai/knowledge/` — project knowledge store

Bootstrap a project once:

```bash
mkdir -p .ai/knowledge/{features,adr,ownership} .ai/work
cp ~/.config/opencode/templates/knowledge/{index.md,critical-paths.md,gotchas.md,adr-template.md} .ai/knowledge/
git add .ai && git commit -m "chore: bootstrap knowledge store"
```

## What lives where

| Path | Written by | When | Budget |
|------|-----------|------|--------|
| `.ai/work/<slug>/scratchpad.md` | investigation | before Gate 1 | 80 lines |
| `.ai/work/<slug>/plan.md` | planning | before Gate 2 | 80 lines |
| `.ai/work/<slug>/tasks.md` | planning | before Gate 3 | 1 row per task |
| `.ai/work/<slug>/implementation-flows.md` | `design-implementation-flows` | after Gate 3, before code | 1 diagram per concern |
| `.ai/work/<slug>/review.md` | `review-implemented-files` | Gate 4 | 1 page |
| `.ai/knowledge/index.md` | every skill that writes here | after each artifact | 1 line per artifact |
| `.ai/knowledge/critical-paths.md` | `map-critical-paths` | after a Full change, or on demand | ≤8 rows per module |
| `.ai/knowledge/features/<slug>/README.md` | `transfer-implementation-knowledge` | after Standard/Full work | 60 lines |
| `.ai/knowledge/features/<slug>/full-flow.md` | `transfer-implementation-knowledge` | after behavior changes | 200 lines |
| `.ai/knowledge/features/<slug>/architecture.md` | `transfer-implementation-knowledge` | Full work, or boundary change | 100 lines |
| `.ai/knowledge/features/<slug>/decisions.md` | `transfer-implementation-knowledge` | Full work, or real decision | 100 lines |
| `.ai/knowledge/gotchas.md` | anyone, immediately | a bug took >15 min to find | append-only |
| `.ai/knowledge/adr/NNN-<slug>.md` | whoever made the decision | a real alternative was rejected | 1 page |
| `.ai/knowledge/ownership/<slug>.md` | `verify-ownership` | knowledge check | 1 page |

Legacy `.ai/knowledge/features/<slug>.md` and `.ai/knowledge/plans/<slug>.md` remain readable.
Do not create new legacy files and do not maintain both forms for the same feature.

## Rules

1. **Read `index.md` first.** If an artifact covers the area, update it — never create
   `orders-v2.md` next to `orders.md`.
2. **Link, don't restate.** If the code, README, or an existing doc says it, point at it.
3. **A gotcha is the highest-value artifact per line.** Write it the moment it costs you time:
   symptom → cause → fix → date. No essays.
4. **No ADR without a rejected alternative.** Otherwise it is a note.
5. **Delete or update stale artifacts in the same commit that makes them stale.** A wrong map is
   worse than no map.
6. **Visual first.** `full-flow.md` is the entry point for understanding; code mapping is the
   second step.
7. **This store is git-tracked.** Write for the next engineer, not for yourself.

## What does not belong here

- Meeting notes, sprint plans, task lists (those live in `.ai/work/<slug>/`).
- API reference (generate it from the code).
- Anything a new hire would need in week one — that is the project README.
