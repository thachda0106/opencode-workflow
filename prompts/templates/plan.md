# Template — plan (engineering decisions)

> Work artifact. Target: `.ai/work/<slug>/plan.md`. Keep under 80 lines.
> The approved plan is the execution baseline. Silent changes are not allowed.

Mode: <Standard | Full Engineering> · Tier: <T1 | T2> · Date: <YYYY-MM-DD>
Status: <draft | approved | superseded> · Approved: <date / gate>
Objective: <one sentence>

## Scope

- In scope: <files, modules>
- Out of scope: <explicit non-goals>
- Re-tier point: <what would change the mode>

## Invariants that must hold

| ID | Invariant | Test / check |
|----|-----------|--------------|
| INV1 | <must remain true> | <how it is asserted> |

## Findings summary

<What the investigation established, with evidence references. Link to scratchpad.>

## Architecture decisions

| ID | Decision | Alternative rejected | Why |
|----|----------|----------------------|-----|
| D1 | <chosen> | <rejected> | <reason> |

## Trade-offs

- <what this costs> — <why acceptable>
- <what becomes harder> — <mitigation>

## Impacted components

| Component | Change | Contract / boundary affected |
|-----------|--------|------------------------------|

## Failure modes

| If this fails | System state | Handled how |
|---------------|--------------|-------------|

## Security

- Trust boundary: <where input crosses>
- Authn/authz: <role and object-level checks>
- Secrets/data exposure: <none / how handled>
- Injection / mass assignment: <risk and control>

## Rollback

<How to undo the change safely. Migration path if schema changed.>

## Verification strategy

```bash
<commands>
```

Scenarios: <happy path, failure path, concurrency/rollback where relevant>

## Acceptance criteria

- [ ] <observable outcome>
- [ ] <test asserts behavior>

## Non-goals

- <explicitly not doing this>

## Approved baseline

<Filled after Gate 2. Any later change gets a delta and re-approval.>
