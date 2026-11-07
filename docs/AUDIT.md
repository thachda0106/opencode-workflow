# Audit — existing opencode skill system

Date: 2026-11-06 · Scope: `C:\Users\thach\Downloads\opencode\opencode` (staging) and
`~/.config/opencode` (live) · opencode 1.19.5 · 136 files in the staging tree at baseline.

Everything below was verified by command, not by reading alone. Evidence is cited per finding.

---

## 1. What the system actually is

| Layer | Count | Loaded by opencode? |
|-------|-------|---------------------|
| `AGENTS.md` (global rules) | 1 | live copy only — staging copy was named `AGENTS - Copy.md` |
| Skills (`skills/*/SKILL.md`) | 14 | yes, via `skills.paths: ["./skills"]` when cwd = staging |
| Agents (`agents/*.md`) | 25 | **no** — see F1 |
| Commands (`commands/*.md`) | 26 | **partly** — 6 existed only in staging, never installed |
| Context templates (`context/*.md`) | 7 | **no** — nothing loads them |
| Prompt templates (`prompts/templates/*.md`) | 0 | referenced 10× by commands/agents |

```
$ opencode agent list          # from staging dir, before the upgrade
16 agents: build, plan, compaction, summary, title (primary) + explore, general (subagent)
           + bug-hunter, code-reviewer, doc-keeper, feature-builder, life-engineer,
             performance-optimizer, test-engineer (mode: all) + goal, goal-verify (plugin)
```

18 of the 25 agents in the staging tree never appeared. That number is the audit's headline.

---

## 2. Findings

### F1 — 18 agents and 6 commands were inert (critical)

opencode loads agents from `.opencode/agent(s)/` (project) or `~/.config/opencode/agent(s)/`
(global). A bare `agents/` folder at an arbitrary path is not read, and there is no config key
that adds agent directories. Evidence: `opencode agent list` returned the same 14 agents from
`$HOME` and from the staging directory (the staging run added only the plugin's `goal` agents).
Missing from the live set: `backend-architect`, `frontend-architect`, `devops-architect`,
`platform-architect`, `security-engineer`, `quality-engineer`, `refactoring-expert`,
`root-cause-analyst`, `requirements-analyst`, `review-agent`, `socratic-mentor`,
`learning-guide`, `repo-index`, `pm-agent`, `business-panel-experts`, `python-expert`,
`deep-research`, `deep-research-agent`.

Impact: the newest and most specialised third of the system had never run. Any judgement about
"the AI doesn't use my architect agent" was unfalsifiable until now.

### F2 — Global rules were an unfilled template (critical)

`~/.config/opencode/AGENTS.md` (9,718 B) is byte-identical to the staging `AGENTS - Copy.md`.
It contains `{{project.name}}`, `{{conventions.file_naming}}`-style placeholders and a
"System Prompt Fragment" header — i.e. the file that loads into **every** session carries no
project facts at all, plus three mandatory approval gates.

### F3 — 45 approval gates across 15 commands (critical, and self-defeating)

```
$ grep -r "Reply APPROVE" --include=*.md . | wc -l
45
```

Every ordinary command (`fix-bug`, `add-tests`, `refactor-feature`, `optimize-performance`,
`update-docs`, `explain-logic`, …) declared SCRATCHPAD → PLAN → TASKS with three hard stops.
Consequences observed in the instruction text itself: `// turbo` markers left over from another
tool, and phrases like "based on approved scratchpad" surviving in files whose gates had already
been bypassed. A gate that is always rubber-stamped carries no signal — and the cost is three
round-trips before a two-file change.

### F4 — No knowledge-transfer artifact existed (critical for the goal)

`review-implemented-files` graded code quality. `deep-dive` produced a document for *source
files*, behind two gates, with a 10-section structure aimed at readers who have never seen the
code. Neither answered: *what must I understand about the change that just landed, and where do
I start when it breaks at 02:00?* Nothing in the system produced it automatically, so the
knowledge stayed in the chat transcript.

### F5 — No risk differentiation (high)

All work was treated identically: a copy change and a payment transaction both required three
approval artifacts. The only risk language in the system was "if > 3 files, verify scope is
appropriate" — a file count, not a consequence count.

### F6 — Verification stopped at green tests (high)

`verify-bug-regression` ran tests, typecheck, lint, build. Nothing asked what happens on partial
failure, duplicate delivery, concurrent writers, a rolling deploy against a new column, or a
missing timeout. The only epistemic language was `code-reviewer`'s four self-check questions —
good, but buried in an agent that (see F1) was one of the seven that did load.

### F7 — 10 dangling references (high)

```
$ grep -rn "prompts/templates" --include=*.md .
agents/code-reviewer.md · agents/review-agent.md (×2) · commands/ai-workflow.md (×4)
commands/review-implemented-files.md (×2) · commands/review-pr.md
```

`prompts/` did not exist. Commands instructed the model to "use `prompts/templates/plan.md`",
which is an instruction to invent a format every time. `AGENTS.md` additionally referenced
`.ai/scripts/validate-template.sh` and `AI_MANIFEST.yaml` — neither exists.

### F8 — Agent frontmatter was invalid in two keys, and every agent was mode `all` (medium)

All 25 agents declared `skills:` and `boundaries:`. Neither is in opencode's agent schema; the
built-in `customize-opencode` skill states unknown fields are "silently routed into `options`" —
i.e. shipped to the provider as model parameters. No agent declared `mode`, which defaults to
`all`, so every specialist appeared in the primary Tab cycle and in the Task tool description.

### F9 — Context files were orphaned (medium)

`context/PROJECT.md` (20 placeholders) and `context/CONVENTIONS.md` (8 placeholders) are
templates. Six commands say "read `context/PROJECT.md`". Nothing copies them into a project, and
nothing loads them globally. So the instruction produced either a not-found error or an empty
template — and `validate-architecture` depends on `CONVENTIONS.md` to have anything to check.

### F10 — Duplication and drift (medium)

| Overlap | Files |
|---------|-------|
| Code review | `agents/code-reviewer`, `agents/review-agent`, `agents/quality-engineer`, `commands/review-pr`, `commands/review-implemented-files` |
| Research | `agents/deep-research`, `agents/deep-research-agent` |
| Architecture | `agents/platform-architect` vs `backend/frontend/devops-architect` |
| Bug flow | `agents/bug-hunter` + `root-cause-analyst` + 3 skills that restate each other's scope |

Two trees had also diverged: staging had 25 agents / 6 unique commands; live had 7 agents /
12 life-* commands and a life-engineering skill that staging lacked. No installer, no git, no
comparison — so "which config am I actually running?" had no answer (F1 made that worse).

---

## 3. What was worth keeping (and was kept)

| Asset | Why it survived |
|-------|-----------------|
| 7 core skills (`analyze-project-structure`, `trace-execution-flow`, `locate-code-patterns`, `validate-architecture`, `diagnose-bug-root-cause`, `apply-targeted-fix`, `verify-bug-regression`) | Correct scope discipline: each has `Non-Goals` that prevent it from doing the next skill's job. Rare and valuable. |
| `review-implemented-files` 7-dimension checklist | The dimensions (correctness, bugs, security, architecture, performance, errors, tests) are the right ones. Only the gate scaffolding was wrong. |
| `deep-dive` document structure | Declarative-before-algorithmic, no forward references, concrete numbers. Reused inside the knowledge report. |
| `context/ADR_CANDIDATES.md` ADR format | Context → Decision → Consequences → Alternatives. Reused verbatim as the ADR template. |
| `repo-index` agent concept | `PROJECT_INDEX.md` + 7-day staleness rule is exactly the right context-economy idea. Kept, now reachable. |
| `build-minimum-system` / `build-large-system` | Multi-phase greenfield builds *should* be gated. Left alone. |
| `opencode.json` permission matrix | Read/edit denials for `.env`, secrets, `node_modules`, `venv`, `.m2`, terraform state, plus `git push` denial. Unchanged. |

The system was not badly designed. It was **undeployed, over-gated at the wrong altitude, and
silent about what was learned.**

---

## 4. Gap analysis against the mission

| Capability | Existing support | Gap | Where it now lives |
|---|---|---|---|
| Codebase understanding | `analyze-project-structure`, `trace-execution-flow` (good, shallow) | nothing produced a durable per-feature explanation | `transfer-implementation-knowledge` |
| Architecture reasoning | 4 architect agents (inert), `review-architecture` | no decision artifact, no rejected-alternative requirement | `AGENTS.md` §2/§5 + `templates/knowledge/adr-template.md` |
| Implementation review | strong 7-dimension checklist | buried in 2 gates; no evidence labels | `review-implemented-files` rewritten |
| Knowledge transfer | none | entire capability missing | `transfer-implementation-knowledge` (9 sections, ≤120 lines) |
| Critical path analysis | none | no risk ranking anywhere | `map-critical-paths` (9 dimensions, promotion rule) |
| Production debugging | `fix-bug` (diagnosis), no failure model | nothing asked about partial failure, retries, concurrency | `stress-test-implementation` (10 surfaces, 4 evidence labels) |
| Knowledge retention | `context/*.md` (orphaned, unfilled) | no per-project store, no index, no gotcha ledger | `.ai/knowledge/` contract + 6 templates |
| Independent verification | `socratic-mentor` (generic Clean Code/GoF) | never grounded in the actual implementation | `verify-ownership` (5 question levels, hidden key, scored bands) |

---

## 5. Severity summary

| Severity | Findings | Effect |
|----------|----------|--------|
| Critical | F1, F2, F3, F4 | a third of the system never loaded; global rules were empty; every task cost 3 stops; understanding was never captured |
| High | F5, F6, F7 | no risk differentiation, green-tests-as-proof, 10 instructions pointing at nothing |
| Medium | F8, F9, F10 | invalid agent schema, orphaned context, duplicated responsibilities, two drifted trees |

Full remediation and validation: `docs/ARCHITECTURE.md`, `docs/VALIDATION.md`.

---

## 6. Engineering Ownership Workflow audit — 2026-11-07

Audited: `AGENTS.md`, 14 skills, 25 commands, 25 agents, prompt/knowledge templates, `docs/`,
`.ai/knowledge/`, `scripts/`, `opencode.json`. Baseline: `python scripts/verify.py` → 10 pass,
0 warn, 0 fail; OpenCode 1.19.5; repo and global `AGENTS.md` identical.

### Findings

| # | Finding | Evidence | Impact |
|---|---------|----------|--------|
| G1 | No explicit Lightweight/Standard/Full mode routing | `AGENTS.md` §1–2; T0/T1/T2 were risk tiers only | Artifact and gate set could not be selected consistently |
| G2 | Only one gate, after the T2 plan | `AGENTS.md` §2; `/ai-workflow` Phase 2 | No Gate 1 (findings), Gate 3 (execution), or Gate 4 (final review) |
| G3 | Investigation and plan collapsed into one file | `prompts/templates/scratchpad.md`; `/ai-workflow` wrote the plan directly | Observations and conclusions were not separately reviewable |
| G4 | No `tasks.md` artifact | `/ai-workflow` Phase 2: "the plan's step list is the task list" | No task IDs, dependencies, acceptance criteria, or context recovery |
| G5 | No implementation-flow stage | No Mermaid or pre-code flow artifact in skills/templates | Code could start without a visual model of intended behavior |
| G6 | No Mermaid requirements | No `mermaid` block in any skill/template | Knowledge reports were text-only |
| G7 | Single-file feature report | `transfer-implementation-knowledge` wrote `features/<slug>.md` | No README/full-flow/architecture/decisions package |
| G8 | No progressive Level 1/2/3 model | Transfer skill had "understand more deeply" only | Ownership depth was not prioritized by risk |
| G9 | No context-recovery procedure | No persisted task status or checkpoint verification | Interrupted sessions relied on chat memory |
| G10 | Review depth not tied to diagrams | `map-critical-paths` ranked paths; review did not require flows | Tier A paths could pass without sequence/state diagrams |
| G11 | `verify.py` capped hard stops at 1 | `scripts/verify.py` `check_commands` | New mode-specific gates needed a contract change |
| G12 | 10+ commands referenced the legacy plan path | grep across `commands/` | Artifact paths would diverge |
| G13 | `context/BOUNDARIES.md` retained the retired 3-gate model | grep for `SCRATCHPAD.md`/`PLAN.md`/`TASKS.md` | Orphaned but conflicting if copied into a project |

### Remediation

Implemented in the same change:

- `AGENTS.md`: modes, four gates, `.ai/work/<slug>/`, implementation flows, Level 1–3 ownership,
  context recovery, updated knowledge package contract.
- `design-implementation-flows` skill: pre-code Mermaid design with `[V]`/`[P]`/`[?]` labels.
- `transfer-implementation-knowledge`: package output (`README`, `full-flow`, `architecture`,
  `decisions`).
- `map-critical-paths`, `stress-test-implementation`, `verify-ownership`: flow priority, flow
  reconciliation, and Level 1–3 mapping.
- Commands rewritten for the new lifecycle; legacy plan paths updated.
- Templates: scratchpad, plan, tasks, implementation flows, review, and knowledge package.
- `verify.py`: workflow contract, Mermaid, stale-path, and gate checks.

Preserved: T0/T1/T2 triggers, evidence labels, existing skills and commands, existing knowledge
files, permission matrix, install/verify scripts.
