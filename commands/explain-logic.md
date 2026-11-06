---
description: Trace and explain a code path from entry point to effect — declarative first, evidence-anchored, no approval gates
---

# Explain Logic

Explain how a path actually works, from trigger to terminal effect. This is a read-only
explanation: no gates, no plan artifact, no code changes.

## 1. Fix the scope

One path. Name it:

```
POST /orders/:id/cancel → order state + refund intent + event
```

If `$ARGUMENTS` gives a symbol or file instead of a flow, trace from the nearest entry point
(controller, consumer, cron). If several paths are plausible, pick the one with side effects and
say which you picked.

## 2. Read, don't simulate

1. Entry point in full — the handler as written, including middleware/decorators/guards.
2. Follow the call chain; at each hop read the callee's real body, not its signature.
3. Note where data changes shape (DTO → entity, entity → row, row → response).
4. Note external interactions: DB writes, queue publishes, HTTP calls, cache, filesystem.
5. Note the branches that matter: guards, state checks, error paths.

Stop when you reach the durable effect. Do not trace framework internals past one level.

## 3. Output shape

```
## Path
<trigger> → <hop> → <hop> → <effect>

## Declarative layer (before the mechanics)
| Term | Meaning here |
| <domain noun> | <one sentence, no jargon> |
| <mechanism> | <what it is for, in one sentence> |

## Hops
| # | Where | What happens | Data in → out |
|---|-------|--------------|---------------|

## Decisions
- <decision> — why here rather than <alternative>; what breaks without it (file:line)

## Branches and guards
| Condition | Result | file:line |

## Failure behaviour
| If this fails | State left behind | Visible how |

## Debug entry
- first breakpoint: file:line (why there)
- log/metric to watch: <name>
- fastest check: <command>
```

Rules:
- Every hop cites `file:line`. If you did not open the file, you cannot claim the hop.
- Concrete identifiers and values. Never `foo`, `bar`, `example.com`.
- No forward references: define a term before the hop that uses it.
- ≤60 lines for a single path. Longer means you are transcribing code, not explaining it.
- One ASCII diagram only if the flow branches; skip it for linear paths.

## 4. Optional persistence

If the path is Tier A (load `map-critical-paths` if unsure), append it to
`.ai/knowledge/features/<slug>.md` under `## Path` — the same content, not a second version.
Otherwise leave it in chat; not every explanation deserves a file.

## Non-goals

- Proposing changes. If you see a defect, state it in one line at the end; do not fix it.
- Line-by-line commentary.
- Teaching the framework — link the doc once if a concept is load-bearing.
