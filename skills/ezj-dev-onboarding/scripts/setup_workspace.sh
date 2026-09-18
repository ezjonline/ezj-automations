#!/usr/bin/env bash
# Builds the EZJ Online workspace, installs the project skills, and turns on auto updates.
# Safe to run again: the dev's own files are never overwritten, only EZJ managed ones
# (CLAUDE.md, docs/, the ezj-* skills) get refreshed to the latest version.
# Usage: setup_workspace.sh [target_dir]   (default ~/ezj-online)
set -u
TARGET="${1:-$HOME/ezj-online}"
TARGET="${TARGET/#\~/$HOME}"
REPO="$HOME/.ezj-automations"

if [ -d "$REPO/.git" ]; then git -C "$REPO" pull -q --ff-only 2>/dev/null; else
  git clone -q --depth 1 https://github.com/ezjonline/ezj-automations.git "$REPO" || {
    echo "Could not download the EZJ Online repo. Check your internet and paste the onboarding prompt again."; exit 1; }
fi
SRC="$REPO/skills/ezj-dev-onboarding"
[ -d "$SRC/workspace" ] || { echo "The onboarding files are missing. Paste the onboarding prompt again."; exit 1; }

copy_new() {  # copy_new <src_dir> <dst_dir>: copies files that don't exist yet
  local src="$1" dst="$2"
  (cd "$src" && find . -type f) | while read -r f; do
    [ -e "$dst/$f" ] || { mkdir -p "$(dirname "$dst/$f")" && cp "$src/$f" "$dst/$f"; }
  done
}

mkdir -p "$TARGET" "$HOME/.claude/skills"
copy_new "$SRC/workspace" "$TARGET"
printf '%s' "$TARGET" > "$HOME/.claude/ezj-workspace-path"
[ -e "$TARGET/CLAUDE.local.md" ] || printf '# My notes\n\nYour own notes for Claude go here. EZJ updates CLAUDE.md automatically, so never edit that one.\n' > "$TARGET/CLAUDE.local.md"

# refresh every EZJ managed file to the latest version
bash "$SRC/scripts/sync.sh" --force >/dev/null

# auto update: run sync.sh at the start of every Claude Code session
HOOK_CMD='bash ~/.ezj-automations/skills/ezj-dev-onboarding/scripts/sync.sh'
SETTINGS="$HOME/.claude/settings.json"
ok_hook=false
if grep -qs "ezj-dev-onboarding/scripts/sync.sh" "$SETTINGS"; then
  ok_hook=true
elif command -v node >/dev/null 2>&1; then
  [ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.bak-ezj"
  node -e '
    const fs = require("fs"), p = process.argv[1], cmd = process.argv[2];
    let s = {};
    try { s = JSON.parse(fs.readFileSync(p, "utf8")); } catch (e) { if (fs.existsSync(p)) { console.error("settings.json is not valid JSON, left it alone"); process.exit(1); } }
    s.hooks = s.hooks || {};
    s.hooks.SessionStart = s.hooks.SessionStart || [];
    s.hooks.SessionStart.push({ hooks: [{ type: "command", command: cmd, timeout: 30 }] });
    fs.writeFileSync(p, JSON.stringify(s, null, 2) + "\n");
  ' "$SETTINGS" "$HOOK_CMD" && ok_hook=true
fi

ok_skills=true
for s in ezj-start-project ezj-deliver ezj-blocked ezj-handoff-doc; do
  [ -f "$HOME/.claude/skills/$s/SKILL.md" ] || ok_skills=false
done

echo "Workspace: $TARGET"
(cd "$TARGET" && find . -not -path '*/.git*' -not -path './clients/*/*' | sort | sed 's/^\.\///' | sed '/^\.$/d' | sed 's/^/  /')
ok_ws=false; [ -f "$TARGET/CLAUDE.md" ] && [ -d "$TARGET/docs" ] && [ -d "$TARGET/clients" ] && ok_ws=true
echo "{\"workspace\":$ok_ws,\"skills\":$ok_skills,\"auto_update\":$ok_hook,\"path\":\"$TARGET\"}"
