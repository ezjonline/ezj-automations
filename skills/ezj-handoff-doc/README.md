# EZJ Handoff Doc skill

A Claude Code skill that turns a finished build into a one page handoff doc anybody can understand: what was built, how it works, how to test it, how to set it up, what breaks it, and what is left. Black and orange, EZJ Online branded, diagrams and real numbers, readable in five minutes.

Every developer delivering work to EZJ Online sends one of these with their Loom and their pull request.

![what it produces](https://raw.githubusercontent.com/ezjonline/ezj-automations/main/skills/ezj-handoff-doc/preview.png)

## Install

**Easiest:** open Claude Code and paste this:

```
Install the Claude Code skill from https://github.com/ezjonline/ezj-automations/tree/main/skills/ezj-handoff-doc into ~/.claude/skills/ezj-handoff-doc (copy the whole folder, including the template, scripts and assets), then confirm the files are there.
```

**Or in a terminal:**

```bash
git clone --depth 1 https://github.com/ezjonline/ezj-automations /tmp/ezj-automations
mkdir -p ~/.claude/skills
cp -r /tmp/ezj-automations/skills/ezj-handoff-doc ~/.claude/skills/
rm -rf /tmp/ezj-automations
```

You need Node.js for the check script and a free Vercel account to publish the link.

## Use it

In the Claude Code session where you built the project, type:

```
/ezj-handoff-doc
```

If the command does not show up, say this instead:

```
Read ~/.claude/skills/ezj-handoff-doc/SKILL.md and follow it to make the handoff doc for this project.
```

Claude asks for your Loom link, your live link, the client name and your name. Then it reads the issue, the PR and your tests, builds the doc, checks it, commits it to your PR branch, publishes it to a link, and gives you the Slack message to send.

## What is in the box

| File | What it does |
|---|---|
| `SKILL.md` | The process, step by step |
| `template/handoff.html` | A complete example handoff doc (fictional project). Open it in a browser to see the target |
| `references/components.md` | Copy and paste snippets for every block on the page |
| `references/writing.md` | How to write it so a non developer understands it |
| `scripts/check.mjs` | Checks the logo, secrets, leftover example text, the Loom link, and dashes. Must say PASS |
| `assets/ezj-logo-white.png` | The logo, embedded into every doc automatically |

## The rules it holds

- One self contained file. The logo is embedded, so it never breaks when the page moves.
- Plain English. Every technical word gets explained or replaced.
- Real numbers only. No invented test results, no fake status.
- Honest status pills: Working now, Needs your go, Waiting on you, Not built, Broken.
- No secret values, no prices, no real customer data.
- Loom link required.
