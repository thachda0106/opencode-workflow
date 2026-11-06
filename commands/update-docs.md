---
description: Update project documentation to match current codebase state
agent: doc-keeper
subtask: false
---

# Update Documentation

> **Gates**: this command follows the tier model in `AGENTS.md`. T0/T1 run with no stops;
> T2 stops once, after the plan. Investigation notes, plan, and step list all live in
> `.ai/knowledge/plans/<slug>.md` — not in three root-level files.

Update project documentation to match the current codebase state.

---

## 1 · INVESTIGATE — Audit

**No documentation changes in this phase. Audit only.**

1. Identify documentation scope:
   - API documentation
   - Architecture diagrams
   - README / onboarding guides
   - Code comments
   - Configuration docs
2. Read current code structure and patterns
3. Compare with existing documentation
4. Identify gaps, inaccuracies, or outdated sections
5. Write findings into `.ai/knowledge/plans/<slug>.md`:
   - Docs that need updating
   - Gaps found
   - Inaccuracies found

---

## 2 · PLAN — Update Strategy

1. Define what to update and in what order:
   - Files to modify
   - Sections to add, update, or remove
   - Priority (critical inaccuracies first)
2. Write into `.ai/knowledge/plans/<slug>.md`

---

## 3 · STEPS — Update Steps

1. Break updates into ordered steps:
   - [ ] Step 1: Fix inaccurate descriptions in [file]
   - [ ] Step 2: Add missing section to [file]
   - [ ] Step 3: Remove references to deleted features
   - [ ] Step 4: Update code examples
   - [ ] Step 5: Verify all file paths referenced exist
2. Write into `.ai/knowledge/plans/<slug>.md`

---

## 4 · IMPLEMENT

- Update documentation per `.ai/knowledge/plans/<slug>.md`
- Do NOT modify production code — documentation only
- If code needs fixing, escalate to Bug Hunter or Feature Builder
- Keep documentation concise and actionable
- Use consistent formatting throughout

---

## 5 · VERIFICATION

After updates:
- Cross-check with actual code
- Verify all code examples work
- Ensure all file paths referenced exist
