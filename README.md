# EZJ Automations

Free Claude Code skills, n8n templates and prompts from [EZJ Online](https://www.ezjonline.com). The same ones I use to run my own business.

**Every resource has a page with a one-click install prompt: [ezjonline.com/resources](https://www.ezjonline.com/resources)**

## Skills

| Skill | What it does | Page |
|---|---|---|
| [`dashboard`](skills/dashboard) | Builds a data dashboard that looks like a designer made it, in one HTML file | [Install](https://www.ezjonline.com/resources/dashboard-skill) |
| [`humanizer`](skills/humanizer) | Rewrites any copy so it stops sounding like AI | [Install](https://www.ezjonline.com/resources/humanizer) |
| [`session-handoff`](skills/session-handoff) | Writes a handoff doc so you can clear Claude Code without losing a decision | [Install](https://www.ezjonline.com/resources/session-handoff) |
| [`session-close`](skills/session-close) | Checks what a Claude Code session actually got done | [Install](https://www.ezjonline.com/resources/session-close) |
| [`discount-codes`](skills/discount-codes) | Screenshot any checkout, get the discount codes that actually work | [Install](https://www.ezjonline.com/resources/discount-codes) |
| [`get-to-the-point`](skills/get-to-the-point) | Makes Claude answer first, in the fewest words | [Install](https://www.ezjonline.com/resources/get-to-the-point) |
| [`os-audit`](skills/os-audit) | Audits a Claude Code project for stale data, broken routing and bloat | [Install](https://www.ezjonline.com/resources/os-audit) |
| [`roast`](skills/roast) | Five personas pressure-test your idea, then one verdict: GO, RESHAPE or KILL | [Install](https://www.ezjonline.com/resources/roast) |
| [`ezj-handoff-doc`](skills/ezj-handoff-doc) | One-page handoff docs anyone can understand | [Install](https://www.ezjonline.com/resources/handoff-doc) |

More skills in their own repos: [Hormozi skill](https://github.com/ezjonline/hormozi-skill) · [Cold outreach skill](https://github.com/ezjonline/cold-outreach-skill)

### Install a skill

Paste this into Claude Code, swapping in the skill name:

```
Install the <skill-name> skill from https://github.com/ezjonline/ezj-automations/tree/main/skills/<skill-name> into ~/.claude/skills/<skill-name>, then confirm it is available.
```

## n8n templates

| Template | What it does |
|---|---|
| [`IG_Research_Agent_Demo.json`](n8n%20templates/IG_Research_Agent_Demo.json) | Finds the reels breaking out in your niche and turns them into hooks and ideas. [Guide](https://www.ezjonline.com/resources/ig-research-agent) |
| [`EZJ_GM_Lead_Scraper.json`](n8n%20templates/EZJ_GM_Lead_Scraper.json) | Scrapes Google Maps for local businesses, finds emails, researches them and writes the first email |
| [`Content_OS.json`](n8n%20templates/Content_OS.json) | YouTube research, an idea bot and posting, run through Notion and Slack |

Import in n8n with **Workflows → Import from file**, then add your own credentials. Every ID in these files is a `YOUR_...` placeholder.

## Prompts

- [Nano Banana Pro prompts](prompts/higgsfield-nano-banana-prompts.md)
- [Map your own AI OS](prompts/map-my-ai-os.md)
- [Build an Instagram Research Agent](prompts/build-ig-research-agent.md)

## Want it built for you?

[Book a free AI Audit](https://www.ezjonline.com/ai-audit). You leave with a plan for your business, whether or not we work together.

MIT licensed. Use anything here, in your business or your clients'.
