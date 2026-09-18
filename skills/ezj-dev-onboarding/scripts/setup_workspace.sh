#!/usr/bin/env bash
# Builds the EZJ Online workspace and installs the project skills. Never overwrites.
# Usage: setup_workspace.sh [target_dir]   (default ~/ezj-online)
set -u
TARGET="${1:-$HOME/ezj-online}"
TARGET="${TARGET/#\~/$HOME}"
REPO="$HOME/.ezj-automations"
SRC="$HOME/.claude/skills/ezj-dev-onboarding"
[ -d "$SRC/workspace" ] || { echo "The onboarding skill folder is missing. Paste the onboarding prompt again."; exit 1; }

if [ -d "$REPO/.git" ]; then git -C "$REPO" pull -q 2>/dev/null; else
  git clone -q --depth 1 https://github.com/ezjonline/ezj-automations.git "$REPO"; fi

copy_new() {  # copy_new <src_dir> <dst_dir>: copies files that don't exist yet
  local src="$1" dst="$2"
  (cd "$src" && find . -type f) | while read -r f; do
    if [ -e "$dst/$f" ]; then echo "kept existing: $dst/${f#./}"; else
      mkdir -p "$(dirname "$dst/$f")" && cp "$src/$f" "$dst/$f"; fi
  done
}

mkdir -p "$TARGET"
copy_new "$SRC/workspace" "$TARGET"

mkdir -p "$HOME/.claude/skills"
ok_skills=true
for s in ezj-start-project ezj-deliver ezj-blocked; do
  copy_new "$SRC/project_skills/$s" "$HOME/.claude/skills/$s"
  [ -f "$HOME/.claude/skills/$s/SKILL.md" ] || ok_skills=false
done
copy_new "$REPO/skills/ezj-handoff-doc" "$HOME/.claude/skills/ezj-handoff-doc"
[ -f "$HOME/.claude/skills/ezj-handoff-doc/SKILL.md" ] || ok_skills=false

echo
echo "Workspace: $TARGET"
(cd "$TARGET" && find . -not -path '*/.git*' | sort | sed 's/^\.\///' | sed '/^\.$/d' | sed 's/^/  /')
ok_ws=false; [ -f "$TARGET/CLAUDE.md" ] && [ -d "$TARGET/docs" ] && [ -d "$TARGET/clients" ] && ok_ws=true
echo "{\"workspace\":$ok_ws,\"skills\":$ok_skills,\"path\":\"$TARGET\"}"
