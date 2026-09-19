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
MANAGED="$HOME/.claude/.ezj-managed-skills"
refresh() {
  # managed files only: the dev's own notes live in CLAUDE.local.md and are never touched
  mkdir -p "$WS/docs" "$SK"
  cp "$SRC/workspace/CLAUDE.md" "$WS/CLAUDE.md"
  cp "$SRC/workspace/docs/"*.md "$WS/docs/"
  # install every skill in skills.txt, named by its last folder
  wanted=""
  while IFS= read -r line; do
    line="${line%%#*}"; line="$(printf '%s' "$line" | tr -d '[:space:]')"
    [ -z "$line" ] && continue
    name="${line##*/}"
    [ -f "$REPO/skills/$line/SKILL.md" ] || continue
    rm -rf "$SK/$name" && cp -R "$REPO/skills/$line" "$SK/$name"
    rm -rf "$SK/$name/project_skills"   # the onboarding skill carries these separately
    wanted="$wanted $name"
  done < "$SRC/skills.txt"
  # remove skills this list installed before but no longer includes, never anything else
  [ -z "$wanted" ] && return   # a missing or broken list must never wipe anything
  if [ -f "$MANAGED" ]; then
    for old in $(cat "$MANAGED"); do
      case " $wanted " in *" $old "*) ;; *) rm -rf "$SK/$old" ;; esac
    done
  fi
  printf '%s\n' $wanted > "$MANAGED"
}

if [ "$before" != "$after" ] || [ "${1:-}" = "--force" ]; then
  [ -d "$WS" ] && refresh
  if [ "$before" != "$after" ]; then
    echo "EZJ Online rules were just updated. Tell the developer in one line what changed:"
    git -C "$REPO" log --format='  %s' "$before..$after" -- skills/ 2>/dev/null | head -10
  fi
fi
exit 0
