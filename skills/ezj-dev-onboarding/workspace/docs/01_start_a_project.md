# Start a Project

Goal: go from "Ethan sent me a project" to "Claude understands the whole project and I have a plan" in under 30 minutes.

## What you get from Ethan

- **A Slack kickoff card.** What the project is, the deadline, the fee, where to start, and what done means.
- **The brief**, `docs/DEVELOPMENT_BRIEF.md` in the repo. Why we're building it and the whole plan.
- **The GitHub epic or issue.** This is the spec. The acceptance criteria live here. If anything disagrees with the issue, the issue wins.
- **The Notion task.** Tracking only. Never build from it.

Dev trial? You get one GitHub issue in the dev-tryouts repo and nothing else. Everything you need is in that issue and its comments.

## Set up the project

1. Accept the GitHub invite. It's in your email or at github.com/notifications.
2. Open a terminal, `cd ~/ezj-online`, run `claude`, and type:

```
/ezj-start-project <paste the issue link>
```

It clones the repo into `clients/<client>/<repo>`, reads everything, and gives you a 5 line summary and a plan. No code until you approve the plan.

Then read Claude's answer yourself. If you can't explain the project to a friend in two sentences, you're not ready to build yet. Anything unclear is almost always answered somewhere in the repo, so ask Claude to find it before you ask anyone.

## Work the issues

- One branch per issue: `yourname/issue-12-short-name`
- One PR per issue, with `Closes #12` in the PR description
- If the issue has the `needs-plan` label, post your plan as a comment on the issue and wait for approval before you build
- Never push to main. Never merge your own PR.
- Anything that sends to real people (texts, emails, DMs) gets built switched off. Ethan switches it on.

## Reply to the kickoff

When you have the plan, reply in the kickoff thread with one line, in your own words:

```
got it, starting today. first PR by thursday.
```
