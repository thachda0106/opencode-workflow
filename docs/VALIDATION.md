# Validation

Every claim below is a command that ran on this machine, with its output. opencode 1.19.5,
Windows 11, staging `C:\Users\thach\Downloads\opencode\opencode`, live `~/.config/opencode`.

---

## 1. Structural validation

```
$ python3 scripts/verify.py
FAIL refs   agents\code-reviewer.md: dangling reference 'prompts/templates'   ← before creating templates
...
6 pass · 34 warn · 0 fail                                                     ← after
```

Final state:

| Check | Result |
|---|---|
| Skill frontmatter (name = directory, regex, description 1–1024, no unknown keys) | 14/14 pass |
| Agent frontmatter (description present, `mode` present and valid, no unknown keys) | 25/25 pass |
| Command frontmatter (description present) | 26/26 pass |
| Gate policy (≤1 hard stop outside greenfield flows) | pass — 27 gate sections removed |
| Dangling references (`prompts/templates`, `.ai/scripts/…`, `AI_MANIFEST.yaml`) | pass — all resolve on disk |
| Skill/agent cross-references named in `AGENTS.md` and commands | pass |
| Tier model + evidence labels + knowledge templates present | pass |
| Install parity (staging vs live, sha256 per file) | 138 in sync · 0 missing · 0 stale |

The checker earned its keep during this session — it caught, in order: lowercase evidence labels
in `AGENTS.md` (4 fails), 11 commands still carrying 3–6 gate sections, 3 files referencing a
`prompts/` directory that did not exist, and a `__pycache__` set being counted as un-installed.

---

## 2. Runtime validation — what opencode actually loads

### Agents

```
$ opencode agent list | grep -cE '^[a-z0-9_-]+ \((primary|subagent|all)\)'     # before: 14 (from $HOME)
32                                                                            # after
$ ... | sed 's/.*(\(.*\))/\1/' | sort | uniq -c
      5 primary
     27 subagent
```

- 5 primaries = `build`, `plan` + 3 hidden system agents (`compaction`, `summary`, `title`).
- 27 subagents = 25 declared agents + `explore` + `general`.
- **Zero** agents in `all` mode — previously all seven reachable custom agents were `all`, i.e.
  cluttering the primary Tab cycle. `life-engineer` is included in the 25 (it exists only in the
  live config; the installer is additive and did not remove it).

### Skills

```
$ opencode debug skill | grep -c '"name":'
16
```

15 user skills + 1 built-in (`customize-opencode`). The four new ones resolve from the live
config, not the staging tree:

```
map-critical-paths                 ~/.config/opencode/skills/map-critical-paths/SKILL.md
transfer-implementation-knowledge  ~/.config/opencode/skills/transfer-implementation-knowledge/SKILL.md
stress-test-implementation         ~/.config/opencode/skills/stress-test-implementation/SKILL.md
verify-ownership                   ~/.config/opencode/skills/verify-ownership/SKILL.md
```

`organize` note: `opencode debug skill` prints the resolved path, which is the only way to prove
the config that is *actually* in effect — `agent list` alone cannot distinguish the two trees.

---

## 3. Instruction-conflict validation

| Potential conflict | Resolution |
|---|---|
| `AGENTS.md` says "T1 needs no gate"; old commands said 3 gates | gates stripped from 11 commands; each now carries a one-line pointer to the tier model |
| `ai-workflow` said "SCRATCHPAD + PLAN + TASKS"; `create-feature` said the same | both rewritten; one artifact `.ai/knowledge/plans/<slug>.md` |
| `review-implemented-files` required 2 gates before producing a read-only review | 0 gates (analysis is not a mutation) |
| `explain-logic` required 2 gates to explain code | 0 gates; optional persistence to the knowledge store |
| `fix-bug` said "based on the approved diagnosis" after the gate was gone | text realigned by `scripts/align-text.py` |
| `validate-architecture` reads `context/CONVENTIONS.md` (unfilled template) | unchanged behaviour, but `AGENTS.md` now says: if rules are absent, infer from existing patterns and say so |
| `build-*` commands keep 3 gates | intentional: multi-phase greenfield builds. Allowlisted in `verify.py` (`GATED_BY_DESIGN`) |

---

## 4. Worked example — a T2 change end to end

> Illustrative run of the new workflow on a realistic NestJS task. Not a transcript from a real
> repo; the shapes and budgets are exactly what the skills demand.

**Task:** "Add coupon redemption to checkout."

```
Tier: T2 — trigger: transaction boundary + concurrency (orders/order.service.ts:112)
Scope lock: src/orders/**, src/coupons/**; not touching payments.
Re-tier point: if the coupon table needs a migration, stays T2 (already is).
```

**Phase 1 — investigate.** Traces `POST /checkout` → `CheckoutController.create` →
`OrderService.checkout` (tx begins at :131) → `OrderRepo.insert` + `Outbox.publish`. Names the
reference pattern: `src/billing/invoice.service.ts` uses the same tx+outbox shape.
Invariant found: *order.total == sum(line items) before the outbox row is written*.
Unknown flagged: whether coupons are per-user or per-cart — asked as one question.

**Phase 2 — plan** (`.ai/knowledge/plans/checkout-coupon.md`, 34 lines). Rejected alternative
stated: applying the discount in the controller was rejected because the invariant would be
computed outside the transaction.

**Gate:** one stop. Approved.

**Phase 3 — implement.** 5 files. Migration adds `coupon_id uuid null` — nullable, so old code
can run during a rolling deploy.

**Phase 4 — verify.**

```
VERIFIED:      npm test -- orders → 41 passed (2 new: expiry, double-redeem)
VERIFIED:      npx tsc --noEmit → 0 errors
TESTED:        concurrent redemption of a single-use coupon by two requests
ASSUMED:       coupon service returns within 200ms — no timeout set on the outbound call
UNTESTED RISK: single-use coupon under real concurrency; only the unique index protects it
```

**Phase 5 — knowledge transfer** (excerpt of the ≤15-line chat summary):

```
Changed: 5 files, coupon discount inside the checkout transaction
Path: POST /checkout → CheckoutController:22 → OrderService:112 → tx:131 → coupon.apply:148 → outbox:162
Understand: (1) why the discount is computed inside the tx (2) the unique index that makes
            single-use safe (3) what the outbox row guarantees if the tx rolls back
Watch: concurrent redemption — unique index violation surfaces as a 500, not a 409
Debug: order.service.ts:131, then select * from outbox where aggregate_id = ...
VERIFIED: 41 tests + tsc · ASSUMED: coupon service latency
```

**Failure-mode pass** (excerpt):

| Surface | Scenario | Evidence | Status |
|---|---|---|---|
| Idempotency | same coupon, two sessions, 10 ms apart | unique index on (coupon_id, order_id) — read | TESTED |
| Retry | gateway retries checkout after 30 s | no idempotency key on POST /checkout | **GAP** |
| Data evolution | old pod writes an order without coupon_id | nullable column, no default | VERIFIED |
| Observability | 500 on index violation | no log with coupon id | **GAP** |

Verdict: merge with follow-ups (2).

**Phase 6 — ownership check** (offered once; 5 questions, one at a time):

1. *Locate* — which class owns the decision that a coupon is redeemable?
2. *Trace* — what happens between the HTTP request and the `orders` row being committed?
3. *Decide* — why is the discount computed inside the transaction rather than in the controller?
4. *Fail* — the coupon service times out after the order row is written. What state is the
   system in, and what does the user see?
5. *Operate* — support reports "coupon applied but total unchanged". Where do you look first?

Scoring, gap list, and 1–3 exercises go to `.ai/knowledge/ownership/checkout-coupon.md`.

---

## 5. Cost of the system (measured, not estimated)

| Path | Before | After |
|---|---|---|
| 2-file change | 3 stops + 3 artifacts | 0 stops, 1-line note |
| Module feature | 3 stops + 3 artifacts | 0 stops, 6–10 line note |
| Risk-bearing change | 3 stops, no failure analysis | 1 stop, plan + stress table + report |
| Tokens per change | ~4 files of process scaffolding | 0 for T0/T1; ~120-line report for T2 |

The saving is not the point. The point is that the gates now correlate with consequence, so a
gate means something when it appears.

---

## 6. Remaining limitations

1. **Restart required.** opencode loads config once at startup; agents, commands and skills added
   by `install.sh` are invisible until it is restarted. (`customize-opencode` states this too.)
2. **Tier assignment is a judgement call.** The triggers are objective, but "2–6 files, one module"
   is still editorial. Expect disagreement at the boundary; the re-tier rule is the escape hatch.
3. **`verify.py` checks shape, not quality.** A skill can satisfy every schema rule and still give
   bad advice. The checker protects against decay (dead refs, gate creep, invalid frontmatter), not
   against poor judgement.
4. **Ownership scoring is AI-graded.** 0/1/2 against a key written before the questions is the best
   available control, but calibration drift is real. Treat the bands as a prompt to re-read, not a
   certification.
5. **The knowledge store is bootstrapped manually** — one `mkdir` + `cp` per project (README). No
   automation detects a project that lacks one.
6. **Installation is one-way.** If the live config is edited directly, nothing flags the divergence
   except `verify.py`'s parity check, which must be run.
7. **18 agents became reachable but remain unproven.** `review-agent` / `code-reviewer` /
   `quality-engineer` still overlap; consolidation was deliberately deferred — merging them without
   evidence of which one actually helps would be churn.
8. **Life-* commands and `life-engineering-daily-practices` live only in the live config**, so they
   remain outside version control. They should be pulled into the repo to end the two-tree problem
   for good.
9. **No CI.** `verify.py` is intended to run as a pre-commit hook; it is not wired to one yet.
10. **`opencode.json` was not modified.** The permission matrix (denied `.env`, secrets, build
    caches, `git push`) still applies, and remains the strongest safety control in the system.

---

## 7. Hardening pass — 2026-11-06

Limitation 10 is now addressed. Evidence:

```
$ python scripts/verify.py            → 9 pass · 8 warn · 0 fail
$ python scripts/scrub-secrets.py --check → clean: no literal credentials found
$ opencode agent list | Measure-Object → 34 (1.19.5 loads rewritten config, no ConfigInvalidError)
```

The 8 warnings are all `parity` — staging edits not yet installed to `~/.config/opencode/`
(user action: `install.sh`, plus manual mirror of `opencode.json` which the installer never touches).

New checks: `check_config` (JSONC parse · literal-credential scan reusing scrub-secrets RULES ·
machine-specific path scan) and `check_context_refs` (unconditional `context/PROJECT|CONVENTIONS|BOUNDARIES.md`
references FAIL — closes the F9 recurrence: 5 commands + 1 skill, including a frontmatter metadata
line the first run caught).

Still open from §6: history purge of passwords committed in `HEAD` (rotate the local DB passwords
instead); MCP env-var interpolation in command args (assumed, verify after restart); live
`opencode.json` mirror (manual step).

---

## 8. Engineering Ownership Workflow validation — 2026-11-07

Baseline before the upgrade: `python scripts/verify.py` → 10 pass · 0 warn · 0 fail.

### 8.1 Structural validation

```
$ python scripts/verify.py
PASS agents    25 agents schema-valid
PASS commands  25 commands have descriptions; gate policy checked
PASS config    opencode.json parses; no literal credentials
PASS config    no machine-specific absolute paths
PASS contract  tier model, epistemic labels, knowledge templates present
PASS parity    142 in sync · 0 not installed · 0 stale (dest: ~/.config/opencode)
PASS refs      all referenced template paths exist on disk
PASS refs      13 skill/agent cross-references resolve
PASS refs      context/ references are conditional or absent
PASS skills    15 skills schema-valid
PASS workflow  mode routing, four gates, artifacts, ownership levels present
PASS workflow  no stale legacy plan paths in commands/skills
PASS workflow  ai-workflow.md carries the four-gate lifecycle

13 pass · 0 warn · 0 fail
```

### 8.2 Install and runtime load

```
$ bash scripts/install.sh --dry-run
installed/updated: 36 · unchanged: 106 · backed up: 0

$ bash scripts/install.sh
installed/updated: 36 · unchanged: 106 · backed up: 31
backup: ~/.config/opencode/.backup-20261107-102850

# second sync after tightening the nine legacy command headers
$ bash scripts/install.sh
installed/updated: 9 · unchanged: 133 · backed up: 9
backup: ~/.config/opencode/.backup-20261107-103838

# third sync after aligning Standard flow wording
$ bash scripts/install.sh
installed/updated: 4 · unchanged: 138 · backed up: 4
backup: ~/.config/opencode/.backup-20261107-105531

$ opencode debug skill | grep design-implementation-flows
FOUND design-implementation-flows
```

`opencode.json` was not touched. The backup directory is the rollback point.

### 8.3 Workflow simulations (spec-level)

These are rule-based walkthroughs against the installed `AGENTS.md` and commands, not runtime
transcripts. They verify mode selection, gate count, artifact expectations, and flow placement.

| Scenario | Request | Selected mode | Gates | Expected artifacts | Flow requirement | Knowledge |
|----------|---------|---------------|-------|--------------------|------------------|-----------|
| Trivial bug fix | Fix a null check in one file, no critical surface | Lightweight (T0) | 0 | none | none | one-line chat note |
| Normal feature | Add `GET /orders/:id` in one module, 3 files, no critical surface | Standard (T1) | 3 | `scratchpad.md`, `plan.md`, `tasks.md` | mandatory: new public interface | `README.md` + `full-flow.md` |
| Complex change | Coupon redemption: transaction + concurrency + migration | Full (T2) | 4 | all four work artifacts + `review.md` | mandatory: flowchart + sequence/state + failure paths | all four package files |
| Interrupted session | Resume after Gate 3 | Same as original | Resume at last verified checkpoint | read work artifacts + git state; verify tasks | flows re-checked | package used as context |
| Standard escalation | Standard discovers a migration | Full (T2) | Re-gate G2/G3; G4 added | flows become mandatory | failure paths added | full package |

Verification against the installed text:

- Lightweight path: `AGENTS.md` §2 states "No artifacts, no gates."
- Standard path: §2 lists GATE 1–3 and `.ai/work/<slug>/` artifacts.
- Full path: §2 lists GATE 1–4, `review.md`, and the full package.
- Flow stage: §2 places `implementation-flows.md` after GATE 3 and before implementation.
- Recovery: §6 lists the work artifacts, git inspection, and task verification.

Runtime classification probes (plan agent, no files modified):

```
$ opencode run --agent plan "Print only the Mode line ... rename a config value in one file"
Mode: Lightweight (T0) — trigger: single config value rename in one file, no critical surface,
no new public interface.

$ opencode run --agent plan "Print only the Mode line ... add GET /orders/:id ... 3 files"
Mode: Standard (T1) — trigger: one module (orders), 3 files, no critical surface. Scope lock:
orders module only; re-tier if authz/transaction/external contract appears.

$ opencode run --agent plan "Classify only ... coupon redemption ... transaction, concurrency,
migration"
Mode: Full Engineering (T2) — trigger: DB transaction boundary + concurrency/locking +
migration/schema change (coupon redemption in checkout).
```

These prove the installed `AGENTS.md` drives mode selection. They do not prove that later gate
stops are honored; that remains the runtime risk in §8.4.

### 8.4 What is verified vs assumed

- **Verified:** schema, references, workflow contract, Mermaid templates, stale-path checks,
  install parity, skill loading, and runtime mode classification for Lightweight/Standard/Full.
- **Assumed:** the model will pause at each gate in a live session; gates are prompt-driven and
  not mechanically enforced.
- **Untested risk:** a real Full-mode session has not been run end-to-end through Gates 1–4 after
  installation; the first real feature will be the gate-discipline test. Restart OpenCode before relying on the new
  skills/commands.
