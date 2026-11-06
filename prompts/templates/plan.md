# Template — plan

> Tier-2 artifact. Target path: `.ai/knowledge/plans/<slug>.md`. Keep it under 40 lines.

Tier: T2 · trigger: <the tier trigger, with file:line>
Objective: <one sentence>

## Invariants that must hold

- <invariant 1>
- <invariant 2>

## Approach

<3–6 lines. The design, not the steps.>

## Rejected alternative

<what you considered and why it loses. If nothing real was considered, write "none worth
considering" — do not invent one.>

## Files

| File | Change |
|------|--------|

## Steps

1. <step — verifiable on its own>
2. <step>

## Failure modes

| If this fails | System state | Handled how |
|---------------|--------------|-------------|

## Verification

```bash
<commands>
```

Scenarios: <the cases that must be exercised, including one failure path>

## Non-goals

- <explicitly not doing this>
