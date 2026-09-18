#!/usr/bin/env bash
# Copies an existing EZJ project into the workspace as clients/<client>/<repo>. Never moves or
# deletes the old folder. Refuses if the old folder has work that isn't safely on GitHub.
# Usage: adopt_repo.sh <old_path> <client-slug>
set -u
OLD="$1"; CLIENT="$2"
WS=$(cat "$HOME/.claude/ezj-workspace-path" 2>/dev/null || echo "$HOME/ezj-online")
[ -d "$OLD/.git" ] || { echo "SKIP: $OLD is not a git repo"; exit 1; }
remote=$(git -C "$OLD" remote get-url origin)
name=$(basename "$(printf '%s' "$remote" | sed -E 's#\.git$##')")
branch=$(git -C "$OLD" rev-parse --abbrev-ref HEAD)
NEW="$WS/clients/$CLIENT/$name"

git -C "$OLD" fetch -q origin 2>/dev/null
if [ -n "$(git -C "$OLD" status --porcelain | grep -v '^??')" ]; then
  echo "SKIP: $OLD has uncommitted changes. Commit and push them first, then run this again."; exit 2; fi
if [ -z "$(git -C "$OLD" rev-parse --abbrev-ref '@{u}' 2>/dev/null)" ]; then
  echo "SKIP: branch $branch in $OLD was never pushed. Push it first (git push -u origin $branch)."; exit 2; fi
if [ -n "$(git -C "$OLD" log --oneline '@{u}..' 2>/dev/null)" ]; then
  echo "SKIP: $OLD has commits that aren't on GitHub yet. Push them first."; exit 2; fi
if [ -e "$NEW" ]; then echo "EXISTS: $NEW is already there, left it alone."; exit 0; fi

mkdir -p "$WS/clients/$CLIENT"
slug="${remote#*github.com}"; slug="${slug#[:/]}"; slug="${slug%.git}"
gh repo clone "$slug" "$NEW" -- -q || { echo "FAIL: could not clone $slug. Check gh auth status and that you have access."; exit 3; }
git -C "$NEW" switch -q "$branch" 2>/dev/null || git -C "$NEW" switch -q -c "$branch" --track "origin/$branch" 2>/dev/null

# local only files the project needs to run (never on GitHub): env files and the Vercel link
copied=""
for f in "$OLD"/.env "$OLD"/.env.* "$OLD"/.dev.vars; do
  [ -f "$f" ] && cp "$f" "$NEW/" && copied="$copied $(basename "$f")"
done
[ -d "$OLD/.vercel" ] && cp -R "$OLD/.vercel" "$NEW/.vercel" && copied="$copied .vercel"

echo "OK: $NEW (branch $branch)${copied:+, copied$copied}. Old folder untouched: $OLD"
