#!/usr/bin/env bash
# Keeps a developer's EZJ Online rules, docs and skills current. Runs at the start of every
# Claude Code session (SessionStart hook). Pulls at most once an hour, never blocks for long,
# prints nothing unless the rules changed. Usage: sync.sh [--force]
REPO="$HOME/.ezj-automations"
STAMP="$HOME/.claude/.ezj-sync-stamp"
WS=$(cat "$HOME/.claude/ezj-workspace-path" 2>/dev/null || echo "$HOME/ezj-online")
[ -d "$REPO/.git" ] || exit 0

if [ "${1:-}" != "--force" ] && [ -f "$STAMP" ] && [ -n "$(find "$STAMP" -mmin -60 2>/dev/null)" ]; then
  exit 0
fi
touch "$STAMP" 2>/dev/null

before=$(git -C "$REPO" rev-parse HEAD 2>/dev/null)
# give up fast when offline or slow instead of holding the session
git -C "$REPO" -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=5 pull -q --ff-only >/dev/null 2>&1
after=$(git -C "$REPO" rev-parse HEAD 2>/dev/null)

SRC="$REPO/skills/ezj-dev-onboarding"
SK="$HOME/.claude/skills"
refresh() {
  # managed files only: the dev's own notes live in CLAUDE.local.md and are never touched
  mkdir -p "$WS/docs" "$SK"
  cp "$SRC/workspace/CLAUDE.md" "$WS/CLAUDE.md"
  cp "$SRC/workspace/docs/"*.md "$WS/docs/"
  for s in ezj-start-project ezj-deliver ezj-blocked; do
    rm -rf "$SK/$s" && cp -R "$SRC/project_skills/$s" "$SK/$s"
  done
  rm -rf "$SK/ezj-handoff-doc" && cp -R "$REPO/skills/ezj-handoff-doc" "$SK/ezj-handoff-doc"
  rm -rf "$SK/ezj-dev-onboarding" && cp -R "$SRC" "$SK/ezj-dev-onboarding"
}

if [ "$before" != "$after" ] || [ "${1:-}" = "--force" ]; then
  [ -d "$WS" ] && refresh
  if [ "$before" != "$after" ]; then
    echo "EZJ Online rules were just updated. Tell the developer in one line what changed:"
    git -C "$REPO" log --format='  %s' "$before..$after" -- skills/ezj-dev-onboarding skills/ezj-handoff-doc 2>/dev/null | head -10
  fi
fi
exit 0
