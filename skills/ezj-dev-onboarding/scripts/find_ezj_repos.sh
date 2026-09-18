#!/usr/bin/env bash
# Lists git repos on this machine that belong to EZJ Online (ezjonline or CAPNOS-Inc on GitHub),
# outside the ezj-online workspace. Read only. One JSON object per line.
WS=$(cat "$HOME/.claude/ezj-workspace-path" 2>/dev/null || echo "$HOME/ezj-online")
find "$HOME" -maxdepth 5 -type d -name .git \
  -not -path "*/node_modules/*" -not -path "*/.ezj-automations/*" -not -path "$WS/*" \
  -not -path "*/Library/*" -not -path "*/.cache/*" 2>/dev/null | while read -r g; do
  repo=$(dirname "$g")
  remote=$(git -C "$repo" remote get-url origin 2>/dev/null)
  case "$remote" in *github.com[:/]ezjonline/*|*github.com[:/]CAPNOS-Inc/*) ;; *) continue ;; esac
  slug=$(printf '%s' "$remote" | sed -E 's#.*github\.com[:/]##; s#\.git$##')
  branch=$(git -C "$repo" rev-parse --abbrev-ref HEAD 2>/dev/null)
  dirty=$(git -C "$repo" status --porcelain 2>/dev/null | grep -vc '^??')
  unpushed=$(git -C "$repo" log --oneline '@{u}..' 2>/dev/null | wc -l | tr -d ' ')
  [ -z "$(git -C "$repo" rev-parse --abbrev-ref '@{u}' 2>/dev/null)" ] && unpushed="no-upstream"
  printf '{"path":"%s","repo":"%s","branch":"%s","uncommitted":%s,"unpushed":"%s"}\n' \
    "$repo" "$slug" "$branch" "${dirty:-0}" "$unpushed"
done
