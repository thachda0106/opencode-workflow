# Engineering Ownership Workflow — README

Mode: Full Engineering · Date: 2026-11-07 · Revised: 2026-11-07
Scope: workflow policy, skills, commands, templates, validation, docs, and knowledge artifacts.

## What it does

Upgrades the OpenCode workflow from risk-tiered ad-hoc delivery into a gated
engineering-ownership lifecycle: investigation, approved decisions, execution tasks, pre-code
Mermaid flows, implementation, verification, final review, and a durable visual knowledge package.

## Why it exists

AI should accelerate implementation without turning the developer into a passive approver.
The workflow keeps the human on the decisions that matter, makes system behavior visible before
code exists, and preserves enough knowledge to debug and evolve the feature later.

## Actors and triggers

| Actor / trigger | What happens | Outcome |
|-----------------|--------------|---------|
| Developer starts a task | Mode classification (Lightweight/Standard/Full) | Correct gate and artifact set |
| Developer approves a gate | Scope, plan, or execution is frozen | AI proceeds within that scope only |
| Implementation finishes | Verification + flow reconciliation | Gate 4 evidence or final summary |
| Feature completes | Knowledge package written | Visual, durable understanding |

## Main components

| Component | Responsibility | Entry point |
|-----------|----------------|-------------|
| `AGENTS.md` | Policy: modes, gates, artifacts, labels, knowledge | always loaded |
| `/ai-workflow` | Master lifecycle | command |
| `/create-feature`, `/fix-bug` | Mode-aware feature/bug entry points | commands |
| `design-implementation-flows` | Pre-code Mermaid flow design | skill |
| `transfer-implementation-knowledge` | Durable visual package | skill |
| `map-critical-paths`, `stress-test-implementation`, `verify-ownership` | Risk, failure, ownership checks | skills |
| `scripts/verify.py` | Contract and install validation | script |

## Source files

| File | Why it matters |
|------|----------------|
| `AGENTS.md` | The single source of workflow policy |
| `commands/ai-workflow.md` | The executable lifecycle |
| `skills/design-implementation-flows/SKILL.md` | The pre-code design contract |
| `skills/transfer-implementation-knowledge/SKILL.md` | The knowledge package contract |
| `templates/knowledge/full-flow.md` | The visual knowledge template |
| `scripts/verify.py` | Prevents workflow drift |

## Read next

- [full-flow.md](full-flow.md) — complete lifecycle, diagrams, debugging guide.
- [architecture.md](architecture.md) — boundaries, dependencies, integration points.
- [decisions.md](decisions.md) — decisions, alternatives, trade-offs, limitations.

## Top risks

- Gate rubber-stamping: approvals become reflexive. Mitigation: explicit gate phrases, artifact
  budgets, and zero gates for Lightweight.
- Diagram staleness: flows diverge from code. Mitigation: Gate 4 reconciliation.
- Install drift: live config not updated. Mitigation: `scripts/install.sh` + parity check.
