#!/usr/bin/env node
// Checks a handoff doc before it gets shared.
//
//   node check.mjs path/to/index.html              run every check
//   node check.mjs path/to/index.html --fix-logo   put the real EZJ logo back, then check
//   node check.mjs --build-template                inject the logo into template/handoff.html
//
// Exit code 0 means PASS. Anything else means fix what it printed and run it again.

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '..');
// The EZJ Online logo, locked 2026-09-30: the orange mark plus "EZJ Online", drawn inline as SVG.
// Both asset files are verbatim copies of the brand kit. The words take the text color, white here.
const LOGO_FILE = join(ROOT, 'assets', 'ezj-online-logo-inline.html');
const LOGO_SVG = readFileSync(LOGO_FILE, 'utf8').trim();
const LOGO_CSS = [readFileSync(join(ROOT, 'assets', 'ezj-online-logo-inline.css'), 'utf8').trim(), '.by .ezj-lockup{height:28px;color:#fff}'];
const LOGO_RE = /<svg\b[^>]*class="ezj-lockup"[^>]*>[\s\S]*?<\/svg>/i;
// Retired logos: the brush "EZJ ONLINE" image and the gradient app icon. Never ship them.
const OLD_LOGO_RE = /<img\b[^>]*class="logo"[^>]*>/i;
const OLD_LOGO_DATA = /iVBORw0KGgoAAAANSUhEUgAAAoAAAABZ|iVBORw0KGgoAAAANSUhEUgAAAdAAAAHPC/;
const OLD_IMG_RE = new RegExp(`<img\\b[^>]*(class="logo"|src="data:image/png;base64,(${OLD_LOGO_DATA.source}))[^>]*>`, 'gi');
const squash = s => s.replace(/\s+/g, '');

// Puts the real logo and its size rule in, replacing a retired, damaged or missing one.
function fixLogo(html) {
  if (LOGO_RE.test(html)) html = html.replace(LOGO_RE, () => LOGO_SVG);
  else if (OLD_LOGO_RE.test(html)) html = html.replace(OLD_LOGO_RE, () => LOGO_SVG);
  else if (html.includes('__EZJ_LOGO__')) html = html.replace('__EZJ_LOGO__', () => LOGO_SVG);
  else html = html.replace(/<div class="by">/, m => m + LOGO_SVG);
  html = html.replace(OLD_IMG_RE, '');
  html = html.replace('retype, or move this img.', 'retype, or move this svg.');
  const missing = LOGO_CSS.filter(r => !squash(html).includes(squash(r)));
  if (missing.length) {
    const old = /^( *)\.by img\.logo \{[^}]*\}[ \t]*$/m;
    html = old.test(html)
      ? html.replace(old, (m, sp) => missing.map(r => sp + r).join('\n'))
      : html.replace('</style>', () => missing.map(r => '  ' + r).join('\n') + '\n</style>');
  }
  return html;
}

const args = process.argv.slice(2);

if (args.includes('--build-template')) {
  const t = join(ROOT, 'template', 'handoff.html');
  const html = readFileSync(t, 'utf8');
  const fixed = fixLogo(html);
  if (fixed === html) { console.log('template already has the logo embedded'); process.exit(0); }
  writeFileSync(t, fixed);
  console.log('logo embedded into template/handoff.html');
  process.exit(0);
}

const file = args.find(a => !a.startsWith('--'));
if (!file || !existsSync(file)) {
  console.error('usage: node check.mjs path/to/index.html [--fix-logo]');
  process.exit(2);
}
let html = readFileSync(file, 'utf8');

if (args.includes('--fix-logo')) {
  html = fixLogo(html);
  writeFileSync(file, html);
  console.log('logo restored');
}

const fails = [];
const warns = [];
const fail = m => fails.push(m);
const warn = m => warns.push(m);

// 1. Logo: inline, character for character the brand kit's. A path to a file breaks the moment the page moves.
const logos = html.match(new RegExp(LOGO_RE.source, 'gi')) || [];
if (OLD_LOGO_RE.test(html) || OLD_LOGO_DATA.test(html)) fail('The old EZJ logo is in the page. It is retired. Run with --fix-logo.');
if (!logos.length) fail('No logo. The <svg class="ezj-lockup"> in the header is missing. Run with --fix-logo.');
else if (logos.some(s => s !== LOGO_SVG)) fail('Logo is not the real EZJ Online logo (edited or damaged). Run with --fix-logo.');
else if (LOGO_CSS.some(r => !squash(html).includes(squash(r)))) fail('The logo size rule is missing from the <style>, so the logo shows at the wrong size. Run with --fix-logo.');

// 2. One self contained file. Images must be embedded. Only Google Fonts may load from outside.
for (const m of html.matchAll(/<(img|script|link|source|video|audio|iframe)\b[^>]*?\s(src|href)="([^"]*)"/gi)) {
  const [, tagName, , url] = m;
  const t = tagName.toLowerCase();
  if (url.startsWith('data:')) continue;
  if (t === 'link' && /^https:\/\/fonts\.(googleapis|gstatic)\.com(\/|$)/.test(url)) continue;
  if (t === 'iframe' && /^https:\/\/(www\.)?loom\.com\/embed\//.test(url)) continue;
  fail(`<${t}> loads "${url.slice(0, 80)}". Embed it as a data: URI or remove it. Files next to the page break when it moves.`);
}

// Everything below scans the page with embedded data stripped, so base64 noise never matches.
const bare = html.replace(/data:[a-z]+\/[a-z0-9.+-]+;base64,[A-Za-z0-9+\/=]+/gi, 'data:');

// 3. Example content from the template left behind.
for (const s of ['Harbor Dental', 'Alex Morgan', 'EXAMPLE', '__EZJ_LOGO__', 'harbor-text-back', '(555) 010', 'TODO', 'TBD', 'lorem']) {
  if (bare.includes(s)) fail(`Template placeholder still in the page: "${s}". Replace it with a real fact from this project.`);
}
if (/LOOM_LINK_NEEDED/.test(bare)) fail('The Loom link is still LOOM_LINK_NEEDED. Record the Loom (5 minutes max) and paste the real link.');

// 4. Required parts.
if (!/<title>[^<]{4,}<\/title>/.test(html)) fail('Missing a real <title>.');
if (!/name="robots" content="noindex"/.test(html)) fail('Missing <meta name="robots" content="noindex">. Handoff docs stay out of Google.');
if (!/<h1[\s>]/.test(html)) fail('Missing the h1 project name in the hero.');
if (!/LOOM_LINK_NEEDED/.test(bare) && !/href="https:\/\/(www\.)?loom\.com\/(share|embed)\/[A-Za-z0-9]+/.test(html)) fail('No Loom link. Every handoff doc links a Loom walkthrough (loom.com/share/...). Ask the dev for it.');
if (!/id="how"/.test(html)) fail('Missing the How it works section (id="how").');
if (!/id="status"/.test(html)) fail('Missing the Status section (id="status").');
if (!/class="(rail|routes|lanes|pipe)"/.test(html)) fail('No diagram. How it works needs at least one rail, routes, lanes, or pipe.');
if (!/github\.com\/[^"]+\/pull\/\d+/.test(html)) warn('No pull request link found. Add the PR button unless this delivery has no PR.');

// 5. Secrets. Names of settings are fine, values never are.
const secretPatterns = [
  [/sk-(ant-|proj-)?[A-Za-z0-9_-]{20,}/, 'an OpenAI or Anthropic key'],
  [/xox[abprs]-[A-Za-z0-9-]{10,}/, 'a Slack token'],
  [/hooks\.slack\.com\/services\/[A-Z0-9]+\/[A-Z0-9]+\/[A-Za-z0-9]+/, 'a Slack webhook URL'],
  [/gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}/, 'a GitHub token'],
  [/AKIA[0-9A-Z]{16}/, 'an AWS key'],
  [/-----BEGIN [A-Z ]*PRIVATE KEY-----/, 'a private key'],
  [/eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}/, 'a JWT'],
  [/\b(re|rk|pk|sk)_(live|test)_[A-Za-z0-9]{16,}/, 'a Stripe or Resend key'],
  [/\bAC[a-f0-9]{32}\b/, 'a Twilio account SID'],
  [/[?&](secret|token|key|s|sig|password)=[A-Za-z0-9_\-]{16,}/i, 'a secret inside a URL'],
];
for (const [re, what] of secretPatterns) {
  if (re.test(bare)) fail(`Looks like ${what} is in the page. Remove the value, keep only the setting name and where to get it.`);
}

// 6. Visible text: dashes as punctuation, length.
const text = bare
  .replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<script[\s\S]*?<\/script>/gi, ' ')
  .replace(/<code[\s\S]*?<\/code>/gi, ' ')
  .replace(/<!--[\s\S]*?-->/g, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&[a-z]+;/g, ' ')
  .replace(/\s+/g, ' ');
if (/[\u2014\u2013]/.test(text)) fail('Em or en dash found in the text. Use a period or a comma instead.');
const spaced = text.match(/\S+ - \S+/g);
if (spaced) fail(`Hyphen used as punctuation: "${spaced[0]}". Use a period or a comma.`);
const words = text.trim().split(' ').filter(w => /[A-Za-z0-9]/.test(w)).length;
if (words > 1800) warn(`${words} words. Aim for 700 to 1,500 so Ethan reads it in about 5 minutes. Cut.`);
if (words < 250) warn(`${words} words. That is probably too thin to set this up from the doc alone.`);

const kb = Math.round(Buffer.byteLength(html) / 1024);
if (kb > 600) warn(`${kb} KB. Big embedded images slow the page. Shrink or drop them.`);

// Skill freshness: the branding lives in the public repo. An installed copy never updates
// itself, so a developer can keep shipping an old logo forever. Compare the logo bytes
// against the canonical copy and say so. Network trouble warns, it never blocks a delivery.
// assets/ezj-logo-white.png is not used any more. It stays in the repo holding the new logo,
// so copies installed before 2026-10-01 (which compare that file) fail and get reinstalled.
const CANON = 'https://raw.githubusercontent.com/ezjonline/ezj-automations/main/skills/ezj-handoff-doc/assets/ezj-online-logo-inline.html';
try {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), 6000);
  const res = await fetch(CANON, { signal: ac.signal });
  clearTimeout(t);
  if (res.ok) {
    const canonBytes = Buffer.from(await res.arrayBuffer());
    const mine = readFileSync(LOGO_FILE);
    if (!canonBytes.equals(mine)) {
      fail('Your installed copy of this skill has an out of date EZJ logo. Reinstall it, then run this again:\n'
        + '        Reinstall the Claude Code skill from https://github.com/ezjonline/ezj-automations/tree/main/skills/ezj-handoff-doc\n'
        + '        into ~/.claude/skills/ezj-handoff-doc, replacing what is there, then rebuild this doc from the new template.');
    }
  } else {
    warn(`Could not check the skill is up to date (GitHub returned ${res.status}). Carry on.`);
  }
} catch {
  warn('Could not reach GitHub to check the skill is up to date. Carry on.');
}

console.log(`\nHandoff doc check: ${file}`);
console.log(`${words} words, ${kb} KB\n`);
for (const f of fails) console.log('FAIL  ' + f);
for (const w of warns) console.log('WARN  ' + w);
if (fails.length) { console.log(`\n${fails.length} failed. Fix them and run again.`); process.exit(1); }
console.log('\nPASS' + (warns.length ? ' (read the warnings)' : ''));
