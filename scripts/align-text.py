#!/usr/bin/env python3
"""One-off text alignment after the gate migration. Idempotent: reports 0 when already applied."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "commands"

EDITS = [
    ("add-tests.md", "1. Define test strategy based on approved scratchpad:",
     "1. Define the test strategy from the plan file:"),
    ("fix-bug.md", "1. Based on the approved diagnosis, plan the fix:",
     "1. Based on the diagnosis in the plan file, plan the fix:"),
    ("refactor-feature.md", "1. Define refactoring strategy based on approved analysis:",
     "1. Define the refactoring strategy from the plan file:"),
    ("review-architecture.md", "Execute the review following the approved plan:",
     "Execute the review following the plan file:"),
    ("review-pr.md", "Execute the review following the approved plan:",
     "Execute the review following the plan file:"),
    ("review-plan.md",
     "description: Review plan files (SCRATCHPAD.md, PLAN.md, TASKS.md) produced by any AI agent — outputs structured critique as review-plan.md",
     "description: Review implementation plans produced by any agent — legacy SCRATCHPAD/PLAN/TASKS or .ai/knowledge/plans/<slug>.md — outputs review-plan.md"),
    ("review-plan.md",
     "   - `TASKS.md` — ordered implementation steps, dependencies, acceptance criteria",
     "   - `TASKS.md` — ordered implementation steps, dependencies, acceptance criteria\n"
     "   - `.ai/knowledge/plans/<slug>.md` — current single-file model (investigation + plan + steps)"),
]

applied = 0
for name, old, new in EDITS:
    p = ROOT / name
    if not p.exists():
        print(f"missing  {name}")
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    if old in text:
        p.write_text(text.replace(old, new, 1), encoding="utf-8")
        print(f"patched  {name}")
        applied += 1
    else:
        print(f"no-op    {name} (already applied or text differs)")
print(f"\n{applied} edit(s) applied")
