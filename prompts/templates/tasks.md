# Template — tasks (execution plan)

> Work artifact. Target: `.ai/work/<slug>/tasks.md`. One task = one reviewable change.
> Every task maps to an approved plan decision or invariant.

Mode: <Standard | Full Engineering> · Plan: `.ai/work/<slug>/plan.md`

| ID | Objective | Status | Depends on | Impacted files | Implementation instructions | Acceptance criteria | Verification | Risk | Plan ref |
|----|-----------|--------|------------|----------------|---------------------------|---------------------|--------------|------|----------|
| T1 | | pending | — | | | | | low/med/high | D1 / INV1 |
| T2 | | pending | T1 | | | | | | |

## Rules

- Status values: `pending`, `in_progress`, `done`, `blocked`, `cancelled`.
- A task is `done` only when its acceptance criteria and verification steps pass.
- If a task cannot be verified independently, split it.
- If implementation reveals a new task or a changed decision, stop and re-gate.
- Risk classification: `high` for authz, money, transactions, concurrency, migrations, external
  contracts, data deletion; `medium` for business logic, API contracts, state, data
  transformations; `low` for boilerplate and docs.

## Gate 3 approval

- Tasks presented: <n> · Highest risk: <...>
- Order: <T1 → T2 → ...>
- Approved: <date / gate>
