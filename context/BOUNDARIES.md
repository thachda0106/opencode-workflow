# Boundaries and Safety Invariants

> **Instructions**: Define what the AI assistant is NOT allowed to do.
> These are hard constraints. The mode table and gate rules live in `AGENTS.md`.

## Scope Rules

- Do NOT modify code outside the scope approved at Gate 1/Gate 3.
- Do NOT refactor unrelated code while fixing bugs.
- Do NOT optimize unless explicitly requested.
- If scope grows, stop, state the delta, and re-gate. Do not silently expand.
- Re-read a file before re-writing it.

## Forbidden Actions

### Destructive Operations
- Never execute `rm -rf` or equivalent destructive commands.
- Never run `git push`, `git reset --hard`, or `git clean` without explicit approval.
- Never modify build output directories (`dist/`, `build/`, `out/`).
- Never modify `node_modules/` or dependency lock files directly.

### Sensitive Data
- Never read `.env` files or environment variable files.
- Never read secrets, credentials, or API keys.
- Never read Terraform state or infrastructure secrets.
- Never expose sensitive data in code, logs, or documentation.

### Code Integrity
- Never mix different editing strategies on the same file.
- Never wipe entire files — edit the targeted section.
- If a file changes externally, re-read before writing.
- When multiple files are related, read all first, then write one by one.

### Approval Gates
- **Never bypass a human approval gate.** This is a critical safety violation.
- Approval must be explicit; silence is not approval.
- Approval of one gate never implies approval of the next.
- Never write source code before the required implementation flows exist.
- Never treat workflow approval as unlimited execution permission.
- Never mark a gate passed because the change looks straightforward.

## MCP / External Tool Usage Rules

### Documentation Tools (e.g., Context7)
- Use for external library documentation only.
- Do NOT use as a substitute for reading project code.
- Do NOT rely on assumed knowledge — fetch latest docs when uncertain.

### Code Analysis Tools (e.g., Serena, language servers)
- Use for symbol-level and semantic code analysis.
- Do NOT use for broad text searches — use grep/search instead.
- Do NOT use for file listing — use directory tools instead.

### Repository Tools (e.g., Bitbucket, GitHub)
- Use for PR management, code review, issue tracking.
- Authentication must be configured separately per developer.
- Never commit secrets through repository tools.

## Human Review Gates

The authoritative gate table is in `AGENTS.md` §2.

| Gate | Artifact | Mode | AI Must Say |
|------|----------|------|-------------|
| 1 | `.ai/work/<slug>/scratchpad.md` | Standard, Full | "Findings and scope ready. Reply `APPROVE GATE 1` to proceed." |
| 2 | `.ai/work/<slug>/plan.md` | Standard, Full | "Plan ready. Reply `APPROVE GATE 2` to freeze the baseline." |
| 3 | `.ai/work/<slug>/tasks.md` | Standard, Full | "Tasks ready. Reply `APPROVE GATE 3` to authorize flow design." |
| 4 | `.ai/work/<slug>/review.md` | Full | "Final review ready. Reply `APPROVE GATE 4` to complete." |

Additional review triggers:

- Architecture decisions: require explicit approval.
- Breaking changes: require explicit approval.
- New dependencies: verify existing alternatives first.
- Approved invariant change: stop and re-gate.
- If a decision changes during execution: update the plan delta and re-gate.
