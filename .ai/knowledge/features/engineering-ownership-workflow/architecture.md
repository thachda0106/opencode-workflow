# Engineering Ownership Workflow — architecture

Mode: Full Engineering · Date: 2026-11-07

## Component boundaries

| Component | Owns | Does not own | Boundary |
|-----------|------|--------------|----------|
| `AGENTS.md` | Policy: modes, gates, artifact paths, evidence labels | Procedure details | always-loaded rules |
| Commands | Entry points and stage sequence | Skill internals | user-invoked |
| Skills | One procedure each | Cross-skill policy | loaded on demand |
| `.ai/work/` | Process state: scratchpad, plan, tasks, flows, review | Durable feature knowledge | git-tracked working set |
| `.ai/knowledge/` | Durable feature packages, risk table, gotchas, ADRs | Task lists, sprint plans | git-tracked knowledge store |
| `scripts/verify.py` | Contract, references, parity | Runtime behavior | validation |

## Dependencies

| From | To | Contract | Direction |
|------|----|----------|-----------|
| Commands | `AGENTS.md` | mode/gate/artifact rules | command reads policy |
| Commands | Skills | named procedure | command loads skill |
| Skills | Templates | artifact shape | skill writes template-derived file |
| `transfer-implementation-knowledge` | `.ai/work/<slug>/implementation-flows.md` | pre-code vs actual reconciliation | skill reads work artifact |
| `scripts/verify.py` | `AGENTS.md`, skills, commands, templates | token/ref/parity checks | validation reads repo |
| `scripts/install.sh` | `~/.config/opencode` | additive copy with backup | repo → live |

## Architectural patterns

- **Risk-tiered lifecycle.** T0/T1/T2 map to Lightweight/Standard/Full; gates follow consequence,
  not file count. Rejected: uniform 3-gate model (reintroduces rubber-stamp gates).
- **Single source of policy.** `AGENTS.md` owns modes and gates; commands/skills reference it.
  Rejected: duplicating gate tables in every command (caused 45 divergent gates previously).
- **Evidence labels.** VERIFIED/TESTED/ASSUMED/GAP in every completion. Rejected: "tests pass" as
  proof of correctness.
- **Visual-first knowledge.** Mermaid flows in `implementation-flows.md` and `full-flow.md`.
  Rejected: text-only reports that force linear reading.

## Data ownership

| Data | Owner | Readers | Written by | Consistency rule |
|------|-------|---------|------------|------------------|
| Mode/gate policy | `AGENTS.md` | commands, skills | maintainer | verify.py contract check |
| Investigation evidence | scratchpad | plan, Gate 1 | AI | observations cite file:line |
| Approved decisions | plan | tasks, flows, review | AI + human | frozen at Gate 2; changes re-gate |
| Execution contract | tasks | implementation, review | AI + human | frozen at Gate 3 |
| Planned behavior | implementation-flows | implementation, knowledge | AI | `[P]` until verified |
| Durable knowledge | feature package | future sessions | AI + human review | update in place; link, don't restate |

## Integration points

| Integration | Protocol | Failure mode | Retry / timeout | Auth |
|-------------|----------|--------------|-----------------|------|
| OpenCode skill loader | filesystem `SKILL.md` | skill missing until restart | restart | none |
| OpenCode command loader | filesystem Markdown | command missing until restart | restart | none |
| `install.sh` | additive copy | partial install; backup exists | manual re-run | local user |
| `verify.py` | Python + filesystem | fails on drift | re-run after fix | none |
| Mermaid renderer | Markdown viewer/IDE | diagram not rendered | view in compatible renderer | none |

## Boundaries that must not be crossed

- Source changes before the required `implementation-flows.md` exists.
- Task lists or sprint plans written into `.ai/knowledge/`.
- Approved decisions changed without a Gate 2 re-entry.
- Scope expanded without re-tiering and re-gating.
- Diagrams containing invented behavior to fill a gap.

## Known limitations

- Gates are prompt-driven, not mechanically enforced by OpenCode.
- `verify.py` checks text/shape, not the quality of engineering judgement.
- Mermaid rendering depends on the viewer.
- Live config requires install + restart; staging changes alone do not affect sessions.
