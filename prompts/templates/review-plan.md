# Template — plan review

> Reviewing artifacts before code exists. The only question that matters: **would this plan
> produce a system we can operate and understand?**

## Metadata

- Reviewed by: <agent>
- Date: <YYYY-MM-DD>
- Mode: <Lightweight | Standard | Full Engineering>
- Artifacts reviewed: `scratchpad.md`, `plan.md`, `tasks.md`, `implementation-flows.md`

## Verdict

APPROVE | APPROVE_WITH_CONDITIONS | REJECT

## What the artifacts get right

<2–4 bullets. Specific; generic praise is noise.>

## Gaps

| # | Gap | Why it matters | What to add |
|---|-----|----------------|-------------|

Check specifically:

- [ ] Observations are separated from hypotheses and cite `file:line`
- [ ] Invariants are stated, IDed, and testable
- [ ] Transaction boundaries named
- [ ] Failure behavior for each external call (timeout, retry, partial success)
- [ ] Migration path for existing data and rolling-deploy compatibility
- [ ] Authorization at object level, not just role
- [ ] Observability: how a failure becomes visible
- [ ] Non-goals stated
- [ ] Rejected alternative named
- [ ] Every task maps to a plan decision
- [ ] Every Tier A path has a flow diagram
- [ ] Diagram elements are labelled `[V]`, `[P]`, or `[?]`
- [ ] Failure and alternative paths are present in the flows

## Unstated assumptions

-

## Conditions to approve

1. <the smallest change that makes this plan safe to execute>
