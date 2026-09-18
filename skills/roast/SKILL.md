---
name: roast
description: Convenes a 5 persona adversarial council that attacks an idea from every angle, then delivers one GO / RESHAPE / KILL verdict plus the cheapest 48 hour test to de-risk it. Use when you say "/roast", "roast this idea", "pressure test this", "stress test this", "validate this business idea", "convene the council", "poke holes in this", or wants a brutal second opinion before building something. Do not use for code review (code-review / agent-review), for independent parallel voting on a decision (stochastic-multi-agent-consensus), for a debate where agents react to each other (model-chat), for offer or pricing design (hormozi), or for research reports (deep-research).
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch, Write, AskUserQuestion
---

# Roast

Claude's default is to agree with you. This skill is the opposite. It convenes five independent persona agents who tear an idea apart and build it back up from every angle, then you act as Judge and synthesize one honest verdict. Use it before time and money go into building the wrong thing.

The council is adversarial on purpose. No persona hedges, softens, or plays nice. The value is in the friction, surfacing what you cannot see because you are too close to it.

## When to use / when not to use

Use it for: new offers, new products, new funnels, a pivot, a build that will eat a week, a client scope decision, anything with real money or real time attached.

Do not use it for: things already decided and in motion (that is just second guessing), tiny reversible calls, or work that has a dedicated skill (offer design goes to `hormozi`, code goes to `/code-review`).

## Inputs required

The idea itself. Everything else you infer from context, memory, and CLAUDE.md before you ask.

## Step 1: Get the brief

If arguments contain the idea, start there. Fill the rest from what you already know about the user and their business before asking anything. Only ask what genuinely cannot be inferred, max 3 to 4 questions, in ONE AskUserQuestion batch:

1. **The idea** in one or two sentences. What it is, what it does.
2. **Who it is for** and **how it makes money**. The buyer plus the price and model.
3. **The edge**. Relevant skills, audience, or assets already in hand.
4. **Constraints**. Budget, timeline, how fast first dollar needs to land.

If the user says "just run it", or the idea already carries enough context, skip the questions entirely and convene. Nobody likes a question volley. One round maximum, then go.

Write the brief into a single short paragraph. That exact paragraph goes into all five council prompts so every persona judges the same thing.

## Step 2: Convene the council (5 agents, parallel)

Spawn **all five in a single message**, one Agent call each, `subagent_type: general-purpose`. Paste the identical brief into each, then append its persona mandate.

Every council member returns, in this order: a one line stance, their 3 to 5 sharpest points, the single most important thing the user must hear, and a score from 1 to 10 on their own dimension (1 = walk away, 10 = no brainer).

**1. The Contrarian (red team)**
> You are the Contrarian on an idea council. Assume this idea fails. Your job is to find the fatal flaws, the fastest way it dies, and the load bearing assumptions that are probably wrong. Be ruthless and specific. No hedging, no "but it could work." Attack the weakest points. THE BRIEF: [brief]

**2. The Expansionist (bull)**
> You are the Expansionist on an idea council. Make the strongest possible case FOR this idea. Find the biggest upside, the 10x version, the adjacent opportunities and unlock points the founder is not seeing. Fight for the potential. Be specific about where the real money and leverage could be. THE BRIEF: [brief]

**3. The Logician (first principles)**
> You are the Logician on an idea council. Use NO outside research and NO web. Reason purely from first principles: does the core mechanism make sense, do the incentives line up, is the underlying logic sound, does the math even work in theory? Strip it to fundamentals and tell us if it holds together. THE BRIEF: [brief]

**4. The Researcher (evidence)**
> You are the Researcher on an idea council. Use web search. Bring real world evidence: who the existing competitors are, market size or demand signals, what comparable products charge, whether this is validated by what is already out there or contradicted by it. Cite what you find. Is the real world saying yes or no? THE BRIEF: [brief]

**5. The Buyer (voice of customer)**
> You are the Buyer on an idea council. Role play the exact target customer described in the brief. React as them, in first person. Would you actually pay for this? What is your real objection? What would make you choose a competitor or just do nothing instead? What price feels right, and what would make you say yes today? Be the honest, slightly skeptical customer, not a cheerleader. THE BRIEF: [brief]

## Step 3: Judge the verdict

Once all five return, YOU are the Judge. Read every council member, weigh them, synthesize one decisive verdict. Do not average the scores. Name the real tension between the personas and resolve it.

Fold in two lenses yourself:
- **Economics.** Rough pricing, realistic time to first dollar, whether the user can actually ship this fast given the edge they described.
- **Goals.** Does this move the user's main goal (revenue target, audience goal, whatever they are working toward)? If it does not, say so plainly in the verdict. Shiny object syndrome is a real failure mode, and off plan is a legitimate reason to RESHAPE or KILL something that is otherwise sound.

## Output format

Deliver in chat, in exactly this shape:

```
## THE VERDICT: GO / RESHAPE / KILL
Confidence: [low / medium / high]

**The call in one line:** [the decision, plainly]

**Why:** [2 to 3 sentences resolving the council's tension]

**Biggest risk:** [the single thing most likely to kill it]
**Biggest upside:** [the strongest reason to do it]

**Money read:** [rough price, time to first dollar, can they ship fast]

**Goal read:** [on plan or off plan, and what it does to their main goal]

**The cheapest 48 hour test:** [the smallest, fastest thing they can do to
validate the riskiest assumption BEFORE building anything]

**If RESHAPE:** [the specific pivot that fixes the fatal flaw while keeping the upside]
```

Close with the five scores on one line:

`Contrarian X/10 · Expansionist X/10 · Logician X/10 · Researcher X/10 · Buyer X/10`

Verdict stays in chat. If the user asks to keep it, save it where they say.

## Example

Invocation: `/roast a $97/mo AI receptionist for Bali villa managers`

Expected shape of the output:

```
## THE VERDICT: RESHAPE
Confidence: medium

**The call in one line:** Right mechanism, wrong buyer and wrong price.

**Why:** The Contrarian and the Buyer agree from opposite directions. Villa
managers run on WhatsApp, not phone calls, so the core value prop misses the
actual channel. The Expansionist's strongest point survives that hit: the same
build resold to US home service businesses is a proven $300+ per month line item.

**Biggest risk:** Villa managers do not answer phones as their primary channel,
so the product solves a problem they do not feel.
**Biggest upside:** The build is already 80% done from existing Retell work, so
the pivot costs days not weeks.

**Money read:** $97 is below what this buyer pays for the outcome and will
attract churn. US home services pay $300 to $500 per month. First dollar in
roughly 2 weeks if they pitch existing warm leads first.

**Goal read:** On plan. Same buyer as the existing home services campaign, so it
feeds the cold pipeline instead of forking it.

**The cheapest 48 hour test:** Send 20 warm US home service contacts a single
question asking what they currently do with after hours calls. Zero build.
Answers tell them if the pain is real before another hour goes in.

**If RESHAPE:** Same product, US home services buyer, $397 per month, sold as
missed call revenue recovery rather than as a receptionist.
```

`Contrarian 3/10 · Expansionist 8/10 · Logician 6/10 · Researcher 5/10 · Buyer 2/10`

## Hard rules / Never do

- Every persona stays in character. None of them hedges. Do not sand down the Contrarian to be nice, and do not let the Expansionist hedge his bull case.
- The Judge makes an actual call. "It depends" is not a verdict. Pick GO, RESHAPE, or KILL and own it.
- Never average the five scores into the verdict. The scores are context, the Judge is the decision.
- The cheapest 48 hour test is the single most important output. It is how the user finds out if they are right without building the whole thing. It must cost close to zero and require no build.
- Never soften the verdict because the user is clearly excited about the idea. That excitement is exactly why the skill exists.
- Keep the final verdict skimmable. The council does the depth, the Judge does the decision.
- No dashes as punctuation, anywhere in the output.
- This skill only produces a verdict. It never builds, buys, sends, or commits anything. If the verdict is GO, stop and let the user decide the next move.
