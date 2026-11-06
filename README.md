# opencode config — staging + install

This directory is the **source of truth** for my global OpenCode configuration. It mirrors the
layout OpenCode reads from `~/.config/opencode/`, and `scripts/install.sh` promotes it there.

## Why this repo exists

OpenCode loads exactly four things from a config directory:

| What | Path | Loaded how |
|------|------|-----------|
| Rules | `AGENTS.md` | always, into every session |
| Agents | `agents/*.md` | subagent/primary definitions |
| Commands | `commands/*.md` | `/command` entry points |
| Skills | `skills/*/SKILL.md` | on demand, via the `skill` tool |

Nothing else. A folder named `agents/` somewhere that is not a config directory is inert —
that is why 18 agents here had never run.

## Install

```bash
./scripts/install.sh --dry-run     # show what would change
./scripts/install.sh               # additive install with timestamped backup
./scripts/install.sh --no-agents   # skip agents/ (rules + skills + commands only)
```

The installer is **additive**: it never deletes anything in `~/.config/opencode/`, backs up every
file it overwrites to `~/.config/opencode/.backup-<timestamp>/`, and refuses to touch
`opencode.json`.

`opencode.json` is never installed — mirror any change here into `~/.config/opencode/opencode.json`
by hand. MCP servers expect these environment variables (set values in your shell, never in this
repo): `POSTGRES_PASSWORD`, `MYSQL_PASSWORD`, `GITHUB_TOKEN`, `PENPOT_TOKEN`. `go-mcp-mysql.exe`
resolves from `PATH` (Go bin directory).

## Verify

```bash
python3 scripts/verify.py          # schema, references, gate audit, install parity
opencode agent list                # what actually loaded
```

## Layout

```
AGENTS.md                  operating contract (tiering, gates, epistemic labels, knowledge store)
skills/                    single-responsibility procedures, loaded on demand
  map-critical-paths/          rank code paths by ownership risk
  transfer-implementation-knowledge/  engineering knowledge report
  verify-ownership/            knowledge check with hidden answer key
  stress-test-implementation/  production failure-mode pass
  analyze-project-structure/ trace-execution-flow/ locate-code-patterns/
  validate-architecture/ diagnose-bug-root-cause/ apply-targeted-fix/ verify-bug-regression/
commands/                  entry points; /knowledge-report and /ownership-check are the new ones
agents/                     specialist subagents
templates/knowledge/       the .ai/knowledge/ contract to copy into a project
context/                   optional per-project templates (PROJECT/CONVENTIONS/BOUNDARIES) —
                           copy into a project by hand; nothing auto-loads them
scripts/                   install.sh · verify.py · normalize.py
docs/                      audit, architecture, validation
_retired/                  superseded files, kept for reference
```

## Design in one paragraph

Effort tracks risk. A two-file change gets no gates and a one-line note; a change that touches a
transaction boundary gets a plan, one approval, a failure-mode pass, and a knowledge report.
Every completion states what was verified by command, what is covered by tests, what is assumed,
and what remains untested. Knowledge lands in the repo's `.ai/knowledge/`, not in chat history.
