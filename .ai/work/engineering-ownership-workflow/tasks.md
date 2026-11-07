# Engineering Ownership Workflow — tasks

Mode: Full Engineering (T2) · Plan: `.ai/work/engineering-ownership-workflow/plan.md`

| ID | Objective | Status | Depends on | Impacted files | Acceptance criteria | Verification | Risk | Plan ref |
|----|-----------|--------|------------|----------------|---------------------|--------------|------|----------|
| T0 | Create work artifacts for this migration | done | — | `.ai/work/engineering-ownership-workflow/*` | scratchpad, plan, tasks, flows present | files exist; plan approved | low | INV5 |
| T1 | Rewrite `AGENTS.md` for modes, gates, artifacts, flows, ownership, recovery | done | T0 | `AGENTS.md` | all workflow tokens present; T0/T1/T2 and labels preserved | `verify.py` workflow check | medium | D1, D2, D3 |
| T2 | Add `design-implementation-flows` skill | done | T1 | `skills/design-implementation-flows/SKILL.md` | valid frontmatter; labels, diagram rules, non-goals | `verify.py` skills check; skill loaded | medium | D4 |
| T3 | Rewrite knowledge transfer to package + full-flow | done | T1 | `skills/transfer-implementation-knowledge/SKILL.md` | README/full-flow/architecture/decisions contract | `verify.py`; template review | medium | D3, INV4 |
| T4 | Integrate risk/flow/ownership into existing skills | done | T1, T2, T3 | `map-critical-paths`, `stress-test-implementation`, `verify-ownership` | flow priority, reconciliation, Level 1–3 | read-through; `verify.py` | medium | INV4 |
| T5 | Rewrite core workflow commands | done | T1–T4 | `ai-workflow`, `create-feature`, `fix-bug`, `review-implemented-files`, `knowledge-report`, `ownership-check`, `review-plan`, `explain-logic` | modes, gates, flows, package paths | `verify.py` gates/workflow | medium | D1, D2 |
| T6 | Update legacy plan path references | done | T5 | 9 commands | no stale `.ai/knowledge/plans/<slug>.md` in commands except review-plan legacy note | `verify.py` stale-path check | low | D5 |
| T7 | Update prompt and knowledge templates | done | T1, T3 | `prompts/templates/*`, `templates/knowledge/*` | required fields, Mermaid, labels, budgets | `verify.py` contract/Mermaid | medium | D2, D3 |
| T8 | Extend `verify.py` | done | T1, T7 | `scripts/verify.py` | workflow contract, Mermaid, stale paths, gate checks | `python scripts/verify.py` | medium | INV8 |
| T9 | Update README, architecture, audit, context | done | T1–T8 | `README.md`, `docs/*`, `context/BOUNDARIES.md` | consistent with new workflow | read-through; `verify.py` | low | INV6 |
| T10 | Install staging → live config | done | T8, T9 | `~/.config/opencode` | install dry-run clean; install succeeds; backup exists | `scripts/install.sh --dry-run`; `install.sh` | high | INV6 |
| T11 | Run workflow simulations | done | T10 | `docs/VALIDATION.md` | Lightweight/Standard/Full scenarios + recovery | documented walkthrough + checks | medium | INV2 |
| T12 | Knowledge package + Gate 4 review | done | T11 | `.ai/knowledge/features/engineering-ownership-workflow/*`, `.ai/work/.../review.md` | package complete; Gate 4 evidence | `verify.py`; final review | medium | INV4 |
