# Architecture — AI accelerates implementation, AI facilitates understanding, human owns

## 1. Design principles

1. **One always-loaded rule file decides the process.** Tiers, gates, evidence labels and the
   knowledge contract live in `AGENTS.md`. Commands and skills reference it instead of restating
   it — that is what caused 45 divergent gates.
2. **Effort tracks consequence, not file count.** Nine risk dimensions, with a promotion rule so
   that a single dangerous property (transaction boundary, concurrency, object-level authz,
   mutable state) cannot be averaged away by cheap ones.
3. **Understanding is a build step, not a bonus.** T2 work is not "done" until a knowledge report
   exists. T1 gets a 6-line note. T0 gets a sentence. There is no tier where the engineer is
   expected to absorb nothing.
4. **Nothing is claimed that was not observed.** Four labels — VERIFIED, TESTED, ASSUMED, GAP —
   and the rule that green tests never upgrade a label.
5. **Few, single-responsibility skills.** Four new skills, each with explicit Non-Goals that name
   the skill that owns the adjacent job. No skill enumerates what another skill does.
6. **Knowledge lives next to the code.** `.ai/knowledge/`, git-tracked, index-first, update-in-place.

---

## 2. Layers

```
┌──────────────────────────────────────────────────────────────────────┐
│ LAYER 0 — AGENTS.md  (loaded every session)                          │
│   tier table · gates · Do-Not list · evidence labels · knowledge map │
└───────────────┬──────────────────────────────────────────────────────┘
                │ referenced by
┌───────────────▼──────────────────────────────────────────────────────┐
│ LAYER 1 — COMMANDS (entry points, thin: sequence + output shape)      │
│   /ai-workflow  /create-feature  /fix-bug  /review-implemented-files  │
│   /explain-logic  /knowledge-report  /ownership-check                 │
└───────────────┬──────────────────────────────────────────────────────┘
                │ loads
┌───────────────▼──────────────────────────────────────────────────────┐
│ LAYER 2 — SKILLS (procedures, loaded on demand)                      │
│                                                                      │
│  INVESTIGATE                    TRANSFER                  VERIFY      │
│  analyze-project-structure      map-critical-paths        stress-test- │
│  trace-execution-flow           transfer-implementation-  implementation│
│  locate-code-patterns             knowledge               verify-      │
│  validate-architecture                                    ownership    │
│                                                                      │
│  FIX: diagnose-bug-root-cause → apply-targeted-fix → verify-regression│
└───────────────┬──────────────────────────────────────────────────────┘
                │ writes
┌───────────────▼──────────────────────────────────────────────────────┐
│ LAYER 3 — .ai/knowledge/  (per project, git-tracked)                 │
│   index.md · critical-paths.md · features/<slug>.md                  │
│   plans/<slug>.md · gotchas.md · adr/NNN-*.md · ownership/<slug>.md    │
└──────────────────────────────────────────────────────────────────────┘

Agents are orthogonal: they are *who* executes (feature-builder, code-reviewer,
repo-index, bug-hunter, …), now all `mode: subagent`. Skills are *how*.
```

---

## 3. The tier model (the whole behavioural change in one table)

| | T0 | T1 | T2 |
|---|---|---|---|
| **Trigger** | ≤2 files, no critical surface | one module, 2–6 files | authz · money · tx boundary · migration · concurrency · idempotency · external contract · cache invalidation · state machine · deletion · cross-service · trust-boundary validation · crypto · >6 files / >1 module |
| **Plan** | none | ≤6 lines inline | artifact ≤40 lines |
| **Human stops** | 0 | 0 | 1 (after plan) |
| **Verify** | typecheck + build | + targeted tests | + full suite + failure-mode pass |
| **Knowledge** | 1 line | 6–10 line note | 9-section report + risk ranking |
| **Ownership check** | no | on request | offered once |

Objective test: *if you cannot name a concrete trigger from the T2 column, it is T1.*

---

## 4. Workflow integration — the 7 target phases, mapped

| Mission phase | Where it lives now | What changed |
|---|---|---|
| 1. Requirement understanding | `/ai-workflow` Phase 0–1 · `/create-feature` Phase 1 | scope lock + re-tier point stated up front; ambiguity answered with one question, not five |
| 2. Codebase investigation | `analyze-project-structure` → `trace-execution-flow` → `locate-code-patterns` | must name the reference implementation being copied; unknowns become plan risks |
| 3. Architecture and planning | `/ai-workflow` Phase 2 (+ `templates/knowledge/plan.md`) | one artifact instead of three; rejected alternative mandatory |
| 4. Implementation | `/ai-workflow` Phase 3 · `/create-feature` Phase 3 | stop conditions defined (contradiction, destructive step, new dependency, scope breach) |
| 5. Verification | `/ai-workflow` Phase 4 + `stress-test-implementation` + `/review-implemented-files` | failure-mode surfaces and evidence labels replace "tests pass" |
| 6. Knowledge transfer | `map-critical-paths` + `transfer-implementation-knowledge` | new; produces the Engineering Knowledge Report |
| 7. Ownership check | `verify-ownership` + `/ownership-check` | new; scored, gap-listed, with 1–3 exercises |

Nothing was removed from phases 1–5. What was removed is the requirement to produce three
separate approval artifacts before touching code.

---

## 5. Before / after

| Dimension | Before | After |
|---|---|---|
| Agents reachable | 7 of 32 declared | 27 subagents + 5 primaries, all declared ones reachable |
| Global rules | 9.7 KB unfilled template | 8 KB operating contract with objective triggers |
| Gates for a 2-file change | 3 hard stops + 3 artifacts | 0 |
| Gates for a payment change | 3 (same as above) | 1, after a plan with invariants + failure modes |
| Dangling instructions | 10 | 0 (templates created; checker enforces) |
| Post-implementation artifact | none | knowledge report + risk ranking (T2), note (T1) |
| Correctness claim | "tests pass" | VERIFIED / TESTED / ASSUMED / GAP, quoted commands |
| Failure analysis | none | 10 surfaces, evidence-labelled, time-boxed probes |
| Understanding check | generic Socratic mentor | 5-level questions from the real diff, hidden key, scored bands |
| Knowledge store | none | `.ai/knowledge/` with index, gotcha ledger, ADR format |
| Source of truth | two diverged trees, no git | one git repo + `install.sh` + `verify.py` parity check |
| Answer to "what am I running?" | unknown | `opencode debug skill` / `agent list` / `verify.py` |

---

## 6. Files

### New (12)
| File | Purpose |
|---|---|
| `AGENTS.md` | operating contract (tiering, gates, labels, knowledge map) |
| `skills/map-critical-paths/SKILL.md` | 9-dimension risk ranking + promotion rule |
| `skills/transfer-implementation-knowledge/SKILL.md` | 9-section report, ≤120 lines, ≤3 "understand deeply" |
| `skills/stress-test-implementation/SKILL.md` | 10 failure surfaces, 4 evidence labels, probe recipes |
| `skills/verify-ownership/SKILL.md` | 5-level questions, hidden key, 0/1/2 scoring, exercise types |
| `commands/knowledge-report.md` | `/knowledge-report` entry point |
| `commands/ownership-check.md` | `/ownership-check` entry point |
| `templates/knowledge/{README,index,feature,critical-paths,gotchas,adr-template}.md` | the `.ai/knowledge/` contract |
| `scripts/install.sh` | additive install with backup |
| `scripts/verify.py` | schema, references, gate policy, install parity |
| `scripts/normalize.py` | frontmatter migration (idempotent) |
| `scripts/migrate-gates.py` · `scripts/align-text.py` | one-off migrations, kept for provenance |

### Rewritten (4)
`commands/ai-workflow.md` · `commands/create-feature.md` ·
`commands/review-implemented-files.md` · `commands/explain-logic.md`

### Mechanically migrated (11 commands, 25 agents, 7 skills)
Gate chains removed from: `add-api-integration`, `add-tests`, `daily-system-boot`, `deep-dive`,
`fix-bug`, `get-docs`, `optimize-performance`, `refactor-feature`, `review-architecture`,
`review-pr`, `update-docs`. Agents: `skills:`/`boundaries:` moved into the body, `mode: subagent`
added. Skills: `category`/`inputs`/`outputs` → `metadata`.

### Created to close F7 (7)
`prompts/templates/{scratchpad,plan,tasks,reflection,review-output,review-plan,review-implementation}.md`

### Retired (5)
`_retired/AGENTS-old-template.md`, `_retired/commands/{ai-workflow,create-feature,explain-logic,review-implemented-files}.md`
— kept on disk for diffing, excluded from validation and install.

---

## 7. Why four skills and not twelve

Each new skill owns one question and refuses the adjacent ones in writing:

| Skill | Answers | Explicitly refuses |
|---|---|---|
| `map-critical-paths` | *where should attention go?* | fixing, benchmarking, explaining, reviewing |
| `transfer-implementation-knowledge` | *what must I understand about this change?* | grading code, restating the plan, teaching frameworks |
| `stress-test-implementation` | *what happens when the world misbehaves?* | rewriting, certifying correctness, security audit |
| `verify-ownership` | *can I maintain this without AI?* | capability judgements, interview prep, whole-repo scope |

The alternative — one "engineering excellence" skill — is how the original system ended up with
`deep-research` and `deep-research-agent`, and with three code reviewers.
