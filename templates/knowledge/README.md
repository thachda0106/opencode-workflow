# `.ai/knowledge/` — project knowledge store

Bootstrap a project once:

```bash
mkdir -p .ai/knowledge/{features,plans,adr,ownership}
cp ~/.config/opencode/templates/knowledge/{index.md,critical-paths.md,gotchas.md,adr-template.md} .ai/knowledge/
git add .ai && git commit -m "chore: bootstrap knowledge store"
```

## What lives where

| File | Written by | When | Budget |
|------|-----------|------|--------|
| `index.md` | every skill that writes here | after each artifact | 1 line per artifact |
| `critical-paths.md` | `map-critical-paths` | after a T2 change, or on demand | ≤8 rows per module |
| `features/<slug>.md` | `transfer-implementation-knowledge` | T1 (short note) / T2 (full report) | 120 lines |
| `plans/<slug>.md` | `/ai-workflow` Phase 2 | T2 before implementation | 40 lines |
| `gotchas.md` | anyone, immediately | a bug took >15 min to find | append-only |
| `adr/NNN-<slug>.md` | whoever made the decision | a real alternative was rejected | 1 page |
| `ownership/<slug>.md` | `verify-ownership` | knowledge check | 1 page |

## Rules

1. **Read `index.md` first.** If an artifact covers the area, update it — never create
   `orders-v2.md` next to `orders.md`.
2. **Link, don't restate.** If the code, README, or an existing doc says it, point at it.
3. **A gotcha is the highest-value artifact per line.** Write it the moment it costs you time:
   symptom → cause → fix → date. No essays.
4. **No ADR without a rejected alternative.** Otherwise it is a note.
5. **Delete stale artifacts in the same commit that makes them stale.** A wrong map is worse
   than no map.
6. **This store is git-tracked.** It is shared with the team; write for the next engineer, not
   for yourself.

## What does not belong here

- Meeting notes, task lists, sprint plans.
- API reference (generate it from the code).
- Anything a new hire would need in week one — that is the README.
