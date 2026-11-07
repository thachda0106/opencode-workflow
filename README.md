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

Nothing else. A folder named `agents/` somewhere that is not a config directory is inert.

## Workflow modes

The workflow scales with consequence, not file count. Full policy: `AGENTS.md`.

| Mode | Tier | Gates | Work artifacts | Knowledge |
|------|------|-------|----------------|-----------|
| Lightweight | T0 | 0 | none | one-line chat note |
| Standard | T1 | 3 (G1–G3) | `.ai/work/<slug>/{scratchpad,plan,tasks}.md`; flows mandatory when behavior changes | `features/<slug>/README.md` + `full-flow.md` |
| Full Engineering | T2 | 4 (G1–G4) | all four + `review.md` | full package: README, full-flow, architecture, decisions |

The main entry point is `/ai-workflow`. `/create-feature` and `/fix-bug` route into the same
lifecycle.

## Artifacts

```text
.ai/work/<slug>/                 # process state, git-tracked
  scratchpad.md
  plan.md
  tasks.md
  implementation-flows.md
  review.md

.ai/knowledge/features/<slug>/   # durable knowledge
  README.md
  full-flow.md
  architecture.md
  decisions.md
```

Legacy `.ai/knowledge/features/<slug>.md` and `.ai/knowledge/plans/<slug>.md` remain readable;
new work does not write them.

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

Restart OpenCode after installing; skills and commands are loaded at startup.

## Verify

```bash
python scripts/verify.py          # schema, references, workflow contract, install parity
opencode debug skill              # which skills actually loaded and from where
opencode agent list               # what actually loaded
```

## Layout

```
AGENTS.md                  operating contract (modes, gates, artifacts, epistemic labels, knowledge)
skills/                    single-responsibility procedures, loaded on demand
  design-implementation-flows/      pre-code Mermaid flow design
  map-critical-paths/               rank code paths by ownership risk
  transfer-implementation-knowledge/ visual knowledge package
  verify-ownership/                 Level 1-3 ownership check
  stress-test-implementation/       production failure-mode pass
  analyze-project-structure/ trace-execution-flow/ locate-code-patterns/
  validate-architecture/ diagnose-bug-root-cause/ apply-targeted-fix/ verify-bug-regression/
commands/                  entry points; /ai-workflow is the master lifecycle
agents/                    specialist subagents
templates/knowledge/       the .ai/knowledge/ contract to copy into a project
prompts/templates/         scratchpad, plan, tasks, implementation-flows, review templates
context/                   optional per-project templates; nothing auto-loads them
scripts/                   install.sh · verify.py · normalize.py
docs/                      audit, architecture, validation
_retired/                  superseded files, kept for reference
```

## Design in one paragraph

Effort tracks consequence. A two-file change gets no gates and a one-line note. A normal feature
gets three approvals and a visual flow before code. A payment, authz, concurrency, or migration
change gets four approvals, a failure-mode pass, and a visual knowledge package. Every completion
states what was verified by command, what is covered by tests, what is assumed, and what remains
untested. Knowledge lands in `.ai/knowledge/`, not in chat history.
