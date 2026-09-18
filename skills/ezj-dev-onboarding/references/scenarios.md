# Real situations: the scenario round

Six situations that really happened on EZJ Online projects. Each tests judgment, not memory. Ask them one at a time, exactly as written. Never show the rubric, never hint, never give options to pick from. The developer answers in their own words.

## How to grade

- **Pass:** the answer contains every "must" point, in any words.
- **Partial:** some must points, none of the "fail" moves. Ask one neutral follow up: "Anything else you'd do?" Then grade again. Still missing a must point: it's a miss.
- **Miss:** a must point missing after the follow up, or any "fail" move.

Grade the FIRST full answer (plus the one follow up). That's the score. Then coach: one or two sentences with the right move and why. Move on. Don't argue, don't re-ask.

Record for each: `S1 pass` or `S1 miss: <what they got wrong, 8 words max>`.

## S1. The leaked token

> You posted your delivery Loom an hour ago. Rewatching it, you notice your `.env` file was on screen for 3 seconds, and it has your GitHub token in it. What do you do?

- Must: revoke or regenerate the token right away. Remove the exposure (delete the Loom or cut it and re-record, delete any screenshot or comment that shows it). Tell Ethan in the project thread.
- Fail: "it was only 3 seconds", "I'll trim the video" without revoking, hiding it from Ethan.
- Why it matters: a leaked token can edit code that runs with EZJ's keys. This exact thing happened.

## S2. The spec disagrees with itself

> The GitHub issue says send the reminder 24 hours before the appointment. The brief says 2 hours. It's midnight for Ethan. What do you do?

- Must: the issue wins (it's the spec). Check the issue comments and ask their own Claude to look for a newer answer. Build to the issue and write the decision in the PR. Keep moving.
- Good extra: tag @Claudia in the project channel.
- Fail: stop working and wait for Ethan, or message him on WhatsApp.

## S3. Stuck on access

> Day 2 of a 5 day project. You need the client's Twilio account to test, and you don't have access. What do you do?

- Must: tell Ethan the same day, in one tagged message in the project thread, with exact click by click steps of what he needs to do (or run `/ezj-blocked`). Label the issue blocked. Work on another issue meanwhile.
- Fail: wait quietly, ask for the password, "I'll mention it at the end", or stop working completely.

## S4. Running late

> It's Wednesday. The deadline is Friday. You're about half done because an API was harder than expected. What do you do?

- Must: tell Ethan now, before the deadline, in one line in the project thread, with a realistic new date and the reason.
- Fail: say nothing and try to rush, tell him on Friday or after, send a long apology essay.

## S5. The PR has waited 3 days

> Your PR has been waiting for Ethan's review for 3 days. You have write access to the repo and the next issue depends on it. Do you merge it yourself?

- Must: no, never merge your own PR. One short follow up in the same Slack thread (allowed after 2 working days). Start the next issue on a branch off your PR branch so you're not stuck.
- Fail: merging it, or messaging him on GitHub and WhatsApp and Slack.
- Why it matters: self merged PRs skipped review and broke things before.

## S6. The real customers

> Your feature sends SMS reminders to the client's real customers. Everything passes. For your delivery Loom, do you switch it on to show it working?

- Must: no. Anything that sends to real people is built switched off. Demo it with test data and your own test number. Ethan switches it on.
- Fail: switching it on "just for the demo", sending to a real customer "just once".
