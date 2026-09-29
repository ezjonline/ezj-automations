# Placement and style model

Where overlays go and how many. **Density is set by the video's VISUAL APPROACH, never by how many
points, steps, or list items the script has.** A 10 step process might get 3 overlays. A screen
recording video might get 1. A story gets 0.

The numbers below are defaults calibrated on a real creator's annotated scripts. Correct them to your
own in the formats table of `references/brand-brain/examples.md`. When that table is filled, it wins.

## Archetypes: density, dominant type, global instruction

| Archetype | Looks like | Density | Overlay types used | Global instruction |
|---|---|---|---|---|
| **Value-teaching** | talking head teaching distinct techniques | **~8, one per distinct teaching point** | all three blended | usually none |
| **Screenshot / settings walkthrough** | nearly every line points at a setting or screenshot | **~10, one per setting** | director notes only, `[PUT PIC N]` inserts. No labels, no toggles | often ("overlay on my head") |
| **Process / "how I did X"** | a chronological story of doing something | **~3, far fewer than the steps** | director notes only, at the moments a visual is needed | usually none |
| **Series / voiceover over a screen recording** | a recurring format carried by one continuous recording | **~1 inline** | one director note, the recording carries the visual | yes ("screen recording on my head") |
| **Storytelling / lifestyle** | talking to camera, carried by the story | **0** | none | none |

**Hitting the low ones (0 and 1) matters as much as the dense ones.** Over-annotating is the main
failure mode.

## The selectivity rule (the single most important rule)

- An enumerable list, a "First / Second / Third", or a new step does **NOT** automatically get an
  overlay.
- **Place an overlay only where a visual adds something the spoken words cannot convey.** If the words
  already carry the meaning, no overlay.
- An overlay fires for: a specific artifact to look at (a screenshot, a template, a tool screen), a
  demonstration the viewer must SEE (`[screen recording of trimming each clip]`), a reusable designed
  list, or a title that headlines a distinct teaching beat.
- It does NOT fire on: narrative, transitions, opinion, motivation, or any step whose payload is purely
  verbal ("then I followed up with them", "then I sent the invoice" get nothing).
- An enumerable list inside ONE spoken beat becomes **one** overlay (a single list graphic), never one
  per item.

## Overlay types, and which archetype uses which

- **`Text on screen: <label>`**, a 2 to 4 word distilled NAME for the beat ("Vary your angles", "Cut
  the pause"), never a caption of the sentence. **Value-teaching only.**
- **Bracketed director note**, "show X", naming the exact visual: a screenshot insert (`[PUT PIC N]`), a
  screen recording, a tool, an example. The workhorse. **The only type in walkthrough, process, and
  series.**
- **`Make an overlay on canva with this` toggle**, whose contents are a detailed designed list or steps
  with shot directions nested in brackets. The richest type. **Value-teaching only, and only where the
  payload is a real list worth building, one per list.** Rename it to match your design tool if you
  do not use Canva (set it in `examples.md`).

## Color: detect, never hardcode

Creators often annotate in more than one color across scripts. Detect the color of any existing
annotation on THIS row and match it. If the row is clean, use the default from `examples.md` and say in
the report "wrote in <color>, tell me if this one should be different".

## Classifying a NEW script (to set density)

Read **Format** first, then confirm against the script body:

1. **Format is voiceover plus B-roll**, or a global note says the visual is a continuous screen
   recording → **series → ~1 overlay.**
2. **A connection, nurture or lifestyle post**, or a talking to camera story with no artifacts →
   **storytelling → 0.**
3. **Talking head teaching** → the CONTENT decides:
   - Nearly every line points at a screenshot or setting to insert → **walkthrough → ~10 `[PUT PIC N]`.**
   - A chronological process where most steps are verbal, few name a real artifact → **process → ~3,
     only at the artifact moments.**
   - Distinct labeled lessons each helped by an on-screen title plus a demo → **value-teaching → ~8,
     all three types.**
4. When ambiguous, the content wins: count the lines that genuinely need a visual the words cannot
   convey. That count IS the density. **Never derive density from step or list count.**

Category and Goal properties never raise density on their own. The same category can sit on the
densest and the lightest videos.
