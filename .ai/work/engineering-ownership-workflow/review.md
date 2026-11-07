# Review — Engineering Ownership Workflow upgrade

Mode: Full Engineering · Tier: B (workflow architecture; no product transaction/authz surface)
Scope: workflow policy, skills, commands, templates, validation, docs, and knowledge artifacts · Base: `a1c5fb4`
Verdict: APPROVED_WITH_COMMENTS · Gate 4: approved 2026-11-07

## Findings

| # | Severity | Evidence | File:line | Finding | Why it matters |
|---|----------|----------|-----------|---------|----------------|
| 1 | SHOULD_FIX | CONFIRMED | `commands/add-tests.md:8-10` and 8 sibling commands | Specialized commands now point at the mode table but do not contain their own gate stops | If invoked directly for Standard/Full work, the model must rely on `AGENTS.md`; the header says to do so, but the command body does not enforce it |
| 2 | SHOULD_FIX | CONFIRMED | `commands/design-platform-core.md:18-119` | Greenfield command still uses root `SCRATCHPAD.md`/`PLAN.md`/`TASKS.md` and 3 phase gates | Intentional greenfield exception, now documented in `AGENTS.md` §2; path style differs from new work artifacts |
| 3 | OPTIONAL | CONFIRMED | `docs/VALIDATION.md:230-260` | Simulations are spec-level walkthroughs, not live runtime transcripts | Honest labeling prevents treating them as runtime proof |

No MUST_FIX findings.

## Plan / task / flow compliance

| Item | Status | Evidence |
|------|--------|----------|
| D1 mode mapping + gate counts | pass | `AGENTS.md` §1–2; `verify.py` workflow check |
| D2 `.ai/work/` vs `.ai/knowledge/` | pass | `AGENTS.md` §11; templates; command paths |
| D3 Standard/Full knowledge depth | pass | `AGENTS.md` §7; transfer skill; knowledge templates |
| D4 one new flow skill | pass | `skills/design-implementation-flows/SKILL.md`; loaded by OpenCode |
| D5 legacy path migration | pass | 9 commands updated; stale-path check passes |
| INV1 labels/tiers preserved | pass | `verify.py` contract check |
| INV2 gate counts | pass | `AGENTS.md`; `verify.py` workflow check |
| INV3 flows before code | pass | `AGENTS.md` §2; `ai-workflow.md`; review checklist |
| INV4 visual knowledge | pass | `full-flow.md` template; transfer skill |
| INV5 work/knowledge separation | pass | directory contract + templates |
| INV6 existing capabilities preserved | pass | all skills/commands retained; legacy notes |
| INV7 no config/dependency changes | pass | `opencode.json` unchanged; config check |
| INV8 verify.py 0 fail | pass | 13 pass · 0 warn · 0 fail |

## Deviations

| Planned | Actual | Reason | Approved? |
|---------|--------|--------|-----------|
| Update artifacts/commands/templates/parser/docs | Done; added a greenfield-exception line to `AGENTS.md` §2 | The existing greenfield commands keep intentional phase gates; without the note, the new mode table would appear to override them | Yes — consistent with preserved-capability requirement |
| Standard final summary without Gate 4 | Done | Approved D1 | Yes |

## Verification evidence

| Check | Command | Result |
|-------|---------|--------|
| Schema/references/contract | `python scripts/verify.py` | 13 pass · 0 warn · 0 fail |
| Install preview | `bash scripts/install.sh --dry-run` | 36 to update, 0 unexpected |
| Install | `bash scripts/install.sh` | 36 updated, 106 unchanged, 31 backed up |
| Second sync | `bash scripts/install.sh` | 9 updated, 133 unchanged, 9 backed up |
| Skill load | `opencode debug skill` | `design-implementation-flows` found |
| Runtime classification | `opencode run --agent plan ...` | Lightweight/Standard/Full selected correctly; no files modified |
| Baseline before change | `python scripts/verify.py` | 10 pass · 0 warn · 0 fail |
| Git state | `git status --short` | pending review; no unrelated files intended |

## What tests actually cover

No automated behavioral test suite exists for prompt-driven workflow behavior. `verify.py` asserts
the text contract: mode tokens, four gates, artifact paths, Mermaid templates, stale-path absence,
schema validity, and install parity. The three simulations document expected mode/artifact
selection but are not runtime assertions.

## What is assumed, not verified

- The model will pause at each gate in a live session.
- Mermaid renders in the developer's viewer.
- The first real Full-mode session will follow the flows correctly.
- OpenCode must be restarted before the new skills/commands are active.

## Remaining risks

| Risk | Impact | Mitigation / follow-up |
|------|--------|------------------------|
| Gate rubber-stamping under time pressure | approvals stop carrying signal | explicit gate phrases; Lightweight stays 0 gates; review after 10 Standard/Full changes |
| Diagram staleness | knowledge contradicts code | Gate 4 reconciliation; update `[P]`→`[V]` only with evidence |
| Specialized commands invoked outside `/ai-workflow` | mode gates may be skipped | header points to `AGENTS.md`; follow-up: add explicit gate lines or a hard route to `/ai-workflow` |
| Greenfield command paths diverge | inconsistent artifact locations | documented exception; follow-up: migrate when greenfield flow is next touched |
| Runtime compliance untested | workflow may not behave as specified | first real feature is the runtime trial |

## Questions for the author

- Should the nine specialized commands be hard-routed through `/ai-workflow` instead of carrying a
  pointer?
- Should `design-platform-core` migrate to `.ai/work/<slug>/` now or remain a greenfield exception?

## Gate 4 decision

- [x] Results reviewed
- [x] Verification evidence reviewed
- [x] Deviations recorded
- [x] Flows updated
- [x] Knowledge links present
- [x] Remaining risks accepted by human
- [x] `APPROVE GATE 4` — 2026-11-07

Knowledge links:

- `.ai/knowledge/features/engineering-ownership-workflow/README.md`
- `.ai/knowledge/features/engineering-ownership-workflow/full-flow.md`
- `.ai/knowledge/features/engineering-ownership-workflow/architecture.md`
- `.ai/knowledge/features/engineering-ownership-workflow/decisions.md`
