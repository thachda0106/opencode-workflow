---
description: Review code strictly against project architecture rules and call out violations
agent: code-reviewer
subtask: false
---

# Review Architecture

> **Gates**: this command follows the tier model in `AGENTS.md`. T0/T1 run with no stops;
> T2 stops once, after the plan. Investigation notes, plan, and step list all live in
> `.ai/knowledge/plans/<slug>.md` — not in three root-level files.

Review the codebase against the project's architecture rules as defined in `context/PROJECT.md` and `context/CONVENTIONS.md`. If those files are absent, infer the rules from existing patterns and state that assumption.

---

## 1 · INVESTIGATE — Scope & Context

**No review output in this phase. Research only.**

1. Read project context if present (`context/PROJECT.md`, `context/CONVENTIONS.md`, `context/BOUNDARIES.md`); if those files are absent, infer conventions from existing code and say so
2. Identify what to review:
   - Which modules/components to check
   - What rules apply (directory structure, imports, naming, layers)
3. Catalog the architecture rules to validate against
4. Write into `.ai/knowledge/plans/<slug>.md`:
   - Review scope
   - Architecture rules to check
   - Files/modules to examine

---

## 2 · PLAN — Review Strategy

1. Define the review strategy:
   - Order of checks (directory → imports → naming → layers → DI)
   - Priority areas (known problem spots vs. full scan)
2. Write into `.ai/knowledge/plans/<slug>.md`

---

## 3 · REVIEW EXECUTION

Execute the review following the plan file:

### What to Check

- **Directory Structure**: Files in correct locations, module boundaries respected, naming patterns match
- **Import Boundaries**: No cross-boundary imports, path aliases used, no circular dependencies
- **Module Structure**: Separation of concerns (controller → service → repository), business logic in correct layer
- **Dependency Injection**: Constructor injection, no circular dependencies, providers registered correctly
- **Naming Conventions**: Files, classes, and variables follow project patterns

### Validation Checklist

- [ ] Import from wrong level
- [ ] Missing path aliases (deep relative imports)
- [ ] Wrong directory structure
- [ ] Incorrect naming
- [ ] Circular dependencies
- [ ] Business logic in API layer
- [ ] Missing input validation
- [ ] Test files in wrong location
- [ ] Hardcoded values

### Output Format

For each violation:
- **File**: Path to file
- **Line**: Line number(s)
- **Rule**: Which architecture rule is violated
- **Impact**: Why this matters
- **Fix**: How to resolve

### Architecture Score

Rate compliance: **Pass** | **Minor Issues** | **Major Violations**
