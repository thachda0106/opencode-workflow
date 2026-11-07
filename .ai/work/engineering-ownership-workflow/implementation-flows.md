# Engineering Ownership Workflow — implementation flows

Mode: Full Engineering · Plan: `.ai/work/engineering-ownership-workflow/plan.md`
Date: 2026-11-07

## Legend

| Label | Meaning |
|-------|---------|
| `[V]` | Verified existing behavior, with `file:line` |
| `[P]` | Planned behavior, with task ID |
| `[?]` | Unknown |

## Diagram inventory

| Diagram | Why it exists | Risk tier | Tasks covered |
|---------|---------------|-----------|---------------|
| Mode routing | Shows how classification selects gates and artifacts | A | T1, T5 |
| Gate lifecycle | Shows the human approval sequence and flow insertion point | A | T1, T5 |
| Knowledge package | Shows what evidence flows into durable knowledge | B | T3, T7, T12 |
| Failure/recovery | Shows context recovery and re-gating paths | A | T5, T11 |

## Feature execution flow — mode routing

```mermaid
flowchart TD
    A["[V] User request<br/>session start"] --> B{"[P] Classify mode<br/>AGENTS.md §1 · T1"}
    B -->|"≤2 files, no critical surface"| C["[P] Lightweight (T0)<br/>0 gates · T1"]
    B -->|"one module, 2–6 files"| D["[P] Standard (T1)<br/>G1–G3 · T1"]
    B -->|"critical trigger / >6 files / >1 module"| E["[P] Full (T2)<br/>G1–G4 · T1"]
    C --> F["[P] Implement → verify → 1-line note<br/>T5"]
    D --> G["[P] scratchpad → G1 → plan → G2 → tasks → G3<br/>T5"]
    E --> H["[P] scratchpad → G1 → plan → G2 → tasks → G3<br/>T5"]
    G --> I["[P] implementation-flows.md<br/>T2"]
    H --> J["[P] implementation-flows.md (mandatory)<br/>T2"]
    I --> K["[P] Implement → verify<br/>T5"]
    J --> L["[P] Implement → verify + stress pass<br/>T5"]
    K --> M["[P] Standard final summary<br/>T5"]
    L --> N["[P] Gate 4 → review.md<br/>T5"]
    M --> O["[P] README + full-flow<br/>T3"]
    N --> P["[P] Full package<br/>T3"]
```

## Gate lifecycle — Standard and Full

```mermaid
sequenceDiagram
    participant H as Human
    participant A as AI
    participant W as .ai/work/<slug>
    A->>W: [P] write scratchpad.md (T1)
    A->>H: [P] present findings, evidence, risks, scope
    H-->>A: [P] APPROVE GATE 1
    A->>W: [P] write plan.md (T1)
    A->>H: [P] present decisions, alternatives, invariants
    H-->>A: [P] APPROVE GATE 2
    A->>W: [P] write tasks.md (T1)
    A->>H: [P] present tasks, dependencies, risk
    H-->>A: [P] APPROVE GATE 3
    A->>W: [P] write implementation-flows.md (T2)
    A->>A: [P] implement in task order (T5)
    A->>H: [P] verification evidence
    A->>H: [P] Gate 4 review (Full)
    H-->>A: [P] APPROVE GATE 4
    A->>W: [P] write review.md (T5)
```

## Knowledge package flow

```mermaid
flowchart LR
    A["[V] git diff<br/>implementation"] --> B["[P] map-critical-paths<br/>T3"]
    C["[V] plan.md / tasks.md<br/>approved intent"] --> D["[P] transfer-implementation-knowledge<br/>T3"]
    E["[V] implementation-flows.md<br/>pre-code design"] --> D
    F["[V] test output<br/>observed"] --> D
    B --> G["[P] critical-paths.md<br/>T3"]
    D --> H["[P] README.md<br/>T3"]
    D --> I["[P] full-flow.md<br/>T3"]
    D --> J["[P] architecture.md<br/>T3"]
    D --> K["[P] decisions.md<br/>T3"]
    H --> L["[P] index.md<br/>T3"]
    I --> L
```

## Failure and recovery paths

```mermaid
flowchart TD
    A["[P] Session interrupted"] --> B["[P] Read .ai/work/<slug>/*<br/>AGENTS.md §6"]
    B --> C["[P] Inspect git status/diff/log<br/>AGENTS.md §6"]
    C --> D{"[P] Task status matches code/tests?"}
    D -->|yes| E["[P] Resume from last verified checkpoint"]
    D -->|no| F["[P] Correct task status; do not trust stale status"]
    F --> G{"[P] Approved decision changed?"}
    G -->|yes| H["[P] Stop and re-gate at G1/G2/G3"]
    G -->|no| E
    E --> I["[P] Continue implementation"]
    J["[P] Flow contradicts plan"] --> K["[P] Stop; return to GATE 2"]
    L["[P] Scope grows to T2 trigger"] --> M["[P] Re-classify to Full; re-gate"]
```

## Business logic and critical decisions

| Decision | Condition | Behavior | Plan ref | Task |
|----------|-----------|----------|----------|------|
| Mode selection | classification triggers | T0/T1/T2 map to Lightweight/Standard/Full | D1 | T1 |
| Gate count | mode | 0/3/4 gates | D1 | T1 |
| Flow insertion | after Gate 3, before code | mandatory Full; mandatory Standard when behavior changes | D1/D4 | T2 |
| Knowledge depth | mode | README+full-flow or full package | D3 | T3 |
| Legacy path | old command | canonical `.ai/work/`; legacy note only | D5 | T6 |

## Error propagation

| Trigger | Symptom | Handled by | State left behind |
|---------|---------|------------|-------------------|
| Install not run | live OpenCode still uses old workflow | operator runs `install.sh` and restarts | staging updated, live unchanged |
| Gate text drift | command and policy disagree | `verify.py` workflow check fails | repository inconsistent until fixed |
| Stale plan path | artifact written in two homes | stale-path check fails | commands inconsistent |
| Flow skipped | code exists without design | Gate 3/4 rule + review finding | change not complete |
| Diagram stale | knowledge contradicts code | Gate 4 reconciliation; update `[P]`→`[V]` only with evidence | review should block completion |

## External services and database interactions

Not applicable. This change modifies Markdown configuration, templates, and a Python validation
script. No database, network, or external service is touched.

## Task → behavior mapping

| Task | Behavior | Flow node(s) | Files | Acceptance |
|------|----------|--------------|-------|------------|
| T1 | Mode routing and gates | Mode routing, Gate lifecycle | `AGENTS.md` | tokens present; verify passes |
| T2 | Pre-code flow design | Mode routing → flows | `skills/design-implementation-flows` | skill valid and loadable |
| T3 | Visual knowledge package | Knowledge package | `skills/transfer-implementation-knowledge`, templates | package contract present |
| T4 | Risk/flow/ownership integration | Mode routing, Knowledge package | 3 skills | flow priority and reconciliation present |
| T5 | Command lifecycle | Gate lifecycle | 8 commands | gates and artifacts referenced |
| T6 | Path consistency | Gate lifecycle | 9 commands | stale-path check passes |
| T7 | Templates | Gate lifecycle, Knowledge package | prompt/knowledge templates | Mermaid + labels present |
| T8 | Validation | Failure/recovery | `scripts/verify.py` | `verify.py` 0 fail |
| T9 | Documentation | All | README/docs/context | consistent with workflow |
| T10 | Install | Failure/recovery | live config | dry-run + install succeed |
| T11 | Simulations | All | `docs/VALIDATION.md` | three scenarios documented |
| T12 | Knowledge/Gate 4 | Knowledge package | package + review | Gate 4 evidence present |

## Invariant coverage

| Invariant | Visible in flow? | Node | How enforced |
|-----------|------------------|------|--------------|
| INV1 | yes | Mode routing | `verify.py` contract check |
| INV2 | yes | Mode routing, Gate lifecycle | `verify.py` workflow check |
| INV3 | yes | Gate lifecycle | Gate 3 rule; review |
| INV4 | yes | Knowledge package | transfer skill + templates |
| INV5 | yes | Mode routing, Knowledge package | `.ai/work/` vs `.ai/knowledge/` |
| INV6 | yes | Failure/recovery | install + parity check |
| INV7 | yes | Failure/recovery | `verify.py` config check |
| INV8 | yes | All | `verify.py` run |

## Open questions

- Runtime gate adherence is prompt-driven. Resolved as a non-goal: gates are not mechanically
  enforced; `verify.py` enforces the text contract and simulations test intended behavior.

## Post-implementation reconciliation (2026-11-07)

| Planned element | Actual | Evidence | Status |
|-----------------|--------|----------|--------|
| `AGENTS.md` modes/gates | Installed and schema-valid | `python scripts/verify.py` | verified |
| New flow skill | Loaded by OpenCode | `opencode debug skill` | verified |
| Work artifact contract | Templates + commands reference `.ai/work/<slug>/` | `verify.py` stale-path check | verified |
| Knowledge package contract | Templates + transfer skill updated | `verify.py` contract check | verified |
| Live config sync | 36 + 9 files installed; backups created | `install.sh` output | verified |
| Runtime gate adherence | Not exercised end-to-end | — | untested |
| Mermaid rendering | Not rendered in a viewer this session | — | assumed |
| Standard/Full simulations | Spec-level walkthroughs only | `docs/VALIDATION.md` §8.3 | assumed |

`[P]` nodes in the diagrams above describe workflow behavior that is installed but not
runtime-proven. They should become `[V]` only after a real Standard/Full session exercises the
gates.
