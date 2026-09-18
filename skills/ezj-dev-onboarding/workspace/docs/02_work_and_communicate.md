# Work and Communicate

**The most important rule.** You have the same repo, brief, issues and context Ethan has. When you ask him a question, he pastes it into his own Claude Code, connected to the same repo, and sends you its answer. Do that yourself. Take ownership and get the project to done.

## Before you ask anything

1. **Ask your Claude Code.** The brief, the client context, the issues, the comments and the code. The answer is usually already there.
2. **Tag @Claudia** in the project's Slack channel. She reads the same repo and answers in a few minutes. Dev trials don't have Claudia yet, so skip this step.
3. **Tag @Ethan** only if it truly blocks you. See Blockers below.

Small decisions inside the spec are yours to make. Decide, write down what you decided in the PR, and keep moving.

## Your daily update

Every working day, one message in the project thread in Slack. 3 sentences max. Like this:

```
day 3, booking bot: finished the reminder texts and their tests. tomorrow the reschedule link. blockers: none.
```

- Write it yourself, in your own words. Typos are fine.
- Never paste Claude Code output. Not summaries, not status reports, not lists of what Claude did. Ethan can tell, and he won't read it.
- Just the TLDR. The details belong in the PR.

## Blockers

A blocker is something only Ethan or the client can do or decide: access, a login, a payment, a business decision. Anything else isn't a blocker. It's your job.

When you're truly blocked, run `/ezj-blocked`. It does both steps:

1. Labels the issue: `gh issue edit <number> --add-label blocked`
2. Writes one tagged message for the project thread, in this format:

```
@Ethan 🚧 blocked on <project> #<issue>
I need: <the one thing>
Steps:
1. <exact click or action>
2. <exact click or action>
3. <what to send back, and where>
Until then I'm working on #<other issue>.
```

This is the one place Claude writes the message, because the steps have to be exact: which website, which menu, which button.

- Bad: "Twilio access doesn't have the right permissions"
- Good: "@Ethan 🚧 blocked on Harbor #14. I need: developer access to the client's Twilio. Steps: 1. twilio.com, Admin, Manage users 2. Invite dev@email.com as Developer 3. Reply done here. Until then I'm on #15."

Say you're blocked the same day. Being blocked is normal. Being blocked quietly for three days is how projects die.

## Deadlines

- Most projects take 1 week. Big ones take 2 at most.
- The deadline is an acceptance criterion. Missing it without warning fails the project.
- Going to miss it? Say so before the date, in one line, with the new date and the reason.

## Where to talk

- Slack only. The project's channel for client work. Your DM with Ethan for dev trials.
- Never message Ethan on GitHub. Don't tag him in PR comments to get his attention.
- Never send the same message on WhatsApp as well. One message, one place.
- No "just checking in" messages. He reads everything tagged.
