---
name: carousel-repurposer
description: Turns a reel script into the text of an Instagram carousel, slide by slide, in the creator's own voice from a Brand Brain. Takes a goal of saves, sales or followers, and lets the goal shape the writing and the CTA. Outputs slide number, slide title and slide body only, because the creator builds the visuals. Never invents a fact, and every CTA comes from a list of real offers. Use when someone says "turn this reel into a carousel", "make this script a carousel", "carousel this", "/carousel-repurposer", or pastes a reel script and names a goal. Do not use for newsletters, captions, hashtags, on-screen overlays, or anything to do with images, templates or design.
---

# Carousel Repurposer

Turning a reel into a carousel by hand takes about half an hour: read the script, decide what goes on
each slide, rewrite it to be read instead of heard. This does the drafting so the creator edits
instead of writing.

**Text only, and that is the whole point.** For each slide: the number, a title, and the body. The
creator builds the visual themselves, usually natively in the Instagram editor from their own photos.
Native carousels built from your phone often outperform polished designed ones, so the writing should
read like a person posting, not like a marketing asset.

## Setup (once): fill the Brand Brain

The skill writes in the creator's voice, and it gets that voice from `references/brand-brain/`. Out of
the box those files are empty templates. Read `references/brand-brain/README.md` and fill:

1. `references/brand-brain/voice.md`, how you write. Register C (Instagram) is the one this skill uses.
2. `references/brand-brain/offers.md`, your real offers and freebie. The only place a CTA may come from.
3. `references/brand-brain/examples.md`, one carousel you actually posted, next to the reel script it
   came from. This is the benchmark.

If a file is still the template when the skill runs, keep going with neutral copy, write
`[CTA: add your offer]` where an offer is missing, and say in the notes exactly which file is empty.
Never make up a voice, an offer or a benchmark.

## Read before drafting

- `references/brand-brain/examples.md`, the benchmark. Read it every run, never a summary of it.
- `references/carousel-structure.md`, slide 1 from the hook, what becomes a slide, how many, how the
  goal shapes the writing, the CTA slide.
- `references/output-rules.md`, the rules shared with the newsletter repurposer.
- `references/brand-brain/voice.md`, Register C only. Other registers are for other surfaces.
- `references/brand-brain/offers.md`, the only place a CTA may come from.

## Process

1. **Take the script and the goal.** The input is a reel script, pasted in, or more than one. Two
   reels can merge into one carousel, so do not assume one script means one carousel. Work from the
   script body and the hook block. Visual notes in the script (`[PUT PIC]`, `[show ...]`, overlay
   instructions) are directions to an editor, not content. Ignore them.

   **The goal is one of `saves`, `sales`, `followers`.** If it was not given, ask once and wait. Do not
   guess it from the topic and do not offer a default. Name the options in two sentences or fewer:

   > Which goal, saves, sales or followers? Saves means people keep it to come back to, sales points at
   > one of your offers, followers leans on your opinion and asks for the follow.

   Then stop. Do not draft a version "to show them" and do not pick the goal that seems to suit the
   script. If no script was pasted, ask for one. This skill has no Instagram access and must not
   pretend to.

2. **List the points.** Before writing any slide, list the substantive points the script makes, in the
   creator's framing. That list is the contract: every point on it appears across the slides, and
   nothing that is not on it does. Separate substance from narration (see
   `references/carousel-structure.md`). **When the script points at something it does not contain**, a
   prompt it says to copy, a template it says to use, a number it does not give, flag it in the notes.
   Do not fill it in. Inventing it is the one failure that costs the creator's trust.

3. **Build slide 1 from the hook.** The creator's hook, rebuilt to be read rather than heard. Never a
   new one. Mechanics in `references/carousel-structure.md`.

4. **Split the rest into slides.** One distinct thing per slide, the step or point as the title, one to
   three plain sentences under it. Keep the script's emphasis. Let a dense point overflow into a second
   slide rather than compressing it. Drop nothing substantive.

5. **Let the goal shape it.** Same points in all three versions. The goal changes emphasis, the framing
   of slide 1, how much of each body is instruction versus meaning, and the CTA. `sales` changes
   structure and order, not adjectives: read "The `sales` lever, in full" in
   `references/carousel-structure.md` and check the output against its threshold. The goal never
   selects a template, a style or a look.

6. **The CTA slide.** Payoff line, then one CTA, drawn only from `references/brand-brain/offers.md`.
   Which offer gets named is decided by rule 2 of `references/output-rules.md`: the creator's own CTA
   first if it maps to a confirmed offer, then topical fit, then the freebie with the mismatch flagged.

7. **Hand it over** in the output format below. Then stop. Do not offer to post it, schedule it, write
   the caption, or suggest hashtags.

## Output format

Plain paste ready text, nothing else, in this order:

```
Slide 1
<title>
<body>

Slide 2
<title>
<body>

...

<one line: how many slides and why>

NOTES
Goal: <goal>, and how it shaped the writing
CTA maps to: <offer from offers.md, or the freebie, or "Brand Brain has no offers yet">
Points covered: <the list from step 2>
Flagged, not invented: <gaps>
Brand Brain: <complete, or which files are still templates>
```

No markdown, no bold, no headers, no code fence around the real output, no bullet characters other
than the creator's own. Nothing on a slide except the copy that goes on that slide.

## Example

User pastes a reel script titled "How I batch a week of content" with the talking hook "I film a whole
week of content in two hours, I'll show you exactly how", six spoken steps, and a line about waiting
for the export. They say "carousel this".

Claude asks: "Which goal, saves, sales or followers?" User: "saves".

Claude lists six points, spots that the export line is narration, and that step 4 says "use my shot
list" without giving it. It writes slide 1 as "Film a week of content in one sitting" over "SO YOU STOP
SETTING UP YOUR CAMERA EVERY SINGLE DAY", six numbered step slides with the export line folded into
slide 5's body, and a CTA slide asking for the save first, then naming the freebie from `offers.md`
because it fits a beginner topic. Notes say: eight slides and why, the six points covered, and "Step 4
mentions a shot list the script does not include. Paste it and I will add it, or it stays as a
mention."

## Never do

- Never mention images, image generation, Canva, templates, layouts, fonts, colours, slide dimensions,
  or any visual or design direction. Not on a slide, not in the notes.
- Never select a template or a style. The goal shapes the writing only.
- Never invent a fact, number, brand, feature, price, story or opinion the script does not contain.
- Never name an offer that is not confirmed in `references/brand-brain/offers.md`.
- Never write a new hook when the script has one.
- Never drop a substantive point to hit a slide count.
- Never output markdown scaffolding in the copy that gets pasted.
- Never use dashes as punctuation.
- Never post, schedule, publish or automate. A human builds and posts the carousel.
- Never claim to read Instagram, Notion or a content calendar. This skill works from what is pasted.
- Never write the caption, the hashtags, or a newsletter. Not in scope.
- Never fake a Brand Brain. If it is empty, say so and write neutral.

## References

- `references/brand-brain/` the creator's voice, offers and benchmark carousel. Fill it first.
- `references/carousel-structure.md` slide 1 from the hook, slide splitting, slide count, the goal
  table, the CTA slide
- `references/output-rules.md` shared rules: never invent, real offers, human approval, paste ready
