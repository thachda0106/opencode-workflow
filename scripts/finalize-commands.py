#!/usr/bin/env python3
"""Finalize the migrated commands.

1. Rename phase headings so one document does not look like three artifacts:
      "## PHASE 1 — SCRATCHPAD (Diagnosis)"  ->  "## 1 · INVESTIGATE — Diagnosis"
      "## PHASE 3 — TASKS (Fix Steps)"       ->  "## 3 · STEPS — Fix Steps"
   Skipped for greenfield flows that really do produce the three artifacts.
2. Add `$ARGUMENTS` where a command silently dropped the user's input.
3. Add `subtask: false` to commands targeting a subagent, so a gated flow runs in the
   primary session instead of a child session (gates must be answerable where you are).

Usage: python3 scripts/finalize-commands.py [--dry-run]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CMDS = ROOT / "commands"
DRY = "--dry-run" in sys.argv

KEEP_THREE_ARTIFACTS = {"design-platform-core", "build-minimum-system",
                        "build-large-system", "build-large-system-phases-01-10",
                        "build-large-system-phases-11-20", "build-large-system-phases-21-30",
                        "dive-into-project"}
PRIMARY_OK = {"build", "plan"}

LABELS = {
    "SCRATCHPAD": "INVESTIGATE",
    "PLAN": "PLAN",
    "TASKS": "STEPS",
    "IMPLEMENTATION": "IMPLEMENT",
    "TESTING & VERIFICATION": "VERIFY",
    "TESTING": "VERIFY",
    "EXECUTION": "EXECUTE",
    "DELIVER REVIEW": "DELIVER",
}
HEADING = re.compile(r"^## PHASE (\d+) — ([A-Z &]+?)(?: \((.+)\))?\s*$")

ARGUMENT_EDITS = [
    ("create-feature.md",
     "## PHASE 0 — CLASSIFY\n",
     "## PHASE 0 — CLASSIFY\n\n"
     "Feature to build: **$ARGUMENTS** (if empty, ask for the feature name and stop).\n"),
    ("fix-bug.md",
     "## PHASE 1 — SCRATCHPAD (Diagnosis)",
     "## PHASE 1 — SCRATCHPAD (Diagnosis)\n\nThe bug to diagnose: **$ARGUMENTS** "
     "(if empty, ask for the symptom and stop)."),
    ("review-implemented-files.md",
     "## 1. Load\n",
     "## 1. Load\n\nScope override: **$ARGUMENTS** (empty = the uncommitted diff).\n"),
]


def frontmatter_bounds(text: str) -> tuple[int, int] | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return 3, end


def add_subtask(text: str) -> tuple[str, str]:
    bounds = frontmatter_bounds(text)
    if not bounds:
        return text, "no frontmatter"
    start, end = bounds
    fm = text[start:end]
    m = re.search(r"^agent:\s*(\S+)\s*$", fm, re.M)
    if not m:
        return text, "no agent line"
    agent = m.group(1).strip()
    if agent in PRIMARY_OK:
        return text, f"agent {agent} is primary — ok"
    if re.search(r"^subtask:", fm, re.M):
        return text, "already set"
    new_fm = fm[:m.end()] + "\nsubtask: false" + fm[m.end():]
    return text[:start] + new_fm + text[end:], f"subtask: false added (agent {agent})"


def main() -> int:
    changed = 0
    for p in sorted(CMDS.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        notes: list[str] = []

        # 1. $ARGUMENTS (before heading rewrite — anchors point at the original headings)
        for name, old, new in ARGUMENT_EDITS:
            if p.name == name and old in text and "$ARGUMENTS" not in text:
                text = text.replace(old, new, 1)
                notes.append("$ARGUMENTS wired")

        # 2. headings
        if p.stem not in KEEP_THREE_ARTIFACTS:
            out_lines = []
            for line in text.replace("\r\n", "\n").split("\n"):
                m = HEADING.match(line)
                if m:
                    num, label, detail = m.group(1), m.group(2).strip(), m.group(3)
                    new = f"## {num} · {LABELS.get(label, label)}"
                    if detail:
                        new += f" — {detail}"
                    out_lines.append(new)
                    notes.append(f"heading {num}: {label} -> {LABELS.get(label, label)}")
                else:
                    out_lines.append(line)
            text = "\n".join(out_lines)

        # 3. subtask
        text, note = add_subtask(text)
        if note.startswith("subtask"):
            notes.append(note)

        if text != original:
            changed += 1
            print(f"{'check' if DRY else 'fix'} commands/{p.name}: " + "; ".join(notes))
            if not DRY:
                p.write_text(text, encoding="utf-8")

    print(f"\n{changed} command(s) {'would change' if DRY else 'updated'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
