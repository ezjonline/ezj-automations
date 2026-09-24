---
name: tally-forms
description: Builds a branded, multi-step Tally form through the Tally API instead of clicking one together by hand, in your own colours with your logo, and wires submissions to a webhook. Use when someone asks for a form, an intake form, an onboarding form, a client kickoff form, an application, a survey, a waitlist, a feedback form, a questionnaire, "spin up a form", "build me a Tally", or when a project needs access and details collected in one pass. Do not use for Notion databases, Airtable forms, booking questions on a scheduling link, or a landing page that happens to have a form on it.
---

# Tally Forms

Builds a form people actually finish. Multi-step, in your brand, live in about a minute, through the Tally API rather than an afternoon of clicking.

A default Tally form is white with purple buttons and looks like every other Tally form. This skill makes one that looks like it came from you, splits the questions into steps so nobody faces a wall of fields, saves the answers as the person types, and posts every submission to whatever automation you point it at.

## When to use, and when not to

Use it any time the answer to a request is "a form". Intake, onboarding, client kickoff, access collection, applications, surveys, feedback, waitlists, event RSVPs.

Do not use it for a Notion database, an Airtable form, the question fields on a Cal.com or Calendly booking link, or a landing page with an embedded form. Those are different tools with different jobs.

## What you need first

1. **A Tally API key.** tally.so, then Settings, then API keys. Put it in your environment as `TALLY_API_KEY`, or in a `.env` file in the directory you run from. If you are building forms for someone else's account, they generate the key and send it to you. Never paste a key into a chat, a form, or a repo.
2. **Python with `requests` and `python-dotenv`.** `pip install requests python-dotenv`.
3. **What the form is for, and who fills it in.** If you were only given a rough list of fields, write the real questions yourself and show the person the plan. Do not hand back a spec asking them to write the questions.
4. **Where submissions should go**, if anywhere. A webhook URL for n8n, Make, Zapier or your own endpoint. Optional, a form works fine without one.

## Make it yours

Open `assets/tally_form_builder.py` and edit three values near the top:

```python
BRAND_ACCENT   = "#F47C20"   # links, focus rings, selected states, buttons
BRAND_BG       = "#0d0d0d"   # page background
BRAND_LOGO_URL = "https://www.ezjonline.com/assets/logo-icon.png"
```

That is the whole theme. The shipped palette is EZJ Online's black and orange, so change it unless you want their branding. Keep the background a true near-black rather than a warm brown-black, and never put a gradient there, Tally renders it badly.

## Process

### 1. Draft the structure before writing any code

Every form is multi-step. One idea per step, three to six questions per step, a `heading` carrying an emoji opening each one. Steps should read like a journey, not a database schema:

```
intro (one line on how long it takes)  →  page_break
👋 Who you are                          →  page_break
🎯 What you need                        →  page_break
🧩 The details                          →  thank_you
```

Write the questions like a person talking. Second person, plain, short. "What's breaking right now?" beats "Please describe your current operational challenges." Mark a question `required` only if the form is genuinely useless without it, especially on a form someone fills in live on a call.

### 2. Build it

```python
import sys; sys.path.insert(0, "skills/tally-forms/assets")
from tally_form_builder import create_form

form_id, url = create_form(
    title="🚀 Client Intake",
    description="Takes about 3 minutes. Your answers save as you go. ⚡",
    questions=[...],
)
print(form_id, url)
```

Block types the builder supports:

- Structure: `page_break`, `heading` (H2, carries the emoji), `subheading` (H3), `label`, `instruction` (prose, basic HTML is fine), `divider`, `thank_you` (takes `title` and optional `body`)
- Inputs: `short_text`, `long_text`, `email`, `number`, `phone`, `website`, `date`, `file_upload`
- Choices: `multiple_choice`, `checkboxes`, `dropdown` (each takes `options`)
- Scales: `linear_scale` (`min`, `max`, `min_label`, `max_label`), `rating` (`stars`)

Every input takes `title`, plus optional `placeholder` and `required`.

### 3. Verify the render. A 201 does not mean it looks right

A 201 from the API means the blocks were accepted, nothing more. A form can return 201 and still render white and purple, or 500 on the respond page. Always fetch the live page and check. Wait about five seconds first, the respond page is cached briefly after a write and you will otherwise read the previous version and chase a ghost.

```bash
sleep 6; python3 -c "
import requests,re
t=requests.get('https://tally.so/r/FORM_ID',timeout=30).text
m=re.search(r'\"theme\":\{\"is\":\"(\w+)\"',t); seg=t[m.start():m.start()+8000]
print(m.group(1), re.search(r'\"background\":\"[^\"]+\",\"accent\":\"[^\"]+\"',seg).group(0))
print(re.search(r'\"button\":\{\"bg\":\"[^\"]+\",\"fg\":\"[^\"]+\"',seg).group(0))
print('logo', 'logo' in t, '| progress', '\"hasProgressBar\":true' in t)
"
```

Expect `CUSTOM`, your background and accent, your button colours, logo `True`, progress `True`. Anything else, the style did not land. Fix it before showing anyone.

### 4. Wire the automation, if it needs one

```python
from tally_form_builder import create_webhook
create_webhook(form_id, url="https://your-n8n-host/webhook/your-path")
```

`create_webhook` is idempotent. It lists the account's webhooks and returns the existing one rather than stacking a second webhook on the same form, which would double-post every submission. Pick one endpoint per kind of form and reuse it instead of building a new automation per form.

### 5. Hand it over

Give the person the link and a one line description of what it collects. Do not send it to the client or customer yourself.

## Editing an existing form

Same URL, new content. Never delete a form to rebuild it clean, that breaks every link already in the wild.

```python
from tally_form_builder import update_form, restyle_form
update_form(form_id, title="...", questions=[...])   # same responder URL
restyle_form(form_id)                                # brand an older form, questions untouched
```

## Output format

Report back in three lines, not a wall:

```
Built: 🚀 Client Intake
https://tally.so/r/abc123
4 steps, 14 questions, brand style verified, submissions go to <destination or "nowhere yet">.
```

## Example

A client project kickoff form, collecting access in one pass. The full version is in `assets/example_client_kickoff.py` and is worth reading before you write your own, particularly for how it handles credentials.

```python
questions = [
  {"type":"instruction","title":"Everything we need to start, in one place. About 10 minutes. Your answers save as you go, so leave anything you need to look up and come back to it. ⚡"},
  {"type":"page_break"},
  {"type":"heading","title":"🔑 The main system"},
  {"type":"instruction","title":"Wherever you can, <b>invite us as our own user with admin rights</b> rather than sharing a password. You can remove us any time. <b>Never type a password or an API key into this form.</b>"},
  {"type":"checkboxes","title":"What is done so far?",
   "options":["Invited as an admin user","That invite has been accepted","API key generated","Nothing yet, we will do it on the call"]},
  {"type":"short_text","title":"Which plan are you on, and who is your account rep?"},
  {"type":"page_break"},
  {"type":"heading","title":"👥 Your team and your rules"},
  {"type":"file_upload","title":"Your team list","placeholder":"Name, email, mobile"},
  {"type":"long_text","title":"What must NEVER go out automatically?",
   "placeholder":"The most important answer on this form. Anything that would embarrass you if a robot sent it"},
  {"type":"dropdown","title":"Where should the weekly report land?","options":["Email","Slack","Both"]},
  {"type":"instruction","title":"<b>Passwords and API keys:</b> do not put them in this form. Use <a href='https://onetimesecret.com'>onetimesecret.com</a> and send us the link. It self destructs after one view."},
  {"type":"thank_you","title":"Got it. 🔥","body":"Anything you left blank we will pick up on the kickoff call."},
]
```

## Collecting access without collecting secrets

A form stores everything typed into it. That makes a form the wrong place for a password or an API key, however convenient it feels in the moment.

Ask instead for **confirmation that access was granted**, and have them invite you as your own named user with admin rights. It is safer, it is revocable, and it leaves an audit trail on their side. Where a credential genuinely has to move, send it through a one time secret link rather than the form. Build this into the form copy, near the top and again at the end, so nobody has to think about it.

## Never do

- **Never send the form link to a client, customer or list without the owner's explicit yes.** Building and publishing the form is fine. Distribution is their call, not yours.
- Never collect passwords, API keys or card details in a Tally form.
- Never ship a form in Tally's default white and purple. If step 3's check fails, fix it before showing anyone.
- Never skip the multi-step structure. One long scroll is the thing this skill exists to avoid.
- Never delete a form to "rebuild it clean". Use `update_form`, which keeps the same responder URL.
- Never stack a second webhook on a form that already has one. Use `create_webhook`, which dedupes, and never bypass its duplicate check.
- Never hand back a written spec describing a form someone else should go build. Build it. Only fall back to a spec if there is a real blocker, and say so plainly.
- Never use dashes as punctuation in form copy.

## Gotchas, all hard won. Do not rediscover these

- **The custom palette only works nested.** `settings.styles` must be `{"theme":"CUSTOM","color":{"background":...,"text":...,"accent":...,"buttonBackground":...,"buttonText":...}}`. Flat keys like `backgroundColor` or `accentColor` are accepted by the API and silently ignored by the renderer, so the form comes back white and purple. `customTheme`, `colors` and `custom` as the nesting key all fail too. Only `color` works.
- **Unknown keys inside `styles` make the respond page return 500.** The API accepts them, the page then dies. Never add speculative style keys.
- **`theme: "CUSTOM"` without a `color` block falls back to white and blue.** Both parts or neither.
- **A PATCH that omits `settings` wipes the theme back to Tally's default.** `update_form` and `restyle_form` re-send the settings every time for exactly this reason. Never hand-roll a PATCH that only sends blocks.
- **The API validates block payloads strictly, and the error message names the offending key.** Read it rather than guessing. `linear_scale` labels are `hasLeftLabel` plus `leftLabel`, not `minLabel`. `rating` takes `stars`, not `max` or `shape`.
- **There is no `THANK_YOU_PAGE` block type.** A thank you screen is a `PAGE_BREAK` flagged `isThankYouPage`, with the copy in the blocks after it. The builder handles this for you.
- **TITLE blocks must not share a `groupUuid` with their input block.** Tally changed this in May 2026 and getting it wrong renders a silently blank form. The builder already separates them.
- **The respond page is cached for a few seconds after a write.** Wait about five seconds before verifying.
- **Building forms through the API needs a paid Tally plan.** On the free plan, Tally branding also shows at the bottom of every form. Mention it once if it matters for a client-facing form, then let it go.
