# Brand Brain (setup step, do this once)

This skill writes in YOUR voice, not a generic one. It gets your voice from this folder. Out of the box
every file here is an empty template. Fill them before the first real run, or the output will be
correct in structure and generic in voice.

**The rule the skill follows:** if a Brand Brain file is still the empty template, it says so in the
notes of every run and writes neutral copy. It never makes up a voice, an offer or a story for you.

## What to fill

| File | What goes in it | Why it matters |
|---|---|---|
| `voice.md` | How you write: register, mechanics, emoji, list markers, words you use and never use | Every line of copy is checked against it |
| `offers.md` | Your real products, prices and freebie, each with who it is best for | The only place a CTA may come from |
| `examples.md` | Real content you already posted, pasted in full | The voice target. Real writing beats any description of it |

## The fastest way to fill it

1. Paste 5 to 10 of your best pieces of real content into `examples.md`. Your own writing, not an
   agency draft and not AI output.
2. Ask Claude: "Read `examples.md` and draft my `voice.md` from it. Only describe patterns that
   actually appear." Then correct it by hand.
3. Write `offers.md` yourself. It is short and it has to be exactly right.

## Keep it private

These files hold your voice, your offers and your prices. If you fork this skill into a public repo,
keep your filled Brand Brain out of it (add `references/brand-brain/*.md` to `.gitignore` apart from
this README).
