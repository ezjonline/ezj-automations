---
name: dashboard
description: Build a genuinely well designed data dashboard as a single self-contained HTML file, with hand-rolled SVG charts, a token-driven design system, real empty and stale states, and no framework or chart library. Use when someone asks for a dashboard, an analytics page, a KPI view, a client reporting page, a metrics overview, an internal ops screen, a "make this data look good" request, or says the current dashboard looks generic or AI generated. Do not use for a single standalone chart inside an existing app, for a marketing landing page, for a spreadsheet, or for a data pipeline with no visual output.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Dashboard

Builds a dashboard that looks like a designer made it and an engineer maintained it. One self-contained HTML file. Zero dependencies. Hand-rolled SVG charts. A token-driven design system you rebrand by editing four lines.

The output is not "a page with some charts on it." It is an instrument: every number earns its position, every color means something, every empty state tells the truth, and the thing still looks right on a phone.

## When to use

Use when the ask is a dashboard, analytics view, KPI page, client report, metrics overview, ops screen, or scoreboard. Also use when someone has a dashboard already and says it looks generic, templated, or AI generated.

Do not use for a single chart dropped into an existing app, a marketing page, a spreadsheet, or a data pipeline that has no visual output.

## Inputs

**Required, and stop and ask if missing:**

1. **The data.** A file, an API, a schema, or a realistic sample. Never invent numbers to fill a layout, not even as a placeholder. Fabricated data in a dashboard gets screenshotted and believed.
2. **The audience and the decision.** Who opens this, and what do they do differently after reading it? A dashboard with no decision attached is decoration.

**Optional, sensible defaults if not given:**

3. Brand colors and fonts. Default is the dark system in `references/design-system.md`.
4. Refresh cadence. Default is a build step run on a schedule.
5. Where it gets hosted. Default is a static file.

## Process

### 1. Interrogate the ask before building

Answer these in one short paragraph back to the user, then build. Do not turn this into an interview.

- What is the **one number** that belongs top left? There is always one.
- What are the 4 to 6 supporting KPIs?
- What is the **time comparison**? Every metric needs a prior period or it means nothing.
- What are the 2 to 4 breakdowns (by channel, client, campaign, stage)?
- What detail table do people scroll to when they want the receipts?
- What should they **do** about it? A closing "what's next" beats another chart.

If the user cannot name the decision, say so plainly and propose one. That conversation is worth more than any styling.

### 2. Design the data contract first

Write the JSON shape before any HTML. It is the actual spec, and it prevents the classic failure where the layout drives the data instead of the other way around.

Read `references/architecture.md` for the full contract and the rules that matter: money as integer cents, labels in the data not the template, deltas precomputed server side, and never summing unique counts across days.

### 3. Build the shell from tokens

Read `references/design-system.md`. Paste the `:root` token block first, then build everything from it. If you are writing a raw hex below that block, you have already lost the rebrand.

Copy `templates/dashboard.html` as the starting point. It is a working dashboard with the token system, the card, the KPI tile, the section shell, a line chart, a sparkline, a donut, a ranked bar list, a table, and the states, all wired to a sample payload.

### 4. Build the page in reading order

Header with the freshness stamp, KPI rail, hero trend, breakdowns, detail table, what's next. Top left is the most important number. If a section cannot justify its position, move it down or cut it.

### 5. Build the charts by hand

Read `references/charts.md`. Every chart is a pure function returning an SVG string. Pick the form from the table at the end of that file, then copy the recipe.

Put a one-line comment above each chart saying why that form. It is the cheapest quality signal in the file and it stops the next person swapping a considered donut for a pie.

### 6. Build the states, not just the happy path

This is the step that separates a real dashboard from a demo, and it is the step that gets skipped.

- **Empty:** a sentence that explains what is missing and how it gets filled. Never "No data."
- **Missing cell:** an em dash in muted ink. Never a blank, never a zero.
- **Broken upstream:** say the source failed. Never fabricate, never silently drop a section.
- **Impossible value:** refuse to print it. A conversion rate over 100% means the data is wrong.
- **Stale:** the freshness dot goes amber and stops pulsing. The label says "showing saved data."
- **Zero:** show it, loudly. A paid channel reporting $0 is the most decision-useful cell on the page.

### 7. Make it responsive and motion-safe

Two or three breakpoints. `min-width: 0` on every grid child. Wide tables either scroll inside their card or become stacked cards via `data-label`. Every animation gated behind `prefers-reduced-motion`.

### 8. Verify before calling it done

Run this checklist and report the result. Do not skip it and do not claim it passes without checking.

```
[ ] Opens correctly as a local file, double click, no server
[ ] Every number has font-variant-numeric: tabular-nums
[ ] Exactly one accent color; status colors are separate and semantic
[ ] Deltas colored by whether the change is GOOD, not by sign
[ ] No fabricated, placeholder, or lorem data anywhere
[ ] Empty, missing, stale, and error states all render correctly when forced
[ ] No horizontal scroll at 375px wide
[ ] Table readable on a phone
[ ] prefers-reduced-motion disables every animation
[ ] The freshness stamp is honest about when the data was pulled
[ ] Page title names the subject, not the word "Dashboard"
```

Force the states to check them. Blank the arrays, set a value to null, set the fetch to fail. A state you have not seen render is a state that does not work.

## Output

A single `.html` file that opens with a double click, plus, when the data is not static:

```
dashboard/
  build.py            fetch, normalize, render
  data/data.json      the contract, human readable, committed
  templates/
    dashboard.html    the template with a {{DATA_JSON}} placeholder
  dist/
    index.html        the built, self-contained output
```

Tell the user, in three lines: where the file is, how to rebuild it, and what is still faked or missing. Never report a dashboard as done while a section is running on invented numbers.

## Example

**Ask:** "Build me a dashboard for my agency's client retainers."

**The paragraph back:**

> One number top left: current MRR against the goal. Supporting KPIs: active retainers, new MRR this month, churned MRR, average retainer value, collection rate. Comparison is the prior month on every tile. Breakdowns: revenue by client (ranked bars, since 12 clients is too many for a donut), revenue by service line (donut, 4 categories, total in the hole), MRR movement over 12 months (area chart). Detail table: every client with status, retainer, start date, last payment. Closes with the three accounts at churn risk and why. Decision it drives: who to call this week.

**What gets built:** one `index.html`, dark tokens, a 5-tile KPI rail with sparklines and prior-month deltas, a hero area chart with crosshair hover resting on the peak, ranked bars with in-cell fills, a 4-slice donut, a paginated table with status chips, and a numbered "what's next" list. Churned MRR shows a green delta when it falls, because down is good there.

## Hard rules

- **Never invent data.** Not for a placeholder, not for a demo, not "just to show the layout." Ask for real or realistic sample data. If the user insists on a visual with no data, label it clearly as a mockup inside the page itself.
- **Never fake a state you have not tested.** Force every empty, stale and error path and look at it.
- **Never let a delta be colored by sign alone.** Pass the direction. Costs going up is not green.
- **Never use the accent color for status,** and never use status colors for decoration.
- **Never put a gradient on a number.** The single loudest AI-slop tell.
- **Never use emoji as UI icons.**
- **Never ship chart library defaults.** Theme every axis, grid, tooltip and legend, or hand-roll it.
- **Never add a dependency** without saying why a hand-rolled 15-line function would not do.
- **Never claim a dashboard is live** until the refresh loop has actually run end to end and been verified. Until then the label says "data through <date>."
- **Do not deploy or publish anything** without explicit approval from the person who asked. Building the file is not permission to put it on the internet.

## Reference files

| File | Read it when |
|---|---|
| `references/design-system.md` | Always, before writing any CSS. Tokens, color law, type, depth, layout, states, motion, and the anti-slop checklist. |
| `references/charts.md` | Before writing any chart. Copy-paste recipes for line, area, sparkline, donut, bars, funnel, gauge, progress, in-cell bars, plus hover and formatting. |
| `references/architecture.md` | Before wiring data. The build pipeline, the data contract, state without a framework, password gating, PDF export, scheduling. |
| `templates/dashboard.html` | Start here. A complete working dashboard to copy and gut. |
