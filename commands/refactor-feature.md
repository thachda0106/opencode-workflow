---
description: Refactor code for clarity and maintainability without changing behavior
agent: feature-builder
subtask: false
---

# Refactor Feature

> **Modes and gates**: follow the mode table in `AGENTS.md`. Lightweight runs with no stops;
> Standard uses Gates 1–3; Full uses Gates 1–4. Work artifacts live under `.ai/work/<slug>/`.

Refactor the selected code for clarity and maintainability without changing behavior.

---

## 1 · INVESTIGATE — Analysis

**No code changes in this phase. Analysis only.**

1. Read and comprehend current code
2. Find all references and dependencies of the code being refactored
3. Identify code smells and improvement areas:
   - Long functions (>80 lines)
   - Deep nesting (>3 levels)
   - Repeated code blocks
   - Magic numbers/strings
   - Complex boolean expressions
   - Large modules/classes (>500 lines)
   - API layer with business logic
   - Missing error handling
4. Read project context if present (`context/PROJECT.md`, `context/CONVENTIONS.md`, `context/BOUNDARIES.md`); if those files are absent, infer conventions from existing code and say so
5. Write analysis into `.ai/work/<slug>/plan.md`

---

## 2 · PLAN — Refactoring Strategy

1. Define the refactoring strategy from the plan file:
   - **Code Clarity** — Extract complex logic into named functions, use descriptive names
   - **DRY** — Extract repeated logic into utilities, create shared services
   - **Type Safety** — Strict typing, leverage inference, extract shared types
   - **Single Responsibility** — Each function/class does one thing
   - **Performance** — Optimize queries, avoid N+1, cache where appropriate
2. For each refactoring:
   - **What** — Describe what is being refactored
   - **Why** — Explain the problem or improvement
   - **How** — Show before/after approach
   - **Impact** — Performance or maintainability gains
3. Risk analysis — what could break?
4. Write into `.ai/work/<slug>/plan.md`

---

## 3 · STEPS — Refactoring Steps

1. Break the refactoring into ordered steps:
   - [ ] Step 1: Description + files to change
   - [ ] Step 2: Description + files to change
   - [ ] Step N: Update/add tests
2. For each step, specify:
   - What changes
   - Why
   - Expected behavior (must be unchanged)
3. Write into `.ai/work/<slug>/plan.md`

---

## 4 · IMPLEMENT — Refactor

- Refactor step by step in the order defined in `.ai/work/<slug>/plan.md`
- Ensure behavior is unchanged at each step
- Do not introduce scope creep

---

## 5 · VERIFY

After refactoring:
- Run tests to verify behavior unchanged
- Run type check and lint
- Verify no regressions
