# Writing the handoff doc

The reader is Ethan, then his client, then the next developer. None of them wrote the code. Some read English as a second language. All of them are busy. Write for that.

## The five minute rule

The whole page reads in about five minutes. That is 700 to 1,500 words. If it runs longer, cut words before cutting sections. The check warns past 1,800.

## Plain English

- Say what it does, not how it is built. "Replies show up in Slack" beats "an inbound webhook posts to a Slack incoming webhook."
- Short sentences. One idea each.
- Common words. "Send" not "dispatch". "Start" not "initialize". "Settings" not "environment configuration".
- If a technical word is unavoidable, explain it in the same sentence: "a webhook (a web address the phone system calls when something happens)".
- Talk about people and outcomes: the patient, the front desk, Ethan, the client.

Translate these every time:

| Instead of | Write |
|---|---|
| env var, environment variable | setting |
| deploy | put it online |
| endpoint, webhook URL | web address |
| payload | the information it sends |
| idempotent, deduplicated | clicking twice does not do it twice |
| auth, credentials | login, password, key |
| repo | the code on GitHub |
| cron, scheduled job | runs every day at 9am (say when) |
| 403, 400, 500 | "says access denied", "says something is missing", "crashes" |
| edge case | when X happens |
| refactor | cleaned up the code, nothing changes for users |

## Headlines

Every section headline says the outcome in plain words, like a newspaper. Not "Architecture". Say "A missed call turns into a conversation". Not "Configuration". Say "Run it from zero in 5 steps". The eyebrow above it (How it works, Set it up) is the label. The h2 is the point.

## Numbers

- Only numbers from real runs, real tests, real data in this project. Say where each came from ("Run with `npm test` on 16 Sept 2026").
- Prefer a number to an adjective. "Under 30 seconds" beats "fast". "18 of 18 tests pass" beats "well tested".
- Never round up to look good. 17 of 18 is 17 of 18, and the failing one goes in Status.
- No real numbers? Do not use `bigstat` or `bars`. An honest page with no chart beats a chart that lies.

## Status pills, fixed meanings

| Pill | Class | Means |
|---|---|---|
| Working now | `ok` | Built, tested end to end on the real setup, nothing left to do |
| Needs your go / Built, needs your go | `go` | Built and tested, switched off until someone approves |
| Waiting on you | `you` | Cannot move until Ethan or the client does something listed in What I need from you |
| Not built | `off` | Out of scope or not started. Say which |
| Broken / Not fixed yet | `bad` | Does not work right now, or a known bug was found and not fixed (even if nothing is switched on yet). Say what it is and that it must be fixed before going live |

Pick the honest one. "Working now" on something only tested on your own laptop is a lie. Use `go` and say what is left.

## What breaks it

Three to five rows, from things that actually happened or clearly could: a setting changed, a key expired, a limit hit, an account permission, a third party outage. Each row is what someone notices (in their words, not the error code), why, and the exact fix.

## What I need from you

Only things that truly need Ethan or the client. Each one is a numbered card with the exact steps: which site, which menu, which button, what to send back and where. "Need Twilio access" is not an ask. "Twilio, Settings, Users, Invite, alex@example.com, role Developer" is.

## Never in the doc

Secret values, prices and fees, real customer data, raw logs, pasted code, pasted Claude output, "TODO", guesses written as facts, and dashes used as punctuation.
