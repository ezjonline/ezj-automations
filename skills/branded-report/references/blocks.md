# Report spec reference

A report is one JSON file. The renderer reads it, lays it out in the house look and checks it.

## Top level

```json
{
  "title": "Your spring open house, by the ==numbers==",
  "kicker": "Campaign results",
  "date": "May 2, 2026",
  "prepared_for": "Northside Fitness",
  "lede": "One or two sentences under the title.",
  "hero": "dark",
  "page_size": "Letter",
  "file_name": "Northside Fitness, Spring Open House Results",
  "closing": "Questions on any of this, message us. We go through it together on Tuesday.",
  "blocks": []
}
```

| Field | Required | What it does |
|---|---|---|
| `title` | yes | The big headline. `==word==` turns one word orange. Also the running header on pages 2 and up. |
| `blocks` | yes | The body, top to bottom. |
| `kicker` | no | Small orange caps above the title (dark header) or under the client name (light header). |
| `date` | no | Written out. Shown next to the kicker. |
| `prepared_for` | no | The client. "Prepared for X" in the dark header, top right in the light one, and in the running header. |
| `lede` | no | The line under the title. |
| `hero` | no | `dark` (default, full bleed black with an orange top edge) or `light` (logo left, client right, a rule). |
| `page_size` | no | `Letter` (default) or `A4`. |
| `file_name` | no | The PDF's name, without `.pdf`. Default: the title. |
| `closing` | no | A small muted last line. |
| `brand` | no | Only for a different company's brand. Keys from `assets/brand.json`: `name`, `website`, `accent`, `ink`, `paper`, `soft`, `font_family`, `font_file`, `logo_on_dark`, `logo_on_light`. File paths are relative to the spec. |

## Inline marks, in any text field

`**bold**`, `*italic*`, `==orange accent==`, `[link text](https://example.com)`. A line break is `\n`. Nothing else is parsed. HTML is shown as text.

## Blocks

Every block is an object with a `type`. A `heading` always travels to the next page together with the block under it.

### heading

```json
{ "type": "heading", "number": true, "text": "How people moved through it", "sub": "Optional muted line under the rule." }
```

`number: true` numbers sections 01, 02, 03 in order. A string (`"A"`) sets it by hand. Leave it out for no number.

### text

```json
{ "type": "text", "size": "lead", "text": "The open house beat its goal by **37%**." }
{ "type": "text", "paragraphs": ["First paragraph.", "Second paragraph."] }
```

`size`: `body` (default), `lead` (larger, for the one sentence that states the result), `small` (muted fine print).

### stats

```json
{ "type": "stats", "items": [
  { "value": "412", "label": "RSVPs", "note": "Goal was 300", "accent": true },
  { "value": "18,940", "label": "Emails delivered", "note": "3 sends" }
]}
```

Tiles in one row, 2 to 4 of them. `accent: true` makes the tile black with an orange number, use it once, for the headline result. `columns` overrides the count per row.

### cards

```json
{ "type": "cards", "columns": 2, "items": [
  { "tag": "Live now", "full": true, "title": "On your site", "bullets": ["**Bold lead.** Detail."] },
  { "tag": "Next", "tag_style": "ghost", "title": "Follow up texts", "text": "A paragraph instead of bullets." },
  { "tag": "What we need from you", "dark": true, "full": true, "numbered": true, "bullets": ["One", "Two"] }
]}
```

`tag` is the pill (orange, or grey with `tag_style: "ghost"`). `full: true` spans the whole row. `dark: true` is the black card. `numbered: true` turns bullets into orange numbered circles. A card takes `text`, `paragraphs`, `bullets` or a mix.

### bullets

```json
{ "type": "bullets", "items": ["**Lead.** Detail.", "Another."], "numbered": false }
```

### table

```json
{ "type": "table", "title": "Optional caption",
  "columns": ["Send", "Date", "Delivered", "Opened"],
  "rows": [["Email 1", "Apr 14", "6,402", "2,690"], ["Email 2", "Apr 21", "6,288", "2,391"],
           ["Email 3", "Apr 27", "6,250", "2,306"], ["Total", "", "18,940", "7,387"]],
  "total_row": true,
  "note": "Muted note under the table." }
```

Every row needs as many cells as `columns`. Cells are text, formatted the way you want them shown (`"15,896"`, `"39%"`, `"$1,290"`). Number columns right align on their own; set `"align": ["left", "left", "right", "right"]` to force it. `total_row: true` bolds the last row with a rule above. A table of 15 rows or fewer never splits across pages; longer ones split with the header repeated.

### bars

```json
{ "type": "bars", "title": "RSVPs by send", "items": [
  { "label": "Email 1", "value": 104 },
  { "label": "Email 2", "value": 77, "muted": true },
  { "label": "Last call", "value": 63, "display": "63 (9%)" }
]}
```

Horizontal bars, scaled to the largest value (or `max`). `value` is a number. `display` replaces the printed number. `muted: true` greys a bar, `ink: true` makes it black, so one or two can stand out.

### funnel

```json
{ "type": "funnel", "title": "Email", "steps": [
  { "label": "Delivered", "value": 18940 },
  { "label": "Opened", "value": 7387, "rate_label": "open rate" },
  { "label": "Clicked RSVP", "value": 902, "rate_label": "of opens" }
]}
```

Each step shows its count, a bar scaled to the first step, and its percentage of the step above with `rate_label` after it (default "of the step above"). Put two funnels side by side with `columns`.

### callout

```json
{ "type": "callout", "tone": "soft", "title": "Next time", "text": "One or two sentences.", "bullets": ["Optional"] }
```

`tone`: `soft` (cream with an orange edge, the default), `orange` (light orange box), `dark` (black).

### asks

```json
{ "type": "asks", "title": "What we need from you", "items": ["Pick the date", "Send the door count"] }
```

The black box with orange numbered circles. Two columns once there are 4 or more items, or set `columns`.

### steps

```json
{ "type": "steps", "items": [
  { "title": "Accept the invite", "text": "Open the link while signed in." },
  { "title": "Paste this prompt", "text": "It sets everything up.", "code": "Text shown in a dark box, copied as is." }
]}
```

### quote

```json
{ "type": "quote", "text": "We had people at the door asking for the trainer named in the text.", "who": "Dana, front desk" }
```

### code

```json
{ "type": "code", "label": "Paste this", "text": "Shown exactly as written, line breaks kept. Not checked for dashes." }
```

### image

```json
{ "type": "image", "path": "assets/flow.png", "caption": "How a lead moves", "width": 100 }
```

PNG, JPG, GIF, WebP or SVG, embedded in the PDF. `path` is relative to the spec. `width` is a percent of the column.

### columns

```json
{ "type": "columns", "widths": [1, 1], "columns": [
  [ { "type": "funnel", "title": "Email", "steps": [] } ],
  [ { "type": "funnel", "title": "Text", "steps": [] } ]
]}
```

Any blocks side by side. `widths` are proportions, `[2, 1]` makes the left column twice as wide.

### sources

```json
{ "type": "sources", "items": ["Emails: the email platform's campaign reports, pulled May 1.", "RSVPs: the form export, duplicates removed."] }
```

Small numbered fine print. Title defaults to "Where these numbers come from", set `title` to change it.

### page_break

```json
{ "type": "page_break" }
```

Starts the next block on a new page. Use it only when the page before is mostly full. Most reports need none.

## The checks

| Check | Result |
|---|---|
| An em dash, en dash, or a hyphen with spaces around it, in any text (code blocks and links excepted) | FAIL |
| TODO, TBD, FIXME, XXX, lorem ipsum, `{{ }}`, `[[ ]]`, PLACEHOLDER | FAIL |
| A block wider than the page | FAIL |
| The last page holds fewer than 300 characters | FAIL |
| The brand font did not load | WARN |
| A missing field, an unknown block, a table row with the wrong cell count, a missing image | Stops, exit 2 |
