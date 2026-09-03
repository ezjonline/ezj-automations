---
name: humanizer
description: Rewrite anything so it reads like a person wrote it, using the full ban list of AI tells. Runs by default on all reader-facing copy (emails, DMs, texts, captions, posts, ads, landing pages, proposals, reports), not just when asked. Use when the user says "humanize this", "sounds like AI", "make it sound like me", "/humanizer", or hands over any draft a real reader will see. Do not use for code, internal notes, skill files, or technical documentation where the ban lists do not apply.
user-invocable: true
argument-hint: "[text to humanize]"
---

> **Demo Library Skill** — This skill is from a demo library. If a step references a brand voice file you do not have, skip it and run the ban lists on their own.

# Humanizer

Rewrite so a real reader never once thinks about how it was written. Not making it casual, not making it clever. Removing the tells.

Source: Learn AI With Mariah, https://learnaiwithmariah.com/guides/make-ai-get-to-the-point/.

## When to use / when not to use

Use on anything a human reader will see: cold emails, client emails, DMs, texts, SMS and chatbot replies, IG captions, reel scripts, landing pages, ad copy, proposals, reports, posts.

Do not use on code, config, internal skill files, or docs where precise repeated technical terms matter more than rhythm.

## Ordering with a brand voice file

If the copy goes out in a specific person's or brand's voice, read that voice file FIRST, then run this pass. The voice file wins on rhythm and vocabulary. The ban lists below still apply on top of it.

## Banned words (the loudest tells)

delve, tapestry, leverage, utilize, robust, seamless, realm, testament, beacon, underscore, showcase, pivotal, crucial, foster, elevate, embark, unleash, navigate, landscape, boast, myriad, plethora, intricate, vibrant, enhance, streamline, optimize, comprehensive, empower, holistic, cultivate, resonate, align, nestled.

## Banned phrases

"in today's fast-paced world", "when it comes to", "it's important to note", "plays a crucial role in", "at the end of the day", "the world of", "more than just", "unlock the power of", "elevate your", "take it to the next level", "supercharge", "move the needle", "deep dive", "low-hanging fruit", "circle back", "best-in-class", "in conclusion", "a journey", "treasure trove", "the possibilities are endless".

## Banned openers and closers

"Imagine a world where", "Have you ever wondered", "Picture this", "So there you have it", "Let's dive in", "Here's the thing", "Here's the kicker", "But here's where it gets interesting", "let that sink in", "plot twist", "trust me".

## Banned shapes (the part most rewrites miss)

1. Negative parallelism: "It's not X, it's Y." Allowed once, only as a final line, never in the body.
2. Rule of three everywhere. Real writing has lists of two, four, and five. Three of everything is a tell.
3. Stacked formal transitions: Furthermore, Moreover, Additionally, Thus, Hence. Use and, so, but, or nothing.
4. Staccato fragments stacked for drama: "One rule. One change. Everything shifts." Write flowing sentences.
5. Every paragraph the same length. Vary them. Some are one line.
6. Em dashes. Use commas, periods, or parentheses instead.
7. Sycophancy: Great question, Absolutely, I'd be happy to.
8. Ending on a rhetorical question when the piece already made its point.

## What human writing actually does

- Sentence lengths vary a lot. A long one, then a short one. Read it out loud and listen for the rhythm.
- Nouns are specific. Not "a solution", but "a spreadsheet". Not "stakeholders", but "my boss".
- Contractions, because people use them.
- Commits to a claim instead of hedging every side of it.
- Admits the limit. "This only works if you already have the data" reads human because it costs the writer something.
- Repeats a word rather than reaching for a thesaurus synonym nobody says out loud.

## Process

1. If the reader and the desired action are not already clear, ask ONE question, then start. Do not stack questions.
2. If the copy goes out in a specific voice, read that brand voice file before rewriting.
3. Rewrite it.
4. List every banned item found in the original, quoted, so the tells get learned and stop getting written.
5. If a writing sample was given, match its rhythm and vocabulary over any rule above except the ban lists.

## Output format

Two blocks, in this order.

**The rewrite.** Clean copy only, no commentary inside it. If the user will paste it somewhere (email, DM, caption), put it in a fenced code block with single-asterisk bold and plain numbered lists.

**Tells found.** A short quoted list from the original. Two to eight items. Skip this block only when the original was already clean, and say so in one line.

## Example

Original: "In today's fast-paced world, when it comes to lead generation, our comprehensive solution empowers businesses to streamline their outreach and unlock the power of automation. It's not just software, it's a journey."

Rewrite: "Most of your leads go cold because nobody follows up in time. This fixes that. Every form fill gets a text back in under two minutes, day or night, and the ones who reply land on your calendar without you touching anything."

Tells found: "In today's fast-paced world", "when it comes to", "comprehensive", "empowers", "streamline", "unlock the power of", "a journey", negative parallelism as a closer.

## Using this inside a chatbot or SMS agent

The ban lists work as a system-prompt block, not just as a rewrite pass. Two ways to wire it:

1. **Inline.** Paste the banned words, banned phrases, banned openers and closers, and banned shapes sections straight into the bot's system prompt under a heading like "Never write like this". Add the SMS rules below.
2. **Second pass.** Let the bot draft, then run the draft through a cheap model with this file as the instruction and "return only the rewrite". Costs one extra call per message, catches more.

Extra rules that only apply to texts and DMs:

- One idea per message. If it needs two paragraphs, it needs to be two messages or a phone call.
- No greeting block, no sign-off, no name at the end. People texting do not do that.
- Lowercase-leaning is fine. Perfect capitalization on every message reads like a system.
- No emoji unless the person used one first.
- Never open with "I hope this message finds you well", "Just checking in", "Following up on", or "I wanted to reach out".
- Ask a real question the person can answer in five words. Not "Does that work for you and would you like me to send some times?"

## Hard rules / Never do

- Never use em dashes, en dashes, or hyphens as punctuation. Use periods, commas, or restructure the sentence.
- Never send or publish the rewrite. Draft only. Emails become drafts, posts wait for explicit approval.
- Never invent facts, numbers, names, or claims that were not in the original. Humanizing is a style pass, not a fiction pass.
- Never strip a legal, medical, or compliance qualifier to make copy punchier. Flag it instead.
- Never ask more than one clarifying question before starting.
- Never hand back the rewrite without the tells list unless the original was clean.

## The test before sending

Could a specific real person have said this sentence out loud, to another person, without sounding strange? If not, rewrite it.
