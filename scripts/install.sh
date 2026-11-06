#!/usr/bin/env bash
# Additive install: staging repo -> ~/.config/opencode
#
# Never deletes. Backs up every file it overwrites. Never touches opencode.json.
#
#   ./scripts/install.sh --dry-run
#   ./scripts/install.sh
#   ./scripts/install.sh --no-agents
set -uo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$DEST/.backup-$STAMP"
DRY=0
WITH_AGENTS=1

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --no-agents) WITH_AGENTS=0 ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "unknown flag: $arg"; exit 2 ;;
  esac
done

installed=0; skipped=0; backed_up=0

copy_file() { # $1 = relative path
  local rel="$1" s="$SRC/$1" d="$DEST/$1"
  if [ ! -f "$s" ]; then return 0; fi
  if [ -f "$d" ] && cmp -s "$s" "$d"; then
    skipped=$((skipped+1)); return 0
  fi
  if [ "$DRY" = "1" ]; then
    if [ -f "$d" ]; then echo "  update  $rel"; else echo "  add     $rel"; fi
    installed=$((installed+1)); return 0
  fi
  mkdir -p "$(dirname "$d")"
  if [ -f "$d" ]; then
    mkdir -p "$(dirname "$BACKUP/$rel")"
    cp "$d" "$BACKUP/$rel"; backed_up=$((backed_up+1))
  fi
  cp "$s" "$d"; installed=$((installed+1))
}

echo "source: $SRC"
echo "dest:   $DEST"
[ "$DRY" = "1" ] && echo "mode:   dry-run"
echo

copy_file "AGENTS.md"

for d in "$SRC"/skills/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  while IFS= read -r f; do
    copy_file "skills/$name/${f#"$d"}"
  done < <(find "$d" -type f ! -path '*/node_modules/*' ! -name '*.pyc')
done

for f in "$SRC"/commands/*.md; do
  [ -f "$f" ] || continue
  copy_file "commands/$(basename "$f")"
done

while IFS= read -r f; do
  copy_file "${f#"$SRC/"}"
done < <(find "$SRC/prompts" "$SRC/templates" -type f ! -path '*/node_modules/*' 2>/dev/null)

if [ "$WITH_AGENTS" = "1" ]; then
  for f in "$SRC"/agents/*.md; do
    [ -f "$f" ] || continue
    copy_file "agents/$(basename "$f")"
  done
else
  echo "  (agents skipped)"
fi

echo
echo "installed/updated: $installed · unchanged: $skipped · backed up: $backed_up"
[ "$backed_up" -gt 0 ] && echo "backup: $BACKUP"
if [ "$DRY" = "0" ]; then
  echo
  echo "verify: python3 scripts/verify.py && opencode agent list"
fi
exit 0
