# EZJ Online Dev Onboarding

One prompt onboards a new EZJ Online developer inside Claude Code. It walks them through 4 levels (intake form, tools, workspace and rules, hello Loom), checks what it can on their machine, builds their `~/ezj-online` workspace, installs the project skills, and pings Ethan in Slack when they start and when they finish.

## The one prompt

Install Claude Code first (https://docs.claude.com/en/docs/claude-code/quickstart). Open a terminal, run `claude`, and paste:

```
Onboard me as an EZJ Online developer. First run this in bash:
git clone --depth 1 https://github.com/ezjonline/ezj-automations.git ~/.ezj-automations 2>/dev/null || git -C ~/.ezj-automations pull; mkdir -p ~/.claude/skills && cp -R ~/.ezj-automations/skills/ezj-dev-onboarding ~/.claude/skills/
Then read ~/.claude/skills/ezj-dev-onboarding/SKILL.md and follow it with me, one step at a time.
```

Stopped halfway? Open Claude Code again and paste the same prompt. It picks up where you left off.

## What you end up with

```
~/ezj-online/
  CLAUDE.md                  how we work, loads in every session here
  docs/                      the 4 SOPs
  clients/<client>/<repo>/   every project, one folder per client
~/.claude/skills/
  ezj-start-project          /ezj-start-project <issue link>
  ezj-blocked                /ezj-blocked
  ezj-deliver                /ezj-deliver
  ezj-handoff-doc            /ezj-handoff-doc
```

## Files

- `SKILL.md`: the onboarding flow
- `scripts/check_env.sh`: read only check of git, gh, Node and Vercel
- `scripts/setup_workspace.sh`: builds the workspace and installs the skills, never overwrites
- `scripts/notify.sh`: tells Ethan's Slack where you are (name, GitHub, country, checks, Loom link, never passwords or bank details)
- `workspace/`: the workspace template
- `project_skills/`: the 3 skills used on every project
