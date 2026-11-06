---
name: stress-test-implementation
description: Probe an implementation for production failure modes — partial failure, concurrency, retries, idempotency, migrations, authz, observability — and label each finding verified, tested, assumed, or untested. Use before merging anything that touches state.
metadata:
  layer: verification
  stage: pre-merge
---


# Skill: stress-test-implementation

Green tests answer "does the happy path work". This skill answers "what happens when the world
misbehaves" — and states plainly which answers are evidence and which are inference.

## When to use

- T2 change, before merge.
- Any change touching: a write path, a queue consumer, a webhook, a migration, an authz check,
  a retry/timeout, a cache.
- When the engineer asks "what could go wrong here".

Not for: load testing, penetration testing, or a full security audit. This is a structured
failure-mode pass on one change.

## Procedure

### 1. Build the surface list

From the diff, list what the change actually touches. Only these ten categories matter:

| # | Surface | Ask |
|---|---------|-----|
| 1 | Transaction boundary | What is inside the tx that should be outside, and vice versa? What is the isolation level and does it prevent the anomaly you are worried about? |
| 2 | Concurrency | Can two of these run at once? What is the shared resource, and what serialises it — row lock, unique index, advisory lock, or nothing? |
| 3 | Retry / timeout | Who retries, how many times, with what backoff? Is the operation safe to repeat? What is the timeout on the outbound call, and what happens when it fires? |
| 4 | Idempotency | What key deduplicates? Where is it stored, what is its TTL, and what happens on a concurrent duplicate? |
| 5 | Partial failure | If step 2 of 4 fails, what is committed? Is there a compensating action, and can it fail? |
| 6 | External dependency | What is the failure mode of the downstream (slow / 500 / 429 / partial success)? Does it fail open or closed? |
| 7 | Data evolution | Is the migration backward compatible? Can old code run against the new schema during a rolling deploy? What happens to in-flight rows? |
| 8 | Authorization | Is the object-level owner checked, or only the role? Can an id from another tenant reach this code path? |
| 9 | Observability | Will a failure here be visible without a customer report? What log, metric, or trace carries the correlation id? |
| 10 | Resource bounds | Unbounded query? Unbounded memory? Connection held across an await/HTTP call? |

Skip a category only with a reason ("no external calls in this path"), never by omission.

### 2. Answer each with an evidence label

```
VERIFIED   a command was run in this session and its output proves the behaviour
TESTED     an existing test asserts this scenario (name the test)
ASSUMED    reasoned from code reading, not executed
GAP        nothing covers it, and the risk is real
```

Rule: `VERIFIED` requires quoting the command and its output. A test that exists but was not run
is `TESTED` only if it genuinely asserts this scenario, and you must say which one.

### 3. Run the cheap probes

Before writing the table, actually run what is runnable. Cheapest first:

```bash
# duplicate delivery
curl -s -X POST :3000/webhooks/x -d @fixture.json -H 'x-event-id: fixed-1'
curl -s -X POST :3000/webhooks/x -d @fixture.json -H 'x-event-id: fixed-1'
psql "$DATABASE_URL" -c "select event_id, count(*) from ledger group by 1 having count(*)>1"

# concurrent claim (two writers, one row)
for i in 1 2; do psql "$DATABASE_URL" -c "update job set state='running' where id=1" & done; wait

# half-commit
# inject a throw between the two writes, then: select count(*) from orders; select count(*) from outbox;

# migration compatibility (read-only check)
psql "$DATABASE_URL" -c "\d+ <table>"   # NOT NULL without default breaks old code mid-deploy
```

Time-box: 15 minutes of probes. Anything not probed stays `ASSUMED`/`GAP` — that is a valid
outcome and must be reported as one.

### 4. Output (≤40 lines, in this shape)

```
| Surface | Scenario | Evidence | Status | Fix if GAP |
```

Then:

```
Top 3 untested risks (impact × likelihood):
1. <risk> — <impact> — <cheapest mitigation>
2. ...
3. ...
```

Then one line:

```
Verdict: merge · merge with follow-ups (<n>) · do not merge (<reason>)
```

### 5. Persist

- Append each `GAP` with real risk to `.ai/knowledge/gotchas.md` only if it bit you or is
  scheduled for follow-up. Do not log every gap.
- Add follow-up tasks to the task tracker/issue list, not into the doc.

## Decision rules

- **Tests passing changes nothing.** Never upgrade a status because the suite is green; that is
  the exact confusion this skill exists to prevent.
- **Unknown isolation level is a finding**, not a detail. Read it or mark `GAP`.
- **A missing timeout on an outbound call is always at least `SHOULD_FIX`.** Say the number.
- **Stale cache + write = GAP** unless you can name the invalidation trigger and its race window.
- Two `GAP`s on the same surface means the design is wrong, not the tests. Say so.

## Non-goals

- Rewriting the implementation. Report; the engineer decides.
- Proving absence of bugs. This bounds known risk; it does not certify correctness.
- Replacing `review-implemented-files` (design and correctness review) — this is the failure-mode
  lens layered on top of it.
