# Plan — workflow hardening pass (2026-11-06)

## Objective
Close the concrete gaps found in the upgraded workflow: credentials in git-tracked config,
dead machine-specific rules, over-broad read denies, PowerShell blind spots, dangling
`context/` references, and a checker that never inspects `opencode.json`.

## Invariants
- opencode 1.19.5 must still load every config file (no new-schema keys; see non-goals).
- `install.sh` stays additive and never touches `opencode.json`.
- No git mutations (commit/push/history rewrite) — user owns those.
- No secret values printed to chat or logs.

## Findings → files
| # | Finding (evidence) | Fix |
|---|---|---|
| 1 | DB passwords literal in `opencode.json:212,222`; also in `HEAD` (no remote) | `{env:...}` refs; extend `scripts/scrub-secrets.py` rules |
| 2 | 12 dead `C:/Users/ICD/...` rules (user is `thach`) | delete; `**/` patterns already cover |
| 3 | `read` denies ALL `**/*.yaml|yml` (opencode.json:23-24) — blocks CI/compose/k8s | remove blanket deny; keep secrets/tfstate denies |
| 4 | no denies for `*.pem`, `*.key`, `id_rsa*`, `.npmrc`, `.pgpass`, `.netrc` | add to `read` deny |
| 5 | bash denies are POSIX-only; `Remove-Item`, `del`, `git clean`, `git checkout --` open | add `ask` rules (broad first, narrow denies last) |
| 6 | `.gitignore:5` typo `.gitignore__pycache__/`; `.opencode/goals/` untracked | fix typo; ignore `.opencode/goals/` |
| 7 | 6 commands + `validate-architecture` read `context/*.md` unconditionally; never installed (F9 recurrence); `context/AGENTS.md` = old 3-gate contract | make refs conditional ("if present, else infer + say so"); retire `context/AGENTS.md` to `_retired/` |
| 8 | `verify.py` never parses `opencode.json`, never checks context refs | add `check_config()` (JSONC parse + secret scan + stale-path scan) and conditional-context-ref check |
| 9 | `git push` = config `deny` but AGENTS.md says "always ask"; MCP DB writes uncovered by approval list | AGENTS.md: push is hard-denied, human runs it; MCP DB writes need same approval as migrations |
| 10 | live `~/.config/opencode/opencode.json` has same secrets; installer never syncs it | gated step: mirror opencode.json edits to live config (outside workdir → explicit approval) |

## Ordered steps
1. `opencode.json`: env-ref DB creds, drop ICD paths + yaml blanket deny, add secret-file denies, add PowerShell `ask` rules.
2. `.gitignore` fixes. 3. Commands ×6 + skill: conditional context refs. 4. Retire `context/AGENTS.md`.
5. `scrub-secrets.py`: URI-userinfo + `--pass` rules. 6. `verify.py`: `check_config()` + context-ref check.
7. `AGENTS.md` §2 wording (push deny, MCP DB approval). 8. `README.md`: context/ purpose + required env var names.
9. Verify (below). 10. With approval: mirror opencode.json changes to live config. 11. Knowledge report + VALIDATION.md append.

## Failure modes
- `{env:VAR}` unset → postgres/mysql MCP fail at startup → README documents required vars; user restarts to confirm.
- Naive JSONC comment stripping breaks on `https://` → string-aware stripper, tested on the real file.
- YAML deny removal exposes secrets-in-yaml → mitigated by AGENTS.md §3.10 + `**/secrets/**` deny (behavioral, not enforced).
- More `ask` prompts during daily work — intended trade.

## Verification
`python3 scripts/verify.py` → 0 fail · `python3 scripts/scrub-secrets.py --check` → clean ·
`opencode agent list` in staging → loads (proves 1.19.5 accepts config) · MCP env interpolation = ASSUMED until user restarts.

## Non-goals (trade-offs)
- **New schema keys** (`permissions`, `mcp.servers`, `plugins`, `commands`): published config.json deprecates current keys, but installed 1.19.5 + built-in skill document the current shape. Rejected: migration now risks ConfigInvalidError. Revisit on opencode upgrade.
- **Git history purge** of committed passwords: destructive, no remote, local dev creds. Rejected: filter-repo without explicit request. Recommend rotating the local DB passwords.
- Agent consolidation, install.ps1, MCP server pruning: no new evidence / user preference.
