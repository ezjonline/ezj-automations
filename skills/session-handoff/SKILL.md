---
name: session-handoff
description: Generate a comprehensive copy-paste-ready handoff document that captures everything the current session has done, is doing, and needs to do next, so you can clear the session (or start a new one) and resume exactly where you left off. Triggers on /session-handoff, "session handoff", "hand off this session", "summarize the session so I can continue elsewhere", "wrap this session for continuation", or when the user says they are about to clear/compact and wants to keep going later. Do not use for daily recaps or journaling, for memory writes (MEMORY.md), or for handing work to another person (that is an email or Slack message, not a session handoff).
allowed-tools: Read, Write, Bash, Glob, Grep
---


# Session Handoff

## Purpose

Long Claude Code sessions fill up their context. When that happens, or the user wants to step away, they need a single doc they can paste into a fresh session that lets the new session pick up **exactly** where the old one left off, with zero lost context.

This skill produces that doc.

## When to Run

- `/session-handoff` typed explicitly
- The user says "hand off this session", "wrap this for continuation", "summarize so I can paste into a new session", "compact this for me"
- Context is getting heavy and the user signals they want to keep going later
- End of a working session where work is mid-flight

## Hard Rules

1. **Output goes in a fenced code block.** The user will copy-paste it. Markdown rendering inside a fenced block is what they want (so `**bold**` shows as literal stars on paste). Wrap the ENTIRE handoff in a single ` ```markdown ` fence.
2. **Single asterisks for bold, plain numbered lists.** Inside the fence, write `*bold*` not `**bold**` when you want emphasis that survives paste.
3. **Write the handoff to disk too.** Path: `<project-root>/tasks/handoff_<YYYY-MM-DD>_<HHMM>.md` (use the project's existing `tasks/` dir if present, else create it at the project root). This is insurance against a copy-paste loss.
4. **Absolute file paths, full IDs, real URLs.** A fresh session has zero context. No "the file we edited", say `/abs/path/to/project/module/dashboard.py:42`. No "the n8n workflow", say workflow ID `AbC123xYz456`.
5. **No dashes as punctuation.** Periods and commas only. Hyphens in compound words like "white-label" are fine.
6. **Do not invent.** If you genuinely don't know something (e.g. why a decision was made), say "unclear from session" and let the new session ask.
7. **Surface uncommitted work.** Run `git status` and `git diff --stat` and list modified/untracked files in the handoff. If a fresh session starts and uncommitted changes get stomped, that's a disaster.
8. **One clear next move.** The handoff must end with a single concrete first instruction for the new session ("Open file X, finish function Y, then run command Z").

## Process

### Step 1: Gather state

Run in parallel where possible:

- `git status` and `git diff --stat` and `git log -5 --oneline` to see what's changed and recent commits
- `pwd` to confirm working directory
- Glob for any `tasks/todo.md` or `tasks/lessons.md` in the project root and read if present
- Glob for any obvious in-flight artifacts the session created (new files, drafts, scaffolds)
- Re-scan the conversation for: stated goal, key decisions made, files touched, commands run, blockers hit, things the user explicitly approved or rejected

### Step 2: Structure the handoff

Use this exact structure. Every section is required. If a section is genuinely empty, write "None." rather than skipping.

1. *MISSION*. One sentence on what this session is trying to accomplish, end-state defined. The "why we're here."
2. *PROJECT CONTEXT*. Working directory, repo, branch, key paths the new session needs to know. If multi-client, name the client. If internal work, name the workstream.
3. *DONE THIS SESSION*. Bullet list of what got finished. Each item with the file(s) touched or command(s) run. Specific, not vague.
4. *IN PROGRESS*. What's mid-flight right now. Current state of each thread. If a function is half-written, name the file and line. If a deploy is queued, say so. If the user is waiting on someone, name them.
5. *NEXT MOVE*. The single concrete first action for the new session. One step, not five. The next step after that can be listed as "then" but the headline is one action.
6. *FULL ROADMAP*. Numbered list of remaining steps after the next move, in order, with rough effort estimate where relevant. This is the path to MISSION.
7. *OPEN QUESTIONS / BLOCKERS*. Things waiting on the user, on a client, on an external system, or on a decision. Be explicit about who or what is blocking.
8. *KEY DECISIONS MADE*. Non-obvious calls the session made that the new session needs to know to stay consistent. e.g. "Decided to use Stripe not the booking platform for retreat checkout because X."
9. *FILES TOUCHED*. Absolute paths of every file created or modified this session, with one-line "what changed" each. Pulled from git status + new files written.
10. *UNCOMMITTED CHANGES*. Output of `git status --short` and `git diff --stat`. Flag if anything risks being lost.
11. *REFERENCES*. URLs, Notion page IDs, n8n workflow IDs, Airtable base/table IDs, Stripe object IDs, Slack channel IDs, ticket numbers, anything by ID that the new session will need to look up.
12. *GOTCHAS / LESSONS LEARNED THIS SESSION*. Non-obvious things the session learned that aren't yet in MEMORY.md or CLAUDE.md. Save a repeat mistake.
13. *RESUME PROMPT*. The exact text the new session will see as its first user message. Write it from the user's perspective, addressed to the assistant. End it with the one concrete next move from Section 5.

### Step 3: Write to disk

- Determine project root (walk up from cwd looking for `.git` or `CLAUDE.md`).
- Path: `<project-root>/tasks/handoff_<YYYY-MM-DD>_<HHMM>.md` using `{{TIMEZONE}}` local time.
- Create `tasks/` if it doesn't exist.
- Write the handoff doc (the same content that goes in the fenced block).

### Step 4: Output to chat

Output ONE message structured as:

````
*Handoff saved* to <absolute path>.

Copy the block below into a new session to continue:

```markdown
<the full handoff doc>
```
````

That's it. No preamble, no "Here's your handoff!" Just the path line and the block.

## Format Reference for the Handoff Doc Body

Inside the ` ```markdown ` fence, write the handoff like this (this is the content, not extra wrapping):

```
# Session Handoff. <YYYY-MM-DD HH:MM {{TIMEZONE}}>

## MISSION
<one sentence>

## PROJECT CONTEXT
- *Working dir:* <abs path>
- *Repo:* <name or "n/a">
- *Branch:* <name>
- *Client/workstream:* <e.g. clients/acme/deliverables/retreat_funnel>

## DONE THIS SESSION
1. <thing>. Files: <paths>. Verified by: <test/command/visual check>.
2. <thing>. Files: <paths>.

## IN PROGRESS
- *<thread name>:* <current state, specific>. File: <path:line>. Last action: <what was just attempted>.

## NEXT MOVE
*Open <file:line> and <action>.* Then <next step>.

## FULL ROADMAP
1. <step>
2. <step>
3. <step>

## OPEN QUESTIONS / BLOCKERS
- <blocker>. Waiting on: <who/what>. Since: <when>.

## KEY DECISIONS MADE
- *<decision>:* <why>. <implication for new session>.

## FILES TOUCHED
- <abs path>. <one line what changed>.

## UNCOMMITTED CHANGES
<output of git status --short>

## REFERENCES
- <label>: <id or URL>

## GOTCHAS / LESSONS LEARNED THIS SESSION
- <thing the new session would otherwise re-learn the hard way>.

## RESUME PROMPT
{{USER_NAME}} here. Picking up from a prior session. Read the handoff above, then <one concrete first action>. Don't re-ask questions answered above.
```

## Anti-Patterns (Do Not Do)

- *Vague handoffs.* "Worked on the funnel" is useless. "Added 2 sections to clients/acme/deliverables/retreat_funnel/index.html lines 340-410 (testimonials + final CTA), unstyled" is useful.
- *Skipping uncommitted-changes check.* This is the easiest way to lose work between sessions. Always run git status.
- *More than one "next move."* The new session needs ONE clear first instruction. Other steps go in FULL ROADMAP.
- *Burying the headline.* The fenced handoff block should be the second thing in the message, after the path line. Nothing else.
- *Long preamble outside the fence.* The user is copy-pasting. Keep the chat output minimal so the relevant block is easy to grab.
- *Dashes as punctuation.* Periods, commas, or rewrite.

## Example Output to Chat

````
*Handoff saved* to /abs/path/to/project/tasks/handoff_2026-06-09_2347.md.

Copy the block below into a new session to continue:

```markdown
# Session Handoff. 2026-06-09 23:47

## MISSION
Ship the Acme women's retreat funnel by June 2 with Stripe checkout, then launch retreat ads.

## PROJECT CONTEXT
- *Working dir:* /abs/path/to/project
- *Repo:* acme/project
- *Branch:* main
- *Client/workstream:* clients/acme/deliverables/retreat_funnel

[...full doc...]

## RESUME PROMPT
{{USER_NAME}} here. Picking up from a prior session. Read the handoff above, then open clients/acme/deliverables/retreat_funnel/configurator.js at line 88 and finish the Stripe payment_link integration started but not tested. Don't re-ask questions answered above.
```
````
