# Engineering Ownership Workflow — decisions

Mode: Full Engineering · Date: 2026-11-07

| ID | Decision | Alternatives considered | Reason | Trade-off | Revisit if |
|----|----------|-------------------------|--------|-----------|------------|
| D1 | T0/T1/T2 map to Lightweight/Standard/Full; Standard gets G1–G3, Full gets G1–G4 | 4 gates for Standard; keep one T2 gate | Consequence-based cost model; preserves zero-gate Lightweight | Standard pays three round-trips; T2 one-liners pay four | Gate fatigue makes approvals meaningless |
| D2 | Work artifacts in `.ai/work/<slug>/`; durable knowledge in `.ai/knowledge/features/<slug>/` | Keep everything under `.ai/knowledge/plans/<slug>/` | The knowledge store excludes task lists; process and knowledge differ in lifetime | New top-level directory; 9 commands needed path updates | Teams want a single `.ai/` root |
| D3 | Standard knowledge = README + full-flow; Full = all four files | Standard also gets all four | Full-flow is the mandatory visual artifact; architecture/decisions fold in when small | Standard may lack a dedicated decisions file | Standard features grow large enough to need separate architecture |
| D4 | Add `design-implementation-flows` skill | Extend `trace-execution-flow` | Pre-code planned behavior is distinct from post-code verified behavior | One more skill to load | The skill duplicates another procedure in practice |
| D5 | Update legacy plan paths in older commands | Leave legacy paths and allow dual homes | One canonical work path; verify.py can enforce it | Mechanical churn in 9 commands | Legacy commands are retired instead |

## Decision detail

### D1 — Mode mapping and gate counts

- **Context:** The old system had one T2 gate; the mission requires investigation, plan, tasks,
  implementation flows, and final review, but also explicitly says not to force the full workflow
  on every task.
- **Chosen:** T0 → Lightweight (0 gates), T1 → Standard (G1–G3), T2 → Full (G1–G4).
- **Rejected:** Four gates for every mode. It recreates the 45-gate failure where approvals become
  rubber stamps.
- **Cost:** Standard features pay three approvals; T2 one-line changes pay four.
- **Enforcement:** `AGENTS.md` mode table; `verify.py` workflow contract.

### D2 — Work vs knowledge separation

- **Context:** The knowledge store's own README says task lists and sprint plans do not belong in
  `.ai/knowledge/`.
- **Chosen:** `.ai/work/<slug>/` for scratchpad, plan, tasks, flows, review; `.ai/knowledge/` for
  durable packages.
- **Rejected:** `.ai/knowledge/plans/<slug>/` for everything. It mixes transient process state
  with durable facts and makes the knowledge index noisy.
- **Cost:** A new directory and path updates in legacy commands.
- **Enforcement:** `AGENTS.md` §11; `verify.py` stale-path check.

### D3 — Standard knowledge depth

- **Context:** The mission says every medium/complex feature must have `full-flow.md`, but Full
  work carries additional architecture and decision artifacts.
- **Chosen:** Standard gets `README.md` + `full-flow.md`; Full gets all four.
- **Rejected:** All four for Standard. It adds ceremony without a clear consumer for small
  features.
- **Cost:** A Standard feature may need a follow-up `architecture.md` when boundaries grow.
- **Enforcement:** `transfer-implementation-knowledge` and `AGENTS.md` §7.

### D4 — One new skill

- **Context:** Implementation flow design is mandatory before code; no existing skill owns it.
- **Chosen:** `design-implementation-flows`.
- **Rejected:** Extending `trace-execution-flow`. That skill traces verified existing behavior;
  conflating it with planned behavior would blur evidence labels.
- **Cost:** One more skill; explicit non-goals keep it from absorbing review or knowledge work.
- **Enforcement:** `AGENTS.md` §3 and §14; commands reference the skill.

### D5 — Legacy path migration

- **Context:** 10+ commands wrote to `.ai/knowledge/plans/<slug>.md`.
- **Chosen:** Update them to `.ai/work/<slug>/plan.md`.
- **Rejected:** Allow both paths. Two homes produce split-brain context recovery.
- **Cost:** Mechanical churn; no behavior change.
- **Enforcement:** `verify.py` stale-path check.

## Known limitations

- Gates are prompt-driven; `verify.py` cannot prove the model paused.
- `verify.py` checks text and references, not engineering judgement.
- Mermaid rendering depends on the viewer.
- Live config must be installed and OpenCode restarted.

## Follow-ups

| Item | Trigger | Owner |
|------|---------|-------|
| Runtime Full-mode trial | first real T2 feature | developer |
| Gate-fatigue review | after 10 Standard/Full changes | developer |
| Diagram staleness audit | first time a flow contradicts code | developer |
