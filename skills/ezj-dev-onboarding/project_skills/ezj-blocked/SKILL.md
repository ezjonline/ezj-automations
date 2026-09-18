---
name: ezj-blocked
description: Handles a real blocker on an EZJ Online project the right way. Confirms it is truly a blocker (only Ethan or the client can do it), labels the GitHub issue blocked, and writes the one tagged Slack message with exact click by click steps. Use when the developer says "/ezj-blocked", "I'm blocked", "I need access", "waiting on Ethan", or "I can't continue without". Do not use for questions the repo can answer (ask Claude instead), starting a project (ezj-start-project), or delivering (ezj-deliver).
---

# Blocked on an EZJ Online project

Full rules: `~/ezj-online/docs/02_work_and_communicate.md`.

## Process

1. **Is it a real blocker?** A blocker is something only Ethan or the client can do or decide: access, a login, a payment, a business decision. First search the repo, the brief, the issue and its comments for the answer. If the answer is there, give it and stop. If it's a small decision inside the spec, tell them to decide, note it in the PR, and keep going.
2. **Find the exact steps.** Work out exactly what Ethan must do: which website, which menu, which button, what to send back and where. Look up the real menu names. Vague steps are the whole problem this skill fixes.
3. **Label the issue** when the developer says go:
   ```bash
   gh issue edit <number> --repo <owner>/<repo> --add-label blocked
   ```
   If the label doesn't exist, create it first with `gh label create blocked --color B60205`.
4. **Write the message** in a code block, for them to post once in the project thread (dev trials: DM with Ethan):
   ```
   @Ethan 🚧 blocked on <project> #<issue>
   I need: <the one thing>
   Steps:
   1. <exact click or action>
   2. <exact click or action>
   3. <what to send back, and where>
   Until then I'm working on #<other issue>.
   ```
5. Pick the other issue they can work on meanwhile and name it in the last line.

## Example

"I can't send test texts." Twilio access is missing. Claude labels #14 blocked and writes: `@Ethan 🚧 blocked on Harbor #14. I need: developer access to the client's Twilio. Steps: 1. twilio.com, Admin, Manage users 2. Invite dev@email.com as Developer 3. Reply done here. Until then I'm on #15.`

## Never do

- Never call something a blocker when the repo answers it.
- Never ask Ethan for a password or key in Slack. Access gets granted by invite.
- Never post the message or edit the issue without the developer's go.
- Never send it anywhere but the project thread. One message, one place.
