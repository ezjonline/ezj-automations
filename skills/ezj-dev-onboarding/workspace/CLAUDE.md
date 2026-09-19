# EZJ Online developer workspace

> Managed by EZJ Online and updated automatically at the start of every Claude Code session. Don't edit this file, your changes get replaced. Put your own notes in `CLAUDE.local.md` next to it.

This folder is where a developer builds every project for EZJ Online, Ethan's AI agency. Any Claude Code session started inside it (or inside any project under `clients/`) loads this file, so Claude already knows how we work.

## Who's who

- **Ethan**: owns EZJ Online. Writes the specs, reviews every PR, merges, talks to the clients. Tag him as @Ethan in Slack.
- **Claudia**: Ethan's AI operator. Reads the same repos you do. Tag @Claudia in a project's Slack channel for questions. Dev trials don't have her yet.
- **The client**: never contact a client directly unless Ethan says so.

## Layout

```
~/ezj-online/
  CLAUDE.md          these rules, auto updated
  CLAUDE.local.md    your own notes, never touched
  docs/              the SOPs, auto updated, read them when unsure
  clients/<client>/<repo>/   one folder per client, one repo per project
```

Start every project with `/ezj-start-project <issue link>`. It clones the repo into the right folder.

## The rules (full detail in docs/)

1. **You own the project.** You have the same repo, brief, issues and context Ethan has. Get it to done without him in the loop.
2. **The GitHub issue is the spec.** If anything disagrees with the issue, the issue wins. Notion is tracking only, never build from it.
3. **Plan before code.** Read CLAUDE.md, docs/DEVELOPMENT_BRIEF.md, docs/CLIENT_CONTEXT.md, the issue and every comment. Get a plan approved before writing code.
4. **Git:** one branch per issue (`yourname/issue-12-short-name`), one PR per issue with `Closes #12`, never push to main, never merge your own PR.
5. **Anything that sends to real people** (texts, emails, DMs, calls) gets built switched off. Ethan switches it on.
6. **One short update a day** in the project's Slack thread, 3 sentences max, written by the developer. Never pasted from Claude.
7. **Stuck?** Ask Claude first, then @Claudia, then @Ethan only for a real blocker. Use `/ezj-blocked`.
8. **Deliver** with 4 parts: PR, Loom under 5 minutes, handoff doc, one Slack message. Use `/ezj-deliver`. Missing a part means it doesn't get reviewed.
9. **One message, one place.** Slack only. No GitHub mentions to get attention, no WhatsApp doubles, no "just checking in".
10. **Deadlines:** most projects take 1 week, big ones 2. Say you'll miss it before the date, never after.

## Your commands

- `/ezj-start-project <issue link>`: start a project the right way
- `/ezj-blocked`: a real blocker, written so Ethan can act in one click
- `/ezj-deliver`: checks all 4 delivery parts before you send
- `/ezj-handoff-doc`: the handoff page
- `/session-close`: end of session, did I finish what I started
- `/session-handoff`: long session or stopping mid task, so the next session picks up exactly here

## Security, no exceptions

- Never commit secrets. Keys live in `.env`, and `.env` is in `.gitignore`.
- Never show a token, key or `.env` on screen in a Loom, a screenshot or a PR comment. If one leaks, revoke it right away and tell Ethan.
- Never use one client's accounts, keys or data for another client.
- Never share client code, data or details outside EZJ Online.

## How Claude should behave here

- Plan first, code after approval. Say what you'll change before changing it.
- When the developer asks for a daily update, give them the facts as rough notes and remind them to write the message in their own words. Don't write the finished update.
- Blocker messages are the exception: write those exactly, with click by click steps (see docs/02_work_and_communicate.md).
- Only touch the files the issue needs. Never rewrite shared files like the root README unless the issue asks.
- No dashes as punctuation in anything written for Ethan or clients.

## When the rules change

A session can start with a note that the EZJ Online rules were updated. Tell the developer in one line what changed, then follow the new rules. The newest docs/ and this file always win over anything older, including an issue template or an old habit.
