#!/usr/bin/env python3
"""Replace literal credentials in opencode.json with {env:...} references.

Never prints the values it removes — only counts.
Usage: python3 scripts/scrub-secrets.py [--check]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "opencode.json"

RULES = [
    # GitHub classic/pat tokens in any string (header values included)
    (re.compile(r"Bearer\s+gh[pousr]_[A-Za-z0-9_]{20,}"), "Bearer {env:GITHUB_TOKEN}"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"), "{env:GITHUB_TOKEN}"),
    # Penpot user token lives in a query string
    (re.compile(r"userToken=eyJ[A-Za-z0-9._\-]+"), "userToken={env:PENPOT_TOKEN}"),
    # OpenAI-style keys
    (re.compile(r"sk-[A-Za-z0-9_\-]{20,}"), "{env:OPENAI_API_KEY}"),
    # Slack bot tokens
    (re.compile(r"xox[abprs]-[A-Za-z0-9\-]{10,}"), "{env:SLACK_TOKEN}"),
    # Database URIs with a literal userinfo password (skips existing {env:...} refs)
    (re.compile(r"://([^/\s:@]+):[^@\s{]+@"), r"://\1:{env:DB_PASSWORD}@"),
    # Literal --pass values in CLI arg arrays (skips existing {env:...} refs)
    (re.compile(r'("--pass",\s*")[^"{]+(")'), r"\1{env:MYSQL_PASSWORD}\2"),
]


def main() -> int:
    check = "--check" in sys.argv
    text = TARGET.read_text(encoding="utf-8", errors="replace")
    total = 0
    for pattern, replacement in RULES:
        text, n = pattern.subn(replacement, text)
        if n:
            print(f"{'would replace' if check else 'replaced'} {n}x {pattern.pattern[:32]}… -> {replacement}")
            total += n
    if total and not check:
        TARGET.write_text(text, encoding="utf-8")
    if not total:
        print("clean: no literal credentials found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
