---
name: ezj-start-project
description: Starts a new EZJ Online project from a GitHub issue link. Clones the repo into ~/ezj-online/clients/<client>/<repo>, reads the brief, client context, the issue and every comment, then gives a 5 line summary and a build plan, with no code until the developer approves. Use when an EZJ Online developer says "/ezj-start-project", "start this project", "new project", or pastes a github.com/ezjonline issue link to begin. Do not use for delivering (ezj-deliver), blockers (ezj-blocked), or onboarding (ezj-dev-onboarding).
---

# Start an EZJ Online project

Turns an issue link into a cloned repo in the right folder, a clear understanding, and an approved plan. Full rules: `~/ezj-online/docs/01_start_a_project.md`.

## Inputs

- The GitHub issue or epic link. If missing, ask for it. Usually it arrives inside the kickoff prompt from the Slack card's 📋 Copy context button, which also names the client slug and the brief path.
- The client name, from the Slack kickoff card. Ask once. For dev trials or internal work use `ezj-online`.

## Process

1. Parse `owner/repo` and the issue number from the link.
2. Check access: `gh repo view <owner>/<repo> --json name`. If it fails, tell them to accept the invite at https://github.com/notifications and try again.
3. Folder: `~/ezj-online/clients/<client-slug>/<repo>`, client slug lowercase with hyphens. If the repo folder exists, `git -C <folder> pull` instead of cloning. Otherwise:
   ```bash
   mkdir -p ~/ezj-online/clients/<client-slug>
   gh repo clone <owner>/<repo> ~/ezj-online/clients/<client-slug>/<repo>
   ```
4. Read, in this order, whatever exists: the repo's `CLAUDE.md`, the brief, the client context, then the issue with comments (`gh issue view <n> --repo <owner>/<repo> --comments`). If it's an epic, read every sub-issue it links, with comments. The brief is `docs/DEVELOPMENT_BRIEF.md`, or `docs/<project>/DEVELOPMENT_BRIEF.md` in a repo with several projects (the kickoff prompt or the epic names the path), with `CLIENT_CONTEXT.md` next to it.
5. Reply with exactly:
   - **What we're building** (1 line)
   - **Who it's for** (1 line)
   - **What done means** (1 line, from the acceptance criteria)
   - **Issue order** (1 line)
   - **Unclear or contradictory** (1 line, or "nothing")
   - Then a build plan for the first issue: numbered steps, files it touches, how each acceptance criterion gets tested.
6. Say: "No code until you approve this plan." Wait.
7. If the issue has the `needs-plan` label, draft the plan as an issue comment and show it. Post it with `gh issue comment` only when the developer says post.
8. After approval, make the issue branch inside the project folder, named `<devname>/issue-<n>-<short-name>` (`git switch -c <branch>`).
9. Remind them to reply to the Slack kickoff with one line in their own words, like `got it, starting today. first PR by thursday.` Don't write it for them.

## Example

`/ezj-start-project https://github.com/ezjonline/todd-booking-funnel/issues/12`, client "Todd Pritchard". Clones to `~/ezj-online/clients/todd-pritchard/todd-booking-funnel`, reads the brief and #12 with 6 comments, gives the 5 lines and a 6 step plan, waits. On "approved", makes the branch `kachi/issue-12-reminder-texts`.

## Never do

- Never write code before the plan is approved.
- Never push to main or merge a PR.
- Never build from the Notion task. The issue wins.
- Never post an issue comment without the developer saying post.
