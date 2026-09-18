---
name: callback
description: Turns a Fathom call recording into vertical short-form reels (IG Reels, TikTok, YouTube Shorts) built on the call reel format that hit ~100k views. You on top, the guest's reaction on the bottom (or your screen share in the middle), a cold open on the most viral line from anyone on the call, word-by-word captions, sticker beats narrating the reaction, and a seamless loop. Claude Code reads the transcript, picks the bangers, looks at the frames to set the crops, and renders with ffmpeg. Use when someone says "cut reels from my call", "clip my last Fathom call", "find the bangers in that call", "turn my sales call into content", "/callback", or after any call worth repurposing. Do not use for footage filmed on a phone, for writing a reel script from scratch, or for long-form YouTube edits.
---

# Callback

Your sales calls are the best content you are not posting. The moment a prospect's face goes from confused to "take my money" is proof no scripted reel can fake. Callback pulls the call from Fathom, finds those moments, and cuts them into vertical reels in one consistent format.

Claude Code does the thinking (picking moments, choosing the cold open, reading frames for crops, writing stickers). Two small scripts do the plumbing: `scripts/fathom.py` and `scripts/render_reel.py`.

## Setup (once)

1. Tools: `ffmpeg`, `yt-dlp`, Python 3 with Pillow, and whisper for word captions.
   Mac: `brew install ffmpeg yt-dlp && pip3 install pillow openai-whisper`.
   Linux: install ffmpeg with your package manager, then `pip3 install yt-dlp pillow openai-whisper`.
2. Fathom API key: Fathom, Settings, API Access, generate a key. Then `export FATHOM_API_KEY=...` (add it to your shell profile so it sticks).
3. Check it: `python3 ~/.claude/skills/callback/scripts/fathom.py list --days 14` prints your recent calls.

If a tool is missing, install it for the user and say what you installed.

## Process

1. **Pick the call.** Run `python3 ~/.claude/skills/callback/scripts/fathom.py list --days 14`. If the user named a person or date, match it. Otherwise show the list and ask which call. Skip internal team calls and family calls.

2. **Consent check.** Ask one question before anything renders: "Is everyone on this call OK with being in a public reel?" If a guest has not agreed, cut in the faces hidden layout (see step 6) or stop. Never post a client's face without their yes.

3. **Pull the transcript.** `python3 ~/.claude/skills/callback/scripts/fathom.py transcript <id> --out callback/<call>/transcript.txt`. Every line is `[seconds] Speaker: text`.

4. **Find the moments.** Read the whole transcript and score every candidate window against `references/hook-formula.md`. Keep windows of 20 to 60 seconds that score 7 or higher. For each keeper, write down: the window start and end, the cold open line (timestamp, speaker, 1.5 to 6 seconds long), whether it loops, whether a screen share is on screen during it, and 3 to 6 stickers. Show the user the ranked list with the cold open quoted and ask which to render (default: the top 3).

5. **Download the recording.** `python3 ~/.claude/skills/callback/scripts/fathom.py download <id> --out callback/<call>/call.mp4`. If it fails for lack of a share link, tell the user to open the call in Fathom, click Share, allow anyone with the link, then rerun.

6. **Set the crops by looking.** For each moment grab a frame from the middle of the window and read it:
   `ffmpeg -y -v error -ss <t> -i call.mp4 -frames:v 1 callback/<call>/frame_<t>.jpg`
   Get the source size with `ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 call.mp4`. Then pick the layout:
   - **halves** (top 960, bottom 960): the host on top, the guest on the bottom. The default when both cameras are on.
   - **stack** (top 600, middle 720, bottom 600): host, screen share, guest. Use it when a share is up during the whole window and it shows what is being talked about.
   - **faces hidden**: halves with the host on top and the screen share on the bottom, no guest face at all.

   Crops are `[x, y, w, h]` in source pixels. Frame each face with headroom. Keep the crop's aspect near the zone's (1080x960 is 1.125 wide per tall, 1080x600 is 1.8, 1080x720 is 1.5). The renderer fills the zone, so an off-aspect crop gets trimmed at the edges. **Never include a name label, a notetaker bot tile, or the call app's toolbar.** Grab a second frame near the end of the window: if the grid reshuffled, split the moment or pick a different one.

7. **Check the screen.** If a share is in the frame, read every line on it. Client names, revenue, inboxes, CRMs: set `"blur": 4` or higher, or pick a layout without the share.

8. **Write the spec** to `callback/<call>/<slug>.json` (field list at the top of `scripts/render_reel.py`):
   ```json
   {"source": "callback/<call>/call.mp4", "out": "callback/<call>/reels/<slug>.mp4",
    "layout": "halves", "crops": {"top": [100, 0, 376, 334], "bottom": [540, 364, 366, 325]},
    "segments": [[2288.4, 2292.9], [2205.0, 2288.4]], "captions": "whisper",
    "stickers": [{"text": "Taking them from confused to 'take my money' in 30 secs", "at": 0, "dur": 4, "zone": "center"},
                 {"text": "Wait for their reaction", "at": 6, "dur": 3, "zone": "bottom"}]}
   ```
   Segment one is the cold open. Segment two is the moment from its real start. For a loop, end segment two right before the cold open line so the replay runs straight into it. Pad every segment edge by 0.2 seconds so no word gets clipped. Sticker `at` is seconds into the finished reel.

9. **Render.** `python3 ~/.claude/skills/callback/scripts/render_reel.py callback/<call>/<slug>.json`. Whisper captions take about a minute on a laptop.

10. **QC every reel.** Stills lie about video, so run both:
    ```
    ffmpeg -i <reel> -vf blackdetect=d=0.02:pix_th=0.10 -an -f null - 2>&1 | grep -c black_start
    ffmpeg -i <reel> -vf 'crop=1080:560:0:0,freezedetect=n=0.003:d=1.5' -an -f null - 2>&1 | grep -c freeze_start
    ```
    Both should print 0. Then pull 4 frames across the reel and look at them: the right face in each zone, captions readable, no sticker covering a face, nothing private on the screen. Fix whisper mishearings in `lines` if a caption is wrong, never reword what anyone said.

11. **Hand it over** in the output format below, with a caption for each reel.

## Output format

```
CALLBACK: <call title>, <date>
1. reels/<slug>.mp4 (<n>s, halves | stack | faces hidden, loops: yes | no)
   Opens on: "<cold open>" (<speaker>)
   Caption: <hook line>. Comment "<KEYWORD>" and I'll send you <the thing>.
DROPPED: <moment>: <why>
CHECK BEFORE POSTING: <anything on a screen share, who still has to say yes>
QC: black 0, freeze 0 on every reel
```

## Example

User: "cut reels from my call with Sam yesterday". Claude lists the calls, finds Sam's, asks the consent question (yes), pulls the transcript and scores it. The best window is Sam watching a demo of an Instagram research agent: 9/10, cold open on Sam saying "this is sick" at 2288s, a share is up the whole time and shows the agent, so the layout is stack. Claude grabs a frame, sets the top crop on the host's tile, the middle on the share, the bottom on Sam's tile with no name labels, blurs the share at 4 because a client dashboard is visible, and writes five stickers: the title card, "Wait for their reaction", "It just clicked", "Now FOMO sets in...", "SOLD". The reel ends right before "this is sick" so it loops. QC prints 0 and 0. Claude hands over `reels/research_agent_reaction.mp4` with the caption "They saw this and said take my money. Comment AGENT and I'll send it to you."

## Never do

- Never render a call before the user confirms the guests agreed to be in public content.
- Never invent, reword or "clean up" what someone said in a caption or sticker. Fix mishearings only.
- Never open a reel on setup ("so what I did was") when a stronger line exists in the window.
- Never show a name label, a notetaker bot tile, or the meeting toolbar in a crop.
- Never ship a reel with a readable screen share you have not read line by line.
- Never put a guest's name or handle on screen. Stickers say they or them.
- Never clip team meetings, internal handoffs or family calls.
- Never post anything yourself. Callback makes files. The user posts.
