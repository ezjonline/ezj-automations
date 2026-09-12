# Dashboard skill

A Claude Code skill that builds dashboards which do not look AI generated.

One self-contained HTML file. No React, no build toolchain, no chart library. Hand-rolled SVG charts, a token-driven design system you rebrand by editing four lines, and the states everyone skips: empty, stale, broken, zero.

![what it produces](https://raw.githubusercontent.com/ezjonline/ezj-automations/main/skills/dashboard/preview.png)

## Install

Drop the folder into your skills directory.

```bash
# for one project
mkdir -p .claude/skills
git clone --depth 1 https://github.com/ezjonline/ezj-automations /tmp/ezj-automations
cp -r /tmp/ezj-automations/skills/dashboard .claude/skills/

# or for every project on your machine
cp -r /tmp/ezj-automations/skills/dashboard ~/.claude/skills/
```

Restart Claude Code. Then just ask:

```
build me a dashboard for my Stripe revenue
turn this CSV into a client report
this dashboard looks generic, fix it
```

Or invoke it directly with `/dashboard`.

## What is in the box

| File | What it does |
|---|---|
| `SKILL.md` | The process. Interrogate the ask, design the data contract, build from tokens, build the states, verify. |
| `references/design-system.md` | Tokens, the color law, typography, depth, layout, states, motion, and an anti-slop checklist. |
| `references/charts.md` | Copy-paste SVG recipes: line, area, sparkline, donut, bars, in-cell bars, funnel, gauge, progress, plus hover and number formatting. |
| `references/architecture.md` | The build pipeline, the data contract, state without a framework, password gating with no backend, PDF export, scheduling. |
| `templates/dashboard.html` | A complete working dashboard. Copy it and gut it. |

## The opinions it holds

- One accent color. Status colors are a separate system and never borrow it.
- Deltas are colored by whether the change is **good**, not by whether it is positive. Churn falling is green.
- Every number gets `tabular-nums`. Gradient text on a number is banned.
- Empty states are sentences that explain the gap, never "No data."
- Zeros get shown, loudly. A paid channel reporting $0 is the most useful cell on the page.
- Data gets baked into the file at build time, so there is no loading state, no CORS, and no API key in the client.
- It will not invent data to fill a layout. Ever.

## Try it in 10 seconds

Open `templates/dashboard.html` in a browser. That is the output, running on a sample payload.

---

Built by [EZJ Online](https://ezjonline.com). If you want a system like this built for your business instead of building it yourself, [book a free AI Audit](https://cal.com/ethan-johnson-imoylp/ai-audit?utm_source=github&utm_medium=dashboard_skill&utm_campaign=dashboard).
