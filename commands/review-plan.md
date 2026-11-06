---
description: Review implementation plans produced by any agent — legacy SCRATCHPAD/PLAN/TASKS or .ai/knowledge/plans/<slug>.md — outputs review-plan.md
agent: review-agent
subtask: false
---

# Review Plan

Review plan artifacts produced by another AI agent. Act as a strict Principal Engineer / Architect. Find architectural flaws, security gaps, missing requirements, and correctness issues before implementation begins.

Execute all steps in sequence without stopping. Output `review-plan.md` when complete.

---

## STEP 1 — LOAD CONTEXT

1. Read project context files if present (`context/PROJECT.md`, `context/CONVENTIONS.md`, `context/BOUNDARIES.md`); if those files are absent, infer conventions from existing code and say so
2. Locate and read the plan artifacts to review:
   - `SCRATCHPAD.md` — exploration notes, assumptions, unknowns
   - `PLAN.md` — architecture decisions, modules, API contracts, schema
   - `TASKS.md` — ordered implementation steps, dependencies, acceptance criteria
   - `.ai/knowledge/plans/<slug>.md` — current single-file model (investigation + plan + steps)
3. Understand what the plan is trying to achieve

---

## STEP 2 — PLAN REVIEW

### 1. Architecture Review
- Are architecture decisions sound and justified?
- Are module boundaries clear?
- Are integration points defined?
- Are there missing dependencies or circular dependencies?

### 2. Requirements Completeness
- Are all requirements addressed?
- Are there missing edge cases?
- Are error scenarios handled?
- Are non-functional requirements addressed (performance, security, observability)?

### 3. Security Analysis
- Are there input validation gaps?
- Are authentication/authorization requirements defined?
- Are there injection or data exposure risks?
- Are secrets/credentials handled properly?

### 4. Data Consistency
- Are transaction boundaries defined?
- Is eventual consistency addressed?
- Are race conditions considered?
- Are idempotency requirements specified?

### 5. Scalability & Performance
- Will the design handle expected load?
- Are there N+1 query risks?
- Are caching strategies defined?
- Are there single points of failure?

### 6. Task Breakdown Validation
- Do tasks cover all plan items?
- Are dependencies correct?
- Are acceptance criteria specific and verifiable?
- Is the ordering correct (no task depends on a later task)?

---

## STEP 3 — OUTPUT

Generate `review-plan.md` with the following structure. Every critique must reference specific plan sections. Classify each issue by severity.

### Output Structure

```markdown
## Review Metadata

- **Reviewed by**: review-agent
- **Review date**: _YYYY-MM-DD_
- **Plan version**: _version from PLAN.md if present_
- **Artifacts reviewed**: SCRATCHPAD.md, PLAN.md, TASKS.md

## Summary

_Brief overview of what the plan proposes and overall assessment. 2-3 sentences._

## Critical Issues (MUST_FIX)

_Issues that block implementation. Architecture flaws, missing critical requirements, security holes, data loss risk._

### CI-1: [Issue Title]
- **Reference**: [plan.md section or scratchpad observation]
- **Problem**: [What is wrong]
- **Impact**: [What breaks if not fixed]
- **Required**: [What must change]

_(Add CI-2, CI-3, etc. as needed. Maximum 5 MUST_FIX items.)_

## Architecture Problems

_Design decisions that are suboptimal or risky._

### AP-1: [Issue Title]
- **Reference**: [plan.md section]
- **Concern**: [What is concerning]
- **Suggestion**: [What to consider instead]
- **Severity**: SHOULD_FIX / OPTIONAL

## Missing Requirements

### MR-1: [Requirement]
- **What's missing**: [Description]
- **Why it matters**: [Impact of omission]

## Scalability Concerns

### SC-1: [Concern]
- **Reference**: [plan.md section]
- **Problem**: [Why it won't scale]
- **Suggestion**: [Alternative approach]

## Security Concerns

### SEC-1: [Concern]
- **Reference**: [plan.md section]
- **Vulnerability**: [What can be exploited]
- **Required**: [What must be added]

## Data Consistency Concerns

### DC-1: [Concern]
- **Reference**: [plan.md section]
- **Problem**: [What can go wrong]
- **Required**: [What must be defined]

## Task Breakdown Issues

### T-1: [Issue]
- **Task**: [Task number and title]
- **Problem**: [Missing step, wrong order, vague criteria]

## Suggested Changes

1. [Change 1]
2. [Change 2]
3. [Change 3]

## Approval Status

- **APPROVED** — No MUST_FIX items. Ready for implementation.
- **NEEDS_REVISION** — MUST_FIX items present. Plan must be updated before implementation.

**Status**: [APPROVED / NEEDS_REVISION]
**MUST_FIX count**: _
**SHOULD_FIX count**: _
**OPTIONAL count**: _
```

**Severity Classification:**
- **MUST_FIX**: Architecture flaws, missing critical requirements, security holes, data loss risk
- **SHOULD_FIX**: Missing edge cases, scalability concerns, anti-patterns
- **OPTIONAL**: Suggestions, nice-to-haves, future improvements

Present the summary to the human with the approval status and issue counts.
