# Architecture — AI accelerates implementation, the engineer owns the system

## 1. Design principles

1. **One always-loaded rule file decides the process.** Modes, gates, artifact paths, evidence
   labels, and the knowledge contract live in `AGENTS.md`. Commands and skills reference it
   instead of restating it.
2. **Effort tracks consequence, not file count.** T0/T1/T2 remain risk tiers; they map directly
   to Lightweight/Standard/Full workflow modes.
3. **Every mode has a distinct cost.** Lightweight has 0 gates, Standard 3, Full 4. The full
   lifecycle is never forced on a trivial change.
4. **Investigation is reviewable before decisions are made.** `scratchpad.md` holds evidence and
   hypotheses; `plan.md` holds approved decisions; `tasks.md` holds the execution contract.
5. **System behavior is designed before code.** `implementation-flows.md` connects approved
   decisions and tasks to Mermaid flows, with verified and planned behavior explicitly labelled.
6. **Understanding is a build step.** Standard/Full work is not complete until the feature
   knowledge package exists. Full-flow documentation is visual, not text-only.
7. **Nothing is claimed that was not observed.** VERIFIED, TESTED, ASSUMED, GAP remain the only
   evidence labels. Green tests never upgrade a label.
8. **Knowledge lives next to the code.** `.ai/knowledge/` is git-tracked, index-first, and updated
   in place.

---

## 2. Layers

```text
┌──────────────────────────────────────────────────────────────────────┐
│ LAYER 0 — AGENTS.md  (loaded every session)                          │
│   modes · gates · artifact paths · evidence labels · knowledge map   │
└───────────────┬──────────────────────────────────────────────────────┘
                │ referenced by
┌───────────────▼──────────────────────────────────────────────────────┐
│ LAYER 1 — COMMANDS (entry points, thin: sequence + output shape)     │
│   /ai-workflow  /create-feature  /fix-bug  /review-implemented-files │
│   /review-plan  /knowledge-report  /ownership-check                  │
└───────────────┬──────────────────────────────────────────────────────┘
                │ loads
┌───────────────▼──────────────────────────────────────────────────────┐
│ LAYER 2 — SKILLS (procedures, loaded on demand)                      │
│                                                                      │
│  INVESTIGATE              DESIGN                 VERIFY               │
│  analyze-project-structure design-implementation- map-critical-paths  │
│  trace-execution-flow       flows                 stress-test-        │
│  locate-code-patterns                             implementation      │
│  validate-architecture                            verify-ownership     │
│                                                                      │
│  TRANSFER: transfer-implementation-knowledge                         │
│  FIX: diagnose-bug-root-cause → apply-targeted-fix → verify-regression│
└───────────────┬──────────────────────────────────────────────────────┘
                │ writes
┌───────────────▼──────────────────────────────────────────────────────┐
│ LAYER 3 — WORK + KNOWLEDGE                                           │
│  .ai/work/<slug>/   scratchpad · plan · tasks · flows · review        │
│  .ai/knowledge/     index · critical-paths · features/<slug>/ · …     │
└──────────────────────────────────────────────────────────────────────┘
```

Agents are orthogonal: they are *who* executes. Skills are *how*. The lifecycle is *when*.

---

## 3. Mode model

| | Lightweight (T0) | Standard (T1) | Full Engineering (T2) |
|---|---|---|---|
| **Trigger** | ≤2 files, no critical surface | one module, 2–6 files | authz · money · tx boundary · migration · concurrency · idempotency · external contract · cache invalidation · state machine · deletion · cross-service · trust-boundary validation · crypto · >6 files / >1 module |
| **Investigation** | none | `scratchpad.md` | `scratchpad.md` |
| **Gates** | 0 | 3 (G1–G3) | 4 (G1–G4) |
| **Flows** | none | mandatory when behavior changes (compact) | mandatory (comprehensive) |
| **Verification** | typecheck + build | + targeted tests | + full suite + stress pass |
| **Knowledge** | 1 line | README + full-flow | all four package files |
| **Ownership** | none | on request | offered once |

Objective test: if you cannot name a concrete T2 trigger, the task is Standard. If it is ≤2 files
with no critical surface and no new public interface, it is Lightweight.

---

## 4. Lifecycle

```text
CLASSIFY
  → INVESTIGATE → scratchpad.md → GATE 1
  → PLAN        → plan.md       → GATE 2
  → TASKS       → tasks.md      → GATE 3
  → FLOWS       → implementation-flows.md
  → IMPLEMENT → VERIFY
  → GATE 4 (Full; Standard on deviation) → KNOWLEDGE → COMPLETE
```

Gate semantics:

| Gate | Freezes | What must be explicit |
|------|---------|-----------------------|
| G1 | Scope | Findings, evidence, assumptions, risks |
| G2 | Plan baseline | Decisions, alternatives, invariants, verification |
| G3 | Execution plan | Tasks, dependencies, order, risk |
| G4 | Completion | Results, evidence, deviations, updated flows, remaining risks |

Approval is explicit; silence is not approval; one gate never implies the next.

---

## 5. Artifact contract

| Artifact | Location | Owner | Purpose |
|---|---|---|---|
| `scratchpad.md` | `.ai/work/<slug>/` | investigation | Evidence, hypotheses, unknowns; no decisions |
| `plan.md` | `.ai/work/<slug>/` | planning | Approved engineering decisions and invariants |
| `tasks.md` | `.ai/work/<slug>/` | planning | Reviewable execution contract |
| `implementation-flows.md` | `.ai/work/<slug>/` | `design-implementation-flows` | Pre-code visual system behavior |
| `review.md` | `.ai/work/<slug>/` | review | Gate 4 evidence and deviations |
| feature package | `.ai/knowledge/features/<slug>/` | `transfer-implementation-knowledge` | Durable visual knowledge |

Legacy `features/<slug>.md` and `plans/<slug>.md` remain readable. New work does not write them.

---

## 6. Visual documentation

`implementation-flows.md` and `full-flow.md` use Mermaid as the primary format:

| Diagram | Use for |
|---|---|
| Flowchart | Business logic and execution paths |
| Sequence | API calls, services, async, external integrations |
| State | State transitions and lifecycle |
| ER | Data relationships and schema |
| Architecture | Component boundaries and dependencies |

Every diagram element is labelled `[V]` verified existing behavior with `file:line`, `[P]` planned
behavior with a task ID, or `[?]` unknown. Diagrams include failure and alternative paths for
Full work. Mermaid source stays inside Markdown.

`full-flow.md` is the first document a maintainer reads. It must cover the complete lifecycle,
critical decision points, source mapping, production debugging, and an ownership checklist.

---

## 7. Risk-based review

| Tier | Diagrams | Review depth | Stress pass | Ownership |
|---|---|---|---|---|
| A | Flowchart + sequence/state | All dimensions, hand-trace, concurrency, rollback | Mandatory | Level 3 |
| B | Flowchart if material | Correctness, bugs, security, architecture, tests | If write/state/external | Level 2 |
| C | None | Correctness and conventions | Lightweight | Level 1 |

High-risk paths are transactions, concurrency, authz, security, data consistency, external
integrations, and critical business invariants. They get deeper verification and diagrams that
explain the execution path. Boilerplate does not.

---

## 8. Skill map

| Skill | Owns | Explicitly refuses |
|---|---|---|
| `design-implementation-flows` | What will the system do before code exists? | implementation, review, durable knowledge |
| `transfer-implementation-knowledge` | What must I understand after the change? | grading code, restating the plan, teaching frameworks |
| `map-critical-paths` | Where should attention go? | fixing, benchmarking, explaining, reviewing |
| `stress-test-implementation` | What happens when the world misbehaves? | rewriting, certifying correctness, security audit |
| `verify-ownership` | Can I maintain this without AI? | capability judgements, interview prep, whole-repo scope |

One new skill was added because pre-code flow design is a distinct stage from post-code knowledge
transfer. Extending `trace-execution-flow` was rejected: it would conflate verified existing
behavior with planned behavior.

---

## 9. Validation

- `scripts/verify.py` checks schema, references, the workflow contract, Mermaid templates, stale
  plan paths, gate policy, config safety, and install parity.
- `opencode debug skill` proves which skills actually loaded.
- `docs/VALIDATION.md` records the audit, install, and the three workflow simulations.

---

## 10. Compatibility

- OpenCode 1.19.5; no new config keys.
- `opencode.json` is unchanged; the permission matrix remains the strongest safety control.
- Existing agents, commands, skills, and knowledge files are preserved or updated in place.
- `scripts/install.sh` is additive and backs up overwritten files.
