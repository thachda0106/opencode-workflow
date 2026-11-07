# Engineering Ownership Workflow — investigation

Mode: Full Engineering (T2) · Date: 2026-11-07
Objective: upgrade the existing OpenCode workflow into a gated engineering-ownership lifecycle
without creating a parallel process or losing existing capabilities.

## Scope

- In scope: `AGENTS.md`, skills, commands, prompt/knowledge templates, `scripts/verify.py`,
  workflow docs, `context/BOUNDARIES.md`.
- Out of scope: `opencode.json` permission matrix, existing agents, `_retired/`, live life-*
  commands/skills, application code.
- Re-tier point: any change requiring a new config key, new dependency, or deletion of existing
  capabilities.

## What exists today

The current system maps T0/T1/T2 to no-plan/inline-plan/one-gate workflows. `/ai-workflow` stops
once for T2; investigation and plan share one file; there is no `tasks.md`, no pre-code flow
design, no Mermaid, and the knowledge store is a single `features/<slug>.md` report.

## Observations

| # | Observation | Evidence | Confidence |
|---|-------------|----------|------------|
| O1 | AGENTS defines only one T2 stop, after the plan | `AGENTS.md` §2 (pre-change) | high |
| O2 | T0/T1/T2 are risk tiers, not named workflow modes | `AGENTS.md` §1 (pre-change) | high |
| O3 | `/ai-workflow` writes investigation into the plan and has no separate tasks artifact | `commands/ai-workflow.md` Phase 1–2 (pre-change) | high |
| O4 | No skill or template mentions Mermaid or pre-code flows | grep of `skills/`, `prompts/templates/`, `templates/knowledge/` | high |
| O5 | Knowledge transfer writes one file, `features/<slug>.md` | `skills/transfer-implementation-knowledge/SKILL.md` (pre-change) | high |
| O6 | 10+ commands reference `.ai/knowledge/plans/<slug>.md` | grep across `commands/` | high |
| O7 | `context/BOUNDARIES.md` still documents `SCRATCHPAD.md`/`PLAN.md`/`TASKS.md` gates | `context/BOUNDARIES.md` (pre-change) | high |
| O8 | `verify.py` caps `HARD STOP` in commands at 1 outside greenfield flows | `scripts/verify.py` (pre-change) | high |
| O9 | Repo and global `AGENTS.md` are byte-identical; install parity is clean | `Get-FileHash`; `python scripts/verify.py` | high |

## Findings

The existing system has strong risk ranking, evidence labels, and ownership checks, but the
workflow is under-specified for Standard/Full engineering: there is no mode routing, no
investigation/decision separation, no execution contract, no visual design stage, and no visual
knowledge package. The gap is architectural, not cosmetic.

## Hypotheses

| # | Hypothesis | Why plausible | How to confirm |
|---|------------|---------------|----------------|
| H1 | One new skill is enough; the rest can be extensions | existing skills already own adjacent jobs | the new skill is only referenced by the workflow and does not duplicate another skill |
| H2 | `.ai/work/` is a better home for process artifacts than `.ai/knowledge/plans/` | the knowledge store excludes task lists | templates and README separate process from durable knowledge |

## Assumptions

- OpenCode 1.19.5 loads new `SKILL.md` and command Markdown without config changes — assumed.
- Mermaid renders in the user's Markdown viewer/IDE — assumed.
- The live config is updated by `scripts/install.sh`; the user restarts OpenCode — assumed.

## Risks

- Gate inflation: Standard/Full stops become rubber stamps. Mitigation: explicit approval phrases,
  artifact budgets, and Lightweight at 0 gates.
- Diagram staleness: flows diverge from code. Mitigation: Gate 4 reconciliation and knowledge
  update rule.
- Documentation duplication: package restates code. Mitigation: link to source and keep budgets.
- Migration drift: old commands keep legacy paths. Mitigation: mechanical path update + verify.py.

## Open questions

- Should Standard carry a formal Gate 4? Resolved in the approved plan: no, except on deviation
  or risk escalation.
- Should T2 one-line changes get a fast lane? Resolved: no; consequence, not diff size, selects
  Full.

## Alternatives considered

| Alternative | Why it might work | Why it loses |
|-------------|-------------------|--------------|
| Keep the single T2 gate and add Mermaid only | less process | cannot review investigation or execution separately; developer remains a late approver |
| Extend `trace-execution-flow` for pre-code design | fewer skills | conflates verified existing behavior with planned behavior |
| Put all artifacts under `.ai/knowledge/plans/<slug>/` | reuses existing path | mixes transient process state with durable knowledge; violates the store's own rules |
| Restore the old 3-gate model for every task | familiar | reintroduces the 45-gate rubber-stamp failure |
