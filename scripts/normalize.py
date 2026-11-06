#!/usr/bin/env python3
"""Normalize agent/skill frontmatter to the OpenCode schema.

OpenCode accepts only these keys in agent frontmatter:
    description, mode, model, temperature, permission, tools, top_p, color,
    steps, maxSteps, hidden, disable, prompt, options, variant

Anything else (notably `skills:` and `boundaries:`) is not part of the schema.
We move that content into the body so nothing is lost, add `mode: subagent`
so specialists stop appearing in the primary agent cycle, and rewrite.

For skills, only name/description/license/compatibility/metadata are valid.
`category`/`inputs`/`outputs` become `metadata:` entries.

Usage: python3 scripts/normalize.py [--check]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AGENT_KEYS = {
    "description", "mode", "model", "temperature", "permission", "tools",
    "top_p", "color", "steps", "maxSteps", "hidden", "disable", "prompt",
    "options", "variant",
}
SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FLAT_KEYS = {"name", "description", "mode", "model", "temperature", "top_p",
             "color", "steps", "maxSteps", "hidden", "disable", "prompt",
             "license", "compatibility"}


def split_frontmatter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = text[3:end].lstrip("\r\n")
    body = text[end + 4:]
    return fm, body


def parse_flat(fm: str) -> list[tuple[str, str | list[str], list[str]]]:
    """Return [(key, value_or_items, raw_lines)] preserving order."""
    entries: list[tuple[str, str | list[str], list[str]]] = []
    cur_key, cur_vals, cur_raw = None, [], []

    def flush():
        nonlocal cur_key, cur_vals, cur_raw
        if cur_key is None:
            return
        if cur_vals:
            entries.append((cur_key, list(cur_vals), cur_raw))
        else:
            entries.append((cur_key, "", cur_raw))
        cur_key, cur_vals, cur_raw = None, [], []

    for raw in fm.replace("\r\n", "\n").split("\n"):
        if not raw.strip():
            continue
        if re.match(r"^\s+-\s+", raw) and cur_key:
            cur_vals.append(re.sub(r"^\s+-\s+", "", raw).strip())
            cur_raw.append(raw)
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if m:
            flush()
            cur_key = m.group(1)
            val = m.group(2).strip()
            cur_raw = [raw]
            if val:
                entries.append((cur_key, val, cur_raw))
                cur_key, cur_raw = None, []
            continue
        # continuation of a nested block (permission:, options:) — keep verbatim
        if cur_key:
            cur_raw.append(raw)
            cur_vals.append(raw)
    flush()
    return entries


def emit_flat(entries) -> str:
    out = []
    for key, val, raw in entries:
        if isinstance(val, list) and val:
            out.append(f"{key}:")
            out.extend(f"  - {v}" if not v.startswith("  ") else v for v in val)
        else:
            out.extend(raw)
    return "\n".join(out)


def normalize_agent(path: Path, check: bool) -> tuple[bool, list[str]]:
    notes: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    sp = split_frontmatter(text)
    if not sp:
        return False, ["no frontmatter"]
    fm, body = sp
    entries = parse_flat(fm)

    kept, dropped_skills, dropped_bounds, other = [], [], [], []
    has_mode = False
    for key, val, raw in entries:
        if key == "skills":
            dropped_skills = val if isinstance(val, list) else [val]
        elif key == "boundaries":
            dropped_bounds = val if isinstance(val, list) else [val]
        elif key == "name":
            if val != path.stem:
                notes.append(f"name '{val}' != filename '{path.stem}' — dropped")
        elif key in AGENT_KEYS:
            kept.append((key, val, raw))
            has_mode = has_mode or key == "mode"
        else:
            other.append(key)

    if not has_mode:
        kept.insert(0, ("mode", "subagent", ["mode: subagent"]))
        notes.append("added mode: subagent")
    if other:
        notes.append("dropped unknown keys: " + ", ".join(other))
    if dropped_skills:
        notes.append(f"moved skills ({len(dropped_skills)}) to body")
    if dropped_bounds:
        notes.append(f"moved boundaries ({len(dropped_bounds)}) to body")

    body = body.lstrip("\n")
    extra = []
    if dropped_skills:
        extra.append("## Declared skills\n\n" + "\n".join(f"- {s}" for s in dropped_skills))
    if dropped_bounds:
        extra.append("## Declared boundaries\n\n" + "\n".join(f"- {s}" for s in dropped_bounds))
    if extra:
        # insert after the H1 title line if present
        lines = body.split("\n")
        idx = 1 if lines and lines[0].startswith("# ") else 0
        body = "\n".join(lines[:idx] + [""] + ["\n\n".join(extra)] + lines[idx:])

    new_text = "---\n" + emit_flat(kept) + "\n---\n" + ("" if body.startswith("\n") else "\n") + body
    if not check and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return True, notes


def normalize_skill(path: Path, check: bool) -> tuple[bool, list[str]]:
    notes: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    sp = split_frontmatter(text)
    if not sp:
        return False, ["no frontmatter"]
    fm, body = sp
    entries = parse_flat(fm)

    known, meta = [], []
    for key, val, raw in entries:
        if key in SKILL_KEYS:
            known.append((key, val, raw))
        else:
            meta.append((key, val))
    if meta:
        notes.append("moved to metadata: " + ", ".join(k for k, _ in meta))

    if meta and not any(k == "metadata" for k, _, _ in known):
        lines = ["metadata:"]
        for key, val in meta:
            if isinstance(val, list):
                flat = ", ".join(v.strip() for v in val)
            else:
                flat = str(val)
            flat = flat.replace('"', "'")
            lines.append(f'  {key}: "{flat}"')
        known.append(("metadata", "", lines))
        notes.append("added metadata map")

    new_text = "---\n" + emit_flat(known) + "\n---\n" + body
    if not check and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return True, notes


def main() -> int:
    check = "--check" in sys.argv
    changed = 0
    problems = 0

    for p in sorted((ROOT / "agents").glob("*.md")):
        ok, notes = normalize_agent(p, check)
        if not ok:
            print(f"FAIL agent {p.name}: {notes[0]}")
            problems += 1
            continue
        if notes:
            changed += 1
            print(f"{'check' if check else 'fix'} agents/{p.name}: " + "; ".join(notes))

    for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
        ok, notes = normalize_skill(p, check)
        if not ok:
            print(f"FAIL skill {p.parent.name}: {notes[0]}")
            problems += 1
            continue
        name = re.search(r"^name:\s*(.+)$", p.read_text(encoding="utf-8"), re.M)
        name_val = (name.group(1).strip() if name else "")
        if name_val != p.parent.name:
            print(f"FAIL skill {p.parent.name}: name field '{name_val}' != directory name")
            problems += 1
        if not NAME_RE.match(p.parent.name):
            print(f"FAIL skill {p.parent.name}: name violates ^[a-z0-9]+(-[a-z0-9]+)*$")
            problems += 1
        if notes:
            changed += 1
            print(f"{'check' if check else 'fix'} skills/{p.parent.name}: " + "; ".join(notes))

    print(f"\n{changed} file(s) {'would change' if check else 'normalized'}, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
