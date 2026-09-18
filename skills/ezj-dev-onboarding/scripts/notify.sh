#!/usr/bin/env bash
# Tells Ethan's #onboarding channel where a developer is. Usage: notify.sh started|completed
# Sends the progress file as is. It never holds passwords, tokens or bank details.
EVENT="${1:-progress}"
STATE="$HOME/.claude/ezj-onboarding.json"
PROGRESS='{}'
[ -f "$STATE" ] && PROGRESS=$(cat "$STATE")
curl -s -m 20 -X POST "https://n8n.ezjonline.com/webhook/dev-onboarding-r7w3k5" \
  -H 'Content-Type: application/json' \
  -d "{\"event\":\"$EVENT\",\"progress\":$PROGRESS}" >/dev/null \
  && echo "notified: $EVENT" || echo "notify failed (not a blocker, tell Ethan in Slack)"
