# Deliver a Project

A delivery has four parts: a pull request, a Loom, a handoff doc, and one Slack message. If any part is missing, Ethan doesn't review it. Run `/ezj-deliver` and it walks you through all four.

## 1. Finish it for real

- Every acceptance criterion in the issue works, and you tested each one yourself, end to end, with test data.
- The PR is open with `Closes #<number>` in the description, no merge conflicts, and no secrets in the code.
- You only changed the files your issue needs. Don't rewrite shared files like the root README unless the issue asks you to.
- If it has a screen, a form or a link, put it online so Ethan can click it. A Vercel preview from the same repo is best.

## 2. Record a Loom, 5 minutes max

- Use Loom (loom.com). Not another screen recorder.
- 5 minutes max. 1 to 3 is better. If you need longer, you're not clear on it yet.
- Show it working end to end the way a real user would, with test data. Click through the real thing.
- Show the error cases the issue asks for, not just the happy path.
- Then take about a minute on how it works underneath. Don't read code line by line.
- Talk clearly. Camera on is a plus.
- Never show a `.env`, a token or a key on screen.

## 3. Make the handoff doc

The `ezj-handoff-doc` skill (installed during onboarding) turns your session into one page anybody can understand: what you built, how it works, how to test it, how to set it up, and what breaks it. In the same Claude Code session where you built the project, type:

```
/ezj-handoff-doc
```

It asks for your Loom link, builds the doc, checks it, commits it to your PR, publishes it to your Vercel, and writes your Slack message.

## 4. Send one Slack message

Post it in the project thread. For dev trials, post it in your DM with Ethan.

```
Hey @Ethan, <project name> is ready for your review ✅

🎥 Loom: <link>
📄 Handoff doc: <link>
🔀 PR: <link>
🌐 Try it: <link, or "no live link, see the doc">

TLDR: <one sentence, in your own words, on what it does now>
```

## 5. Then stop

- Don't post it on GitHub, WhatsApp or email as well.
- Don't follow up for 2 working days. After that, one follow up in the same thread is fine.
- Review notes come back on the PR. Fix them on the same branch, push, and reply in the same Slack thread: "fixed, same links". Record a new Loom only if what it shows has changed.
- Don't merge your own PR and don't mark the task done. Ethan does both.

## Checklist before you hit send

- [ ] Every acceptance criterion tested by you, end to end
- [ ] PR open, `Closes #number`, no conflicts, no secrets
- [ ] Loom on loom.com, under 5 minutes
- [ ] Handoff doc link opens in a private browser window with no login
- [ ] One Slack message, tagged, in the right place
