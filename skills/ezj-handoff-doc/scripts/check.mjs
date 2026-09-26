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
const LOGO_PNG = join(ROOT, 'assets', 'ezj-logo-white.png');
const LOGO_URI = 'data:image/png;base64,' + readFileSync(LOGO_PNG).toString('base64');
const LOGO_TAG_RE = /<img\b[^>]*class="logo"[^>]*>/i;

const args = process.argv.slice(2);

if (args.includes('--build-template')) {
  const t = join(ROOT, 'template', 'handoff.html');
  const html = readFileSync(t, 'utf8');
  if (!html.includes('__EZJ_LOGO__')) { console.log('template already has the logo embedded'); process.exit(0); }
  writeFileSync(t, html.replace('__EZJ_LOGO__', LOGO_URI));
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
  const tag = '<img class="logo" src="' + LOGO_URI + '" alt="EZJ Online" width="158" height="22">';
  if (LOGO_TAG_RE.test(html)) html = html.replace(LOGO_TAG_RE, tag);
  else html = html.replace(/<div class="by">/, '<div class="by">' + tag);
  writeFileSync(file, html);
  console.log('logo restored');
}

const fails = [];
const warns = [];
const fail = m => fails.push(m);
const warn = m => warns.push(m);

// 1. Logo: embedded, byte for byte the real file. A path to a file breaks the moment the page moves.
const logoTag = html.match(LOGO_TAG_RE);
if (!logoTag) fail('No logo. The <img class="logo"> in the header is missing. Run with --fix-logo.');
else {
  const src = (logoTag[0].match(/src="([^"]*)"/) || [])[1] || '';
  if (src !== LOGO_URI) fail('Logo is not the real embedded EZJ logo (wrong file, a path, or damaged data). Run with --fix-logo.');
}

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
const CANON = 'https://raw.githubusercontent.com/ezjonline/ezj-automations/main/skills/ezj-handoff-doc/assets/ezj-logo-white.png';
try {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), 6000);
  const res = await fetch(CANON, { signal: ac.signal });
  clearTimeout(t);
  if (res.ok) {
    const canonBytes = Buffer.from(await res.arrayBuffer());
    const mine = readFileSync(LOGO_PNG);
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
