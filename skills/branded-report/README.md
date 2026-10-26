# Branded Report skill

A Claude Code skill that turns your numbers and notes into a branded PDF report a client can read on their phone in two minutes: a one page project update, release notes, campaign results, a retrospective or postmortem. Claude writes a short spec, the bundled renderer lays it out (stat tiles, funnels, tables, bar charts, cards, an asks box, a running header and page numbers) and checks it for dashes, leftover placeholders, overflow and a stranded last page.

It ships in EZJ Online's brand. Swap in your own in one file.

![what it produces](https://raw.githubusercontent.com/ezjonline/ezj-automations/main/skills/branded-report/preview.png)

## Install

**Easiest:** open Claude Code and paste this:

```
Install the Claude Code skill from https://github.com/ezjonline/ezj-automations/tree/main/skills/branded-report into ~/.claude/skills/branded-report (copy the whole folder, including scripts, assets, references and examples), then render examples/campaign-retro.json with scripts/render.sh to prove it works.
```

**Or in a terminal:**

```bash
git clone --depth 1 https://github.com/ezjonline/ezj-automations /tmp/ezj-automations
mkdir -p ~/.claude/skills
cp -r /tmp/ezj-automations/skills/branded-report ~/.claude/skills/
rm -rf /tmp/ezj-automations
```

You need Python 3 (on a Mac: `xcode-select --install`). The first render sets up Playwright in `~/.cache/branded-report` by itself, about a minute, one time. If Google Chrome is installed it uses that, otherwise it downloads Chromium once.

## Use it

```
/branded-report make a results report for <client> from <where the numbers are>
```

If the command does not show up, say:

```
Read ~/.claude/skills/branded-report/SKILL.md and follow it to make a branded PDF report for <client> about <what>.
```

Render a spec by hand:

```bash
bash ~/.claude/skills/branded-report/scripts/render.sh path/to/report.json
```

## Your own brand

Pass a `brand` object in the spec, or edit `assets/brand.json`: name, website, accent colour, ink colour, a font file and two logos (one for dark backgrounds, one for light). Every block is documented in `references/blocks.md`.

## Files

| File | What it is |
|---|---|
| `SKILL.md` | The process Claude follows |
| `references/blocks.md` | Every block and field in a report spec |
| `scripts/render.sh` | Sets up Playwright once, then renders |
| `scripts/render.py` | Spec to HTML to PDF, plus the checks |
| `scripts/report.css` | The look |
| `assets/` | Brand file, Figtree font (SIL Open Font License), logos |
| `examples/` | A two page results report and a one page update |
