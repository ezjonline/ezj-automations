---
name: newsletter-repurposer
description: Turns one Instagram post (caption, reel script or carousel) into a newsletter draft in the creator's own voice from a Brand Brain, ready to paste into any email platform. Can also suggest which posts are worth turning into newsletters, ranked on story, connection and vulnerability rather than on how they performed. Produces three subject line options, the email body, the list segment with a reason, and one CTA from real offers only. Use when someone says "turn this post into a newsletter", "write the newsletter for this", "make this an email", "which posts would make good newsletters", "/newsletter-repurposer", or pastes a post and asks for an email. Do not use for carousels, captions, scripts, overlays, or for sending anything. A pasted post on its own is not a newsletter request: if no email is asked for, ask which output is wanted.
---

# Newsletter Repurposer

The usual problem: someone on the team turns the creator's Instagram posts into newsletters and the
tone is always off. This drafts it in the creator's actual voice instead, so the editor edits rather
than writes.

**A human stays the editor and the creator stays the approver.** This produces a first draft. It never
sends, schedules, or publishes, and it has no connection to any email platform.

## Setup (once): fill the Brand Brain

The skill writes in the creator's voice, and it gets that voice from `references/brand-brain/`. Out of
the box those files are empty templates. Read `references/brand-brain/README.md` and fill:

1. `references/brand-brain/examples.md`, five to ten real newsletters, real subject lines, the merge
   tag, and the list segments. This is the voice target.
2. `references/brand-brain/voice.md`, how you write. Register B (email) is the one this skill uses.
3. `references/brand-brain/offers.md`, your real offers and freebie. The only place a CTA may come from.

If a file is still the template when the skill runs, keep going with neutral copy, write
`[CTA: add your offer]` where an offer is missing, use `{first name}` as the merge tag, and say in the
notes exactly which file is empty. Never make up a voice, an offer or a segment.

## Read before drafting

- `references/brand-brain/examples.md`, the real newsletters. Read them every run, never a summary.
- `references/newsletter-structure.md`, the body component, the shell, subject lines, mechanics.
- `references/output-rules.md`, the rules shared with the carousel repurposer.
- `references/brand-brain/voice.md`, Register B only. Other registers are for other surfaces.
- `references/brand-brain/offers.md`, the only place a CTA may come from.

## Process

1. **Suggest source posts (optional).** Run this only when asked which posts would make good
   newsletters, or when started without a post. **If a post is pasted, skip to step 3.**

   Use whatever post set is given: a pasted list, a content calendar export, a handful of captions. If
   there is no set, ask for one. Never go looking for posts. This skill has no Instagram access.

   **Rank on story, connection and vulnerability.** Is there a story in it, does it say something the
   creator actually believes, are they a bit exposed in it, does the reader get something they can use.
   **Never rank on performance**: not views, likes, saves, shares, reach or follower growth. If the set
   carries numbers, ignore them and say so in one line. A post that flopped is often the best
   newsletter, because it was more personal.

   Output three to five candidates, each with the post as named in the set, one line on its story
   value, and the segment it would go to. End with: "Which one do you want? Or paste a different post
   and I will use that instead." Then stop.

2. **The approval gate.** Only draft once a human has chosen the post. Take any notes they add about
   what to cover. Never draft from your own pick. There is no automatic path from step 1 to step 3.

3. **Read the source.** A reel transcript or script, a short caption, a carousel, a lifestyle post, all
   valid. List the substantive points the post makes, in the creator's framing, before writing. That
   list is the contract: every point appears in the newsletter, nothing else does. **When the source is
   thin**, draft what it genuinely supports and flag the rest in the notes. A caption saying "comment
   TEMPLATE for the template" does not tell you what is in the template, and guessing is the one
   failure that costs trust.

4. **Pick the segment** from the segments table in `references/brand-brain/examples.md`, by the topic
   of the post. **The voice does not change between segments. The assumed context does**: whether you
   explain a term or assume it. Say which segment and why in one line in the notes. If no segments are
   set up, write for everyone and say so.

5. **Draft the body component** per `references/newsletter-structure.md`: the way in, the turn, the
   teaching. A standalone block that could drop into a different newsletter shell untouched.

6. **Wrap it in the flat shell.** Greeting, body, one soft offer mention, reply prompt, sign off. The
   CTA comes from `references/brand-brain/offers.md` only, chosen by rule 2 of
   `references/output-rules.md`. If the post promotes something not in that file, do not name it. Flag
   it.

7. **Write three subject lines** that differ in angle, checked against the real ones in `examples.md`.

8. **Hand it over** in the output format below. Then stop. Do not offer to send it, schedule it, or put
   it in the email platform.

## Output format

Plain paste ready text, in this order:

```
SUBJECT LINES
1. <option>
2. <option>
3. <option>

<greeting>

<body component, one blank line between every block>

<soft offer mention>

<reply prompt>

<sign off>

NOTES
Segment: <segment>, <one line reason>
CTA maps to: <offer from offers.md, or the freebie, or "Brand Brain has no offers yet">
Points covered: <the list from step 3>
Flagged, not invented: <gaps>
Brand Brain: <complete, or which files are still templates>
```

No markdown, no headers, no bold, no bullet characters other than the creator's own markers, no code
fence around the real output.

## Example

User pastes a reel script about the week they almost quit posting, then three things that changed
their mind, and says "make this a newsletter".

Claude lists four points (the almost quitting moment and the three lessons), picks the "everyone
engaged" segment because it is a mindset post, and writes the body: a way in from the moment in the
script, a one line turn, then the three lessons as a list using the creator's marker from `voice.md`,
ending on a line that lands the idea. It wraps it in the creator's greeting with the merge tag from
`examples.md`, one soft mention of the freebie (nothing paid fits a mindset post), a one word reply
prompt, and their sign off. Three subject lines: one confessional, one curiosity, one flat statement.
Notes flag that the script says "the app I switched to" without naming it, so the draft says "a
different app" and asks.

## Never do

- Never send, schedule, publish, or automate. A human approves the post and edits the draft.
- Never rank or recommend a post on views, likes, saves, reach or follower growth.
- Never invent a fact, number, brand, feature, price, story or opinion the source does not contain.
- Never name an offer that is not confirmed in `references/brand-brain/offers.md`.
- Never change the voice between segments. Only the assumed reader context changes.
- Never blend the body and the shell into one piece of prose.
- Never output markdown scaffolding in the copy that gets pasted.
- Never use dashes as punctuation.
- Never claim to read Instagram, the email platform, Notion or a spreadsheet. Work from what is pasted.
- Never write carousels. That is the carousel repurposer.
- Never fake a Brand Brain. If it is empty, say so and write neutral.

## References

- `references/brand-brain/` the creator's real newsletters, list setup, voice and offers. Fill it first.
- `references/newsletter-structure.md` body component, shell, subject lines, mechanics
- `references/output-rules.md` shared rules: never invent, real offers, human approval, paste ready
