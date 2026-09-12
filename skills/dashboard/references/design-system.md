# The design system

Everything below is one decision repeated: **the data is the design.** Color, motion and chrome exist to make numbers readable and comparable. Anything that does not serve that gets cut.

---

## 1. Tokens first, always

Define the entire visual language as CSS custom properties at the top of the file, then never write a raw hex or pixel value below that block. This is what makes a dashboard re-skinnable in 60 seconds and what keeps 40 components looking like one product.

```css
:root {
  color-scheme: dark;

  /* Surfaces. A ladder, not a palette. Each step is a layer of elevation. */
  --page:      #000000;
  --surface:   #101010;
  --surface-2: #181818;
  --surface-3: #222222;

  /* Ink. Three levels. Do not invent a fourth. */
  --ink:    #ffffff;   /* values, headlines */
  --ink-2:  #cfcfcf;   /* body, table cells */
  --muted:  #969696;   /* labels, axis text, meta */

  --border:   #2a2a2a;
  --border-2: #1e1e1e;
  --track:    #262626;  /* the unfilled part of a bar */

  /* ONE accent. This is the brand. Change these four lines to rebrand everything. */
  --accent:      #F47C20;
  --accent-deep: #f8944c;                          /* lighter step for small text */
  --accent-soft: rgba(244, 124, 32, 0.14);         /* fills, chips */
  --accent-line: rgba(244, 124, 32, 0.35);         /* rings, hairlines */

  /* Status is its own system and NEVER borrows the accent. */
  --good: #22c55e;  --good-soft: rgba(34, 197, 94, 0.16);
  --bad:  #ef4444;  --bad-soft:  rgba(239, 68, 68, 0.16);
  --warn: #eab308;  --warn-soft: rgba(234, 179, 8, 0.16);

  /* Fixed rem scale, ~1.25 ratio. Dashboards want predictable type, not fluid. */
  --t-xs: 0.75rem; --t-sm: 0.8125rem; --t-base: 0.9375rem;
  --t-md: 1.0625rem; --t-lg: 1.375rem; --t-xl: 1.75rem; --t-2xl: 2.25rem;

  /* 4pt spacing scale, semantic names. */
  --space-2xs: 4px; --space-xs: 8px;  --space-sm: 12px; --space-md: 16px;
  --space-lg: 24px; --space-xl: 32px; --space-2xl: 48px;

  --font-display: "Montserrat", ui-sans-serif, system-ui, sans-serif;
  --font-body:    "Open Sans", ui-sans-serif, system-ui, -apple-system, sans-serif;
  --font-mono:    ui-monospace, "SF Mono", Menlo, monospace;

  --radius: 14px; --radius-sm: 10px; --radius-lg: 18px;
  --shadow: 0 1px 2px rgba(0,0,0,.45), 0 8px 22px rgba(0,0,0,.30);
  --shadow-lift: 0 20px 40px -24px rgba(0,0,0,.75), 0 0 0 1px var(--accent-line);
  --inset-hi: inset 0 1px 0 rgba(255,255,255,.04);
}
```

**Rebranding = editing the four accent lines.** Nothing else. If you find yourself editing more than that to match a client's brand, your tokens leaked.

Swap the surface ladder and ink ramp for a light theme and the entire system still works. The structure is what carries the quality, not the darkness.

---

## 2. The color rules that separate a dashboard from a slide deck

**One accent, used sparingly.** The accent marks what matters: the primary series, the active state, the section marker dot, the one hero number. If five things on screen are accent colored, none of them are.

**Status color is semantic and separate.** Green means good, red means bad, amber means attention. Never use green just because it looks nice next to orange. Never render a delta in the accent. A viewer must be able to trust that a color means something.

**Direction is not universal.** Higher cost is bad, higher revenue is good. Pass the direction in:

```js
// dir: "up" = higher is better, "down" = lower is better, "neutral" = no judgement
function delta(cur, prior, dir) { /* ... */ }
```

Bounce rate going up rendered in green is the single most common credibility killer in a client dashboard.

**Categorical color is identity, not decoration.** When you have entities (clients, channels, campaigns), assign each a color once from a fixed palette and reuse it everywhere: donut slice, avatar, table bar, chart line. The viewer learns the mapping in three seconds and then reads the whole page faster.

```js
const PAL = ['#6fe3ff','#9b8cff','#ffcf6b','#43e0a8','#ff86b0','#5ad1e0','#c69bff','#ffd98a'];
const colorFor = id => PAL[Math.max(0, ENTITIES.findIndex(c => c.id === id)) % PAL.length];
```

**Some colors are data.** A payment rail's own brand color (Stripe violet, Wise green) tells you where money came in without a legend. That is semantic color, not decor, and it is worth the exception.

---

## 3. Typography

**Numbers are the point. Set them like it.**

```css
.num { font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1; }
```

Every number, everywhere. Without this, digits jitter as values change and columns stop aligning, which is the difference between "instrument panel" and "webpage with numbers on it."

The hero value:

```css
.tile-value {
  font-family: var(--font-display);
  font-size: var(--t-xl);          /* --t-2xl for the one hero tile */
  font-weight: 800;
  letter-spacing: -0.035em;        /* big type needs negative tracking */
  line-height: 1.05;
  font-variant-numeric: tabular-nums;
}
```

The label above it, the opposite treatment:

```css
.tile-label {
  font-size: var(--t-xs);
  font-weight: 650;
  letter-spacing: .07em;
  text-transform: uppercase;
  color: var(--muted);
}
```

That contrast, **tiny tracked-out uppercase label over a huge tight-tracked number**, is most of the "designed" feeling. It costs nothing.

Mono for timestamps, IDs, and dense numeric columns. Never for prose.

**Never put a gradient on a number.** Gradient text on a KPI is the loudest AI-slop tell there is. Gradients belong on chart strokes and active-state fills.

---

## 4. Surfaces, depth, and why you should not reach for a drop shadow

At rest, a card is: subtle vertical gradient, 1px border, 1px inset top highlight. No drop shadow.

```css
.card {
  background: linear-gradient(180deg, #141414, #0d0d0d);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--inset-hi);
  transition: transform .2s cubic-bezier(.22,.61,.36,1), border-color .2s, box-shadow .2s;
}
.card:hover {
  transform: translateY(-3px);
  border-color: var(--border-hi);
  box-shadow: var(--inset-hi), 0 20px 40px -24px rgba(0,0,0,.7), 0 0 0 1px var(--accent-line);
}
```

The hover shadow is the signature: a **large negative-spread ambient shadow** plus a **1px accent ring at low opacity**. It reads as a glow without being one.

Ambient depth comes from the page, not the cards. Two off-axis radial washes at very low opacity, fixed so they do not scroll:

```css
body {
  background-color: var(--page);
  background-image:
    radial-gradient(72% 55% at 90% -10%, rgba(244,124,32,.10), transparent 60%),
    radial-gradient(55% 45% at 0% 108%, rgba(244,124,32,.07), transparent 58%);
  background-attachment: fixed;
  background-repeat: no-repeat;
}
```

Barely visible on purpose. If you can clearly see the gradient, turn it down.

Radii ladder, and stick to it: 18px outer cards, 14px cards, 10px inner tiles and controls, 8px chips, 999px pills.

No `backdrop-filter`. Frosted glass over a data table is a readability tax paid for a 2021 trend.

---

## 5. Layout

```css
.page { max-width: 1180px; margin: 0 auto; padding: var(--space-md) var(--space-lg) var(--space-2xl); }

/* Flex + gap so every child is spaced identically, whatever element it is. */
.section { margin-top: var(--space-lg); display: flex; flex-direction: column; gap: var(--space-sm); }

.stat-grid { display: grid; gap: var(--space-xs); grid-template-columns: repeat(auto-fit, minmax(168px, 1fr)); }
.split { display: grid; gap: var(--space-sm); grid-template-columns: 1fr 1fr; align-items: start; }
.split.wide-left { grid-template-columns: 1.35fr 1fr; }

/* Grid children default to min-width:auto, so a wide table would push the track
   past the viewport on phones. This is what keeps the scroll container scrolling. */
.split > * { min-width: 0; }
```

That `min-width: 0` line is the single most common cause of "why does my dashboard scroll sideways on mobile."

**Reading order is a ranking.** Top left is the most important number on the page. Then the trend that explains it. Then the breakdown. Then the detail table. Then what to do about it. If a section cannot justify its position, move it down or delete it.

**Two responsive decisions worth copying:**

```css
@media (max-width: 720px) {
  /* Two compact columns beat one endless stack of full-width tiles. */
  .stat-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  /* Tables scroll edge to edge of the card so more columns stay visible. */
  .table-scroll { margin: 0 calc(-1 * var(--space-md)); padding: 0 var(--space-md); }
}
```

For wide tables, the best mobile pattern is turning rows into cards using `data-label`:

```css
@media (max-width: 600px) {
  table, tbody, tr, td { display: block }
  thead { display: none }
  tr { border: 1px solid var(--border-2); border-radius: 14px; padding: 12px 15px; margin: 0 0 12px; }
  td { display: flex; justify-content: space-between; gap: 12px; padding: 7px 0; text-align: right; }
  td::before {
    content: attr(data-label);
    font-size: 10.5px; font-weight: 700; text-transform: uppercase;
    letter-spacing: .05em; color: var(--muted);
  }
}
```

---

## 6. Section structure

Every section is the same three parts: eyebrow, title, optional right-aligned note. One constructor, used everywhere.

```js
function sectionShell(eyebrow, title, note) { /* returns the header markup */ }
```

```css
.section-eyebrow {
  display: flex; align-items: center; gap: var(--space-2xs);
  font-size: var(--t-xs); font-weight: 700; letter-spacing: .07em;
  text-transform: uppercase; color: var(--muted);
}
.section-eyebrow::before {
  content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--accent);
}
```

That 6px accent dot before every eyebrow is a two-line detail that ties the whole page together.

---

## 7. Icons

Inline SVG, 9px to 16px, `stroke="currentColor"`, `stroke-width="2"`. Defined once as constants and reused.

```js
const UP   = '<svg viewBox="0 0 10 10" fill="currentColor"><path d="M5 1l4 6H1z"/></svg>';
const DOWN = '<svg viewBox="0 0 10 10" fill="currentColor"><path d="M5 9L1 3h8z"/></svg>';
```

Never emoji as UI icons. A 📊 in a section header is the fastest way to make a dashboard look generated.

---

## 8. The anti-slop checklist

Things that instantly mark a dashboard as machine-made. Avoid all of them.

- Gradient text on headings or numbers
- Purple-to-blue gradient on everything, glassmorphism on every card
- Emoji used as icons or in headings
- The word "Dashboard" as the page title when the page has a real subject
- Rainbow-colored KPI tiles where each metric gets a different accent
- A pie chart with 11 slices
- Dual y-axes, 3D bars, drop shadows on chart elements
- Chart library defaults left untouched, the tell being the default tooltip and legend
- Numbers without `tabular-nums`
- Deltas colored by sign instead of by whether the change is good
- Lorem ipsum, placeholder avatars, or invented data anywhere, ever
- "No data" as an empty state
- Six different font sizes chosen by feel instead of a scale
- Cards with a heavy drop shadow at rest
- Every metric given equal visual weight, so the page has no focal point

Things that mark one as considered:

- One accent, a separate status system, and categorical colors that mean something
- Tabular numerals on every figure
- Tiny tracked uppercase labels over large tight-tracked values
- Dotted gridlines that sit behind the data
- A visible, honest freshness stamp
- Empty states written as sentences that explain how to fix the gap
- A hover state on every interactive element and on nothing else
- Real density, because a dashboard is an instrument, not a landing page

---

## 9. States are part of the design

**Loading.** If the data is baked in, there is no loading state, which is the best kind. If you fetch, show a real overlay from first paint so navigating in never flashes a blank page.

```css
/* Black screen, accent trailing comet. */
.spinner {
  background: conic-gradient(from 0deg, transparent 0turn,
    color-mix(in oklab, var(--accent) 22%, transparent) .55turn,
    var(--accent) .92turn, var(--accent) 1turn);
  -webkit-mask: radial-gradient(farthest-side, #0000 calc(100% - 4px), #000 calc(100% - 3.5px));
          mask: radial-gradient(farthest-side, #0000 calc(100% - 4px), #000 calc(100% - 3.5px));
  animation: spin .7s linear infinite;
}
```

**Empty.** Write a sentence that says what is missing and how it gets filled. Not "No data."

> "Instagram is not linked for this account yet. Once connected, followers, posts, views and reach land here automatically."

```css
.empty {
  color: var(--muted); font-size: 13.5px;
  border: 1px dashed var(--border); border-radius: 15px; padding: 22px; text-align: center;
}
```

**Missing cell.** An em dash in muted ink. Never a blank, never a zero. A zero is a claim and blanks look broken.

**Broken upstream.** Say so. Never fabricate, never silently drop the section.

```js
function valid(block) {
  return block && typeof block === "object" && !block.error && Object.keys(block).length > 0;
}
// Honest unavailable state. Never a fabricated empty table.
var why = block.reason ? String(block.reason) : "the source did not respond";
```

**Impossible value.** Refuse to print nonsense. A conversion rate over 100% means the data is wrong, so show an em dash, not the number.

```js
const convDisp = m => (m.sessions > 0 && m.rate <= 100) ? m.rate + '%' : '—';
```

**Stale.** The freshness indicator changes state rather than lying:

```js
status("Live, updated just now", false);     // fetch succeeded
status("Showing saved data", true);          // fetch failed, fallback rendered
status("Could not load", true);              // nothing to show
```

```css
.live-dot .d { width: 7px; height: 7px; border-radius: 50%; background: var(--good);
  box-shadow: 0 0 0 0 rgba(34,197,94,.5); animation: livepulse 2.4s infinite; }
.live-dot.stale .d { background: var(--warn); animation: none; }
@keyframes livepulse {
  0%   { box-shadow: 0 0 0 0 rgba(34,197,94,.45); }
  70%  { box-shadow: 0 0 0 7px rgba(34,197,94,0); }
  100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
}
```

---

## 10. Motion

Motion confirms causality and directs attention. That is the whole job. Nothing on a dashboard should move for delight.

**Staggered entrance**, four or five steps, then stop:

```css
.reveal { opacity: 0; transform: translateY(10px); animation: rise .55s cubic-bezier(.22,.61,.36,1) forwards; }
@keyframes rise { to { opacity: 1; transform: none; } }
.d1 { animation-delay: .04s } .d2 { animation-delay: .10s }
.d3 { animation-delay: .16s } .d4 { animation-delay: .22s } .d5 { animation-delay: .28s }
```

**Count-up on values.** Parse the already-formatted string so it works on `$12,345` and `4.8%` alike, and restore the exact original text at the end so no rounding drift survives.

```js
function countUp() {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('[data-cu]').forEach(el => {
    const txt = el.textContent;
    const m = txt.match(/^([^0-9]*)([\d,]+(?:\.\d+)?)(.*)$/);
    if (!m) return;
    const pre = m[1], suf = m[3], target = parseFloat(m[2].replace(/,/g, ''));
    const dec = (m[2].split('.')[1] || '').length;
    const t0 = performance.now(), dur = 700;
    (function step(t) {
      const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + (target * e).toLocaleString('en-US',
        { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf;
      if (p < 1) requestAnimationFrame(step); else el.textContent = txt;
    })(performance.now());
  });
}
```

**Micro-interactions.** `transform: translateY(-3px)` on card hover, `translateX(2px)` on nav hover, `scale(.96)` on button press, `.6s` width transition on progress bars. Durations 150ms to 250ms, easing `cubic-bezier(.22,.61,.36,1)`.

**Always give motion an escape hatch:**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
  }
}
```

Never: parallax, scroll-jacking, looping background animation, an animated gradient behind a table, a chart that redraws on every scroll.
