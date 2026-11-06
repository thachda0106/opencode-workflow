#!/usr/bin/env python3
"""Retire the SCRATCHPAD -> PLAN -> TASKS three-gate chain from ordinary commands.

The tier model lives in AGENTS.md and /ai-workflow. Commands keep their domain procedure
but stop re-implementing a lifecycle with 3 hard stops per command.

Transform per file:
  1. drop "### 🛑 HARD STOP — ..." heading + its fenced block
  2. drop the "> [!CAUTION]" callout
  3. drop "**... must be APPROVED ...**" lines
  4. drop '**Output**: `SCRATCHPAD.md`' style lines
  5. drop "// turbo" markers
  6. point the three artifacts at one file: .ai/knowledge/plans/<slug>.md
  7. insert a Gates note after the H1
  8. collapse runs of blank lines

Usage: python3 scripts/migrate-gates.py [--dry-run]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    "add-api-integration", "add-tests", "daily-system-boot", "deep-dive", "fix-bug",
    "get-docs", "optimize-performance", "refactor-feature", "review-architecture",
    "review-pr", "update-docs",
]
SKIP_HEADING = re.compile(r"^#{2,3}\s*🛑|^#{2,3}.*HARD STOP", re.I)
FENCED_OPEN = re.compile(r"^\s*```")

GATES_NOTE = (
    "> **Gates**: this command follows the tier model in `AGENTS.md`. T0/T1 run with no stops;\n"
    "> T2 stops once, after the plan. Investigation notes, plan, and step list all live in\n"
    "> `.ai/knowledge/plans/<slug>.md` — not in three root-level files.\n"
)


def migrate(text: str) -> tuple[str, int, list[str]]:
    lines = text.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    warnings: list[str] = []
    removed = 0
    i = 0
    while i < len(lines):
        line = lines[i]

        if SKIP_HEADING.match(line):
            removed += 1
            # skip heading, then the following fenced block, then trailing blanks
            j = i + 1
            fence_seen = 0
            while j < len(lines) and j < i + 14:
                if FENCED_OPEN.match(lines[j]):
                    fence_seen += 1
                    if fence_seen == 2:
                        j += 1
                        break
                j += 1
            if fence_seen < 2:
                # unfenced variant: heading, blank, "Say: ..." / "WAIT for ..." lines
                j = i + 1
                while j < len(lines) and j < i + 8 and (
                    not lines[j].strip() or re.match(r'^(Say:|WAIT|")', lines[j].strip())
                ):
                    j += 1
                warnings.append("unfenced gate (Say/WAIT form) removed")
            while j < len(lines) and not lines[j].strip():
                j += 1
            i = j
            continue

        if line.startswith("> [!CAUTION]") or line.startswith("> [!WARNING]"):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            i = j
            continue

        if re.search(r"\*\*[^*]*must be APPROVED[^*]*\*\*", line, re.I):
            i += 1
            continue

        if re.match(r"^\*\*Output\*\*:\s*`(SCRATCHPAD|PLAN|TASKS)\.md`\s*$", line):
            i += 1
            continue

        if line.strip() in {"// turbo", "//turbo"}:
            i += 1
            continue

        out.append(line)
        i += 1

    text = "\n".join(out)
    text = text.replace("SCRATCHPAD.md", ".ai/knowledge/plans/<slug>.md")
    text = text.replace("PLAN.md", ".ai/knowledge/plans/<slug>.md")
    text = text.replace("TASKS.md", ".ai/knowledge/plans/<slug>.md")

    # insert gates note after the first H1
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            lines[idx + 1:idx + 1] = ["", GATES_NOTE.rstrip("\n")]
            break
    text = "\n".join(lines)

    text = re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"
    return text, removed, warnings


def main() -> int:
    dry = "--dry-run" in sys.argv
    total = 0
    for name in TARGETS:
        p = ROOT / "commands" / f"{name}.md"
        if not p.exists():
            print(f"MISSING {p.name}")
            continue
        original = p.read_text(encoding="utf-8", errors="replace")
        new, removed, warnings = migrate(original)
        left = len(re.findall(r"APPROVE", new))
        flag = "!" if left else " "
        print(f"{flag} {name}: gates removed={removed}, 'APPROVE' left={left}, "
              f"{len(original)}B -> {len(new)}B")
        for w in warnings:
            print(f"    warn: {w}")
        total += removed
        if not dry and new != original:
            p.write_text(new, encoding="utf-8")
    print(f"\n{total} gate section(s) {'would be' if dry else ''} removed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
