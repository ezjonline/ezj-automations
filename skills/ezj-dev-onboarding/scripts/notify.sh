#!/usr/bin/env bash
# Tells Ethan's #onboarding channel where a developer is. Usage: notify.sh started|completed
# Sends the progress file as is. It never holds passwords, tokens or bank details.
EVENT="${1:-progress}"
STATE="$HOME/.claude/ezj-onboarding.json"
PROGRESS='{}'
if [ -f "$STATE" ]; then
  PROGRESS=$(cat "$STATE")
  # a broken progress file must not break the payload: validate with node or python, else send {}
  if command -v node >/dev/null 2>&1; then
    node -e 'JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"))' "$STATE" 2>/dev/null || PROGRESS='{}'
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c 'import json,sys;json.load(open(sys.argv[1]))' "$STATE" 2>/dev/null || PROGRESS='{}'
  fi
fi
curl -sf -m 20 -X POST "https://n8n.ezjonline.com/webhook/dev-onboarding-r7w3k5" \
  -H 'Content-Type: application/json' \
  -d "{\"event\":\"$EVENT\",\"progress\":$PROGRESS}" >/dev/null \
  && echo "notified: $EVENT" || echo "notify failed (not a blocker, tell Ethan in Slack)"
