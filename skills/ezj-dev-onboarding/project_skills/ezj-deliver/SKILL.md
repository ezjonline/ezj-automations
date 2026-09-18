---
name: ezj-deliver
description: Walks an EZJ Online developer through a complete delivery, the 4 parts Ethan requires (PR, Loom under 5 minutes, handoff doc, one Slack message), checking each one before they send. Use when the developer says "/ezj-deliver", "I'm done", "ready to deliver", "ready for review", or "submit this project". Do not use for starting a project (ezj-start-project), making only the handoff doc (ezj-handoff-doc), or blockers (ezj-blocked).
---

# Deliver an EZJ Online project

Missing any of the 4 parts means Ethan doesn't review it. This skill checks all 4. Full rules: `~/ezj-online/docs/03_deliver_a_project.md`.

## Process

Show a score as you go: `📦 Delivery · 2 of 4 parts ready`.

1. **Finished for real.** List every acceptance criterion from the issue. For each, ask how they tested it end to end, or run the tests (`npm test`, `pytest`, whatever the repo uses). Any criterion not tested blocks the delivery.
2. **PR.** Check with `gh pr view --json number,url,body,mergeable,files`:
   - Body contains `Closes #<issue>`. If not, offer to fix it with `gh pr edit`.
   - `mergeable` is not `CONFLICTING`.
   - Changed files: flag anything the issue didn't ask for, especially the root README or shared config.
   - Secrets: scan the diff (`gh pr diff`) for keys and tokens (patterns like `sk-`, `ghp_`, `github_pat_`, `xox`, `AKIA`, `-----BEGIN`, `api_key=`, `.env` files). Any hit blocks the delivery until removed and the key is revoked.
   - No PR yet: push the branch and draft `gh pr create` with `Closes #<issue>`, show it, run it when they say go.
3. **Loom.** Ask for the link. Must start with `https://www.loom.com/share/`. Ask: under 5 minutes? shows it working end to end with test data? shows the error cases? no `.env` or token on screen? All yes, or it's not ready.
4. **Handoff doc.** Run the `ezj-handoff-doc` skill (`/ezj-handoff-doc`). The link must open in a private browser window with no login.
5. **Slack message.** Print this filled with the real links, in a code block, and leave the TLDR for them to write:
   ```
   Hey @Ethan, <project name> is ready for your review ✅

   🎥 Loom: <link>
   📄 Handoff doc: <link>
   🔀 PR: <link>
   🌐 Try it: <link, or "no live link, see the doc">

   TLDR: <write one sentence yourself>
   ```
6. Close with: post it once, in the project thread (dev trials: DM with Ethan). Don't repeat it on GitHub or WhatsApp. Don't follow up for 2 working days. Don't merge or mark anything done.

## Example

Developer types `/ezj-deliver`. Tests pass for 4 of 4 criteria, the PR body is missing `Closes #12` (fixed with `gh pr edit`), the diff scan is clean, the Loom is 3:40, the handoff doc publishes to `https://12-reminders-handoff.vercel.app`, and the Slack message is printed with the TLDR left blank for them.

## Never do

- Never mark a delivery ready with an untested criterion, a conflict, a secret, a missing Loom or a missing handoff doc.
- Never post to Slack or GitHub for them without their explicit go.
- Never merge the PR.
- Never write the TLDR sentence for them.
