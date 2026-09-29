---
name: overlay-assistant
description: Adds on-screen overlay annotations to video scripts directly inside a Notion content calendar. Reads a script row, works out where overlays genuinely belong based on the video's visual approach (selective, never one per line), reuses entries from the creator's own overlay bank where they fit, drafts new ones in the creator's voice from a Brand Brain where they do not, flags rather than inventing, and writes them inline so the editor can build the graphics. Use when someone says "do the overlays for this video", "annotate this script", "add the overlays", "/overlay-assistant", or pastes a Notion link to a script. Do not use for writing scripts, hooks or captions, designing graphics, or publishing.
---

# Overlay Assistant

Deciding and writing every overlay is often the slowest part of a creator's week. This turns it into a
review pass. It edits the script **in place** in the Notion content calendar. The creator reviews in
Notion. The editor's workflow does not change.

The single most important thing this skill gets right is **selectivity**. Good creators do not overlay
every line. They overlay only where a visual adds something the words cannot. A 10 step process might
get 3 overlays, a screen recording video 1, a story 0.

## Setup (once)

1. **Fill the Brand Brain.** Read `references/brand-brain/README.md`, then fill:
   - `references/brand-brain/examples.md`, where your scripts live, your overlay bank link, your
     annotation color, your formats with overlay counts, and two or three scripts you already
     annotated. This is what calibrates the skill to you.
   - `references/brand-brain/voice.md`, how you write. Register C (on-screen and social) is the one
     overlays use.
   - `references/brand-brain/offers.md`, only needed if overlays ever name a product.
2. **Connect Notion.** In Claude, turn on the Notion connector and give it access to your content
   calendar and your overlay bank.
3. **First run checks.** The first time it runs, the skill confirms setup before any work. If a check
   fails, it stops and explains in plain language, it does not guess:
   - A Notion tool is available. If not: "I need Notion connected first. Open your connectors
     settings, turn on Notion, give it access to your content calendar, then paste me a script link."
   - It can open a pasted script link and see the Script block and the row's Format.
   - It can edit that page.
   - The row matches the scaffold in `examples.md`. If it looks different, say what it sees and ask.

   Only start once read and write are both confirmed. Skip these on later runs.

If `examples.md` is still the template, run with the defaults in `references/placement-rules.md`, skip
bank reuse, and say in the report which setup is missing.

## Read before annotating

- `references/placement-rules.md`, archetypes, density, selectivity, type by archetype, color.
- `references/annotation-format.md`, the scaffold, the three annotation types, the write format.
- `references/drafting-and-reuse.md`, drafting quality and the reuse, draft or flag decision.
- `references/brand-brain/examples.md`, your real annotated scripts and setup.

## Process

1. **Read and orient.** Open the row. Read Format, Category, Goal, Pillar (whatever properties
   `examples.md` lists), and the Script block. Then three things that govern everything else:
   - **Global overlay instruction.** A note at the top of the Script like "put the screen recording on
     top of my head". If present: never delete or reword it, treat it as the video's primary visual
     treatment (usually meaning FEW inline overlays), and restate it in the report.
   - **Existing annotations and their color.** Detect overlays already on the page (colored spans,
     "Make an overlay" toggles) so you never duplicate them, and note the color to match it.
   - **The overlay bank.** Once per run, open the bank linked in `examples.md` and read it live,
     including its sub-pages. Reading it live every run means new entries are always available.

2. **Set density from the video's VISUAL APPROACH**, not from category or step count. Classify the
   archetype with `references/placement-rules.md`, reading Format first:
   - Voiceover plus B-roll, series, continuous screen recording → ~1 inline overlay. A bulleted list of
     steps in the script is NOT a list of overlays.
   - Storytelling, lifestyle, connection → 0 to very few.
   - Talking head teaching, decided by content: walkthrough ~10 `[PUT PIC N]`, process ~3, value-teaching ~8.

   Use the counts from the formats table in `examples.md` when it is filled.

3. **Segment into beats.** Break the spoken script into beats.

4. **Place selectively.** For each beat, place an overlay only where a visual adds something the spoken
   words cannot convey. Skip narrative, transitions, opinion, motivation, and any purely verbal step.
   A list inside one beat is ONE overlay, never one per item. When in doubt, leave it clean.
   Under-annotating is closer to how good creators work than over-annotating.

5. **Choose the type and fill it.** Match the type to the archetype, do not default to all three:
   walkthrough, process and series get director notes only; value-teaching gets `Text on screen:`
   labels, director notes, and a toggle only for genuine lists. Then for each placement, per
   `references/drafting-and-reuse.md`: **reuse** a relevant bank entry first, **draft new** where the
   bank has nothing and the content is derivable from the script, **flag** where a real fact or a
   named asset is needed and you do not have it. The result is a mix, never the whole bank.

6. **Write back.** Insert the annotations inline in the Script block, in the detected color (or the
   default, and say so), at the chosen beats. Leave the spoken script untouched.

7. **Report** in the output format below. If you used the default color, ask the creator to confirm.

## Output format

```
OVERLAYS: <video title>
Archetype: <archetype>, because <one line>
Placed: <n> (reused <n>, new <n>, flagged <n>)
Color: <color> (<matched existing | default, confirm?>)
Global instruction: <quoted, honored | none>
Flags: <each flagged line and what is needed>
Setup: <complete | what is missing in the Brand Brain>
```

## Example

User pastes a Notion link to a row with Format "Talking head", a script teaching five editing tricks,
and a clean Script block. Claude opens it, finds no global instruction and no existing annotations,
reads the overlay bank, and classifies it as value-teaching (five distinct lessons, each helped by a
title and a demo). It places 6 overlays: five `Text on screen:` labels, one per trick, plus one toggle
for the spoken list of export settings. Two labels reuse bank entries, the rest are new. The line "use
my favourite transition" names nothing specific, so it writes `[reference your own transition here]`
instead of inventing one. It writes in the default color and reports: "value-teaching, 6 placed (2
reused, 3 new, 1 flagged), wrote in pink, tell me if this one should be different."

## Never do

- Never edit, reword, reorder or delete the spoken script, hook, or caption. Only add overlays in the
  Script block.
- Never over-annotate. Density comes from the visual approach, not from step or list count.
- Never drop or overwrite a global overlay instruction at the top of the script.
- Never invent facts or assets: no fabricated brands, numbers, template page references, or preset
  names. Flag instead.
- Never hardcode a color. Detect and match, default only on a clean row and say so.
- Never use all three overlay types by default. Match the type to the archetype.
- Never generate or attach graphic files. The editor designs them.
- Never duplicate an overlay already on the page.
- Never write to a client's live workspace before they approve the skill going live.
- Never use dashes as punctuation in generated copy.

## References

- `references/brand-brain/` your setup, annotated examples, voice. Fill it first.
- `references/placement-rules.md` archetypes, density, selectivity, type by archetype, color
- `references/annotation-format.md` scaffold, the three annotation types, write format, color detection
- `references/drafting-and-reuse.md` drafting quality and the reuse, draft or flag decision
