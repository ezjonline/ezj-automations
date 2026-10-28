---
name: branded-report
description: Turns facts, numbers and notes into a branded EZJ Online PDF report, the kind a client reads on their phone in two minutes. A one page project update, release notes, a campaign results report, a retrospective or postmortem, a status sheet. Claude writes a short JSON spec, the bundled renderer lays it out in the house look (black and orange, Figtree, the locked logo, stat tiles, funnels, tables, bar charts, cards, an asks box) and checks it for dashes, placeholders, overflow and a stranded last page. Use when someone says "make a branded report", "branded PDF", "make a PDF for <client>", "results report", "campaign report", "numbers report", "retrospective", "postmortem", "update sheet", "one pager for the client", "one pager update", "a quick one page update", "here's everything we changed", "here's what we're waiting on from you", "send the client a recap of the changes", or "/branded-report". Do not use for priced proposals (proposal-builder), AI audit reports on a web page (ai-audit-report), developer handoff docs (ezj-handoff-doc), invoices, live dashboards (dashboard) or slide decks.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Branded Report

Produces one PDF in the EZJ Online house look from a JSON spec you write. You decide what the report says and in what order. The renderer decides how it looks, so every report matches the last one: the dark or light header with the logo, stat tiles, funnels, tables, cards, the black "what we need from you" box, a running header and page numbers. The bar: the reader knows the result in ten seconds and what they need to do in thirty.

## When to use

- A client update after a round of work ("here's what's live, and what's next").
- Results of a campaign, an event, a month of ads: what went out, what came back, what we change.
- A retrospective or postmortem: what happened, what worked, what we missed and the fix.
- Release notes for an app or a site.

Not for: a priced proposal, an AI audit web page, a developer handoff doc, an invoice, a live dashboard, a deck. Those have their own skills.

## Inputs

**Find these yourself first:** the facts live in the repo, issue threads, exports, transcripts, notes and the tools you can reach. Read them before asking anyone anything.

**Ask the person for what you cannot reach, in ONE message, all at once:** exports you cannot pull (a platform report, a form export, a message log), who the report is for, and any number only they know. Never ask one question at a time.

## Process

### 1. Find the renderer

```bash
ls ~/.claude/skills/branded-report/scripts/render.sh
```

Every render below uses `bash ~/.claude/skills/branded-report/scripts/render.sh <spec.json>`. If the skill lives elsewhere, use that path. The first run builds a private Python setup with Playwright (about a minute, one time, it says so). If it says python3 is missing on a Mac, run `xcode-select --install` and try again.

### 2. Build the fact sheet, in the chat, before writing anything

List every number the report will use, each with where it came from and when it was pulled. Then check them:

- **Recompute every total yourself.** The parts must add up to the total. Rates are numerator over denominator, say both.
- **Keep one source per number.** If two sources disagree, pick one, and say which and why in the sources block.
- **Know what each number counts.** Sent is not delivered. Delivered is not opened. A click is not an RSVP. Unique people is not messages.
- **No estimates dressed as facts.** An estimate is labelled "about" or "estimated", or it stays out.

If a number you need is missing, ask for it (step "Inputs"), or leave that line out. Never fill a gap with a guess.

### 3. Pick the shape

| Report | Header | Pages | Shape, in order |
|---|---|---|---|
| Update sheet | `light` | 1 | Full width "Live now" card, two cards for what is finishing and what is dated, a dark card or `asks` box for what we need from them, a closing line |

**Update sheets: the "what we need from you" list comes from live status, not memory.** Before writing it, check where the client really is (their onboarding or intake progress, open questions in the latest email thread, assets they promised). Put the step that unblocks the most work first, with its link. Every item is one line they can act on.
| Release notes | `dark` | 1 | Numbered headings, each with 2 to 5 bullets, a `callout` for "how to get it" |
| Results, retrospective, postmortem | `dark` | 2 to 4 | `stats` row (3 or 4 tiles, the headline result as the `accent` tile), one `lead` sentence that states the result, `01` how it performed (a `funnel` per channel, `bars`), `02` every send (`table` with a total row), `03` what worked and what we change (two `cards`, Keep and Change), a `callout` for next time, `asks`, `sources` |

Start from the closest example and edit it, never from a blank file: `examples/campaign-retro.json` (results, two pages) and `examples/update.json` (update sheet, one page). Every block and every field is in `references/blocks.md`.

### 4. Write the spec

Save it next to the deliverable, in the client's folder, as `report.json` (or a clear name). Set `file_name` to what the client should see as the file name, for example `"Northside Fitness, Spring Open House Results"`. Set `date` to the day it goes out, written out (`October 27, 2026`).

### 5. Render

```bash
bash ~/.claude/skills/branded-report/scripts/render.sh path/to/report.json
```

It prints the PDF path, the page count, and `FAIL` or `WARN` lines. Exit 0 is clean. Exit 1 means a check failed: fix every `FAIL` in the JSON and render again. Exit 2 means the spec is broken (a missing field, a bad block type, a table row with the wrong number of cells): the message says exactly what. Add `--html` to also write the HTML for debugging, `--out <file.pdf>` to choose the path.

The checks: dashes used as punctuation, placeholders left in (TODO, TBD, `{{`), a block wider than the page, a last page holding a stranded line or two, the brand font failing to load.

### 6. Look at every page

Read the PDF with the Read tool (Claude Code shows each page as an image). Check, page by page:

- The result is readable at a glance on page 1, above the fold.
- No page except the last is mostly empty. A big gap above a heading means the next section did not fit: move a smaller block up, trim, or reorder.
- No heading sits alone at the bottom of a page (the renderer prevents it, still look).
- Every number on the page matches the fact sheet. Totals match their parts.
- Nothing is cut off, wraps awkwardly, or reads as a wall.

Fix and render again until a page by page look finds nothing. Never hand over a report you have not looked at.

### 7. Read it as the client

One pass in their shoes, with the rules below. Would they understand every line without us on a call? Does anything sound like an excuse? Is anything in there that should never leave the building (see "Never in a client report")?

### 8. Hand it over

Reply with the output format below. You do not send it. The person running you sends it.

## Writing rules

- **Lead with the result.** The title says the outcome or what is inside ("Your October campaigns, by the numbers"). The first sentence under the stats says the one thing that matters most.
- **Numbers over adjectives.** "412 RSVPs" beats "a great turnout". Put the number first.
- **Plain words, short sentences.** The reader is a business owner on a phone between meetings.
- **No dashes as punctuation.** Use commas and periods. Ranges are "10 to 12". The renderer fails the build on them.
- **Bullets are a bold lead and one sentence.** `"**Texts close fast.** 61% of text RSVPs came within an hour."`
- **Every rate names its base.** "39% opened (of emails delivered)", never a bare percentage.
- **Own misses in one line each, with the fix.** "We missed 600 members with no email topic set. That one is on us, it is fixed for summer." No blame on their team, no excuses, no paragraphs of context.
- **One accent word at most** in the title, with `==word==`.
- **Results reports end with a `sources` block** naming where each number came from and when it was pulled.

## Never in a client report

- What a contractor is paid, our margins, our cost to deliver.
- Developer names, internal tools, branches, scripts, retries, failed runs that never reached the client. Say "we".
- Another client's name or results.
- Personal data of the people on their lists: no names, phone numbers or emails, counts only. Their own staff can be named when it helps.
- Anything unverified presented as fact.

## Output format

- **The file:** `<file_name>.pdf` next to the spec, Letter size (A4 with `"page_size": "A4"`).
- **The reply in chat:** the PDF path, the page count, the three numbers that matter most, anything you could not verify or left out and why, and a send message in a fenced block (60 to 90 words, plain, in the voice of whoever sends it, no dashes) that says what the PDF is and the one thing to look at first.

## Example

Ask: "Make a results report for Northside Fitness's spring open house, the numbers are in these exports."

1. Fact sheet in chat: 3 emails and 2 texts, delivered counts per send from the platform reports, RSVPs from the form export with duplicates removed, 412 yes against a goal of 300. Totals recomputed: 18,940 + 6,102 = 25,042 delivered.
2. Shape: results, dark header, two pages.
3. Spec: `examples/campaign-retro.json` is exactly this report.
4. Render: `Pages: 2`, no FAIL lines. Page by page look: page 1 holds the stats, both funnels and the bar chart, page 2 the table, Keep and Change, next time, asks and sources.
5. Reply: the path, "2 pages", "412 RSVPs (goal 300), 25,042 messages delivered, $1.12 per RSVP", "door count not in yet, left out", and the send message.

## Hard rules

- Never send, upload or post the PDF yourself. You hand it to the person running you.
- Never invent, round up or "smooth" a number to tell a better story.
- Never hand-write HTML or CSS to get around the renderer, and never change colours, fonts or the logo for one report. The `brand` override exists only for a different company's brand.
- Never hand over a report with FAIL lines, and never use `--allow-dashes` on EZJ Online work.
- Never paste raw exports or contact lists into the spec. Counts only.
- Never skip the page by page look in step 6.
