---
name: session-close
description: Closes out the current Claude Code session with a fast, verified recap. What the session's original intent was, whether it actually got accomplished (checked against git status, files on disk, and command/test evidence, not just the transcript's word for it), what else got done beyond the original ask, and what if anything is still needed from the user to call it closed. Chat output only, nothing written to disk. Triggers on /session-close, /closeout, /close, "close this out", "let's wrap this session", "give me the session recap", "did we accomplish what we set out to do", "what was the initial intention of this session", or whenever the user signals they are ending a session and want the accomplishment check. Do not use when the user wants to resume this exact work in a NEW session later (that is session-handoff, which produces a long copy-paste continuation doc), for daily journaling, or for writing decisions into project memory.
allowed-tools: Bash, Read, Grep, Glob
---

# Session Close

## Purpose

Most working sessions end the same way: you want to know if the thing you came in to do actually got done, what else happened along the way, and whether anything is still hanging that needs you before you move on. This skill is that question, automated and sharpened.

The output is a verified accomplishment check, not a summary. A summary describes activity. This confirms outcome.

Pairs with `session-handoff`: close when the work is finished, hand off when it is not.

## When to Run

- `/session-close`, `/closeout`, or `/close` typed explicitly
- "close this out", "let's wrap this session", "wrap this up", "give me the recap", "did we accomplish what we set out to do", "is this done"
- Any point the user signals they are ending the session and want the closeout check before they go

Do not use for:
- Resuming this same work in a fresh session later. That is `session-handoff`, a different job (long technical continuation doc, written to disk, meant to be pasted elsewhere).
- Daily journaling.
- Writing session decisions into project memory. That happens through the normal memory process, not this skill.

## Hard Rules

1. **Verify, don't recall.** Never mark something accomplished because the transcript says it happened. Check it: files exist, commands ran clean, tests passed. If it can't be checked, say so, don't round up to "done."
2. **Answer the yes/no plainly.** Was the original intent accomplished: yes, no, or partial. No hedging, no "sort of, in a sense."
3. **If the session drifted, name it once.** If the actual work diverged from the original ask and that ask never got closed, say so directly, in one line. Not a lecture, just the fact.
4. **Short. Scannable in under 60 seconds.** No emoji walls, no filler, no "Great session!"
5. **Open loops are decisions, not questions.** State what's needed from the user as a specific action ("needs your go on X", "needs the API key for Y"), not a vague "let me know what you think."
6. **Nothing written to disk.** This is a chat answer, not a document. If the user wants it saved, that's a separate ask.

## Process

### Step 1: Find the original intent

Scan back to the first real user message in the conversation, the one that set the session's actual goal (skip past injected system reminders and memory context, those aren't the ask). Paraphrase it in one line, specific enough that the user recognizes it instantly. "Fix the inbox-draft threading bug" not "some technical work."

If the conversation has been compacted, the summary at the top of context carries the original intent forward, use that. If even that doesn't make the original ask clear, say "original intent unclear from available context" rather than inventing one.

### Step 2: Gather verification evidence

Run in parallel where possible:

- `git status --short`
- `git diff --stat`
- `git log --oneline -8`
- Glob for `tasks/todo.md` in the project root and read it if present, it may already carry a review section from earlier in the session.
- For every deliverable claimed finished earlier in the conversation (a file written, a script run, a fix applied), spot check it: Read the file, Grep for the change, rerun the command if cheap to do. Don't take the transcript's word for it.

### Step 3: Judge accomplishment honestly

- **Yes**, only if the original ask has direct, checked evidence of completion.
- **Partial**, if some but not all of the ask landed, or it landed but was never actually verified (code written, never run).
- **No**, if the original ask never got closed, even if the session was busy. Say so plainly. This is the accountability check, not a formality.

### Step 4: Compile what else happened

List real accomplishments beyond the original ask, each one line, concrete (name the file or command, not "worked on some stuff"). If the extra work effectively replaced the original ask and that ask is still open, flag it as drift here, once, directly.

### Step 5: Compile open loops

Anything that needs a decision, approval, credential, or outside action from the user before this is actually closed. State each as a specific action. If there's genuinely nothing, say so.

### Step 6: Output

One chat message. Exact structure below. Nothing else, no preamble before it.

## Output Format

```
*Original ask:* <one line, specific>

*Accomplished:* Yes / No / Partial. <one line, tied to actual evidence from Step 2>

*Also this session:*
- <concrete bullet, file or command named>
- <concrete bullet>

(or, if nothing beyond the ask: "Nothing beyond the original ask.")

*Open loops, need from you:*
- <specific decision or action needed>

(or, if none: "None. Clean close.")

*Next move:* <the one thing that closes this out, if not already closed. If fully closed: "Nothing pending, you're clear to move on.">
```

## Example

Session opened with: "fix the inbox-draft threading bug, subject search is dropping matches when there's punctuation in the line."

```
*Original ask:* Fix inbox-draft subject search dropping thread matches when the subject has punctuation.

*Accomplished:* Yes. Root cause was the search matching on the raw string instead of a punctuation-stripped comparison. Fixed in the matcher, verified against three subject lines that were previously failing to thread, all three now match. Committed as 50a6aeb.

*Also this session:*
- Caught and fixed a second edge case in the same function (double spaces after punctuation strip) while verifying the first fix.

*Open loops, need from you:*
None. Clean close.

*Next move:* Nothing pending, you're clear to move on.
```

## Never Do

- Never mark "Accomplished: Yes" on the strength of the transcript alone. Check it.
- Never produce a long handoff-style document here, that's a different skill.
- Never pad with congratulations, hype, or "Great work this session!"
- Never phrase an open loop as a vague open question. Name the specific decision or action needed.
- Never write files or save anything to disk as part of this skill.
