---
name: proposal-builder
description: Turn a discovery or audit call transcript into a priced proposal as one self contained HTML page, built from the EZJ Online orange and black template (assets/ezj_template, true black and #F47C20, Montserrat and Figtree, an animated hero metric band with a visual per number, proof before price, hand built SVG diagrams of their bottleneck and the proposed system, a 90 day roadmap quoting them verbatim, anchor plus recommended pricing cards, a guarantee). Switches to the prospect's own brand skin only when Ethan explicitly asks for the page in the client's branding. Built for the follow up call where the page gets screen shared. Use when you are asked to "build the proposal for <name>", "make the proposal page", "priced follow up for <name>", "pitch proposal for <name>", "retainer proposal for <name>", "/proposal-builder", or after any call where a priced pitch is the next step. Do not use for a free no price audit report, for a thin technical quote with no transcript, or for a plain text quote in an email.
---

# Proposal Builder (EZJ Online orange and black, priced)

One self contained HTML page per prospect, built from one template, pitched live on the
follow up call while Ethan screen shares.

**You build the page. You never publish it, never create a payment link, and never send it
to the prospect.** You save it as `<client-slug>.html` and send it to Ethan with a handoff
note. He deploys it and wires the payments.

## The design standard

Every proposal starts from one template in EZJ Online's own branding. Ethan, on the proposal
this template came from:

> "I love the underlined bits. Everything that's the accent colour. If it's just my orange,
> and then no more grays, but nice black and cool gradients between the two, that's a great
> template for a proposal. That needs to be every proposal moving forward."

> "The only feedback I do have is the numbers in the banner could be a little sicker, more
> visual, a little cleaner."

| File | What it is |
|---|---|
| `assets/ezj_template/index.html` | The template. Every client string is a `{{TOKEN}}`, every section opens with a comment giving its rules, and all colours and fonts live in one `:root` block. |
| `assets/ezj_template_pattern.md` | The spec. **Read it in full before building.** Section order, palette and gradient rules, fonts, metric band patterns, pricing card rules, OG recipe, QA. |
| `assets/example_filled_proposal.html` | A filled reference in this exact markup. Every name and number in it is invented. Keep it open beside the template and copy its shape, never its content. |
| `assets/logo.txt` | The EZJ mark as one line of base64. Paste it into every `{{LOGO_EMBED}}` so the page carries its own logo. |
| `assets/fonts.css` | Montserrat and Figtree embedded as base64. Only needed if the page has to render with no internet. |

**Two skins, one page.**

- **EZJ skin, the default, every time.** EZJ mark, true black `#0d0d0d`, orange `#F47C20`,
  white and off white grounds, no greys, Montserrat headings, Figtree body. Orange only
  linear gradients, a thin orange top edge with a tight glow on black blocks (wide orange
  glows read brown), never a linear black to orange fade (it passes through brown, and it has
  been rejected twice).
- **Client brand skin, only when Ethan explicitly asks for the page in the client's own
  branding.** Same template: swap the `:root` block (the commented block in the template is
  the worked example) and the Google Fonts link, and put their logo in the bar. Spec section
  11 has the whole swap.

## The two path idea (read before drafting anything)

Every audit lead gets two paths. Path A, do it yourself: the off the shelf tools and quick
wins, free, take it or leave it. Path B, done for you: the custom systems EZJ Online would
build, priced.

If a free no price report already went out, it owns Path A in full. This page does not
re litigate it. Acknowledge it in one line, point back to the report they already have, and
spend the whole page on Path B, because that is what a follow up call pitch is for.

Whether a lead gets Path B pitched at all is Ethan's read of the call, not automatic. Some
audit calls are pure free value with no pitch. Ask him if it is not obvious. A retainer
follow on for an existing client skips Path A entirely and leads with the systems already
live.

## What you need before you start

- The prospect's call transcript. Not notes about it, the transcript.
- Anything already known about them: their site, the intake form, the CRM row, the free
  report if one went out.
- Real data on their business if the page needs a finding. See step 4.
- Ethan available for one round of questions. Step 3 does not proceed without him.

You do not need any accounts, keys or logins. Everything this skill produces is a file.

## Process

### 1. Read the source material

The transcript in full. Pull real facts: pain quotes (verify who actually said each one
against the transcript's own speaker tags, never paraphrase from memory), revenue and budget
signals, numbers they stated, what they have tried before, and what a past contractor or
agency got wrong for them if they said so. That last one is usually the strongest guarantee
material on the page.

Write the facts down before you write any copy. Every number on the finished page has to
trace back to this list or to Ethan's answer in step 3.

### 2. Shape the offer before you price it

If the `hormozi` skill is installed, invoke it (mode: audit or diagnose) with the transcript
facts and the pieces you are about to propose. If it is not, answer these four questions
yourself, in writing, before you draft a word:

- Is the dream outcome the actual destination (money, time, status) or just an activity
  metric? Push past "more leads booked" to what that means for them.
- What is the single clearest reframe, in their own words? "You do not have an X problem, you
  have a Y problem."
- Does this need a guarantee, and which one? If they named a specific fear about a past
  agency, that fear is the guarantee to write.
- Is the scope sequenced, one constraint fixed at a time, with everything else pushed to an
  explicit unpriced Phase 2? Not everything crammed into Phase 1.

### 3. Run the pricing lock with Ethan (THE APPROVAL GATE)

One round of questions, four at most. Cover:

1. Offer shape. What is actually in Phase 1 and what is deferred.
2. The price for each tier. Two tiers is the default: the anchor plus the recommended start.
3. What is in each tier's feature list.
4. Whether a guarantee applies, and what it says.

Bring recommendations from step 2 into this. Do not ask Ethan to invent numbers cold, give
him a proposal to accept or correct.

**You never invent a price and you never soften one.** Every dollar figure on the page is a
number Ethan said in this step, repeated exactly.

**If a tier carries a recurring monthly fee, its scope must be explicit** on the page itself,
both in the plan card's include list and in the terms table: the monthly fee covers hosting,
uptime and small fixes, never new builds or new features. New builds get scoped and quoted
separately, every time. The one exception is a build retainer where the monthly fee openly
buys new builds at a stated pace, and then the 90 day roadmap names every build it buys.

### 4. Write the page from the template

The page is a **self contained `index.html`**: inline CSS, inline SVG, one small script, the
logo embedded as one line of base64. Start from the template, never from a blank file:

```bash
D=~/proposals/<client-slug>
mkdir -p "$D"
cp assets/ezj_template/index.html "$D/<client-slug>.html"
```

Fill every `{{TOKEN}}` in place, following the comment at the top of each section and the
spec. Paste the single line inside `assets/logo.txt` into every `{{LOGO_EMBED}}`. Delete
the commented client skin block on an EZJ skin page, and delete any section with no real
material rather than padding it. Then prove nothing is left:

```bash
grep -o '{{[A-Z0-9_]*}}' "$D/<client-slug>.html" | sort -u
```

That should print only the six placeholders Ethan fills on deploy: `{{PAGE_URL}}`,
`{{OG_IMAGE_URL}}`, `{{PLAN_A_MONTHLY_URL}}`, `{{PLAN_A_UPFRONT_URL}}`,
`{{PLAN_B_MONTHLY_URL}}`, `{{PLAN_B_UPFRONT_URL}}`. Nothing else.

Non negotiables, with the detail in `assets/ezj_template_pattern.md`:

- **Hero metric band, exactly four numbers**, taken from the call's key takeaways, not prose.
  Each tile gets the visual that encodes its number: **pips** for a small count, **ring** for
  a time against a clock, **stair** for steps in a process, **meter** for a share of a whole
  (spec section 6). The final value sits in the HTML and the count up only animates it, so
  the band reads with JavaScript off and with reduced motion on.
- **Proof before price.** A real finding about their own business, produced by the thing you
  are selling. For an existing client, the systems already live and what they did. Three stat
  cards with one inverted to black carrying the bad news, and a verdict bar underneath. If
  there is no real data on the prospect yet, get it. A day's delay is worth more than a
  proposal without this section.
- **Two hand built inline SVG diagrams.** Today: white nodes with the bottleneck as the black
  block with the orange outline, labelled with what it costs them. Proposed: inputs, into the
  black agent or developer block, into outputs, into impact. Colours come only from the `dg-*`
  classes, never a hex value inside SVG, so a skin swap recolours them. Literal characters
  inside SVG, never HTML entities, and validate the XML before you ship.
- **Deliberately not included**, eight to twelve chips that fill orange on hover. This bounds
  the scope and it proves you listened.
- **Investment as separate cards with gaps.** Anchor plan first, recommended plan second with
  the orange border and the orange badge, a monthly button and an upfront button on each, and
  third party costs as the dashed low contrast row so they never read as our fee. Quote the
  measured cost of those tools, never a padded guess.
- **The 90 day roadmap** whenever there is a monthly fee, one card per month, each carrying a
  verbatim quote from the call attributed by first name and date. A retainer objection gets
  answered by naming what ships, not by adjectives.
- Every number traceable to the transcript or the step 3 lock. No dashes as punctuation.

### 5. Leave the payment links as placeholders

**You never create a payment link.** Not a Stripe link, not a bank link, nothing. You do not
have access and you do not need it.

Leave `{{PLAN_A_MONTHLY_URL}}`, `{{PLAN_A_UPFRONT_URL}}`, `{{PLAN_B_MONTHLY_URL}}` and
`{{PLAN_B_UPFRONT_URL}}` exactly as they are in the file. The button label above each one
already carries the exact amount, which is what Ethan needs to wire it.

Then list all four in the handoff note (step 9), each with its plan name and its exact price.
A one off build with a single plan keeps one button and one placeholder.

### 6. Make the social share image

Never skip this. A proposal link with a blank preview card undoes the whole impression, and
these get forwarded into group chats.

A 1200x630 HTML composite, no AI image tool: black `#0d0d0d` ground, a soft orange glow
behind an abstract orange SVG (lines converging into an orange node), the EZJ mark top left
with the offer name, the hero headline as three uppercase Montserrat 900 lines with the
payoff line in orange, and three of the metrics from the band. The full HTML is in spec
section 10.

```bash
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$C" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=4000 \
  --window-size=1200,630 --screenshot="$D/og.png" "file://$D/og.html"
sips -s format jpeg -s formatOptions 90 "$D/og.png" --out "$D/<client-slug>-og.jpg"
```

**Open the JPG and look at it before you send it.** Check for brown tones, a missing mark, a
clipped headline. Shorten the copy before you shrink the type.

### 7. Check the page stands on its own

The finished file has to open correctly from a double click, from an email attachment and
from a Slack file, with nothing beside it. Confirm:

- Every `{{LOGO_EMBED}}` is filled with the line from `logo.txt`, so the mark shows in the
  top bar, the footer and the browser tab.
- No `src` or `href` points at a file on your computer.
- The only thing it loads from the internet is the Google Fonts link. If the page has to work
  with no internet, inline `assets/fonts.css` into the `<style>` block in place of that link.

### 8. QA before you hand it over (do not skip)

Run the full QA in `assets/ezj_template_pattern.md` section 12. Every command is there. In
short:

1. **Desktop at 1200 wide** with `--virtual-time-budget=6000`, so the fonts load and the band
   count up finishes before the screenshot. Cut the tall PNG into 1200x1400 crops and read
   every one. A 10,000 pixel image read whole is too small to judge.
2. **Mobile at a true 390px.** Headless Chrome will not open a window under 500px wide, so
   `--window-size=390,...` silently renders a 500px layout. Load the page in a 390 wide iframe
   inside a 500px window with a 12000 budget, crop it with PIL, and read it.
3. **Look for** brown haze on black, grey leftovers, a broken logo, cramped band tiles, a
   highlight bar that misses its line, card text that overflows.

Then the mechanical checks (spec section 12 runs them in one script):

- **SVG is well formed XML.** An "undefined entity" error means an HTML entity leaked into a
  diagram.
- **The script parses.** `node --check` on the last `<script>` block. A syntax error there
  leaves half the page invisible.
- **No leftover tokens** beyond the six placeholders, zero em dashes and en dashes, no spaced
  hyphens.
- **No greys on the EZJ skin.** Every hex value on the page is in the spec section 2 palette.
  Muted text and hairlines are black or white at reduced opacity.
- **No linear black to orange gradient**, and no `invert(` filter on any logo.
- Every dollar amount matches the step 3 lock exactly, in the plan card, the button label,
  the terms table and the sticky bar.
- Hero copy and the metric band agree with each other. On one build the hero said "Or 22"
  while the band said "25+", and Ethan caught it before the model did.

### 9. Save it and hand it to Ethan

Save the finished page as `<client-slug>.html` and send it to Ethan. He deploys it.

Send `<client-slug>-og.jpg` with it, and a plain text **handoff note**:

```
PROPOSAL: <Client name>, <offer name>
File: <client-slug>.html   Social card: <client-slug>-og.jpg

PLACEHOLDERS FOR YOU TO FILL
  {{PAGE_URL}}               the live URL once it is up
  {{OG_IMAGE_URL}}           the live URL of the social card
  {{PLAN_A_MONTHLY_URL}}     <Plan A name>, $X per month
  {{PLAN_A_UPFRONT_URL}}     <Plan A name>, $Y for 3 months upfront
  {{PLAN_B_MONTHLY_URL}}     <Plan B name>, $X per month
  {{PLAN_B_UPFRONT_URL}}     <Plan B name>, $Y for 3 months upfront

EVERY PRICE ON THE PAGE
  <list each one, so you can check them against what you locked>

WHAT I WAS NOT SURE ABOUT
  <anything you guessed, or left out for lack of material. Say so plainly.>
```

### 10. Draft the message, never send it

Draft a short message (WhatsApp or email, whichever that relationship uses) inviting them to
the follow up call where Ethan pitches this live, or, if the call is already booked, a light
touch confirming it.

**Do not put the proposal link in the draft.** The page gets pitched live over screen share,
not sent ahead, unless Ethan explicitly says otherwise.

Hand Ethan the file, the handoff note and the draft. **He sends. You never send the proposal,
the message, or book the call.**

## What you hand back

1. `<client-slug>.html` and `<client-slug>-og.jpg`.
2. The handoff note.
3. The copy paste ready send draft.
4. One line on the thinking: the reframe you used, the guarantee, and whether anything got
   deferred to Phase 2 and why.

## Worked example (illustrative, invented)

Brightline Media, a small video agency, already had two systems from EZJ Online live in their
Slack: **Atlas**, a bot that writes each client's monthly shot list into a Google Doc, and
**Echo**, an SMS assistant that follows up with sales leads who did not close. On the call the
three founders each named the build that would take the most off their plate, and one of them
said builds waiting two to three weeks was the real blocker.

**Metric band:** `9` client channels already running Atlas, `< 20 min` from asking Atlas to an
approved shot list, `10 steps` to book one contractor today, `2 hrs` a manager sits stuck
waiting on a login code. Four different visual patterns: pips, ring, stair, meter.

**Proof before price:** Atlas and Echo, live in their Slack on their real clients. Three stat
cards, with the ten step booking process as the black bad news card. Verdict: "the systems
work. The bottleneck now is how fast the next ones ship."

**Diagrams:** the wish list waiting on a shared developer, then Monday priorities into one
dedicated developer into three shipped systems into hours back for the team.

**Pricing:** the bigger plan first as the anchor, the recommended start second with the orange
border, four payment link placeholders, a 3 month minimum, third party costs in the dashed
row. **Guarantee:** miss a committed ship date because of us, and that week comes off the next
invoice.

The full page is `assets/example_filled_proposal.html`. Every name and number in it is made
up. Copy its structure, its section order and its voice. Never its content.

## Hard rules, never do

- **Never create a payment link.** Leave the placeholders and list them in the handoff note.
- **Never deploy or publish the page.** You save a file and send it to Ethan. He deploys.
- **Never send the proposal, the draft message, or book a call.** Ethan does all three.
- **Never put a price on the page that Ethan did not confirm** in step 3.
- **Never invent a pain point, a quote or a number.** Every figure traces to the transcript or
  the step 3 lock. Check quote attribution against the transcript's own speaker tags. A
  misattributed quote has already shipped once.
- **Never start from a blank file.** Start from `assets/ezj_template/index.html`.
- **Never ship the client brand skin unless Ethan explicitly asked for their branding.**
- **Never ship greys on the EZJ skin.** No `#5c5c5c`, `#8c8c8c`, warm taupes or cream
  surfaces. Muted text and hairlines are black or white at reduced opacity.
- **Never use a linear black to orange gradient.** It passes through brown. Linear gradients
  are orange only, glows are radial, compact, and sit on solid black under a visible orange
  source.
- **Never ship a page with a leftover `{{TOKEN}}`** other than the six handoff placeholders.
- **Never let the metric band depend on JavaScript.** Final values live in the HTML, the count
  up respects `prefers-reduced-motion`, and the band fits a 2 by 2 grid at 390px.
- **Never ship a font we do not have rights to.** Substitute the closest free face and say
  nothing about it.
- **Never invert a logo to a white silhouette**, ours or theirs. The EZJ mark reads in full
  colour on white and on black.
- **Never use an HTML entity or a hex colour inside inline SVG.** Literal characters, `dg-*`
  classes for colour, and validate the XML.
- **Never inflate a third party tool or hosting cost.** Quote the measured number. Buyers who
  run their own dev shops will know, and the honest figure is the stronger one.
- **Never trust a `--window-size` under 500 for a mobile check.** Use the 390 iframe.
- **Never use a dash as punctuation** anywhere on the page or in the draft message.
- **Never hand it over without the step 8 QA pass**, including the SVG and script checks.
- **Never present the page top to bottom on a call.** That is Ethan's job and he demos first,
  then scrolls to the investment cards when they ask the price. Under three minutes on the
  page. Everything above the price is for the person reading it alone afterwards.
