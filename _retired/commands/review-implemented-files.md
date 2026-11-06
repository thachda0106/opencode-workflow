---
description: Review implemented file changes (git diff, changed files) produced by any AI agent — outputs structured critique as review-implementation.md
agent: review-agent
---

# Review Implemented Files

Review code changes produced by another AI agent. Act as a strict Principal Engineer / Security Reviewer. Find bugs, security vulnerabilities, architecture violations, and correctness issues in the implementation.

> [!CAUTION]
> This workflow requires human approval between every phase.
> Do NOT skip phases. Do NOT combine phases into a single response.

---

## PHASE 1 — LOAD CONTEXT

**No review output in this phase. Research only.**

1. Read project context files (`context/PROJECT.md`, `context/CONVENTIONS.md`, `context/BOUNDARIES.md`)
2. Gather the changes to review:
   - Run `git diff` to see uncommitted changes
   - Run `git diff HEAD~1` or `git log --oneline -5` to see recent commits
   - Read the full content of all changed files
3. If a plan exists (`PLAN.md`, `TASKS.md`), read it to understand intended behavior
4. Write into `SCRATCHPAD.md` (your own scratchpad for this review):
   - Which files changed
   - What the changes are supposed to do
   - Initial observations
   - Areas of concern

**Output**: `SCRATCHPAD.md`

### 🛑 HARD STOP — APPROVAL GATE 1

```
Say: "Phase 1 (Load Context) complete. Please review SCRATCHPAD.md.
Reply APPROVE to continue to the review execution phase, or provide feedback."
WAIT for explicit approval.
```

---

## PHASE 2 — IMPLEMENTATION REVIEW EXECUTION

**Scratchpad must be APPROVED.**

Execute the review following the structure from `prompts/templates/review-implementation.md`:

### 1. Correctness Analysis
- Does the code match the plan (if plan exists)?
- Are there logic errors?
- Are there off-by-one errors, null pointer risks, type mismatches?
- Are edge cases handled (empty arrays, null values, boundary conditions)?

### 2. Bug Detection
- Are there race conditions?
- Are there resource leaks (unclosed connections, missing cleanup)?
- Are there infinite loops or missing termination conditions?
- Are there unhandled promise rejections or missing error boundaries?

### 3. Security Review
- Is user input validated and sanitized?
- Are there SQL injection, XSS, or command injection risks?
- Are secrets/credentials exposed in code or logs?
- Are authentication/authorization checks present where needed?
- Are file paths validated (path traversal prevention)?

### 4. Architecture Compliance
- Does code follow existing patterns in the codebase?
- Are import boundaries respected?
- Is the correct layer used (service vs controller vs repository)?
- Are there circular dependencies introduced?

### 5. Performance Review
- Are there N+1 query patterns?
- Are there missing database indexes for new queries?
- Are large datasets loaded into memory unnecessarily?
- Are there unnecessary re-renders or computations?

### 6. Error Handling
- Are exceptions caught at the right level?
- Are error messages user-safe (no internal details leaked)?
- Are HTTP status codes correct?
- Are database transactions rolled back on error?

### 7. Testing Assessment
- Do tests exist for the changes?
- Are success and failure paths tested?
- Are edge cases covered?
- Are mocks used correctly?

### Output

Generate `review-implementation.md` using the template from `prompts/templates/review-implementation.md`.

**Severity Classification:**
- **MUST_FIX**: Bugs, security vulnerabilities, data corruption risk, correctness errors
- **SHOULD_FIX**: Architecture violations, performance issues, missing error handling
- **OPTIONAL**: Style improvements, test coverage suggestions, maintainability concerns

**Approval Status:**
- **APPROVED**: No MUST_FIX items. Code is ready for merge.
- **APPROVED_WITH_COMMENTS**: No MUST_FIX but SHOULD_FIX items exist. Code can merge with follow-up.
- **CHANGES_REQUESTED**: MUST_FIX items present. Code must be fixed before merge.

---

## PHASE 3 — DELIVER REVIEW

**Review must be complete.**

1. Present the review summary to the human
2. If APPROVED or APPROVED_WITH_COMMENTS: Recommend merge or follow-up
3. If CHANGES_REQUESTED: List the MUST_FIX items that need to be addressed
4. Wait for human decision on next steps

### 🛑 HARD STOP — HUMAN DECISION

```
Say: "Review complete. review-implementation.md generated.
Status: [APPROVED / APPROVED_WITH_COMMENTS / CHANGES_REQUESTED]
[X] MUST_FIX, [Y] SHOULD_FIX, [Z] OPTIONAL items found.

If CHANGES_REQUESTED: Have the implementing agent fix MUST_FIX items, then re-run this review.
If APPROVED_WITH_COMMENTS: Create follow-up tasks for SHOULD_FIX items.
If APPROVED: Ready to merge.

What would you like to do next?"
WAIT for human decision.
```
