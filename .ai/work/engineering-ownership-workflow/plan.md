# Engineering Ownership Workflow — plan

Mode: Full Engineering (T2) · Tier: T2 · Date: 2026-11-07
Status: approved · Approved: 2026-11-07 (human APPROVE of the architecture)
Objective: integrate a gated engineering-ownership lifecycle into the existing OpenCode skills,
commands, templates, and knowledge store without creating a parallel workflow.

## Scope

- In scope: `AGENTS.md`, skills, commands, prompt/knowledge templates, `scripts/verify.py`,
  workflow docs, `context/BOUNDARIES.md`, this change's work and knowledge artifacts.
- Out of scope: `opencode.json`, agents, `_retired/`, live-only life-* commands/skills, product
  code.

## Invariants that must hold

| ID | Invariant | Test / check |
|----|-----------|--------------|
| INV1 | T0/T1/T2 triggers and VERIFIED/TESTED/ASSUMED/GAP labels remain | `verify.py` contract check |
| INV2 | Every mode has a fixed gate count: 0/3/4 | `verify.py` workflow check + AGENTS table |
| INV3 | No source changes before required implementation flows exist | command text + Gate 3 rule |
| INV4 | Full features get visual `full-flow.md`; Standard behavior changes get it too | transfer skill + templates |
| INV5 | Work artifacts and durable knowledge are separate | `.ai/work/` vs `.ai/knowledge/` contract |
| INV6 | Existing skills/commands/knowledge files remain usable | parity/ref checks; legacy notes |
| INV7 | No new config keys or dependencies | `opencode.json` unchanged; `verify.py` config check |
| INV8 | `verify.py` stays at 0 fail after the upgrade | command run |

## Findings summary

The audit found 13 gaps: no mode routing, one gate, collapsed investigation/plan, no tasks, no
implementation flows, no Mermaid, single-file knowledge, no ownership levels, no context recovery,
review not tied to diagrams, a gate-policy checker limit, legacy path drift, and a stale gate
context file. Details: `.ai/work/engineering-ownership-workflow/scratchpad.md`.

## Architecture decisions

| ID | Decision | Alternative rejected | Why |
|----|----------|----------------------|-----|
| D1 | Map T0/T1/T2 to Lightweight/Standard/Full; Standard = G1–G3, Full = G1–G4 | 4 gates for Standard too | preserves the consequence-based cost model; Gate 4 still applies on deviation |
| D2 | Work artifacts in `.ai/work/<slug>/`; durable knowledge in `.ai/knowledge/features/<slug>/` | all artifacts under `.ai/knowledge/plans/<slug>/` | keeps task lists out of the knowledge store; one location per artifact type |
| D3 | Standard knowledge = README + full-flow; Full = all four files | Standard also gets all four | full-flow is the mandatory visual artifact; architecture/decisions fold in when small |
| D4 | Add one skill, `design-implementation-flows` | extend `trace-execution-flow` | pre-code planned behavior is distinct from post-code verified behavior |
| D5 | Update legacy plan paths in older commands | leave them and allow dual paths | consistency; one canonical work path |

## Trade-offs

- Standard and Full work pay more approval round-trips. Accepted because the mission prioritizes
  ownership over throughput; Lightweight remains zero-gate.
- `AGENTS.md` grows. Mitigation: policy only; procedures live in skills/commands.
- Mermaid diagrams can go stale. Mitigation: Gate 4 reconciliation and the knowledge-update rule.
- One new skill increases skill count. Accepted because it owns a mandatory stage and has explicit
  non-goals.

## Impacted components

| Component | Change | Contract |
|-----------|--------|----------|
| `AGENTS.md` | modes, gates, artifacts, flows, knowledge, recovery | always-loaded policy |
| `ai-workflow`, `create-feature`, `fix-bug` | mode-aware lifecycle | command entry points |
| `review-implemented-files`, `review-plan` | Gate 4 + artifact review | review contract |
| `knowledge-report`, `ownership-check`, `explain-logic` | package paths and levels | knowledge interface |
| `transfer-implementation-knowledge`, `map-critical-paths`, `stress-test-implementation`, `verify-ownership` | package/flow/level integration | skill interface |
| `verify.py` | workflow contract checks | validation interface |

## Failure modes

| If this fails | System state | Handled how |
|---------------|--------------|-------------|
| Install not run | staging updated, live workflow unchanged | run `install.sh`, restart OpenCode |
| Gate text drifts | commands and AGENTS disagree | `verify.py` workflow/gate checks fail |
| Legacy path remains in a command | two artifact homes | stale-path check fails |
| Flows are skipped | code proceeds without design | Gate 3/4 rules + review checklist |
| Diagram contradicts code | false knowledge | Gate 4 reconciliation; update `[P]`→`[V]` only with evidence |

## Security

- No trust-boundary or authz code changes.
- No secrets read or written; `opencode.json` permissions unchanged.
- Workflow artifacts are git-tracked; no sensitive data may be written into them.

## Rollback

- `install.sh` creates a timestamped backup of every overwritten file.
- Revert is a normal git revert of this repository plus restore from the backup directory.
- No database or production state is touched.

## Verification strategy

```bash
python scripts/verify.py
opencode debug skill
opencode agent list
```

Scenarios: Lightweight bug fix; Standard feature; Full architectural change; interrupted-session
recovery; Standard risk escalation to Full.

## Acceptance criteria

- [ ] `python scripts/verify.py` → 0 fail.
- [ ] New skill loads and is referenced by the workflow.
- [ ] All commands use the canonical work path or an explicit legacy note.
- [ ] Templates contain Mermaid and evidence labels.
- [ ] Three simulations show correct mode selection and artifact expectations.
- [ ] Knowledge package for this upgrade exists after Gate 4.

## Non-goals

- Changing `opencode.json` or the permission matrix.
- Rewriting agents.
- Deleting legacy knowledge files or retired commands.
- Automating runtime gate enforcement (gates remain prompt-driven).

## Approved baseline

Approved by explicit human `APPROVE` on 2026-11-07. Gate 3 for this migration is covered by the
same approval because the plan already contained the file set, task order, and verification
strategy. Gate 4 applies after implementation.
