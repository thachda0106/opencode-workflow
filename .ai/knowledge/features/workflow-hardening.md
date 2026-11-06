# Feature — workflow hardening (config layer)

Revised: 2026-11-06

## 1. What changed

| File | Change | Why |
|------|--------|-----|
| `opencode.json` | DB passwords → `{env:...}` refs; 35 dead `C:/Users/ICD/` rules removed; `**/*.yaml|yml` read-deny removed; 9 secret-file denies added; bash: 9 PowerShell/git `ask` rules | secrets out of git; rules match this machine; unblock CI/yaml reads; close PS deletion gap |
| `scripts/verify.py` | new `check_config()` (JSONC parse + credential scan + machine-path scan) and `check_context_refs()` | the checker never inspected the file where most drift lived |
| `scripts/scrub-secrets.py` | +2 rules: URI userinfo passwords, literal `--pass` values (both skip existing `{env:}` refs) | coverage matched the actual leak class |
| `AGENTS.md` §2 | `git push` documented as config-denied; MCP DB writes added to approval list | text and config contradicted each other |
| 5 commands + `skills/validate-architecture/SKILL.md` | `context/*.md` reads now conditional ("if present, else infer and say so") | F9 recurrence: refs pointed at files nothing installs |
| `context/AGENTS.md` → `_retired/context-AGENTS-old.md` | retired | it was the superseded 3-gate contract, silently conflicting |
| `.gitignore` | typo `.gitignore__pycache__/` → `__pycache__/`; ignore `.opencode/goals/` | plugin state should never be committed |
| `README.md` | context/ purpose; required env var names; opencode.json manual-mirror note | install.sh refuses to sync the file that matters most |

## 2. Why it changed this way

The ownership upgrade deliberately left `opencode.json` untouched ("strongest safety control"),
so every drift class accumulated there while `verify.py` only audited markdown. Chosen: extend
the existing checker and scrubber rather than add new tooling. Rejected alternatives: migrating
to the new published schema keys (installed opencode 1.19.5 documents the current shape —
migration risks ConfigInvalidError); git history purge of committed passwords (destructive, no
remote, local dev creds — rotate the DB passwords instead).

## 3. How it works

1. Tool-call arrives → opencode.json `permission` rules evaluated, **last matching rule wins**
   (opencode.json bash block: `rm *` ask sits before `rm -rf *` deny, so recursive deletes hard-fail).
2. Secret material never enters the repo: `scripts/scrub-secrets.py` rewrites literals → `{env:VAR}`.
3. `python scripts/verify.py` → `check_config()` parses opencode.json as JSONC (string-aware
   comment stripper), imports `RULES` from scrub-secrets.py via importlib, FAILs on literals or
   drive-letter user paths.
4. `check_context_refs()` FAILs any command/skill line referencing `context/PROJECT|CONVENTIONS|BOUNDARIES.md`
   without a conditional marker on the same line.
5. MCP DB writes require human approval per AGENTS.md §2 (behavioral, not enforced by config).
6. `check_parity()` WARNs until `install.sh` syncs staging → live (opencode.json excluded by design).

## 4. Components that interact

| Component | Direction | Contract | Breaks if |
|-----------|-----------|----------|-----------|
| verify.py → scrub-secrets.py | imports `RULES` | list of `(compiled_re, replacement)` tuples | tuple shape changes → check_config crashes loudly |
| staging repo → live config | install.sh (manual run) | all files except opencode.json | opencode.json edits silently stay local — parity check can't see it |
| commands/skills → `context/*.md` | runtime reads | optional templates, inference fallback | projects without templates rely on inference quality |
| MCP servers → env vars | `{env:VAR}` interpolation | vars set in the shell that launches opencode | unset var → server fails or connects with literal string |

## 5. Technical decisions worth knowing

- **Env-ref the password only** (`postgresql://postgres:{env:POSTGRES_PASSWORD}@localhost:...`)
  · rejected whole-URI env var · cost: two vars to set instead of one; host/db stay visible in git.
- **`git push` kept as deny, wording fixed** · rejected switching to `ask` · cost: agent can never
  push even with approval — intended; the human pushes.
- **PowerShell deletion = `ask`, not `deny`** · rejected deny · cost: more prompts; watch for
  rubber-stamp fatigue (the F3 failure mode).
- **YAML blanket read-deny removed** · rejected narrowing to `*secret*.yaml` · cost: secrets in
  arbitrary yaml are now covered only by the AGENTS.md §3.10 behavior rule, not enforced.
- **`context/` refs made conditional** · rejected installing context/ globally · it is per-project
  by nature; installing templates into `~/.config` would load nothing.

## 6. Assumptions this relies on

1. `{env:VAR}` interpolates in MCP `environment` values and `command` args — `assumed` (documented
   for headers/environment; command args unverified until restart).
2. `go-mcp-mysql.exe` resolves via PATH on this machine — `assumed`.
3. Live `~/.config/opencode/opencode.json` contains the same literal DB passwords — `assumed`
   (read of that dir was rejected; parity check covers only installed files).
4. `POSTGRES_PASSWORD` / `MYSQL_PASSWORD` will be set in the launching shell — `assumed`.

## 7. What can go wrong in production

- Env var unset → postgres-mcp/go-mcp-mysql fail at startup or connect with a literal `{env:...}`
  string → MCP tools error at call time → check `$env:POSTGRES_PASSWORD` in the launching shell.
- Ask-fatigue: `Remove-Item *: ask` on every delete → approvals become reflexive → the gate
  carries no signal (same failure mode as F3's 45 gates).
- scrub-secrets URI rule skips passwords containing `{` by design → a literal with a brace survives
  → caught only by manual review.
- verify.py importlib load breaks if scrub-secrets.py is renamed → check_config raises → verify
  fails loudly (acceptable, but confusing message).
- Live config keeps old literals because install.sh never syncs opencode.json → staging looks
  clean while every real session still exposes them → mirror by hand (README now says so).

## 8. Where debugging begins

| Symptom | Start at | Then |
|---------|----------|------|
| command unexpectedly blocked / allowed | opencode.json `bash` block — check rule ORDER (last match wins) | reproduce with the exact command string |
| MCP DB tools fail after this change | `$env:POSTGRES_PASSWORD` / `$env:MYSQL_PASSWORD` in launching shell | opencode startup logs for that server |
| verify.py FAILs on `config` | scripts/verify.py `check_config` | run `scripts/scrub-secrets.py --check` |
| old 3-gate behavior resurfaces | `_retired/context-AGENTS-old.md` should not be referenced | grep for `context/AGENTS.md` |

## 9. What you should understand more deeply

- **Last-match-wins permission ordering**: one misordered line turns a deny into an allow ·
  question: "why does `rm -rf *` still deny when `rm *` asks?" · read: opencode.json bash block.
- **verify.py ↔ scrub-secrets.py RULES coupling**: one pattern list, two consumers (rewrite +
  detect) · question: "what exactly breaks if a rule tuple gains a third element?" ·
  read: scripts/verify.py `check_config`, scripts/scrub-secrets.py `RULES`.
- **The opencode.json mirror gap**: install.sh syncs everything except the most sensitive file ·
  question: "which file do parity warnings NOT cover, and how do its changes reach live?" ·
  read: scripts/install.sh (copy list), README env-var note.
