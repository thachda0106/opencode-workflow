#!/usr/bin/env python3
"""Validate the opencode config: schema, references, gate policy, install parity.

Exit 1 on any FAIL. WARN does not fail unless --strict.
Usage: python3 scripts/verify.py [--strict]
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = Path(os.environ.get("OPENCODE_CONFIG_DIR", Path.home() / ".config" / "opencode"))

AGENT_KEYS = {
    "description", "mode", "model", "temperature", "permission", "tools",
    "top_p", "color", "steps", "maxSteps", "hidden", "disable", "prompt",
    "options", "variant",
}
SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
GATED_BY_DESIGN = {
    "build-minimum-system", "build-large-system", "build-large-system-phases-01-10",
    "build-large-system-phases-11-20", "build-large-system-phases-21-30",
    "design-platform-core", "dive-into-project",
}

results: list[tuple[str, str, str]] = []  # (level, area, message)


def add(level: str, area: str, msg: str) -> None:
    results.append((level, area, msg))


def frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    out: dict[str, str] = {}
    for line in text[3:end].replace("\r\n", "\n").split("\n"):
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def check_skills() -> None:
    dirs = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    for d in dirs:
        f = d / "SKILL.md"
        if not f.exists():
            add("FAIL", "skills", f"{d.name}: missing SKILL.md")
            continue
        fm = frontmatter(f)
        if fm is None:
            add("FAIL", "skills", f"{d.name}: no frontmatter")
            continue
        if fm.get("name") != d.name:
            add("FAIL", "skills", f"{d.name}: name '{fm.get('name')}' != directory")
        if not NAME_RE.match(d.name):
            add("FAIL", "skills", f"{d.name}: invalid name characters")
        desc = fm.get("description", "")
        if not desc:
            add("FAIL", "skills", f"{d.name}: missing description")
        elif not (1 <= len(desc) <= 1024):
            add("FAIL", "skills", f"{d.name}: description length {len(desc)} (max 1024)")
        elif len(desc) < 40:
            add("WARN", "skills", f"{d.name}: description is thin ({len(desc)} chars)")
        extra = set(fm) - SKILL_KEYS
        if extra:
            add("FAIL", "skills", f"{d.name}: unsupported keys {sorted(extra)}")
    add("PASS", "skills", f"{len(dirs)} skills schema-valid")


def check_agents() -> None:
    files = sorted((ROOT / "agents").glob("*.md"))
    for f in files:
        fm = frontmatter(f)
        if fm is None:
            add("FAIL", "agents", f"{f.name}: no frontmatter")
            continue
        if not fm.get("description"):
            add("FAIL", "agents", f"{f.name}: missing description (required)")
        mode = fm.get("mode")
        if not mode:
            add("FAIL", "agents", f"{f.name}: missing mode (defaults to 'all' → pollutes Tab cycle)")
        elif mode not in {"primary", "subagent", "all"}:
            add("FAIL", "agents", f"{f.name}: mode '{mode}' invalid")
        extra = set(fm) - AGENT_KEYS - {"name"}
        if extra:
            add("FAIL", "agents", f"{f.name}: unsupported keys {sorted(extra)}")
        if fm.get("name") and fm["name"] != f.stem:
            add("WARN", "agents", f"{f.name}: name '{fm['name']}' != filename")
    add("PASS", "agents", f"{len(files)} agents schema-valid")


def check_commands() -> None:
    files = sorted((ROOT / "commands").glob("*.md"))
    for f in files:
        fm = frontmatter(f)
        if fm is None:
            add("FAIL", "commands", f"{f.name}: no frontmatter")
            continue
        if not fm.get("description"):
            add("FAIL", "commands", f"{f.name}: missing description")
        agent = fm.get("agent", "")
        if agent and agent not in {"build", "plan"} and fm.get("subtask") != "false":
            add("FAIL", "commands",
                f"{f.name}: targets subagent '{agent}' without 'subtask: false' "
                f"(gated flow would run in a child session)")
        text = f.read_text(encoding="utf-8", errors="replace")
        gates = len(re.findall(r"HARD STOP", text))
        if gates > 1 and f.stem not in GATED_BY_DESIGN:
            add("FAIL", "gates", f"{f.stem}: {gates} hard stops (max 1 outside greenfield flows)")
        elif gates == 1 and f.stem not in GATED_BY_DESIGN:
            add("WARN", "gates", f"{f.stem}: 1 hard stop — confirm it is a real approval gate")
    add("PASS", "commands", f"{len(files)} commands have descriptions; gate policy checked")


def check_dead_refs() -> None:
    bad = 0
    needles = ("prompts/templates", ".ai/scripts/validate-template.sh", "AI_MANIFEST.yaml")
    scopes = [ROOT / "AGENTS.md"]
    for sub in ("skills", "commands", "agents", "prompts", "templates"):
        scopes.extend((ROOT / sub).rglob("*.md"))
    for p in scopes:
        if not p.exists() or "_retired" in p.parts:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for needle in needles:
            if needle in text and not (ROOT / needle.split("/")[0] if "/" in needle else ROOT / needle).exists():
                add("FAIL", "refs", f"{p.relative_to(ROOT)}: dangling reference '{needle}'")
                bad += 1
    if not bad:
        add("PASS", "refs", "all referenced template paths exist on disk")


def check_skill_refs() -> None:
    names = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    names |= {p.stem for p in (ROOT / "agents").glob("*.md")}
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
    refs = set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", text))
    missing = sorted(r for r in refs if r not in names and not r.startswith(("git", "npm", "npx")))
    if missing:
        add("WARN", "refs", f"AGENTS.md mentions unknown names: {missing}")
    for cmd in (ROOT / "commands").glob("*.md"):
        ctext = cmd.read_text(encoding="utf-8", errors="replace")
        for ref in re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)` skill", ctext):
            if ref not in names:
                add("FAIL", "refs", f"{cmd.name}: references missing skill '{ref}'")
    add("PASS", "refs", f"{len(refs & names)} skill/agent cross-references resolve")


def check_contract() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
    for token in ("T0", "T1", "T2", "VERIFIED", "TESTED", "ASSUMED", "GAP"):
        if token not in text:
            add("FAIL", "contract", f"AGENTS.md missing '{token}'")
    for f in ("index.md", "feature.md", "critical-paths.md", "gotchas.md", "adr-template.md"):
        if not (ROOT / "templates" / "knowledge" / f).exists():
            add("FAIL", "contract", f"templates/knowledge/{f} missing")
    if not (ROOT / "scripts" / "install.sh").exists():
        add("FAIL", "contract", "scripts/install.sh missing")
    add("PASS", "contract", "tier model, epistemic labels, knowledge templates present")


def _strip_jsonc(text: str) -> str:
    """Remove // line comments without touching URLs or braces inside strings."""
    out: list[str] = []
    in_str = esc = False
    i = 0
    while i < len(text):
        c = text[i]
        if in_str:
            out.append(c)
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            i += 1
        elif c == '"':
            in_str = True
            out.append(c)
            i += 1
        elif c == "/" and text[i + 1 : i + 2] == "/":
            while i < len(text) and text[i] != "\n":
                i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def check_config() -> None:
    cfg = ROOT / "opencode.json"
    text = cfg.read_text(encoding="utf-8", errors="replace")
    try:
        json.loads(_strip_jsonc(text))
    except json.JSONDecodeError as e:
        add("FAIL", "config", f"opencode.json does not parse as JSONC: {e}")
        return
    spec = importlib.util.spec_from_file_location("scrub_secrets", ROOT / "scripts" / "scrub-secrets.py")
    scrub = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scrub)
    hits = [r for r, _ in scrub.RULES if r.search(text)]
    if hits:
        add("FAIL", "config",
            f"{len(hits)} literal credential pattern(s) in opencode.json — run scripts/scrub-secrets.py")
    else:
        add("PASS", "config", "opencode.json parses; no literal credentials")
    if re.search(r"[A-Za-z]:/Users/", text):
        add("FAIL", "config", "machine-specific absolute path (drive-letter /Users/) — use **/ or ~/ patterns")
    else:
        add("PASS", "config", "no machine-specific absolute paths")


CONTEXT_REF_RE = re.compile(r"context/(?:PROJECT|CONVENTIONS|BOUNDARIES)\.md")
CONDITIONAL_RE = re.compile(r"\bif\b|exists|present|absent", re.IGNORECASE)


def check_context_refs() -> None:
    bad = 0
    scopes = list((ROOT / "commands").glob("*.md")) + list((ROOT / "skills").rglob("*.md"))
    for p in scopes:
        if "_retired" in p.parts:
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if CONTEXT_REF_RE.search(line) and not CONDITIONAL_RE.search(line):
                add("FAIL", "refs",
                    f"{p.relative_to(ROOT)}: unconditional context/ reference — make it conditional (F9)")
                bad += 1
    if not bad:
        add("PASS", "refs", "context/ references are conditional or absent")


def check_parity() -> None:
    pairs: list[tuple[Path, Path]] = [(ROOT / "AGENTS.md", DEST / "AGENTS.md")]
    for sub in ("skills", "commands", "agents", "templates", "prompts"):
        for f in (ROOT / sub).rglob("*"):
            if f.is_file() and "__pycache__" not in f.parts and f.suffix != ".pyc":
                pairs.append((f, DEST / sub / f.relative_to(ROOT / sub)))
    missing = stale = ok = 0
    for src, dst in pairs:
        if not dst.exists():
            missing += 1
        elif hashlib.sha256(src.read_bytes()).hexdigest() != hashlib.sha256(dst.read_bytes()).hexdigest():
            stale += 1
            add("WARN", "parity", f"stale in dest: {dst.relative_to(DEST)}")
        else:
            ok += 1
    level = "PASS" if missing == 0 and stale == 0 else "WARN"
    add(level, "parity", f"{ok} in sync · {missing} not installed · {stale} stale (dest: {DEST})")


def main() -> int:
    strict = "--strict" in sys.argv
    for fn in (check_skills, check_agents, check_commands, check_dead_refs,
               check_skill_refs, check_contract, check_config, check_context_refs,
               check_parity):
        fn()

    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    for level, area, msg in sorted(results, key=lambda r: (order[r[0]], r[1])):
        print(f"{level:4} {area:9} {msg}")

    fails = sum(1 for r in results if r[0] == "FAIL")
    warns = sum(1 for r in results if r[0] == "WARN")
    passes = sum(1 for r in results if r[0] == "PASS")
    print(f"\n{passes} pass · {warns} warn · {fails} fail")
    if fails or (strict and warns):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
