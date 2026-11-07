# Template — implementation review / Gate 4 evidence

> Target: `.ai/work/<slug>/review.md` for a gated change; otherwise `review-implementation.md`
> at repo root (or `docs/reviews/<date>-<slug>.md`).

# Review — <change>

Mode: <Lightweight | Standard | Full Engineering> · Tier: <A/B/C per path>
Scope: <n> files · Base: <branch/commit>
Verdict: APPROVED | APPROVED_WITH_COMMENTS | CHANGES_REQUESTED

## Findings

| # | Severity | Evidence | File:line | Finding | Why it matters |
|---|----------|----------|-----------|---------|----------------|

Severity: MUST_FIX | SHOULD_FIX | OPTIONAL
Evidence: CONFIRMED | LIKELY | QUESTION

## Plan / task / flow compliance

| Item | Status | Evidence |
|------|--------|----------|
| Plan decisions D1–Dn implemented | pass/fail | |
| Invariants INV1–INVn hold | pass/fail | |
| Every approved task implemented or deferred | pass/fail | |
| Implementation flows match code | pass/fail | |
| Diagrams updated `[P]` → `[V]` where verified | pass/fail | |

## Deviations

| Planned | Actual | Reason | Approved? |
|---------|--------|--------|-----------|

## Verification evidence

| Check | Command | Result |
|-------|---------|--------|

## What tests actually cover

| Scenario | Test |
|----------|------|

## What is assumed, not verified

-

## Remaining risks

| Risk | Impact | Mitigation / follow-up |
|------|--------|------------------------|

## Questions for the author

-

## Gate 4 decision

- [ ] Results reviewed
- [ ] Verification evidence reviewed
- [ ] Deviations accepted or rejected
- [ ] Flows updated
- [ ] Knowledge links present
- [ ] Remaining risks accepted

Approved: `APPROVE GATE 4` · Date: <YYYY-MM-DD>
