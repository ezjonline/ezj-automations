# The Discount Code Skill

Screenshot any checkout page. Claude finds the codes that actually work, ranked, in order to try them.

## Install (2 minutes)

1. Install Claude Code if you do not have it: `npm install -g @anthropic-ai/claude-code`
2. Make the skills folder if it does not exist: `mkdir -p ~/.claude/skills/discount-codes`
3. Drop `SKILL.md` into `~/.claude/skills/discount-codes/`
4. Open Claude Code and type `/discount-codes`

## Use it

Screenshot your cart or checkout page, drag it into Claude Code, and say "find me a discount code."

You get back:
- The three to five codes most likely to work, in the order to try them
- What each one saves on your actual cart
- The savings levers that need no code at all (cashback, cart abandonment, first order offers)

## What it will not do

It will not make up a code. Every code it gives you traces to a real source it found in that run. If nothing is live, it tells you that instead of wasting your time at checkout.

Built by EZJ. More free skills at [ezjonline.com/resources](https://www.ezjonline.com/resources).
