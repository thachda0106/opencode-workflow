# Template — tasks

> Only for gated flows. Ordinary work keeps the step list inside `plan.md`; a separate task
> file is duplication unless several people or sessions execute the steps.

| # | Step | Files | Depends on | Done when |
|---|------|-------|-----------|-----------|
| 1 | | | — | <observable check> |
| 2 | | | 1 | <observable check> |

Rules:
- One step = one reviewable change.
- Every step has an observable completion check, not "code written".
- If a step cannot be verified alone, it is two steps.
