# Annotation format

Overlays are a structured system inside the script block of a calendar row (the block named in
`references/brand-brain/examples.md`, usually a "Script" callout). Density and type selection are in
`references/placement-rules.md`.

## The page scaffold

A typical script row body, in order. Confirm the real one from `examples.md` or from the page itself:

1. **Video idea / length**, brainstorm notes.
2. **Hook**, often three labeled lines: `Visual hook:`, `Talking hook:`, `Text-on-screen hook:`.
3. **Script**, the working surface. This is the only place the skill writes.
4. **Visuals to create**, a checklist.
5. **Caption**, the caption plus a CTA line.

Read the whole row for context. Write only inside the Script block.

## The three annotation types

The spoken script is default colored text. Everything added for the editor is in the annotation color.

1. **`Text on screen: <label>`**, a short distilled label placed before the spoken lines it overlays.
2. **`[director note]`**, a bracketed instruction to the editor on what to show: B-roll, a screen
   recording, a screenshot, an example. Example: `[PUT PIC 2]`, `[screen recording of the export
   settings]`.
3. **`Make an overlay on canva with this`**, a toggle whose contents are the detailed overlay to be
   designed (lists, steps with shot directions). Reuse a named asset only if it appears in this row or
   in the overlay bank, otherwise draft or flag (see `references/drafting-and-reuse.md`).

Which archetype uses which type is in `references/placement-rules.md`. Do not use all three by default.
The spoken script is never rewritten.

## Global overlay instruction

Some scripts carry a note at the top of the Script block like "put the screen recording on top of my
head". That is the video's primary visual treatment. Never delete or reword it, usually place FEW
inline overlays because of it, and restate it in the report.

## Color: detect and match, do not hardcode

Before writing:
- Detect the color of any existing annotation on THIS row and match it.
- If the row is clean, use the default color from `examples.md` (pink if none is set) and note in the
  report: "wrote in <color>, tell me if this one should be different."

## Writing it via the Notion connector

- Inline color: `<span color="pink">Text on screen: Vary your angles</span>` (swap `pink` for the
  detected color).
- Toggle: `<details><summary><span color="pink">Make an overlay on canva with this</span></summary>`
  then indented children.
- The color persists and round trips, so existing annotations are **detectable** for safe re-runs.
  Find the existing colored spans and "Make an overlay" toggles first and never duplicate them.
