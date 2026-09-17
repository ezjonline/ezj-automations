---
name: ezj-handoff-doc
description: Turns a finished build into a branded EZJ Online handoff doc, one self contained HTML page in black and orange that explains what was built, how it works, how to test it, how to set it up, what breaks it, and what is still needed, in plain English anyone can follow, with diagrams, status pills and real numbers. Then publishes it to a link and writes the Slack delivery message. Use when a developer says "make the handoff doc", "create a handoff doc", "handoff doc for this project", "/ezj-handoff-doc", "I'm ready to deliver", "write up what I built for Ethan", or when EZJ Online needs a client facing project update page. Do not use for priced proposals, AI audit reports, data dashboards, or a continuation note for a new Claude session.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# EZJ Handoff Doc

Produces one HTML page that lets Ethan (and his client, and the next developer) understand a finished build in about five minutes without opening GitHub, reading code, or asking the developer a single question. It sits next to a Loom walkthrough and a pull request. It is the written half of every delivery to EZJ Online.

The bar: a smart person who has never seen the project reads it once and can explain what it does, test it, set it up from zero, and fix the three most likely problems. If they would need to message the developer, the doc failed.

The look is fixed. Black, orange `#F47C20`, Montserrat and Open Sans, the EZJ Online logo embedded in the header, the components in `template/handoff.html`. You write the content. You do not redesign the page.

## When to use

Use at the end of a build, in the same Claude Code session and repo where the work was done, so the whole context is available. Also use for a client facing project update page.

Do not use for a proposal with pricing, an AI audit report, a live data dashboard, a README, or a note that helps a new Claude session continue work.

## Inputs

**From the repo and this session, never ask for these:** the issue or epic and its acceptance criteria, the PR, the diff, the README, `.env.example`, the tests and their real output, what was tried and what broke during the build.

**Ask the developer for these in ONE message before building, all at once:**

1. The Loom link (loom.com, 5 minutes or less). If it is not recorded yet, build the doc with `LOOM_LINK_NEEDED` in the button. The check fails until the real link is in.
2. The PR link, if it is not already findable with `gh pr view`.
3. A live link to try it (Vercel preview, test form, test number), or "none".
4. Who it is for (the client or project name) and their own name for the byline.

## Process

### 1. Gather the facts first, write nothing yet

Run what applies:

```bash
gh issue view <n> --comments          # the spec and the acceptance criteria
gh pr view --json title,body,url      # the PR, if it exists
git log --oneline main..HEAD
git diff --stat main...HEAD
cat README.md .env.example
```

Run the tests and keep the real output. If the project has a build or generate step (an n8n export built from code, a compiled bundle), rerun it and confirm the output matches what is committed. Then write a private fact sheet in the chat (it does not go in the doc):

- What it does, in one sentence a 12 year old understands.
- Who uses it and what starts it (a click, a form, a call, a schedule).
- The steps, in order, and every place it branches.
- What comes out the other end.
- Every setting it needs: the name, what it is, where to get it. Names only, never values.
- How to run it, how to deploy it, how to test it with test data.
- At least three real ways it breaks, taken from this build (errors hit, limits, things a setting change would break).
- Every acceptance criterion and whether it is truly met, with proof.
- Anything only Ethan or the client can do or decide, with exact click by click steps.

If a fact is not in the repo or the session, it goes on the list of questions for the developer. Never guess it.

### 2. Copy the template

```bash
SLUG=<issue-number>-<short-name>          # example: 12-missed-call-text-back
mkdir -p docs/handoff/$SLUG
cp ~/.claude/skills/ezj-handoff-doc/template/handoff.html docs/handoff/$SLUG/index.html
```

Each delivery gets its own folder, so two developers in one repo never overwrite each other. If the skill was installed inside the project (`.claude/skills/ezj-handoff-doc/`) instead of `~/.claude/skills/`, use that path here and in step 4.

### 3. Fill it section by section with Edit

Never rewrite the whole file in one go, and never retype the logo `<img class="logo">` line. It carries the real logo as embedded data and it breaks if touched. Replace the example content (Harbor Dental, a fictional project) section by section.

| Section | `id` | Needed | Built from (see `references/components.md`) |
|---|---|---|---|
| Hero | header | Always | byline, h1, one line sub, link buttons (Loom first), 3 tiles with status pills |
| How it works | `how` | Always | at least one diagram: `rail`, `routes`, `lanes` or `pipe`. Add `feature` + `phone` when a person sees messages or screens |
| See it work | `try` | Unless nothing can be run | `trysteps` with "You should see", plus `bigstat` + `bars` for real test results |
| Set it up | `setup` | When there is code, a workflow or config | `setup` steps with commands, the settings `table.env`, `cards` for what can be changed |
| What breaks it | `breaks` | Always | 3 to 5 `brk` rows: you notice, why, fix |
| Status | `status` | Always | `board` rows with honest pills |
| What I need from you | `asks` | Only if something is needed | numbered `ask` cards with exact steps |

Delete a section you do not need entirely. Do not leave it empty. Drop a hero button that has no real link (no live link means no Try it button). Put the Loom length in `<small>m:ss</small>` only if you know it, otherwise leave the `<small>` out.

**Big projects.** The page stays about five minutes long no matter how big the build is. Group, never list everything: at most 3 hero tiles (one per main part), one Status row per thing that can be switched on or can fail on its own (8 rows max), 3 to 5 break rows, 5 asks max. Eleven acceptance criteria do not become eleven rows.

**Settings table.** The first column is the exact name where the setting lives: the environment variable, or the credential name in n8n or the platform. Never a made up friendly name there. The plain English goes in the second column. Do not add new CSS unless a component truly does not exist, and then only in the existing style.

Read `references/writing.md` before writing a word. The short version: plain English, one idea per card, headlines that say the outcome, real numbers only, honest status.

### 4. Check it

```bash
node ~/.claude/skills/ezj-handoff-doc/scripts/check.mjs docs/handoff/$SLUG/index.html
```

It fails on: a missing or damaged logo, anything loaded from a file next to the page, leftover example content, a missing Loom link, missing How it works or Status, no diagram, anything that looks like a secret, and dashes used as punctuation. Fix every FAIL and run it again until it prints PASS. If the logo fails, run it once with `--fix-logo`.

### 5. Look at it

Open `docs/handoff/$SLUG/index.html` in a browser. Check it at full width and at phone width (browser dev tools, 375px). Headless Chrome screenshots cannot go below a 500px wide layout, so text looks cut off at 375px when it is not; check phone width in dev tools or inside a 375px iframe instead. Read it top to bottom as Ethan. Anything confusing, anything that needs the code to understand, anything that would make him message the developer: fix it.

### 6. Commit it to the PR branch

```bash
git add docs/handoff/$SLUG/index.html
git commit -m "Add handoff doc"
git push
```

### 7. Publish it to a link

The doc must open for anyone with the link, with no login. The default is the developer's own free Vercel account:

```bash
rm -rf /tmp/$SLUG-handoff && mkdir -p /tmp/$SLUG-handoff
cp docs/handoff/$SLUG/index.html /tmp/$SLUG-handoff/
npx vercel deploy /tmp/$SLUG-handoff --prod --yes
```

First time only, `npx vercel login`. Use the short production address it prints (`https://<name>.vercel.app`), not the long one with random letters. Open that link in a private browser window. If it asks for a login, turn off Vercel Authentication in that Vercel project's Settings, Deployment Protection, and check again. Any other host is fine if the link opens with no login.

### 8. Hand the developer the Slack message

Print the finished delivery message, filled in, inside a code block so they can copy it. No dashes in it either. The developer sends it. You never post it.

## Output format

1. `docs/handoff/<slug>/index.html` committed on the PR branch, check PASS.
2. A public link that opens with no login.
3. This message, filled in, in a code block:

```
Hey @Ethan, <Project name> is ready for your review ✅

🎥 Loom: <link>
📄 Handoff doc: <link>
🔀 PR: <link>
🌐 Try it: <link, or "no live link, see the doc">

TLDR: <one plain sentence on what it does now>
```

## Example

`template/handoff.html` is a complete handoff doc for a fictional Missed Call Text Back build. Open it in a browser to see the target: one line diagram, three branches, a phone mock, four test steps, a test results chart, five setup steps with copy buttons, a settings table, three break and fix rows, an honest status board, and three asks. About 870 words. `preview.png` is a screenshot.

A good run: the developer types `/ezj-handoff-doc`. Claude asks for the Loom, the preview link, the client name and the developer's name in one message. It reads the issue, the PR and the test output, writes the fact sheet, fills the template, runs the check (fixes one em dash and a leftover example phone number), publishes to `https://12-missed-call-text-back-handoff.vercel.app`, confirms it opens in a private window, and prints the Slack message ready to paste.

## Never do

- Never put a real secret value in the doc: no API keys, tokens, passwords, webhook URLs, or signing secrets. Setting names and where to get them only.
- Never put prices, fees, what the client pays, or what the developer is paid.
- Never put real customer data: names, emails, phone numbers, messages. Use test data.
- Never invent a number, a test result, or a status. If it was not run, it is not shown. "Not tested" is an honest status.
- Never mark something Working that only works on the developer's machine or account.
- Never change the logo line, link the logo as a file, or load images from next to the page.
- Never redesign the page, change the colors or fonts, or switch to a light theme.
- Never paste code, logs, or raw Claude output into the doc. Commands to run are fine.
- Never use jargon without saying what it means in the same sentence.
- Never use dashes as punctuation. Use a period or a comma.
- Never post the Slack message, comment on GitHub, or message anyone. The developer sends it.
