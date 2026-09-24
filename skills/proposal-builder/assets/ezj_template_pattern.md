# The EZJ Online proposal template (house standard)

Ethan, on the proposal this template came from:

> "I love the underlined bits. Everything that's the accent colour. If it's just my orange,
> and then no more grays, but nice black and cool gradients between the two, that's a great
> template for a proposal. That needs to be every proposal moving forward."

> "The only feedback I do have is the numbers in the banner could be a little sicker, more
> visual, a little cleaner."

This file is the spec for that template. Read it in full before building a proposal.

| File | Role |
|---|---|
| `ezj_template/index.html` | The template. `{{TOKENS}}` for every client string, a rules comment at the top of every section, one `:root` block for every colour and font. |
| `example_filled_proposal.html` | The filled reference. Same page, filled in. Every name and number in it is made up, so copy its shape and its voice, never its content. |
| `logo.txt` | The EZJ mark as one line of base64. Paste it into `{{LOGO_EMBED}}` so the page carries its own logo. |
| `fonts.css` | Montserrat and Figtree embedded as base64. Only needed if the page must render with no internet. |

**Default skin is EZJ's own brand, every time.** The client brand skin (§11) is used only
when Ethan explicitly asks for a page in the client's branding.

**You never deploy and you never create a payment link.** The finished page is one HTML file
you save and send to Ethan. He deploys it and wires the payments. See §13.

---

## 1. The build in one screen

```bash
# from inside this skill's folder
D=~/proposals/<client-slug>          # any working folder you like
mkdir -p "$D"
cp assets/ezj_template/index.html "$D/<client-slug>.html"
```

1. Fill every `{{TOKEN}}` section by section, following each section's comment.
2. Paste the one line inside `assets/logo.txt` into every `{{LOGO_EMBED}}`. The page then
   carries its own logo and needs no image files beside it.
3. Delete the commented client skin block in `:root` and every section with no real material.
4. `grep -o '{{[A-Z0-9_]*}}' "$D/<client-slug>.html" | sort -u` prints nothing except the
   five placeholders Ethan fills on deploy: `{{PAGE_URL}}`, `{{OG_IMAGE_URL}}` and the four
   `{{PLAN_*_URL}}` payment links.
5. Build the OG card (§10) and save it as `<client-slug>-og.jpg` beside the page.
6. Run the QA (§12). Read every screenshot.
7. Save and hand off (§13). You do not deploy.

---

## 2. Palette and gradient rules (EZJ skin)

Every colour on the page is one of these tokens. Nothing else gets a hex value.

| Token | Value | Use |
|---|---|---|
| `--dark` | `#0d0d0d` | Every dark block: band, proof header, verdict, bad news card, large size card, guarantee, footer, black button, sticky bar. True black, never a warm near black. |
| `--dark-deep` | `#000000` | Hover on black buttons. |
| `--dark-rgb` | `13,13,13` | Shadows and the sticky bar alpha. |
| `--accent` | `#F47C20` | EZJ orange. Hover borders, the recommended plan border, diagram hot lines, numbers and labels on black. |
| `--accent-dk` / `--accent-lt` | `#e8680f` / `#ff8f3a` | Gradient ends. |
| `--accent-rgb` / `--accent-lt-rgb` | `244,124,32` / `255,143,58` | Glows and orange shadows. |
| `--accent-ink` | `#c2560a` | Small orange text on light grounds (kicker, eyebrows, pick labels, size and save pills). `#F47C20` on white is under 3:1 at 12px; `#c2560a` is 4.5:1. |
| `--accent-tint` | `#fff1e5` | Pale orange notes, pills, tinted diagram boxes. |
| `--ground` | `#f7f7f5` | Page ground, a clean off white. |
| `--card` / `--card-2` | `#ffffff` / `#fbfbfa` | Cards / inner cards, alternating term rows, the not included box. |
| `--ink` | `#0d0d0d` | Text on light. |
| `--muted` / `--dim` | `rgba(13,13,13,.7)` / `rgba(13,13,13,.54)` | Body copy / labels, cites, the third party row. |
| `--line` / `--line-2` | `rgba(13,13,13,.16)` / `rgba(13,13,13,.09)` | Outlines and dashed rows / card borders and dividers. |
| `--on-dark` / `--on-dark-muted` / `--on-dark-dim` | `#fff` / `rgba(255,255,255,.76)` / `rgba(255,255,255,.52)` | Text on black. |
| `--on-accent` | `#0d0d0d` | Text on orange buttons and pills. |
| `--grad` | `linear-gradient(95deg, dk 0%, accent 55%, lt 100%)` | Primary buttons, the hero underline bar, month pills, the recommended badge, list dots, gradient numerals, the 2px top edge of every dark block. |
| `--glow-top` | compact radial, `lt` at .32, 50% by 72px from the top edge | The spill under the top edge of dark blocks. |
| `--glow-band` | compact radial, `lt` at .42 to .1 to 0, 460 by 120px | The spill under the band's top edge. |

The only hex values allowed in a filled EZJ skin page:
`#0d0d0d #000000 #f47c20 #ff8f3a #e8680f #c2560a #fff1e5 #f7f7f5 #fbfbfa #ffffff`.

**Gradient rules, learned the hard way:**
- **Linear gradients are orange only**, `#e8680f` to `#F47C20` to `#ff8f3a`. Never a linear
  black to orange fade: the sRGB blend passes through brown, and EZJ rejected that on
  2026-09-11 and again in this template's brief.
- **Glows are radial, compact, and always sit under a visible orange source** (a 2px orange
  top edge, a bright node). Then the falloff reads as light. A wide faint glow with no
  source reads as a brown stain: on 2026-09-15 a 70% by 160% corner glow at .26 and a wide
  ambient glow at .13 both looked brown on black in side by side renders, while the top
  edge plus a tight spill read as clean orange light. The recipe for any dark block is
  `background: var(--grad) 0 0/100% 2px no-repeat, var(--glow-top), var(--dark)`.
- Everywhere a page would reach for a second colour (underlines, highlights, buttons,
  accents, the featured plan, tags), the template uses orange.
- **No greys and no warm taupes** as surfaces or borders. Muted text and hairlines are black
  or white at reduced opacity.
- **No red.** The bad news stat card inverts to black with an orange gradient numeral, and
  the diagram bottleneck is the black block with a 2px orange outline.

---

## 3. Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
```

- **Montserrat** (EZJ brand guideline) for all display type. Headings 900, uppercase,
  tracking `-0.03em` (`--disp-weight`, `--disp-track`). Card, month and plan titles 900 at
  `-0.02em`. Montserrat is wide, so headline sizes run about 10% under a condensed face.
- Small uppercase labels (kicker, eyebrows, cites, pills, buttons) Montserrat 700 to 800
  with positive tracking, `.08em` to `.16em`.
- **Figtree** (approved on EZJ's live site, 2026-09-13) for body, leads, list items and band
  labels. Band numerals use `font-variant-numeric: tabular-nums` so the count up never jitters.

---

## 4. Section order (this order, every time)

| # | Section | Hooks | Must contain |
|---|---|---|---|
| 1 | Top bar | `.bar` | EZJ mark (38px) and the EZJ ONLINE wordmark, a hairline, the offer name, the date on the right. The client's name is never a logo here, it goes in the kicker. |
| 2 | Hero | `.hero`, `h1 em` | Kicker "Prepared for <names>", a three or four line uppercase H1 with the payoff lines wrapped in `<em>` (the orange underline bar), one sub sentence opening with the proof in bold, two buttons: the plans, and the first section worth reading. |
| 3 | Metric band | `.band`, `.tile` | Exactly four numbers from the Fathom Key Takeaways, each with a visual (§6). |
| 4 | Proof before price | `.proof`, `.find`, `.verdict` | Black header (context line and title), two context rows, three stat cards with one `.find.alert` carrying the bad news, the verdict bar, an optional "To be clear" tint note, one verbatim quote. |
| 5 | Today diagram | `svg.diag` | Their current path with the bottleneck as the black block (§8), then a verbatim quote. |
| 6 | Proposed system diagram | `svg.diag` | Inputs to the black agent or developer block to outputs to impact. |
| 7 | Where it starts | `.cards` | Three cards: whose pick, the system named as an outcome, what it does, a verbatim quote. Cards invert to black on hover. |
| 8 | The first 90 days | `.mon`, `.note-band` | One card per month: month pill, whose ask, title, items with size pills, verbatim quotes. A black note band closes it. Only when there is a monthly fee. |
| 9 | How we work | `.facts`, `.sizes` | Four numbered facts, then build size cards with the largest inverted to black. |
| 10 | Deliberately not included | `.out`, `.chip` | Eight to twelve chips that fill orange on hover, one bold closing line. |
| 11 | Investment | `.plans`, `.both`, `.muted-row`, `.guar` | §7. |
| 12 | Terms in plain English | `.agr`, `.arow` | Key and value rows, every price repeated exactly. |
| 13 | What happens next | `.steps` | Three or four numbered steps, then two buttons back to the plans. |
| 14 | Footer | `footer` | EZJ mark, wordmark, "Prepared by EZJ Online". |
| 15 | Sticky bar | `.sticky` | Appears after 640px of scroll, hides over the plans, mirrors the recommended price. |

- **New AI Audit prospect, nothing live yet:** section 4 carries a real finding about their
  business produced by the thing you are selling: run the tool on their own account and show
  what it found. No real data means the page is not ready. Get the data.
- **One-off build with no monthly fee:** delete section 8 and the size cards, and use one plan card.
- Delete any section with no real material. Never pad.

---

## 5. Copy rules

- No dashes as punctuation anywhere, visible text or meta tags. Use "to" for ranges.
- Banned: delve, leverage, utilize, robust, seamless, streamline, optimize, enhance,
  comprehensive, empower, elevate, unleash, navigate, landscape, crucial, pivotal, holistic.
- Every quote verbatim from the transcript, attributed by first name and date, speaker
  checked against the transcript tags.
- Every number traces to the transcript or EZJ's pricing lock. The hero, the band, the proof
  cards and the terms must agree with each other.
- Systems are named as outcomes ("Videographer contract flow"), never as mechanisms.

---

## 6. The hero metric band

**Layout.** Four tiles on solid black with the orange top edge and `--glow-band` spill.
Thin orange hairline dividers (`rgba(accent, .34)`) between tiles. At 760px and below it
becomes a 2 by 2 grid with a hairline cross, and it must not scroll horizontally at 390px.

**Each tile**, top to bottom:
1. The visual, an inline SVG 44px tall (36px on mobile), `aria-hidden`.
2. The numeral: Montserrat 900, 58px (44px on mobile), filled with the orange gradient,
   an optional small prefix (`<`, `~`, `+`) and a white uppercase unit (`min`, `steps`, `hrs`).
3. The label, Figtree 14.5px, white at .76, the exact wording from the takeaways.

**Markup rules.**
- The full value is in a screen reader span (`<span class="sr">&lt; 20 min</span>`) and the
  visual numeral is `aria-hidden`, so the count up never gets announced digit by digit.
- The count up target is `<b data-to="20">20</b>`. The final value is always in the HTML.
  The script sets it to 0 and counts up over 1.1s with an ease out when the band is 30%
  visible, and skips everything under `prefers-reduced-motion` or without
  IntersectionObserver. Integers only. For a decimal ("2.5x") leave `data-to` off and the
  number simply shows.
- Visual animation is CSS: the script adds `.pre` (start state) then `.go` (transitions).
  Without JS the visuals render in their final state.
- Shared `<defs>` (`#vzGrad`, `#vzGlow`) live in one hidden SVG at the top of `<body>`. Never
  `display:none` it, or the gradient and glow vanish.

**The four visual patterns.** Pick by the kind of number, not by looks.

| Pattern | Use for | Examples | How to set it |
|---|---|---|---|
| **Pips** | A small count of things, 2 to 12 | "9 client channels", "4 locations", "3 of 5 live" | One `circle.pip` per item, `r=5`, `cx = 6 + 13i`, viewBox width `13N minus 2` (9 pips is 116). Lit pips `class="pip"`, the rest of a total `class="pip off"`. `--i` is the stagger index. |
| **Ring** | A time or duration against a clock | "< 20 min", "48 hrs", "in 15 minutes" | Dial is 60 for minutes, 24 for hours, 7 for days. Set `--off` to 100 minus the percent of the dial and `--deg` to percent times 3.6deg. 20 of 60 is `--off:66.67` and `--deg:120deg`. |
| **Stair** | Steps in a process, handoffs, a manual chain | "10 steps", "6 handoffs" | `M2 40` then N treads `h(112/N)` joined by N minus 1 risers `v(-32.4/(N-1))`. One `stair-node` at the end of each tread, the last one is the bigger `stair-end`. 10 steps is tread 11.2, riser 3.6. |
| **Meter** | A share of a whole, time lost out of a day, a before and after | "2 hrs" of an 8 hour day, "80%", "13 to 25 accounts" | Track 116 wide. Fill `width = 116 x share`, knob `cx` at the fill end. Ticks: 9 for an 8 hour day, 5 for quarters, 11 for tenths. Before and after: fill to the after value, name the before in the label. |

Avoid two tiles with the same pattern unless the two numbers really are the same kind.

---

## 7. Pricing card rules

- **Two plans side by side**, stacked under 820px. **Anchor plan first** (the bigger plan,
  plain card, black monthly button `.btn.ink`). **Recommended plan second**: `.plan.rec`
  with the 2px orange border and orange shadow, the `.ptag.accent` badge ("Recommended
  start"), and the orange gradient monthly button.
- Each card: tag, plan name, big price and unit, the upfront alternative with a `save $X`
  pill, an include list of real deliverables with the differentiator in bold, then two
  full width stacked buttons, **monthly** ("Start monthly · $X") and **upfront**
  ("3 months upfront · $Y", outline). The amount on each button matches the price above it.
  One payment link per button.
- A **"Both plans" row** under the cards: minimum term and notice.
- **Third party costs row**, `.muted-row`: transparent ground, 1.5px dashed `--line` border,
  every piece of text in `--dim`, no grey fill, heading "Third party costs · not our fee",
  right side "Billed direct" or the real measured number. It must never read as our fee.
- **The guarantee** sits right under pricing on black, the second half of its heading in
  gradient orange.
- **One-off build:** a single plan card, Stripe first and Wise as the alt, no save pill.
- The **sticky bar** shows the recommended plan's price and links to both plans.

---

## 8. Diagrams

- Hand-built inline SVG, `class="diag"`, `viewBox="0 0 980 300"` (or 360 for a taller
  system), width 100%. Text in Figtree 11 to 17px via attributes.
- **Colour only through classes**, never hex in SVG attributes, so the skin swap recolours
  them: `dg-card`, `dg-back1`, `dg-back2`, `dg-t` (title), `dg-s` (sub), `dg-arrow` and
  `dg-ah` (neutral arrow and head), `dg-hot` and `dg-ah-hot` (orange), `dg-block` (black),
  `dg-block-line` (orange outline), `dg-cap` (orange column caption), `dg-on-dark`,
  `dg-on-dark-t`, `dg-accent-t`, `dg-accent-lt`, `dg-rule-dark`, `dg-tint`,
  `dg-tint-soft`, `dg-out` (white box with orange outline). Gradient stops use
  `style="stop-color:var(--accent)"`.
- **Today:** white nodes and neutral arrows, the bottleneck as `dg-block` plus a 2px
  `dg-block-line` outline, caption in `dg-cap`, the cost line in `dg-accent-t`.
- **Proposed:** `dg-tint` input, white choice boxes, `dg-hot` curves into the black agent or
  developer block (top edge and compact spill clipped to the block), `dg-out` outputs,
  `dg-tint-soft` impact boxes, two `dg-s` summary lines under it.
- Marker, gradient and clipPath ids are unique across the page.
- **Literal characters only** inside SVG (`·`, `→`), never HTML entities. Validate (§12).

---

## 9. Motion

- Scroll reveal on `section > .wrap > *, .tile, .card, .find, .mon, .fact, .size, .plan,
  .step, .diag`, staggered `Math.min(i % 6, 5) * 55ms`. After an element lands the script
  removes the reveal classes so its own hover lift works again.
- Hover: cards lift 2 to 4px with an orange tinted shadow, founder cards invert to black,
  chips fill orange, buttons lift and slide their gradient.
- Band: count up plus the pattern animations (pips light in sequence, the ring arc and hand
  sweep, the stair draws and its nodes light, the meter fills and its knob pulses).
- Everything respects `prefers-reduced-motion`, and the page is fully readable with JS off.

---

## 10. OG image recipe (EZJ orange and black)

1200x630, black ground, an orange top edge, a soft glow under a bright orange node that
lines converge into, the EZJ mark top left with the offer name in orange, the hero headline
in uppercase Montserrat 900 with the payoff in orange, and three metrics from the band. This is
the house recipe. Build it in HTML and screenshot it, never generate it with an image model.

The OG card is Ethan's step, not yours. He fills `{{OG_IMAGE_URL}}` when he deploys.
It is documented here so the recipe stays in one place. If you do build one, embed the
logo from `logo.txt` the same way the page does, there is no separate image file in this
package.

Write `og.html` in the scratchpad:

```html
<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Figtree:wght@500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;background:#0d0d0d;position:relative;font-family:'Figtree',sans-serif;color:#fff}
.edge{position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(95deg,#e8680f,#F47C20,#ff8f3a)}
.glow{position:absolute;left:750px;top:55px;width:520px;height:520px;background:radial-gradient(closest-side,rgba(255,143,58,.4),rgba(244,124,32,.1) 45%,rgba(244,124,32,0))}
svg{position:absolute;left:0;top:0}
.c{position:absolute;left:64px;top:56px;width:700px}
.top{display:flex;align-items:center;gap:14px}
.top img{width:46px;height:46px}
.top span{font-family:'Montserrat';font-weight:800;font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:#F47C20}
h1{font-family:'Montserrat';font-weight:900;font-size:56px;line-height:1.02;letter-spacing:-.03em;text-transform:uppercase;margin-top:42px}
h1 span{color:#F47C20}
.m{display:flex;gap:44px;margin-top:40px}
.m div{font-size:15px;color:rgba(255,255,255,.64);font-weight:500;line-height:1.35;max-width:180px}
.m b{display:block;font-family:'Montserrat';font-weight:900;font-size:34px;letter-spacing:-.03em;color:#F47C20;line-height:1.05;margin-bottom:4px}
</style></head><body>
<div class="edge"></div><div class="glow"></div>
<svg width="1200" height="630" viewBox="0 0 1200 630">
  <defs><radialGradient id="nd" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#ff8f3a"/><stop offset="1" stop-color="#e8680f"/></radialGradient></defs>
  <g fill="none" stroke="#F47C20" stroke-opacity=".3" stroke-width="1.2">
    <path d="M720 40 C880 40 900 315 1010 315"/><path d="M740 130 C880 130 910 315 1010 315"/>
    <path d="M760 220 C890 220 920 315 1010 315"/><path d="M770 315 L1010 315"/>
    <path d="M760 410 C890 410 920 315 1010 315"/><path d="M740 500 C880 500 910 315 1010 315"/>
    <path d="M720 590 C880 590 900 315 1010 315"/>
  </g>
  <circle cx="1010" cy="315" r="118" fill="none" stroke="#F47C20" stroke-opacity=".16"/>
  <circle cx="1010" cy="315" r="82" fill="none" stroke="#F47C20" stroke-opacity=".3"/>
  <line x1="1060" y1="315" x2="1200" y2="315" stroke="#F47C20" stroke-width="2"/>
  <circle cx="1010" cy="315" r="50" fill="url(#nd)"/>
</svg>
<div class="c">
  <div class="top"><img src="ezj-logo.png" alt=""><span>{{OFFER_NAME}} · Proposal for {{CLIENT_COMPANY}}</span></div>
  <h1>{{HERO_LINE_1}}<br>{{HERO_LINE_2}}<br><span>{{HERO_PAYOFF_LINE_1}}<br>{{HERO_PAYOFF_LINE_2}}</span></h1>
  <div class="m"><div><b>{{METRIC_1_SHORT}}</b>{{METRIC_1_LABEL_SHORT}}</div><div><b>{{METRIC_2_SHORT}}</b>{{METRIC_2_LABEL_SHORT}}</div><div><b>{{METRIC_3_SHORT}}</b>{{METRIC_3_LABEL_SHORT}}</div></div>
</div>
</body></html>
```

Render, convert, read back:

```bash
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$C" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=4000 \
  --window-size=1200,630 --screenshot="$SS/og.png" "file://$SS/og.html"
sips -s format jpeg -s formatOptions 90 "$SS/og.png" --out "$SS/og.jpg"
```

- Read the JPG. Check the headline is not clipped, no brown haze, the mark is visible, the
  metrics fit on one row. Shorten copy before shrinking type. A three line headline drops
  the fourth `<br>` line.
- Save it as `<client-slug>-og.jpg` beside the page and send it with the page. Ethan puts it
  on the live URL.
- The template head carries the `og:*` and `twitter:*` tags with `{{PAGE_URL}}` and
  `{{OG_IMAGE_URL}}` left in place. Leave them. List them in the handoff note.
- Never put private client performance numbers on a card that will sit on a public URL.

---

## 11. Client brand skin swap (only when EZJ asks for their branding)

1. Pull their brand: open their site, read the two colours that actually carry it (the dark
   and the accent), note the display and body faces, and save their logo as a PNG with a
   transparent background. **Confirm the two hex codes with Ethan before building.** If their
   display face is licensed, substitute the closest free Google font and say nothing about it.
2. Replace the live `:root` values with theirs. The commented block in the template is the
   worked example, an ink and gold brand:

| Token | EZJ skin | Worked example skin |
|---|---|---|
| `--dark` / `--dark-deep` / `--dark-rgb` | `#0d0d0d` / `#000000` / `13,13,13` | `#2b2927` / `#1c1a19` / `43,41,39` |
| `--accent` / `--accent-lt` / `--accent-dk` | `#F47C20` / `#ff8f3a` / `#e8680f` | `#FFC71D` / `#FFD64A` / `#EFC13B` |
| `--accent-rgb` / `--accent-lt-rgb` | `244,124,32` / `255,143,58` | `255,199,29` / `255,214,74` |
| `--accent-ink` / `--accent-tint` | `#c2560a` / `#fff1e5` | `#7a5c00` / `#fbf3d9` |
| `--ground` / `--card` / `--card-2` | `#f7f7f5` / `#fff` / `#fbfbfa` | `#efece8` / `#fff` / `#f8f7f4` |
| `--ink` / `--muted` / `--dim` | `#0d0d0d` / black .7 / black .54 | `#2b2927` / `#5c5955` / `#77726b` |
| `--line` / `--line-2` | black .16 / black .09 | `#d9d3c8` / `#e4e0da` |
| `--on-dark-muted` / `--on-dark-dim` / `--on-accent` | white .76 / white .52 / `#0d0d0d` | `#d6d0c6` / `#bdb6aa` / `#2b2927` |
| `--disp` / `--body` | Montserrat / Figtree | Barlow Semi Condensed / Jost |
| `--disp-weight` / `--disp-track` | `900` / `-.03em` | `800` / `-.01em` |

3. Swap the Google Fonts link for their faces (free substitutes for licensed ones).
4. In `.bar`, replace the EZJ mark and wordmark with their logo in full colour, embedded as one
   line of base64 the same way, 40px tall. The footer keeps the EZJ mark.
5. For the OG card, keep the §10 recipe and swap its hexes for their two brand colours.

A client's brand may carry greys or warm neutrals. That is their brand, so the no greys
rule applies to the EZJ skin only.

---

## 12. QA (do not skip)

**Local copy with relative paths, reveals forced on:**

```bash
F=~/proposals/<client-slug>/<client-slug>.html; SS=~/proposals/qa
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$SS" && cp "$F" "$SS/page.html"
python3 - "$SS/page.html" <<'PY'
import sys
p = sys.argv[1]; h = open(p).read()
h = h.replace('</style>', '</style><style>.rv{opacity:1!important;transform:none!important}</style>', 1)
probe = '<script>setTimeout(function(){var d=document.documentElement;var v=d.scrollWidth+"x"+d.clientWidth;document.body.setAttribute("data-sw",v);if(parent!==window)parent.postMessage(v,"*")},3000)</script>'
open(p, 'w').write(h.replace('</body>', probe + '</body>'))
PY
```

**Desktop, 1200 wide.** `--virtual-time-budget` lets fonts load and the band count up finish
before capture. Cut the tall PNG into crops, because a 10,000 pixel image read whole is too
small to judge:

```bash
"$C" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=6000 \
  --window-size=1200,12000 --screenshot="$SS/full.png" "file://$SS/page.html"
python3 -c "
from PIL import Image
im = Image.open('$SS/full.png')
for i, y in enumerate(range(0, im.height, 1400)): im.crop((0, y, 1200, min(y + 1400, im.height))).save(f'$SS/cut{i}.png')"
```

**Mobile at a true 390px.** Headless Chrome will not open a window under 500px wide, so
`--window-size=390,...` silently lays the page out at 500px. Put the page in a 390 wide
iframe inside a 500px window, then crop. Use a 12000 budget here: animations inside an iframe start
later, and at 6000 the band was captured half lit on 2026-09-15.

```bash
cat > "$SS/m.html" <<'EOF'
<body style="margin:0"><iframe src="page.html" width="390" height="2400" style="border:0;display:block"></iframe>
<script>addEventListener('message',function(e){document.body.setAttribute('data-sw',e.data)})</script></body>
EOF
"$C" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=12000 --window-size=500,2400 \
  --dump-dom "file://$SS/m.html" 2>/dev/null | grep -o 'data-sw="[^"]*"'     # must be 390x390
"$C" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=12000 --window-size=500,2400 \
  --screenshot="$SS/m500.png" "file://$SS/m.html"
python3 -c "from PIL import Image; Image.open('$SS/m500.png').crop((0,0,390,2400)).save('$SS/mobile.png')"
```

Do not crop with `sips -c`: it crops from the centre and ignores `--cropOffset` here.

**Read every crop and the mobile PNG.** Look for brown haze on black, grey leftovers, a
broken logo, cramped band tiles, a highlight bar that misses its line, card text that
overflows, a label column that misaligns.

**Static checks, all at once:**

```bash
python3 - "$F" <<'PY'
import re, sys, subprocess, tempfile, xml.etree.ElementTree as ET
t = open(sys.argv[1]).read()
for s in re.findall(r'(<svg .*?</svg>)', t, re.S): ET.fromstring(s)
print('svg ok')
js = tempfile.NamedTemporaryFile('w', suffix='.js', delete=False)
js.write(re.findall(r'<script>(.*?)</script>', t, re.S)[-1]); js.close()
print('script', 'ok' if subprocess.run(['node', '--check', js.name]).returncode == 0 else 'BROKEN')
print('tokens left', sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t))))
print('em or en dashes', t.count('\u2014') + t.count('\u2013'))
code = re.sub(r'<!--.*?-->|/\*.*?\*/', ' ', t, flags=re.S)
allowed = {'#0d0d0d','#000000','#f47c20','#ff8f3a','#e8680f','#c2560a','#fff1e5','#f7f7f5','#fbfbfa','#ffffff'}
print('off palette hex', sorted({h.lower() for h in re.findall(r'#[0-9a-fA-F]{6}\b', code)} - allowed))
print('invert filter', 'invert(' in code)
PY
```

Then by hand: every dollar amount matches EZJ's lock, every payment link resolves, the hero
and the band agree, no spaced hyphen in visible copy.

---

## 13. Save and hand off (you do not deploy)

- Save the finished page as `<client-slug>.html`, with `<client-slug>-og.jpg` beside it, and
  **send both to Ethan. He deploys it.** You never publish a proposal, never create a payment
  link, and never send the page to the prospect.
- The page is one self-contained file. The logo is embedded from `logo.txt`, the CSS and the
  script are inline, and the only thing it loads from the internet is the Google Fonts link.
  So it opens correctly from a double click, from an email attachment, and from a Slack file.
  Check that before you send it.
- Write a short **handoff note** beside it, in plain text, listing exactly:
  1. Every placeholder still in the file: `{{PAGE_URL}}`, `{{OG_IMAGE_URL}}`, and each
     `{{PLAN_*_URL}}` with the plan name and the exact price its button shows.
  2. Every price on the page, so Ethan can check them against what he locked with you.
  3. Anything you were not sure about and guessed.
- If the page must survive with no internet (a call on bad wifi), inline `fonts.css` into the
  `<style>` block in place of the Google Fonts link. Otherwise leave the link alone, it keeps
  the file small.

---

## 14. Never do

- Never start a proposal from a blank file. Always start from `ezj_template/index.html`.
- Never ship a leftover `{{TOKEN}}` or the commented client skin block on an EZJ skin page.
- Never use a linear black to orange gradient, and never a wide glow without an orange source.
- Never ship greys or warm taupes on the EZJ skin.
- Never put a hex colour or an HTML entity inside inline SVG.
- Never invert a logo to a white silhouette.
- Never let the band's numbers depend on JS, or animate without the reduced motion guard.
- Never trust `--window-size` under 500 for a mobile check.
- Never create a payment link, deploy the page, or send it to the prospect yourself.
- Never use a dash as punctuation.
