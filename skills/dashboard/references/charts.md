# Chart recipes (hand-rolled SVG, zero dependencies)

Every chart below is a pure function that takes data and returns an SVG string. No Chart.js, no D3, no Recharts. Reasons: the page stays a single file, nothing breaks when a CDN changes, the visual language stays yours, and you never fight a library's defaults to make it look like anything other than a library.

Copy these, change the numbers, keep the structure.

---

## The one primitive everything shares: a smooth path

A Catmull-Rom spline. Straight polylines look like a school project. This makes a line chart look designed.

```js
function spline(p) {
  if (p.length < 2) return p.length ? ('M' + p[0][0] + ',' + p[0][1]) : '';
  let d = 'M' + p[0][0].toFixed(1) + ',' + p[0][1].toFixed(1);
  for (let i = 0; i < p.length - 1; i++) {
    const a = p[i - 1] || p[i], b = p[i], c = p[i + 1], e = p[i + 2] || c;
    d += 'C' + (b[0] + (c[0] - a[0]) / 6).toFixed(1) + ',' + (b[1] + (c[1] - a[1]) / 6).toFixed(1)
       + ' ' + (c[0] - (e[0] - b[0]) / 6).toFixed(1) + ',' + (c[1] - (e[1] - b[1]) / 6).toFixed(1)
       + ' ' + c[0].toFixed(1) + ',' + c[1].toFixed(1);
  }
  return d;
}
```

Scale helpers, always the same shape:

```js
const X = i => pad + (i / Math.max(1, series.length - 1)) * innerW;
const Y = v => pad + innerH - ((v - min) / ((max - min) || 1)) * innerH;
const pts = series.map((d, i) => [X(i), Y(d[key])]);
```

---

## 1. Hero area + line

The big chart at the top. Gradient stroke, soft area fill, a blurred glow, a dashed previous-period line behind it, dotted gridlines.

```js
const line = spline(pts);
const area = line + 'L' + pts[pts.length-1][0] + ',' + (pad+innerH) + 'L' + pts[0][0] + ',' + (pad+innerH) + 'Z';

const svg =
  '<svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none">'
+ '<defs>'
+   '<linearGradient id="lng" x1="0" x2="1">'
+     '<stop offset="0" stop-color="var(--accent-1)"/>'
+     '<stop offset="1" stop-color="var(--accent-2)"/>'
+   '</linearGradient>'
+   '<linearGradient id="arg" x1="0" x2="0" y1="0" y2="1">'
+     '<stop offset="0" stop-color="var(--accent-1)" stop-opacity=".28"/>'
+     '<stop offset="1" stop-color="var(--accent-2)" stop-opacity="0"/>'
+   '</linearGradient>'
+   '<filter id="glo" x="-20%" y="-60%" width="140%" height="220%">'
+     '<feGaussianBlur stdDeviation="5" result="b"/>'
+     '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
+   '</filter>'
+ '</defs>'
+ grid
+ (prevPts.length ? '<path d="' + spline(prevPts) + '" fill="none" stroke="var(--ink-3)" stroke-opacity=".55" stroke-width="1.8" stroke-dasharray="5 6" stroke-linecap="round"/>' : '')
+ '<path d="' + area + '" fill="url(#arg)"/>'
+ '<path d="' + line + '" fill="none" stroke="url(#lng)" stroke-width="3" stroke-linecap="round" filter="url(#glo)"/>'
+ '</svg>';
```

**Dotted gridlines, not dashed.** `stroke-dasharray="1 5"` with a round linecap renders as a dot rail. Dashes look like a spreadsheet, dots disappear behind the data where they belong.

```js
const grid = ticks.map(t =>
  '<line x1="' + pad + '" x2="' + (pad+innerW) + '" y1="' + Y(t) + '" y2="' + Y(t) + '" '
+ 'stroke="var(--line)" stroke-width="1" stroke-dasharray="1 5" stroke-linecap="round"/>').join('');
```

**Label 3 x-axis points, not 30.** First, middle, last. Every date on the axis is noise.

**Handle the degenerate single-point window explicitly.** One data point has no trend, so draw a flat reference line slightly above center so it reads as a level, not a full block:

```js
// a single-day window has no trend: draw a flat reference line, centered so it
// reads as a level rather than a filled block. Its true value is in the headline.
const flat = cur.length < 2;
if (flat) pts[0][1] = pad + innerH * 0.42;
```

---

## 2. Sparkline (goes inside every KPI tile)

```js
function spark(series, key, color) {
  const vals = series.map(d => d[key]);
  if (!vals.length) return '';
  const max = Math.max.apply(null, vals.concat([1]));
  const min = Math.min.apply(null, vals.concat([0]));
  const w = 120, h = 26;
  const X = i => series.length < 2 ? w/2 : i/(series.length-1)*w;
  const Y = v => h - 3 - ((v - min) / ((max - min) || 1)) * (h - 6);
  const pts = series.map((d, i) => [X(i), Y(d[key])]);
  const last = pts[pts.length - 1];
  const gid = 's' + Math.random().toString(36).slice(2, 7);   // unique id per instance
  return '<svg class="spark" viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" style="overflow:visible">'
    + '<defs><linearGradient id="' + gid + '" x1="0" x2="1">'
    + '<stop offset="0" stop-color="' + color + '" stop-opacity=".25"/>'
    + '<stop offset="1" stop-color="' + color + '"/></linearGradient></defs>'
    + '<path d="' + spline(pts) + '" fill="none" stroke="url(#' + gid + ')" stroke-width="2" stroke-linecap="round"/>'
    + '<circle cx="' + last[0].toFixed(1) + '" cy="' + last[1].toFixed(1) + '" r="2.4" fill="' + color + '"/></svg>';
}
```

Two details that matter. The **random gradient id** stops eight sparklines on one page from all inheriting the first one's `<defs>`. The **dot on the last point** tells the eye where "now" is without a label.

When a tile has no series, render an empty placeholder of the same size so tile footers stay aligned:

```js
const sp = d.seriesKey ? spark(s, d.seriesKey, d.color) : '<span class="spark"></span>';
```

---

## 3. Donut

Stacked circles using `stroke-dasharray` and `stroke-dashoffset`. No arc math, no path strings.

```js
const R = 46, C = 2 * Math.PI * R;
let acc = 0;
const segs = parts.map(p => {
  const f = p.value / total;
  const gap = parts.length > 1 ? 4 : 0;              // visual gap between segments
  const seg = '<circle r="' + R + '" cx="60" cy="60" fill="none" stroke="' + p.color + '" '
    + 'stroke-width="13" stroke-linecap="round" '
    + 'stroke-dasharray="' + Math.max(2, f * C - gap).toFixed(1) + ' ' + C + '" '
    + 'stroke-dashoffset="' + (-acc * C).toFixed(1) + '" transform="rotate(-90 60 60)"/>';
  acc += f;
  return seg;
}).join('');
```

Alternative separation trick if you prefer butt caps: give every segment a 2px stroke in the card's background color so adjacent slices read as separate marks.

```css
.seg { stroke: var(--surface); stroke-width: 2; transition: opacity .15s ease; }
.donut:hover .seg { opacity: .45; }     /* dim the ring */
.donut .seg:hover { opacity: 1; }       /* except the one under the cursor */
```

Always put a value in the hole. An empty donut center is wasted focal space.

```js
+ '<text x="60" y="58" text-anchor="middle" class="donut-val">' + shortNum(total) + '</text>'
+ '<text x="60" y="74" text-anchor="middle" class="donut-lbl">TOTAL</text>'
```

Rule: donuts max out at 5 slices. Past that use a ranked bar list, which humans can actually read.

---

## 4. Bar chart with a CSS-only tooltip

No JS listeners. `data-tip` plus `::after`.

```js
'<div class="bcol" data-tip="' + label + ' · ' + fmt(v) + '">'
+ '<div class="bwrap"><div class="bar" style="height:' + h + 'px"></div></div>'
+ '<span class="blbl">' + shortLabel + '</span></div>'
```

```css
.bcol { position: relative; }
.bcol::after {
  content: attr(data-tip);
  position: absolute; bottom: calc(100% + 8px); left: 50%;
  transform: translateX(-50%) translateY(4px);
  background: var(--surface-3); border: 1px solid var(--line);
  border-radius: 8px; font-size: 10px; font-weight: 800; padding: 5px 9px;
  white-space: nowrap; opacity: 0; pointer-events: none; transition: .15s; z-index: 5;
}
.bcol:hover::after { opacity: 1; transform: translateX(-50%) translateY(0); }
```

---

## 5. Bar in a table cell (share of max)

The highest-value-per-pixel chart there is. It turns a column of numbers into a ranked shape without adding a chart.

```js
'<td data-label="Revenue"><div class="barcell">'
+ '<span class="money num">' + usd(v) + '</span>' + deltaEl(delta)
+ '<span class="track"><span class="fill" style="width:' + (v/max*100).toFixed(0) + '%;'
+ 'background:linear-gradient(90deg,' + col + '66,' + col + ')"></span></span>'
+ '</div></td>'
```

---

## 6. Funnel as lit slats

Reads better than stacked trapezoids and is pure divs.

```js
const N = 12;
stages.map((s, si) => {
  const rawRatio = s.value / base;
  const ratio = Math.min(1, rawRatio);
  const lit = Math.max(s.value > 0 ? 1 : 0, Math.round(ratio * N));
  let bars = '';
  for (let i = 0; i < N; i++) {
    const on = i < lit;
    bars += '<i style="height:' + (46 - ((N-1-i) % 3) * 5) + 'px;background:'
          + (on ? ('linear-gradient(180deg,' + s.color + ',' + s.color + '88)') : 'var(--track)') + '"></i>';
  }
  const pctTop = si === 0 ? '100%' : (rawRatio > 1 ? '100%+' : (rawRatio*100).toFixed(0) + '%');
  return '<div class="stage">' + bars + '<span class="pct">' + pctTop + '</span></div>';
});
```

---

## 7. Hover interaction on the hero chart

Map mouse X to the nearest index. And on mouse leave, **rest on the peak instead of hiding** so the chart always displays a labelled value.

```js
let peak = 0;
for (let i = 1; i < cur.length; i++) if (cur[i][mk] > cur[peak][mk]) peak = i;
show(peak);

svg.addEventListener('mousemove', e => {
  const r = wrap.getBoundingClientRect();
  const frac = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width));
  const i = Math.round(((frac * w) - pad) / innerW * (cur.length - 1));
  show(Math.min(cur.length - 1, Math.max(0, i)));
});
svg.addEventListener('mouseleave', () => show(peak));
```

Flip the tooltip below the point when it would clip the top edge:

```js
tip.style.top = (py < 58 ? py + 92 : py) + 'px';
tip.style.transform = py < 58 ? 'translate(-50%,8%)' : 'translate(-50%,-112%)';
```

A crosshair line plus a halo dot beats a floating box alone:

```js
'<line id="cross" x1="0" x2="0" y1="' + pad + '" y2="' + (pad+innerH) + '" stroke="var(--line-2)" stroke-dasharray="3 4" opacity="0"/>'
+ '<circle id="halo" r="10" fill="var(--accent-1)" opacity="0"/>'
+ '<circle id="dot" r="4.4" fill="var(--page)" stroke="var(--accent-1)" stroke-width="2.6" opacity="0"/>'
```

---

## 8. Two number formatters, deliberately

```js
const usd      = c => '$' + (c/100).toLocaleString('en-US', {maximumFractionDigits: 0});
const usdShort = c => { const v = c/100;
  return v >= 1e6 ? '$' + (v/1e6).toFixed(1) + 'M'
       : v >= 1e3 ? '$' + (v/1e3).toFixed(1) + 'k'
       : '$' + v.toFixed(0); };
```

Exact values in tables and tooltips. Short values in axis labels and donut centers. Mixing them up is how axes end up cramped or tables end up imprecise.

Money is stored as integer cents everywhere and divided only at render time. Floats and money do not mix.

---

## Choosing the form

| You want to show | Use |
|---|---|
| A value moving over time | Line or area, smoothed |
| Trend inside a KPI tile | Sparkline, no axes, no labels |
| Comparing a handful of categories | Horizontal bars, sorted by value |
| Comparing across time buckets | Vertical bars |
| Parts of a whole, 5 or fewer | Donut with the total in the hole |
| Parts of a whole, more than 5 | Ranked bar list |
| Ranked entities with a metric | Table with a bar in the cell |
| Stage-to-stage dropoff | Funnel |
| One number against a target | Progress meter, not a gauge |

Never a 3D chart. Never a pie with 11 slices. Never dual y-axes.

---

## 9. Gauge / goal ring

Two builds. Pick by feel.

**Ticked arc.** 54 discrete ticks over a 250 degree sweep starting at -215 degrees, each staggering in 11ms after the last. Reads as an instrument.

```js
const N = 54, R = 74, cx = 90, cy = 90;
const lit = Math.round(N * pct / 100);
let ticks = '';
for (let i = 0; i < N; i++) {
  const a = (-215 + i * (250 / (N - 1))) * Math.PI / 180, on = i < lit;
  const x1 = cx + Math.cos(a) * (R - 11), y1 = cy + Math.sin(a) * (R - 11);
  const x2 = cx + Math.cos(a) * R,        y2 = cy + Math.sin(a) * R;
  ticks += '<line class="tick' + (on ? ' on' : '') + '" style="--d:' + (i * 11) + 'ms" '
    + 'x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" '
    + 'stroke="' + (on ? 'url(#ringg)' : 'var(--line)') + '" stroke-width="3.4" stroke-linecap="round"/>';
}
```

```css
.tick { opacity: 0; animation: tickin .5s ease forwards; animation-delay: var(--d); }
@keyframes tickin { to { opacity: 1 } }
```

**Dashoffset ring.** Simpler, one circle over a track circle.

```js
const R = 40, C = 2 * Math.PI * R, off = C * (1 - pct / 100);
'<circle cx="56" cy="56" r="' + R + '" fill="none" stroke="var(--track)" stroke-width="7"/>'
+ '<circle cx="56" cy="56" r="' + R + '" fill="none" stroke="url(#gg)" stroke-width="7" stroke-linecap="round" '
+ 'stroke-dasharray="' + C.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '" '
+ 'transform="rotate(-90 56 56)" filter="url(#ggf)"/>'
```

Put the number and "to go" in the middle. A gauge without a target is just a donut with one slice.

---

## 10. Progress bar, the workhorse

More honest than a gauge for "X of Y" and takes a tenth of the space.

```css
.goalbar { height: 5px; background: var(--track); border-radius: 3px; overflow: hidden; flex: 1; }
.goalbar .fill {
  height: 100%; border-radius: 3px;
  background: linear-gradient(90deg, var(--accent), var(--accent-deep));
  box-shadow: 0 0 10px var(--accent-line);
  width: 0; transition: width .9s cubic-bezier(.16,1,.3,1);
}
```

Widths must be written **one frame after** the element lands in the DOM or the transition never fires:

```js
requestAnimationFrame(() => {
  document.querySelectorAll('.fill').forEach(f => { f.style.width = f.dataset.w + '%'; });
});
```

Or skip the second pass entirely with a keyframe that reads a custom property:

```css
.fill { width: 0; animation: grow 1s cubic-bezier(.22,1,.36,1) forwards; }
@keyframes grow { to { width: var(--w) } }
```
```js
'<span class="fill" style="--w:' + pct + '%"></span>'
```

---

## 11. Ranked bar list

The most reused chart there is. Three-column grid: name, value, track spanning both.

```css
.brow { display: grid; grid-template-columns: 1fr auto; gap: 8px 12px; align-items: center; font-size: 12.5px; }
.brow .bt { grid-column: 1 / -1; height: 6px; border-radius: 4px; background: var(--track); overflow: hidden; }
/* display:block matters. .bf is a span, and an inline box ignores height,
   which silently renders every bar as an empty track. */
.brow .bf { display: block; height: 100%; border-radius: 4px; }
```

**Bar width scales to the max, the printed percentage is share of total.** Two different denominators, on purpose: the bar shows relative magnitude, the number shows contribution.

---

## 12. Vertical bars with drill-down

Selection by **desaturation, never by dimming the brand hue.** A faded orange reads brown on black and breaks the palette.

```js
// Non-selected months go neutral gray, never dimmed accent.
const barColor = (on) => on ? 'var(--accent)' : '#3d3d3d';
```

```css
.mbar .mb {
  border-radius: 7px 7px 3px 3px;
  background: linear-gradient(180deg, var(--accent), var(--accent-soft));
  transition: height .5s cubic-bezier(.22,.61,.36,1), box-shadow .15s, filter .15s;
}
.mbar.dimmed .mb { opacity: .34 }
.mbar.sel .mb    { box-shadow: 0 0 16px var(--accent-line) }
.mbar:hover .mb  { filter: brightness(1.14) }
```

Clamp a hover popover on **both** axes or it will spill the card:

```js
tip.style.left = Math.min(cr.width - 114, Math.max(114, x)) + 'px';
tip.style.top  = Math.max(8, Math.min(cr.height - th - 8, want)) + 'px';
```

---

## 13. Two hover patterns, pick one per chart

**A. Nearest index from mouse fraction** (section 7 above). Best for dense series.

**B. Invisible dots that light up.** Every point gets a transparent circle; hover fills it. Per-point snap without drawing 30 visible dots.

```js
const dots = pts.map((p, i) =>
  '<circle class="gpt" data-i="' + i + '" cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="3.2"/>').join('');
```
```css
.gpt { fill: transparent; stroke: none; transition: .12s; }
.gpt.on { fill: #fff; stroke: var(--accent); stroke-width: 2.4; }
```

Converting a mouse position into viewBox space:

```js
const vb = svg.viewBox.baseVal;
const sx = (e.clientX - r.left) / r.width * vb.width;
```

---

## 14. The gotcha that will bite you

**Never put text inside an SVG that uses `preserveAspectRatio="none"`.** The stretch that makes the chart fill its container also stretches the letterforms horizontally. Axis labels go in HTML next to the SVG, not inside it.

```js
// X labels live in HTML, not inside the stretched SVG, so date text never distorts.
const xlabs = '<div class="chart-x"><span>' + pts[0].x + '</span>'
            + '<span>' + pts[mid].x + '</span><span>' + pts[last].x + '</span></div>';
```
```css
.chart-x { display: flex; justify-content: space-between; margin-top: 2px; padding: 0 4px;
  font-size: 10px; color: var(--muted); font-weight: 600; }
```

---

## 15. If you must use a chart library

Chart.js is the reasonable choice. Never ship its defaults. Theme everything from your CSS variables so one palette rules the page:

```js
const C = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

function chartOpts(extra) {
  return Object.assign({
    responsive: true, maintainAspectRatio: false,
    animation: { duration: 700, easing: 'easeOutQuart' },
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: C('--surface-2'), borderColor: C('--border'), borderWidth: 1,
        titleColor: C('--ink'), bodyColor: C('--ink-2'), padding: 10,
        callbacks: { label: c => `${c.dataset.label}: ${usd(c.parsed.y)}` },
      },
    },
    scales: {
      x: { grid: { display: false },          ticks: { color: C('--muted'), font: { size: 11 } } },
      y: { grid: { color: C('--border-2') },  ticks: { color: C('--muted'), font: { size: 11 }, callback: v => usdShort(v) } },
    },
  }, extra || {});
}
```

X gridlines off. Y gridlines faint. Legend off unless there are 2+ series. Y ticks formatted short. `borderRadius: 4` and `maxBarThickness: 30` on bars.

One more fix worth knowing: if you color bars per-item (to show selection), the legend swatch inherits the first item's color, which may be the dimmed one. Pin it:

```js
// Pin legend swatches to the true series colors, not the per-bar array.
generateLabels: () => [{ text: 'Revenue', fillStyle: C('--accent') }],
```

---

## 16. Write down why the chart is that shape

A one-line comment above each chart, explaining the form choice, is the cheapest quality signal in the whole file. It also stops the next person swapping a considered donut for a pie.

```js
/* A donut earns its place here because the question is composition, "what share
   came from where", across few categories, and the hole carries the total. The
   bars beside it stay: the donut answers share, the bars answer magnitude, and
   neither is good at both. */
```

```js
/* Ranked bars in one hue, not a pie: this is magnitude across 16 named things,
   and 16 pie slices is unreadable at any size. */
```
