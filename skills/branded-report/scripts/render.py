#!/usr/bin/env python3
"""Turn a report spec (JSON) into a branded PDF, then check it.

    bash render.sh report.json              # normal use, sets up Playwright on first run
    python3 render.py report.json [--out file.pdf] [--html] [--allow-dashes]

Writes the PDF next to the JSON, named from "file_name" (else the title). Prints a summary.
Exit 0: clean. Exit 1: a check failed, the PDF is still written so you can look at it.
Exit 2: the spec or the machine is broken. Block reference: ../references/blocks.md
"""
import argparse
import base64
import json
import re
import subprocess
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
PAGE_SIZES = {"letter": "Letter", "a4": "A4"}
PAGE_WIDTH_PX = {"Letter": 816, "A4": 794}


class SpecError(Exception):
    pass


# ---------- inline text: **bold**, *italic*, ==accent==, [text](url) ----------

LINK = re.compile(r"\[([^\]]+)\]\(((?:https?://|mailto:)[^)\s\"]+)\)")
MARKS = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<b>\1</b>"),
    (re.compile(r"==(.+?)=="), r'<span class="hl">\1</span>'),
    (re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])"), r"<i>\1</i>"),
]


def md(text):
    if text is None:
        return ""
    s = escape(str(text), quote=False)
    s = LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    for rx, rep in MARKS:
        s = rx.sub(rep, s)
    return s.replace("\n", "<br>")


def plain(text):
    s = LINK.sub(lambda m: m.group(1), str(text or ""))
    return re.sub(r"\*\*|==|\*", "", s)


def need(b, key, kind):
    if key not in b:
        raise SpecError(f'"{kind}" block is missing "{key}": {json.dumps(b)[:120]}')
    return b[key]


def num(v, kind):
    try:
        return float(str(v).replace(",", ""))
    except ValueError:
        raise SpecError(f'"{kind}" value must be a number, got {v!r}')


def fmt(v):
    v = float(v)
    return f"{v:,.0f}" if v == int(v) else f"{v:,.1f}"


def pct(p):
    return f"{p:.1f}%" if p < 10 else f"{p:.0f}%"


def paras(b):
    items = b.get("paragraphs") or ([b["text"]] if b.get("text") else [])
    return "".join(f"<p>{md(t)}</p>" for t in items)


def dots(items, numbered=False):
    if not items:
        return ""
    tag, cls = ("ol", "nums") if numbered else ("ul", "dots")
    return f'<{tag} class="{cls}">' + "".join(f"<li>{md(i)}</li>" for i in items) + f"</{tag}>"


# ---------- blocks ----------

def r_heading(b, ctx):
    text = need(b, "text", "heading")
    n = b.get("number")
    if n is True:
        ctx["section"] += 1
        n = f"{ctx['section']:02d}"
    no = f'<span class="no">{escape(str(n))}</span>' if n else ""
    sub = f'<p class="sec-sub">{md(b["sub"])}</p>' if b.get("sub") else ""
    return f'<h2 class="sec">{no}{md(text)}</h2>{sub}'


def r_text(b, ctx):
    if not (b.get("text") or b.get("paragraphs")):
        raise SpecError('"text" block needs "text" or "paragraphs"')
    size = b.get("size", "body")
    return f'<div class="txt {escape(size)}">{paras(b)}</div>'


def r_bullets(b, ctx):
    return dots(need(b, "items", "bullets"), b.get("numbered", False))


def r_stats(b, ctx):
    items = need(b, "items", "stats")
    cols = b.get("columns") or min(len(items), 4)
    tiles = []
    for it in items:
        note = f'<div class="n">{md(it["note"])}</div>' if it.get("note") else ""
        tiles.append(f'<div class="tile{" dark" if it.get("accent") else ""}">'
                     f'<div class="v">{md(need(it, "value", "stats item"))}</div>'
                     f'<div class="l">{md(need(it, "label", "stats item"))}</div>{note}</div>')
    return f'<div class="stats" style="grid-template-columns:repeat({cols},1fr)">{"".join(tiles)}</div>'


def r_cards(b, ctx):
    items = need(b, "items", "cards")
    cols = b.get("columns", 2)
    out = []
    for c in items:
        cls = "card" + (" dark" if c.get("dark") else "") + (" full" if c.get("full") else "")
        tag = ""
        if c.get("tag"):
            tag = f'<span class="tag{" ghost" if c.get("tag_style") == "ghost" else ""}">{md(c["tag"])}</span>'
        title = f"<h3>{md(c['title'])}</h3>" if c.get("title") else ""
        out.append(f'<div class="{cls}">{tag}{title}{paras(c)}{dots(c.get("bullets"), c.get("numbered", False))}</div>')
    return f'<div class="cards" style="grid-template-columns:repeat({cols},1fr)">{"".join(out)}</div>'


NUMERIC = re.compile(r"^[\s$€£¥+\-−~≈(]*[0-9][0-9.,\s]*[%xX×kKmMbB)]*(\s*(of|/)\s*[0-9.,]+)?$")


def r_table(b, ctx):
    cols, rows = need(b, "columns", "table"), need(b, "rows", "table")
    for i, row in enumerate(rows):
        if len(row) != len(cols):
            raise SpecError(f'table row {i + 1} has {len(row)} cells, the header has {len(cols)}')
    align = b.get("align")
    if not align:
        align = ["left"]
        for i in range(1, len(cols)):
            cells = [str(r[i]).strip() for r in rows if str(r[i]).strip() not in ("", "-")]
            align.append("right" if cells and all(NUMERIC.match(plain(c)) for c in cells) else "left")
    th = "".join(f'<th class="{align[i]}">{md(c)}</th>' for i, c in enumerate(cols))
    trs = []
    for i, row in enumerate(rows):
        cls = ' class="total"' if b.get("total_row") and i == len(rows) - 1 else ""
        trs.append(f"<tr{cls}>" + "".join(f'<td class="{align[j]}">{md(v)}</td>' for j, v in enumerate(row)) + "</tr>")
    cap = f'<div class="cap">{md(b["title"])}</div>' if b.get("title") else ""
    note = f'<p class="note">{md(b["note"])}</p>' if b.get("note") else ""
    keep = " keep" if len(rows) <= 15 else ""
    return f'<figure class="tbl{keep}">{cap}<table><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>{note}</figure>'


def r_bars(b, ctx):
    items = need(b, "items", "bars")
    top = num(b["max"], "bars max") if b.get("max") else max(num(i["value"], "bars") for i in items) or 1
    rows = []
    for it in items:
        v = num(need(it, "value", "bars item"), "bars")
        w = max(0.0, min(100.0, v / top * 100))
        style = " muted" if it.get("muted") else (" ink" if it.get("ink") else "")
        rows.append(f'<div class="brow"><div class="bl">{md(need(it, "label", "bars item"))}</div>'
                    f'<div class="track"><div class="bar{style}" style="width:{w:.2f}%"></div></div>'
                    f'<div class="bv">{md(it.get("display", fmt(v)))}</div></div>')
    cap = f'<div class="cap">{md(b["title"])}</div>' if b.get("title") else ""
    note = f'<p class="note">{md(b["note"])}</p>' if b.get("note") else ""
    return f'<figure class="chart">{cap}{"".join(rows)}{note}</figure>'


def r_funnel(b, ctx):
    steps = need(b, "steps", "funnel")
    first = num(need(steps[0], "value", "funnel step"), "funnel") or 1
    rows, prev = [], None
    for s in steps:
        v = num(need(s, "value", "funnel step"), "funnel")
        rate = ""
        if prev:
            label = s.get("rate_label", "of the step above")
            rate = f'<span class="rate">{pct(v / prev * 100)} {md(label)}</span>'
        rows.append(f'<div class="brow"><div class="bl">{md(need(s, "label", "funnel step"))}{rate}</div>'
                    f'<div class="track"><div class="bar" style="width:{max(0.6, v / first * 100):.2f}%"></div></div>'
                    f'<div class="bv">{md(s.get("display", fmt(v)))}</div></div>')
        prev = v
    cap = f'<div class="cap">{md(b["title"])}</div>' if b.get("title") else ""
    note = f'<p class="note">{md(b["note"])}</p>' if b.get("note") else ""
    return f'<figure class="chart funnel">{cap}{"".join(rows)}{note}</figure>'


def r_callout(b, ctx):
    tone = b.get("tone", "soft")
    if tone not in ("soft", "orange", "dark"):
        raise SpecError(f'callout tone must be soft, orange or dark, got {tone!r}')
    title = f'<b class="ct">{md(b["title"])}</b>' if b.get("title") else ""
    return f'<div class="callout {tone}">{title}{paras(b)}{dots(b.get("bullets"))}</div>'


def r_asks(b, ctx):
    items = need(b, "items", "asks")
    cols = b.get("columns", 2 if len(items) > 3 else 1)
    lis = "".join(f"<li>{md(i)}</li>" for i in items)
    return (f'<div class="asks"><span class="tag">{md(b.get("title", "What we need from you"))}</span>'
            f'<ol style="grid-template-columns:repeat({cols},1fr)">{lis}</ol></div>')


def r_steps(b, ctx):
    out = []
    for n, s in enumerate(need(b, "items", "steps"), 1):
        code = f'<div class="code">{escape(s["code"])}</div>' if s.get("code") else ""
        body = f"<p>{md(s['text'])}</p>" if s.get("text") else ""
        out.append(f'<div class="step"><div class="num">{n}</div><div><h3>{md(need(s, "title", "steps item"))}</h3>{body}{code}</div></div>')
    return f'<div class="steps">{"".join(out)}</div>'


def r_quote(b, ctx):
    who = f'<div class="who">{md(b["who"])}</div>' if b.get("who") else ""
    return f'<blockquote class="quote"><p>{md(need(b, "text", "quote"))}</p>{who}</blockquote>'


def r_code(b, ctx):
    label = f'<div class="code-label">{md(b["label"])}</div>' if b.get("label") else ""
    return f'{label}<div class="code">{escape(need(b, "text", "code"))}</div>'


MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
        ".webp": "image/webp", ".svg": "image/svg+xml"}


def r_image(b, ctx):
    p = Path(need(b, "path", "image")).expanduser()
    p = p if p.is_absolute() else ctx["base"] / p
    if not p.exists():
        raise SpecError(f"image not found: {p}")
    mime = MIME.get(p.suffix.lower())
    if not mime:
        raise SpecError(f"image type not supported: {p.suffix} (use png, jpg, gif, webp or svg)")
    data = base64.b64encode(p.read_bytes()).decode()
    width = b.get("width", 100)
    cap = f"<figcaption>{md(b['caption'])}</figcaption>" if b.get("caption") else ""
    return f'<figure class="img"><img src="data:{mime};base64,{data}" style="width:{width}%" alt="{escape(plain(b.get("caption", "")))}">{cap}</figure>'


def r_columns(b, ctx):
    columns = need(b, "columns", "columns")
    widths = b.get("widths") or [1] * len(columns)
    grid = " ".join(f"{w}fr" for w in widths)
    here = ctx["p"]
    inner = "".join(f"<div>{render_blocks(col, ctx, here + '.' + str(i + 1))}</div>" for i, col in enumerate(columns))
    return f'<div class="cols" style="grid-template-columns:{grid}">{inner}</div>'


def r_sources(b, ctx):
    items = need(b, "items", "sources")
    return (f'<div class="sources"><h4>{md(b.get("title", "Where these numbers come from"))}</h4>'
            + "<ol>" + "".join(f"<li>{md(i)}</li>" for i in items) + "</ol></div>")


RENDER = {"heading": r_heading, "text": r_text, "bullets": r_bullets, "stats": r_stats, "cards": r_cards,
          "table": r_table, "bars": r_bars, "funnel": r_funnel, "callout": r_callout, "asks": r_asks,
          "steps": r_steps, "quote": r_quote, "code": r_code, "image": r_image, "columns": r_columns,
          "sources": r_sources}


def render_blocks(blocks, ctx, prefix=""):
    out, glue = [], False
    for i, b in enumerate(blocks):
        kind = b.get("type")
        if kind == "page_break":
            out.append('<div class="pb"></div>')
            continue
        if kind not in RENDER:
            raise SpecError(f"unknown block type {kind!r}. Known: {', '.join(sorted(RENDER))}, page_break")
        path = f"{prefix}.{i + 1}" if prefix else str(i + 1)
        ctx["p"] = path
        html = f'<div class="blk blk-{kind}" data-block="{path} {kind}">{RENDER[kind](b, ctx)}</div>'
        if glue:  # a heading never ends a page: it travels with the block under it
            out[-1] = f'<div class="keep">{out[-1]}{html}</div>'
        else:
            out.append(html)
        nxt = blocks[i + 1].get("type") if i + 1 < len(blocks) else None
        glue = kind == "heading" and nxt not in (None, "page_break")
    return "".join(out)


# ---------- page ----------

CSS = (HERE / "report.css").read_text() if (HERE / "report.css").exists() else ""


def css_str(s):
    return '"' + plain(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def load_brand(spec, base):
    brand = json.loads((ASSETS / "brand.json").read_text())
    root = {k: ASSETS for k in brand}
    for k, v in (spec.get("brand") or {}).items():
        brand[k], root[k] = v, base
    files = {}
    for key in ("font_file", "logo_on_dark", "logo_on_light"):
        p = Path(brand[key]).expanduser()
        p = p if p.is_absolute() else root[key] / p
        if not p.exists():
            raise SpecError(f"brand {key} not found: {p}")
        files[key] = p
    return brand, files


def build_html(spec, base, page_numbers):
    brand, files = load_brand(spec, base)
    size = PAGE_SIZES.get(str(spec.get("page_size", "Letter")).lower())
    if not size:
        raise SpecError('page_size must be "Letter" or "A4"')
    title = need(spec, "title", "report")
    blocks = need(spec, "blocks", "report")
    ctx = {"section": 0, "base": base, "p": ""}
    body = render_blocks(blocks, ctx)

    font = base64.b64encode(files["font_file"].read_bytes()).decode()
    ff = brand["font_family"]
    hero = spec.get("hero", "dark")
    kicker, date, who = spec.get("kicker", ""), spec.get("date", ""), spec.get("prepared_for", "")
    lede = f'<p class="lede">{md(spec["lede"])}</p>' if spec.get("lede") else ""
    if hero == "dark":
        line = " &nbsp;/&nbsp; ".join(md(x) for x in (kicker, date) if x)
        for_line = f'<div class="for">Prepared for <b>{md(who)}</b></div>' if who else ""
        head = (f'<header class="hero dark">{files["logo_on_dark"].read_text()}'
                f'<div class="kicker">{line}</div><h1>{md(title)}</h1>{lede}{for_line}</header>')
    elif hero == "light":
        meta = " · ".join(md(x) for x in (kicker, date) if x)
        head = (f'<header class="hero light"><div class="top">{files["logo_on_light"].read_text()}'
                f'<div class="meta"><b>{md(who)}</b><br>{meta}</div></div><h1>{md(title)}</h1>{lede}</header>')
    else:
        raise SpecError('hero must be "dark" or "light"')
    closing = f'<p class="closing">{md(spec["closing"])}</p>' if spec.get("closing") else ""

    if page_numbers:
        foot_l, foot_r = css_str(f"{brand['name']}  ·  {brand['website']}"), '"Page " counter(page) " of " counter(pages)'
    else:
        foot_l, foot_r = css_str(brand["name"]), css_str(brand["website"])
    top = f'font: 600 7.5pt "{ff}", sans-serif; color: rgba(13,13,13,.55); vertical-align: bottom;'
    bot = f'font: 500 7.8pt "{ff}", sans-serif; color: rgba(13,13,13,.6); vertical-align: top;'
    page_css = f"""
@font-face {{ font-family: "{ff}"; src: url(data:font/ttf;base64,{font}) format("truetype"); font-weight: 100 900; }}
:root {{ --accent: {brand['accent']}; --ink: {brand['ink']}; --paper: {brand['paper']}; --soft: {brand['soft']}; --ff: "{ff}"; }}
@page {{ size: {size}; margin: 0.55in 0 0.62in;
  @top-left {{ content: {css_str(title)}; {top} padding: 0 0 9pt 0.6in; }}
  @top-right {{ content: {css_str(who or brand['name'])}; {top} padding: 0 0.6in 9pt 0; text-align: right; }}
  @bottom-left {{ content: {foot_l}; {bot} padding: 12pt 0 0 0.6in; }}
  @bottom-right {{ content: {foot_r}; {bot} padding: 12pt 0.6in 0 0; text-align: right; }} }}
@page :first {{ margin-top: 0; @top-left {{ content: none; }} @top-right {{ content: none; }} }}
"""
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{escape(plain(title))}</title>'
            f"<style>{page_css}{CSS}</style></head><body>{head}<main class=\"wrap\">{body}{closing}</main></body></html>"), size


# ---------- checks on the words ----------

DASH = re.compile(r"[—–]|\s-{1,2}\s|^-{1,2}\s|\s--|--\s")
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b|lorem ipsum|\{\{|\}\}|\[\[|\]\]|PLACEHOLDER|<insert", re.I)
SKIP_KEYS = {"type", "tone", "tag_style", "align", "path", "file_name", "page_size", "hero", "brand", "size", "widths"}
URL = re.compile(r"(https?://|mailto:)\S+")


def walk(node, where="", in_code=False):
    if isinstance(node, dict):
        code = node.get("type") == "code"
        for k, v in node.items():
            if k in SKIP_KEYS or (code and k == "text") or k == "code":
                continue
            yield from walk(v, f"{where}.{k}" if where else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{where}[{i}]")
    elif isinstance(node, str):
        yield where, node


def word_checks(spec, allow_dashes):
    fails = []
    for where, s in walk(spec):
        t = URL.sub("", s)
        if not allow_dashes and DASH.search(t):
            fails.append(f"dash used as punctuation at {where}: {s[:90]!r}")
        if PLACEHOLDER.search(t):
            fails.append(f"placeholder left in at {where}: {s[:90]!r}")
    return fails


# ---------- browser ----------

def launch(p):
    tried = []
    for kw in ({}, {"channel": "chrome"}, {"channel": "msedge"}):
        try:
            return p.chromium.launch(**kw)
        except Exception as e:  # noqa: BLE001, a missing browser raises a plain Error
            tried.append(str(e).splitlines()[0][:120])
    print("No browser found. Installing Playwright's Chromium once (about 150 MB)...", file=sys.stderr)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    return p.chromium.launch()


LAYOUT_JS = """() => {
  const over = [];
  document.querySelectorAll('[data-block]').forEach(el => {
    if (el.scrollWidth > el.clientWidth + 2) over.push(el.dataset.block);
  });
  return { font: document.fonts.check('700 12px ' + getComputedStyle(document.documentElement).getPropertyValue('--ff')),
           over };
}"""


def page_texts(pdf):
    """Text of each page, or None when pypdf is not installed (then only the page count is known)."""
    try:
        from io import BytesIO
        from pypdf import PdfReader
    except ImportError:
        return None
    return [pg.extract_text() or "" for pg in PdfReader(BytesIO(pdf)).pages]


def page_count(pdf):
    found = re.findall(rb"/Type\s*/Page(?![a-zA-Z])", pdf)
    if found:
        return len(found)
    counts = [int(c) for c in re.findall(rb"/Count\s+(\d+)", pdf)]
    return max(counts) if counts else 0


def body_chars(text, chrome):
    for s in chrome:
        text = text.replace(s, "")
    text = re.sub(r"Page \d+ of \d+", "", text)
    return len(re.sub(r"\s+", "", text))


def to_pdf(browser, html, size):
    page = browser.new_page(viewport={"width": PAGE_WIDTH_PX[size], "height": 1100})
    page.emulate_media(media="print")
    page.set_content(html, wait_until="load")
    page.evaluate("() => document.fonts.ready.then(() => true)")
    layout = page.evaluate(LAYOUT_JS)
    pdf = page.pdf(prefer_css_page_size=True, print_background=True)
    page.close()
    return pdf, layout


def main():
    ap = argparse.ArgumentParser(description="Render a branded PDF report from a JSON spec.")
    ap.add_argument("spec")
    ap.add_argument("--out", help="PDF path. Default: next to the JSON, named from file_name or title.")
    ap.add_argument("--html", action="store_true", help="Also write the HTML next to the PDF, for debugging.")
    ap.add_argument("--allow-dashes", action="store_true", help="Skip the no-dashes check.")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is missing. Run: bash render.sh <spec.json> (it sets itself up).", file=sys.stderr)
        return 2

    spec_path = Path(args.spec).expanduser().resolve()
    try:
        spec = json.loads(spec_path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"Cannot read the spec: {e}", file=sys.stderr)
        return 2
    base = spec_path.parent
    name = re.sub(r'[\\/:*?"<>|]+', "", plain(spec.get("file_name") or spec.get("title", "report"))).strip() or "report"
    out = Path(args.out).expanduser().resolve() if args.out else base / f"{name}.pdf"

    try:
        html, size = build_html(spec, base, page_numbers=True)
        fails = word_checks(spec, args.allow_dashes)
        with sync_playwright() as p:
            browser = launch(p)
            pdf, layout = to_pdf(browser, html, size)
            pages = page_count(pdf)
            if pages == 1:
                html, size = build_html(spec, base, page_numbers=False)
                pdf, layout = to_pdf(browser, html, size)
            browser.close()
    except SpecError as e:
        print(f"Spec problem: {e}", file=sys.stderr)
        return 2

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(pdf)
    if args.html:
        out.with_suffix(".html").write_text(html)

    warns = []
    if not layout["font"]:
        warns.append("brand font did not load, the PDF fell back to a system font")
    texts = page_texts(pdf)
    if texts and pages > 1:
        brand, _ = load_brand(spec, base)
        chrome = [plain(spec.get("title", "")), plain(spec.get("prepared_for", "")), brand["name"], brand["website"], "·"]
        left = body_chars(texts[-1], chrome)
        if left < 300:
            fails.append(f"the last page holds only {left} characters. Trim, tighten or reorder so the report "
                         f"ends on page {pages - 1}, or add enough that page {pages} earns its place")
    for blk in layout["over"]:
        fails.append(f"block {blk} is wider than the page (shorten the text or cut a column)")

    print(f"PDF: {out}")
    print(f"Pages: {pages}")
    for w in warns:
        print(f"WARN {w}")
    for f in fails:
        print(f"FAIL {f}")
    print("Next: open the PDF and look at every page." if not fails else "Fix the FAIL lines in the JSON and render again.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
