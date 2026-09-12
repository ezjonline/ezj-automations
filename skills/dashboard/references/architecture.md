# Architecture: how a dashboard should actually be built

The default is boring on purpose, and it is why these ship fast and never rot.

**A script pulls the data, renders one self-contained HTML file, and that file gets served statically.**

No React. No build toolchain. No API the page depends on at runtime. One file you can email, open with a double click, host anywhere, and archive as a permanent record of what the numbers were that day.

---

## The pipeline

```
source APIs / CSV / DB
        |
   fetch + normalize          (Python, one script)
        |
   data/data.json             (the contract, human readable)
        |
   render into template       (string replace, not a framework)
        |
   dist/index.html            (self-contained, ~200KB to 3MB)
        |
   deploy                     (Vercel, S3, any static host, or just open it)
```

Dependencies for the whole thing:

```
httpx>=0.27
jinja2>=3.1
```

You often do not even need Jinja. A `str.replace` on two placeholders is enough and it keeps the template a valid, openable HTML file during development.

---

## Data reaches the page as a baked-in JSON blob

```html
<script id="report-data" type="application/json">{{DATA_JSON}}</script>
```

```python
def render(data: dict) -> None:
    tpl  = (REPO / "templates" / "dashboard.html").read_text()
    logo = (REPO / "templates" / "logo.svg").read_text()
    blob = json.dumps(data).replace("</", "<\\/")      # cannot break out of the script tag
    html = tpl.replace("{{DATA_JSON}}", blob).replace("{{LOGO_SVG}}", logo)
    (REPO / "dist" / "index.html").write_text(html)
```

```js
const DATA = JSON.parse(document.getElementById('report-data').textContent.trim());
```

That `.replace("</", "<\\/")` is not optional. Without it a string in the data containing `</script>` ends the script tag and breaks the page, or worse.

**The payoff:** there is no loading state, because there is nothing to load. No spinner, no skeleton, no flash of empty chart, no CORS, no API key in the client, no 3am page that went blank because an upstream service is down. The numbers were true at build time and the page says exactly when that was.

Use a live fetch only when the dashboard genuinely needs to be real-time. Most do not. "Refreshed every morning at 6" covers almost every internal dashboard and client report ever asked for.

---

## Design the data contract first

Write the JSON shape before you write a single line of HTML. It is the actual spec.

```json
{
  "generated_at": "2026-09-12T06:00:12Z",
  "ref_date": "2026-09-11",
  "currency": "USD",
  "window_labels": { "yesterday": "Yesterday", "this_week": "This week", "90d": "Last 90 days" },
  "window_days":   { "yesterday": 1, "this_week": 6, "90d": 90 },
  "entities": [ { "id": "acme", "name": "Acme Co", "avatar": null } ],
  "daily":   { "ALL": [ { "date": "2026-08-28", "net": 135036, "subs": 92 } ] },
  "windows": { "90d": { "total": { "metrics": {}, "prev_metrics": {}, "delta": {} } } }
}
```

Rules that save you later:

1. **Money as integer cents.** Divide by 100 at render time only. Never store money as a float.
2. **Labels live in the data, not the template.** The UI builds its own filter pills from `Object.keys(DATA.window_labels)`, so adding a time window is a pipeline change with zero frontend edits.
3. **Precompute deltas server side.** Ship `metrics`, `prev_metrics` and `delta` together. The page should never guess at a comparison period.
4. **Additive vs non-additive metrics.** Sums (revenue, new signups) can be added across days. Uniques (unique visitors, unique buyers, active users) cannot, ever. Compute those at the exact window level in the pipeline or you will overcount and publish a wrong number with total confidence.
5. **Stamp `generated_at`.** Then show it on the page.

---

## State and rendering, without a framework

One state object, one render function, re-render on change. This scales much further than people expect.

```js
const state = { win: '90d', view: 'overview', id: null, sort: 'net', dir: -1 };

function render() {
  document.getElementById('app').innerHTML =
      header() + kpiRail() + heroChart() + breakdown() + table();
  wire();        // rebind listeners on the fresh DOM
  countUp();     // animate the numbers in
}
```

Deep links for free, no router:

```js
if (location.hash.indexOf('#id=') === 0) { state.view = 'detail'; state.id = location.hash.slice(4); }
```

Embed mode for nesting one dashboard in another:

```js
const EMBED = new URLSearchParams(location.search).get('embed') === '1';
if (EMBED) app.classList.add('embed');   // .embed .sidebar { display:none }
```

---

## Password gating without a backend

When a dashboard holds client revenue and lives on a public URL, encrypt the data blob at build time. The page source then carries ciphertext, not numbers. Same template serves gated and ungated builds, decided by one flag in the payload.

Build side:

```python
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pw.encode())
ct  = AESGCM(key).encrypt(iv, data_json.encode("utf-8"), None)
gate = {"__gate__": True, "iter": ITER,
        "salt": b64(salt), "iv": b64(iv), "ct": b64(ct)}
```

Browser side, Web Crypto only, no library:

```js
async function decryptGate(g, pw) {
  const enc = new TextEncoder();
  const b = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
  const km  = await crypto.subtle.importKey('raw', enc.encode(pw), 'PBKDF2', false, ['deriveKey']);
  const key = await crypto.subtle.deriveKey(
      { name:'PBKDF2', salt:b(g.salt), iterations:g.iter, hash:'SHA-256' },
      km, { name:'AES-GCM', length:256 }, false, ['decrypt']);
  const pt = await crypto.subtle.decrypt({ name:'AES-GCM', iv:b(g.iv) }, key, b(g.ct));
  return JSON.parse(new TextDecoder().decode(pt));
}

(function init(){
  const parsed = JSON.parse(document.getElementById('report-data').textContent.trim());
  if (parsed && parsed.__gate__) showGate(parsed);
  else { DATA = parsed; boot(); }
})();
```

Blur the page behind the prompt so the shape is visible but the numbers are not:

```css
.locked { filter: blur(9px); pointer-events: none; user-select: none; }
```

Be honest about the threat model. This stops a link being forwarded and read. It is not defence against someone determined with the file and time. Real secrets need a real backend.

---

## Export to PDF with zero libraries

Build a print-optimized deck as an HTML string, drop it into a hidden iframe, call print.

```js
function exportDeck() {
  let f = document.getElementById('deckframe');
  if (!f) {
    f = document.createElement('iframe');
    f.id = 'deckframe';
    f.setAttribute('style', 'position:fixed;width:0;height:0;border:0;right:0;bottom:0;opacity:0');
    document.body.appendChild(f);
  }
  f.onload = () => setTimeout(() => { f.contentWindow.focus(); f.contentWindow.print(); }, 150);
  f.srcdoc = deckHTML();
}
```

```css
@page { size: 13.333in 7.5in; margin: 0 }        /* 16:9 slide */
* { -webkit-print-color-adjust: exact; print-color-adjust: exact }   /* keep the dark theme */
.slide { page-break-after: always }
```

Or reshape the live dashboard for paper instead of maintaining a second page:

```css
@media print {
  @page { size: 13.333in 7.5in; margin: .5in .55in }
  .sidebar, .topbar, .filters { display: none !important }
  .printhead { display: flex !important }        /* a header that only exists on paper */
  .kpi-rail { grid-template-columns: repeat(4, 1fr) !important }
  .card, .chart, tr { break-inside: avoid }
}
```

---

## Scheduling and the rule nobody follows

Run the pipeline on a cron (Railway cron service, GitHub Actions, launchd, anything). Then do the part people skip:

**"The scheduler is loaded" is not "the job ran."** Wrap the job so it reports success, failure, and a mid-way kill.

```bash
STEP="start"
trap 'rc=$?; ./notify.py --rc "$rc" --step "$STEP" --log "$LOG"' EXIT
STEP="fetch";   python scripts/pull.py
STEP="render";  python scripts/render.py
STEP="deploy";  vercel --prod --yes --token "$VERCEL_TOKEN"
```

Silence is what lets a dashboard quietly go stale for a week while everyone keeps reading last Tuesday's numbers.

**Matching honesty rule for the freshness label.** The page may only say "Updated daily" once the loop has actually been verified end to end. Until then it says "Data through <date>". A dashboard that lies about its own freshness is worse than no dashboard.
