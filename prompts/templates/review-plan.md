# Template — plan review

Reviewing a plan before code exists. The only question that matters: **would this plan produce
a system we can operate?**

## Verdict

APPROVE | APPROVE_WITH_CONDITIONS | REJECT

## What the plan gets right

<2–4 bullets. Be specific; generic praise is noise.>

## Gaps

| # | Gap | Why it matters | What to add |
|---|-----|----------------|-------------|

Check specifically:

- [ ] Invariants are stated and testable
- [ ] Transaction boundaries named
- [ ] Failure behaviour for each external call (timeout, retry, partial success)
- [ ] Migration path for existing data, and rolling-deploy compatibility
- [ ] Authorization at object level, not just role
- [ ] Observability: how a failure becomes visible
- [ ] Non-goals stated (prevents scope creep)
- [ ] Rejected alternative named

## Unstated assumptions

-

## Conditions to approve

1. <the smallest change that makes this plan safe to execute>
