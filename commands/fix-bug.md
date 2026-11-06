---
description: Systematically diagnose and fix bugs in the codebase
agent: bug-hunter
subtask: false
---

# Fix Bug

> **Gates**: this command follows the tier model in `AGENTS.md`. T0/T1 run with no stops;
> T2 stops once, after the plan. Investigation notes, plan, and step list all live in
> `.ai/knowledge/plans/<slug>.md` — not in three root-level files.

Systematically diagnose and fix bugs following the Bug Hunter agent protocol.

---

## 1 · INVESTIGATE — Diagnosis

The bug to diagnose: **$ARGUMENTS** (if empty, ask for the symptom and stop).

**No code changes in this phase. Investigation only.**

1. Read the bug description/error message carefully
2. Identify affected functionality
3. Determine reproduction steps
4. Check if it's a regression (did it work before?)
5. Use error stack trace to find source
6. Search for relevant code patterns
7. Check related modules and layers
8. Review recent changes (`git blame`/`git log`)
9. Diagnose root cause — categorize the bug:
   - **Request Lifecycle**: Middleware, guard failures, interceptor problems
   - **Dependency Injection**: Missing providers, circular dependencies
   - **Database/ORM**: Query errors, mapping issues, migration problems
   - **Type Errors**: Type mismatches, null/undefined, incorrect assertions
   - **Async Issues**: Unhandled promises, race conditions
   - **Validation**: Incorrect validation, missing checks
   - **API/Data**: Wrong endpoint, incorrect format, missing error handling
10. Write all findings into `.ai/knowledge/plans/<slug>.md` including:
    - **Symptom**: What's wrong
    - **Root Cause**: Why it's happening
    - **Impact**: What's affected

---

## 2 · PLAN — Fix Strategy

1. Based on the diagnosis in the plan file, plan the fix:
   - Minimal change needed
   - Side effects and edge cases
   - Files to modify
   - Risk of breaking other features
   - Verification strategy
2. Document:
   - **Approach**: How to fix it
   - **Changes**: What code will change
   - **Trade-offs**: Any considerations
3. Write into `.ai/knowledge/plans/<slug>.md`

---

## 3 · STEPS — Fix Steps

1. Break the fix into ordered steps:
   - [ ] Step 1: Description + files to change
   - [ ] Step 2: Description + files to change
   - [ ] Step N: Add regression test
2. For each step, specify:
   - What changes
   - Why
   - Expected result
3. Write into `.ai/knowledge/plans/<slug>.md`

---

## 4 · IMPLEMENT — Apply Fix

- Make targeted changes (avoid over-engineering)
- Add defensive checks if needed
- Update types if necessary
- Add comments for non-obvious fixes
- Implement in the order defined in `.ai/knowledge/plans/<slug>.md`

---

## 5 · VERIFY

After the fix is implemented:
- Test the specific bug scenario
- Test related functionality
- Run unit/integration tests
- Check for new type errors
- Verify no regressions

### Prevention
- Document how to avoid similar bugs in the future
