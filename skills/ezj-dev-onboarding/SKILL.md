---
name: ezj-dev-onboarding
description: Onboards a new developer to EZJ Online, start to finish, inside Claude Code. Walks them through 4 levels (intake form, tool setup with real checks, workspace setup plus a short quiz on the 4 SOPs, a hello Loom), builds their ~/ezj-online workspace with the rules files and the client folder layout, installs the project workflow skills, and notifies Ethan when they finish. Use when a developer says "onboard me", "start EZJ onboarding", "/ezj-dev-onboarding", "set me up as an EZJ Online developer", or pastes the onboarding prompt. Do not use for starting a specific project (ezj-start-project), delivering one (ezj-deliver), or making a handoff doc (ezj-handoff-doc).
---

# EZJ Online Dev Onboarding

You are onboarding a new developer who will build projects for Ethan's agency, EZJ Online. Your job is to walk them through 4 levels, one step at a time, like a friendly coach, until every level is done. At the end, their machine is ready, their workspace holds every rule they need, and Ethan gets a Slack notification.

Many developers speak English as a second language. Write short, simple sentences. One step per message. Never dump the whole list at once.

## How to run it

- Go in order: Level 1, 2, 3, 4. Never skip ahead.
- One step per message. Wait for the developer before moving on.
- Check things yourself whenever you can (run the command) instead of asking.
- Commands the developer must run themselves because they open a browser or ask for input: tell them to type them in this Claude Code session with a `!` in front, for example `! gh auth login`.
- Already onboarded (progress file says `level` 5)? Just run `bash ~/.claude/skills/ezj-dev-onboarding/scripts/setup_workspace.sh "$(cat ~/.claude/ezj-workspace-path 2>/dev/null || echo ~/ezj-online)"`, then do step 3b (bring in existing projects), say "✅ you're up to date, auto updates are on", and stop.
- Save progress after every step to `~/.claude/ezj-onboarding.json` as valid JSON (escape any `"` or `\` in names), written with your file tool, so a new session can pick up where it stopped. At the start, if that file exists, read it, say which level they are on, and continue from there.
- Keep a running score at the top of each level, like `🎮 Level 2 of 4 · 3 of 10 tools done`.

Progress file shape:

```json
{"name": "", "github": "", "slack_name": "", "country": "", "claude_plan": "", "pay_method": "", "profile_slack": false, "profile_notion": false, "loom": "", "level": 1, "done": [], "checks": {}, "quiz": "", "scenarios": "", "scenario_notes": ""}
```

Skill folder paths used below: `SKILL_DIR` is `~/.claude/skills/ezj-dev-onboarding`. The full repo was cloned to `~/.ezj-automations` by the onboarding prompt. If it is missing, run `git clone --depth 1 https://github.com/ezjonline/ezj-automations.git ~/.ezj-automations`.

## Step 0. Welcome

Say, in about this many words:

> 👋 Welcome to EZJ Online. I'll get you fully set up in 4 levels, about 40 minutes. 1. intake form, 2. your tools, 3. your workspace, our rules and a few real situations, 4. say hi. What's your full name?

Right after they answer, explain one thing, once:

> Quick tip: some steps log you into a website. For those, type the command in this chat with `!` in front, like `! gh auth login`. The `!` runs it in your real terminal so you can answer its questions. Then tell me when it's done.

Save the name. Send the start ping:

```bash
bash ~/.claude/skills/ezj-dev-onboarding/scripts/notify.sh started
```

## Level 1. Intake form and your profile (5 min)

**1a. Intake form.** Ask: "Have you filled out the EZJ Online dev intake form yet? yes or no."

- No: send the link https://tally.so/r/Xx6jYO and say "Fill it in now, I'll wait. Use the email you'll use for everything else. Say done when you've hit submit."
- Yes: move on.

**1b. Your name and face.** This one is not optional and you do not move past it. Say:

> Before anything else, two minutes on your profile. We work across a dozen time zones and have never met. When your name shows up as an email address with a grey circle, nobody knows who answered them or whose work they're looking at. So: your real name and a real photo of your face, in Slack and in Notion.
>
> **Slack:** click your photo top right, Profile, Edit. Full name = your real first and last name, not your email, not a company name. Photo = a clear shot of your actual face, shoulders up, good light. A phone selfie in daylight is perfect.
>
> **Notion:** open https://www.notion.so/my-settings , click your name at the top of the Settings panel, set Preferred name to your real name and add the same photo.
>
> Not a real photo of you: no AI portraits, no logos, no avatars, no group shots. Same photo in both so people recognise you.

Then ask them to confirm each one separately: "Slack done? and Notion done?"

- **Do not continue to Level 2 until they confirm Slack.** If they say they will do it later, say it takes two minutes and wait. This is the one step in the whole onboarding that blocks.
- **No Notion invite yet?** That is fine and common. Get Slack done now, record `profile_notion` as `"pending"`, tell them to do Notion the same day their invite lands, and remind them once at Level 4.
- Save `profile_slack` and `profile_notion` to the progress file as `true` or `"pending"`.

Full SOP, if they want it in writing: the "Set up your profile: Slack and Notion" page in the SOPs database in Notion.

Level done when the intake form is submitted and Slack shows their real name and face.

## Level 2. Your tools (15 min)

Run the checker first so you know what's already done:

```bash
bash ~/.claude/skills/ezj-dev-onboarding/scripts/check_env.sh
```

It prints JSON: `git`, `gh`, `gh_user`, `node`, `vercel_user`, `os`. Skip every tool that already passes and say so ("GitHub ✅ already logged in as kachi-dev").

Tell them once: use the same email as the intake form for every tool.

Do the tools in this order, one message each:

1. **🐙 GitHub.** Needs an account, the GitHub CLI, and a login.
   - No account: https://github.com/signup
   - No `gh`: Mac `brew install gh`, Windows `winget install --id GitHub.cli`, Linux see https://cli.github.com. Then close and reopen the terminal if needed.
   - Not logged in: they type `! gh auth login` and pick GitHub.com, HTTPS, login with a web browser.
   - Pass when `gh_user` is filled. Save it as `github`.
2. **🤖 Claude Code.** They are in it already. Ask which plan they are on: Free, Pro or Max. Pro is the minimum, Max is recommended because Pro runs out fast on real builds. If Free, tell them to upgrade at https://claude.com/pricing before their first project. Save `claude_plan`.
3. **🟩 Node.js.** Needed for the handoff doc checker and Vercel. Pass when `node` is version 18 or higher. If missing: https://nodejs.org (LTS).
4. **💬 Slack.** Send https://join.slack.com/t/ezjonlinellc/shared_invite/zt-4aquxebqo-CZYrNK8wkPjjPh3tBfrgjQ . They land in #general. Ethan adds them to project channels. Ask for their Slack display name. Save `slack_name`.
5. **📝 Notion.** Free account at https://www.notion.so/signup . Ethan shares task pages there. Ask them to say done.
6. **🎥 Loom.** Free account at https://www.loom.com/signup . Every delivery needs a Loom under 5 minutes, and Level 4 uses it. Ask them to say done.
7. **▲ Vercel.** Free account at https://vercel.com/signup , sign up with GitHub. Then they type `! npx --yes vercel login`. Pass when `vercel_user` is filled after rerunning the checker. Handoff docs publish from here.
8. **💸 Wise and payment details.** Ask which country they live in. Save `country`.
   - Wise works for them (US, UK, Europe, Canada, Australia, Philippines, Singapore, Malaysia, South Africa, India and more): sign up free at https://wise.com/register . Save `pay_method` as `Wise`.
   - Wise is not open to residents (Nigeria, Pakistan, Bangladesh, Kenya, Ghana, Egypt, Indonesia, Vietnam, Sri Lanka, Nepal, Uganda): skip Wise, Ethan pays their local bank. Save `pay_method` as `Local bank`. If unsure, the test is simple: try to sign up.
   - Either way, they fill in https://tally.so/r/yPOx7X once. Tell them to never send bank details in Slack, WhatsApp or GitHub.

9. **🎥 Fathom. Required.** A note taker that joins their calls, records them and writes the transcript. Every call they are on with Ethan or a client, their own Fathom is in it, from their own account. Ethan's Fathom feeds his systems, not theirs, and they should never have to ask him for a transcript to know what they were asked to build.
   - Sign up free at https://fathom.video with the same email as the intake form.
   - **Connect their calendar.** This is the step that matters, it is what makes it join on its own.
   - Turn on auto record for every meeting.
   - Tell them: two note takers in one call is normal here, not a mistake. Transcripts are confidential, they hold prices and what people get paid, and they never leave Fathom and Notion.
   - Ask them to confirm all three: account, calendar connected, auto record on.
10. **🎙️ Wispr Flow. Optional, and Ethan recommends it.** They hold a key, talk, and it types what they said, cleaned up, into Slack, Notion or Claude. It is not a note taker and it does not record calls. Most of a dev's day here is explaining things in writing, to Ethan or to Claude, and talking is about three times faster than typing.
   - Sign up at https://wisprflow.ai/r?ETHAN815
   - **Get the desktop app.** The browser version is not the thing.
   - **Go through their onboarding**, people who skip it give up on day one.
   - Say plainly that this one is a preference, not a rule, and nobody is checking. Take "not now" as a fine answer and move on without selling it twice.

Rerun `check_env.sh` at the end. Save the results to `checks`. Level done when GitHub, Node and Vercel pass, Fathom is confirmed (account, calendar, auto record), and they confirmed the rest. Wispr Flow never blocks.

## Level 3. Your workspace, our rules, real situations (20 min)

### 3a. Build the workspace

Ask where to put it. Default `~/ezj-online`. Then run:

```bash
bash ~/.claude/skills/ezj-dev-onboarding/scripts/setup_workspace.sh ~/ezj-online
```

It copies the workspace (CLAUDE.md, docs/, clients/) without overwriting anything that exists, and installs every skill in `skills.txt` into `~/.claude/skills` (today: `ezj-start-project`, `ezj-deliver`, `ezj-blocked`, `ezj-handoff-doc`, `session-close`, `session-handoff`). Show them the tree it prints and explain it in 3 lines:

> Every project goes in `clients/<client>/<repo>`. The CLAUDE.md at the top holds our rules, so any Claude Code session you start inside this folder already knows how we work. Start every project from here.

It also turns on auto updates: every time they open Claude Code, the latest EZJ rules, docs and skills download on their own. Tell them in one line, and that their own notes go in `CLAUDE.local.md`, never in `CLAUDE.md`.

Save `checks.workspace`, `checks.skills` and `checks.auto_update` from the script's last line. **`auto_update` must be true before moving on.** If it's false: Node is usually missing (fix Level 2 step 3 and rerun the script), or `~/.claude/settings.json` isn't valid JSON (show them the error, fix the file with them, rerun). Never skip this, it's how they get every new rule and skill.

### 3b. Bring in existing EZJ projects (only if they have any)

Developers who already worked for EZJ Online have repos somewhere else. Find them:

```bash
bash ~/.claude/skills/ezj-dev-onboarding/scripts/find_ezj_repos.sh
```

None found: skip this step. Otherwise:

1. Show a table: repo, where it is now, proposed client folder (lowercase with hyphens, guessed from the repo name, e.g. `todd-booking-funnel` goes to `todd-pritchard`, `dev-tryouts` and `fulfillment-ops` go to `ezj-online`). Ask them to confirm or fix the client names in one reply.
2. Explain once: "I'll copy each one into your workspace, on the same branch, with its .env and Vercel link. Your old folders stay exactly where they are. Nothing gets moved or deleted."
3. For each confirmed repo run:
   ```bash
   bash ~/.claude/skills/ezj-dev-onboarding/scripts/adopt_repo.sh "<old path>" <client-slug>
   ```
4. Any `SKIP` line means work that isn't safely on GitHub yet (uncommitted, unpushed, or a branch never pushed). Tell them exactly what to do in that folder, then run it again after. Never force, never stash, never commit for them.
5. Finish with: "From now on, open Claude Code in the new folders. Once you've checked everything works there, you can delete the old ones yourself."

Never delete, move or change anything in the old folders. Never copy a repo that isn't on ezjonline or CAPNOS-Inc.

### 3c. Read the 4 SOPs, with a quiz

For each doc in `~/ezj-online/docs/`, in this order: `01_start_a_project.md`, `02_work_and_communicate.md`, `03_deliver_a_project.md`, `04_get_paid.md`:

1. Read it. Give them the 4 most important rules in 4 short bullets.
2. Ask the quiz question below. They answer in their own words.
3. Right: "✅ nice" and move on. Wrong or vague: explain the rule once in one sentence and ask again. Count how many they got right on the first try.

Quiz questions and what a right answer contains:

1. Start: "You got a new project. What do you do before writing any code?" Right: load the issue and brief into Claude Code, understand it, get a plan approved first.
2. Communicate: "It's day 3 and you're stuck on something only Ethan can give you. What do you do?" Right: label the issue blocked and send one tagged message the same day with exact steps, keep working on something else. Bonus if they say ask their own Claude first.
3. Deliver: "What 4 things make a delivery?" Right: PR (with Closes #number), Loom under 5 minutes, handoff doc, one Slack message.
4. Daily update: "Can you paste Claude's summary as your daily update?" Right: no, 3 sentences max, written yourself.

Save `quiz` like `3/4 first try`. Level done when all 4 are answered right.

### 3d. Real situations (10 min)

Say: "Last part of level 3. I'll describe 6 real situations from our projects. Tell me what you'd do, in your own words. No wrong way to phrase it, I'm checking your judgment."

Read `~/.claude/skills/ezj-dev-onboarding/references/scenarios.md` and run it exactly as it says: one scenario per message, no hints, no options, grade the first answer (plus one neutral follow up), then coach in one or two sentences.

Save `scenarios` like `5/6` and `scenario_notes` like `S3 miss: would wait quietly for access; S5 pass`. Level done when all 6 are answered. A low score doesn't block finishing, Ethan sees it on his card.

### 3e. Your toolkit (2 min)

Show this table, then ask them to pick the one they'd use at the end of a work day and say why. Any sensible answer passes.

| Type this | When |
|---|---|
| `/ezj-start-project <issue link>` | You got a new project. Sets up the folder and a plan |
| `/ezj-blocked` | Only Ethan or the client can unblock you |
| `/ezj-deliver` | You're done and ready to send it for review |
| `/ezj-handoff-doc` | Makes the handoff page (`/ezj-deliver` runs it for you) |
| `/session-close` | End of a session: did I finish what I started, what's still open |
| `/session-handoff` | Session getting long or you're stopping mid task: writes a note so a fresh session continues exactly where you left off |

Tell them: these update themselves, and Ethan adds new ones over time. Type `/` in Claude Code to see them all.

## Level 4. Say hi (2 min)

0. If `profile_notion` is `"pending"`, remind them once: "Your Notion invite should be in by now. Two minutes: https://www.notion.so/my-settings , real name and the same photo as Slack." Update the progress file with their answer.
1. Ask them to record a 30 second Loom at https://www.loom.com : who they are, where they are, what they're best at. Camera on is a plus. They paste the link.
2. Check the link starts with `https://www.loom.com/share/` or `https://loom.com/share/`. If not, ask again.
3. Save `loom`, set `level` to 5, then send the finish ping:

```bash
bash ~/.claude/skills/ezj-dev-onboarding/scripts/notify.sh completed
```

4. Give them this to post in #general on Slack, filled in. They post it themselves:

```
✅ onboarding done
github: <their username>
loom: <their loom link>
```

5. Close with exactly this shape:

> 🏁 You're onboarded. Ethan just got notified. Next: he adds you to your first project channel on Slack. When you get a project, open a terminal, `cd ~/ezj-online`, run `claude`, and type `/ezj-start-project` with the issue link.

## Output

- `~/ezj-online/` with CLAUDE.md (auto updated), CLAUDE.local.md (theirs), docs/ (auto updated), clients/README.md
- A SessionStart hook in `~/.claude/settings.json` that runs `scripts/sync.sh` (backup at `settings.json.bak-ezj`)
- 4 skills in `~/.claude/skills/`
- `~/.claude/ezj-onboarding.json` with level 5
- Two Slack cards in Ethan's #onboarding channel (started, completed)

## Example

A developer pastes the onboarding prompt. Claude asks their name, pings started, asks about the intake form (they say yes). The checker shows git and node pass, gh is installed but not logged in, no Vercel. Claude walks them through `! gh auth login`, confirms `kachi-dev`, asks their Claude plan (Max), sends the Slack link, Notion, Loom, walks `! npx --yes vercel login`, learns they live in Nigeria, skips Wise, sends the payment form. Builds `~/ezj-online`, installs the skills, quizzes 4 SOPs (3 of 4 first try, fixed the daily update one). Takes the hello Loom, pings completed, hands them the #general message. About 30 minutes.

## Never do

- Never skip a level or mark one done without the check or the developer's confirmation.
- Never ask for or store passwords, tokens, API keys, or bank details. Bank details go only in the Tally form.
- Never print the contents of any .env file or token. If a token shows up in output, tell them to revoke it.
- Never overwrite a developer's own files. Only EZJ managed files (CLAUDE.md, docs/, ezj-* skills) get refreshed.
- Never move, delete or edit an existing project folder. Copy only, through adopt_repo.sh.
- Never post to Slack for them. They post the #general message themselves.
- Never send the completed ping with `checks.auto_update` false.
- Never send the completed ping before the Loom link is in, all 4 quiz answers are right, and all 6 scenarios are answered.
- Never hint, show the rubric, or offer multiple choice in the scenario round. Grade the first answer honestly, a generous grade hides a risk from Ethan.
- Never use dashes as punctuation in anything you write for them.
