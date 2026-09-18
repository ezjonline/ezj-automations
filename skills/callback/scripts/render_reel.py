#!/usr/bin/env python3
"""Render one vertical call reel from a spec file.

  python3 render_reel.py spec.json

Needs ffmpeg and Pillow (pip install pillow). Word-level captions need
openai-whisper (pip install openai-whisper); without it, pass "lines" in the spec.
Uses only core ffmpeg filters (crop, scale, vstack, drawbox, overlay, concat),
so it works on builds without libass or drawtext.

Spec (all times in SOURCE seconds unless noted):
{
  "source": "call.mp4",
  "out": "reels/this_is_sick.mp4",
  "layout": "stack",                    stack = top 600 / middle 720 / bottom 600
                                        halves = top 960 / bottom 960
  "crops": {"top": [x, y, w, h],        you, from the source frame
            "middle": [x, y, w, h],     the screen share (stack only)
            "bottom": [x, y, w, h]},    the guest
  "blur": 0,                            blur on the middle band, raise it if client info is on screen
  "segments": [[2288.4, 2292.9], [2205.0, 2288.4]],   in order, first one is the cold open
  "captions": "whisper",                or "none"
  "lines": [[2205.0, 2209.5, "text"]],  fallback captions when whisper is not installed
  "stickers": [{"text": "Wait for their reaction", "at": 6.0, "dur": 3, "zone": "bottom"}],
                                        "at" is REEL seconds, zone = top | center | bottom, emoji are dropped
  "accent": "#F47C20",
  "font": "/path/to/Bold.ttf"           optional
}
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
LAYOUTS = {
    "stack": [("top", 0, 600), ("middle", 600, 720), ("bottom", 1320, 600)],
    "halves": [("top", 0, 960), ("bottom", 960, 960)],
}
FONTS = [
    "~/Library/Fonts/Montserrat-ExtraBold.ttf", "~/Library/Fonts/Montserrat-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"command failed: {' '.join(cmd[:6])}...\n{r.stderr[-1500:]}")
    return r.stdout


def font(spec, size):
    for f in [spec.get("font")] + FONTS:
        if f and os.path.exists(os.path.expanduser(f)):
            return ImageFont.truetype(os.path.expanduser(f), size)
    return ImageFont.load_default(size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=fnt) <= width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = word
    return lines + [cur] if cur else lines


def caption_png(spec, text, path):
    fnt = font(spec, 64)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines = wrap(probe, text, fnt, 920)
    lh = 78
    img = Image.new("RGBA", (W, lh * len(lines) + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        d.text((W / 2, 15 + i * lh + lh / 2), line, font=fnt, anchor="mm",
               fill="white", stroke_width=7, stroke_fill="black")
    img.save(path)
    return img.size


def plain(text):
    # Text fonts have no emoji glyphs; they render as empty boxes, so drop them.
    return " ".join("".join(c for c in text if ord(c) < 0x2190 or 0x2E80 <= ord(c) < 0x1F000).split())


def sticker_png(spec, text, path):
    text = plain(text)
    fnt = font(spec, 50)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines = wrap(probe, text, fnt, 820)
    lh, pad = 62, 30
    tw = max(probe.textlength(l, font=fnt) for l in lines)
    box = Image.new("RGBA", (int(tw + pad * 2), lh * len(lines) + pad * 2 - 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(box)
    d.rounded_rectangle([0, 0, box.width - 1, box.height - 1], radius=22, fill="white")
    for i, line in enumerate(lines):
        d.text((box.width / 2, pad - 5 + i * lh + lh / 2), line, font=fnt, anchor="mm", fill="black")
    box = box.rotate(2.5, expand=True, resample=Image.BICUBIC)
    box.save(path)
    return box.size


def cut_segment(spec, seg, idx, work):
    a, b = seg
    zones = LAYOUTS[spec["layout"]]
    parts, labels = [], []
    for name, _, zh in zones:
        x, y, w, h = spec["crops"][name]
        f = f"crop={w}:{h}:{x}:{y},scale={W}:{zh}:force_original_aspect_ratio=increase,crop={W}:{zh},setsar=1"
        if name == "middle" and spec.get("blur"):
            f += f",gblur=sigma={spec['blur']}"
        parts.append(f"[s{len(parts)}]{f}[{name}]")
        labels.append(f"[{name}]")
    accent = spec.get("accent", "#F47C20").replace("#", "0x")
    seams = ",".join(f"drawbox=x=0:y={top - 1}:w={W}:h=3:color={accent}:t=fill" for _, top, _ in zones[1:])
    fc = (f"[0:v]split={len(zones)}" + "".join(f"[s{i}]" for i in range(len(zones))) + ";"
          + ";".join(parts) + ";" + "".join(labels) + f"vstack=inputs={len(zones)},fps=30,{seams}[v]")
    out = os.path.join(work, f"seg{idx}.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(a), "-to", str(b), "-i", spec["source"],
         "-filter_complex", fc, "-map", "[v]", "-map", "0:a:0",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-ar", "48000", out])
    return out


def whisper_words(seg_file, work, idx):
    if not shutil.which("whisper"):
        return None
    wav = os.path.join(work, f"seg{idx}.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", seg_file, "-ac", "1", "-ar", "16000", wav])
    run(["whisper", wav, "--model", "small", "--language", "en", "--word_timestamps", "True",
         "--output_format", "json", "--output_dir", work, "--fp16", "False", "--verbose", "False"])
    data = json.load(open(os.path.join(work, f"seg{idx}.json")))
    return [(w["start"], w["end"], w["word"].strip()) for s in data["segments"] for w in s.get("words", [])]


def chunk(words, max_words=3, max_len=1.4):
    out, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w[1] - cur[0][0] > max_len):
            out.append((cur[0][0], cur[-1][1], " ".join(x[2] for x in cur)))
            cur = []
        cur.append(w)
        if w[2][-1:] in ".?!":
            out.append((cur[0][0], cur[-1][1], " ".join(x[2] for x in cur)))
            cur = []
    if cur:
        out.append((cur[0][0], cur[-1][1], " ".join(x[2] for x in cur)))
    return out


def captions(spec, seg_files, work):
    caps, offset = [], 0.0
    for i, ((a, b), f) in enumerate(zip(spec["segments"], seg_files)):
        words = whisper_words(f, work, i) if spec.get("captions", "whisper") == "whisper" else None
        if words is not None:
            caps += [(offset + s, offset + e, t) for s, e, t in chunk(words)]
        else:
            for s, e, t in spec.get("lines", []):
                s, e = max(s, a), min(e, b)
                if s < e:
                    caps.append((offset + s - a, offset + e - a, t))
        offset += b - a
    # One caption on screen at a time: hold each until the next starts, never past it.
    caps.sort()
    for i in range(len(caps) - 1):
        s, e, t = caps[i]
        nxt = caps[i + 1][0]
        caps[i] = (s, nxt - 0.02 if nxt - e < 0.4 or nxt < e else e, t)
    return [c for c in caps if c[1] > c[0]], offset


def main():
    spec = json.load(open(sys.argv[1]))
    if spec["layout"] not in LAYOUTS:
        sys.exit("layout must be stack or halves")
    work = tempfile.mkdtemp(prefix="callback_")
    seg_files = [cut_segment(spec, s, i, work) for i, s in enumerate(spec["segments"])]
    caps, total = captions(spec, seg_files, work)
    if spec.get("captions") != "none" and not caps:
        print("warning: no captions. Install whisper (pip install openai-whisper) or pass lines.")

    cap_y = {"stack": 1250, "halves": 960}[spec["layout"]]
    zone_y = {"top": 70, "center": 640 if spec["layout"] == "stack" else 730,
              "bottom": 1360 if spec["layout"] == "stack" else 1010}
    overlays = []
    for i, (s, e, t) in enumerate(caps):
        p = os.path.join(work, f"cap{i}.png")
        w, h = caption_png(spec, t, p)
        overlays.append((p, 0, cap_y - h // 2, s, e))
    for i, st in enumerate(spec.get("stickers", [])):
        p = os.path.join(work, f"stk{i}.png")
        w, h = sticker_png(spec, st["text"], p)
        overlays.append((p, (W - w) // 2, zone_y[st.get("zone", "center")], st["at"], st["at"] + st.get("dur", 3)))

    n = len(seg_files)
    inputs = sum((["-i", f] for f in seg_files), []) + sum((["-i", o[0]] for o in overlays), [])
    fc = "".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v0][a0]"
    for k, (_, x, y, s, e) in enumerate(overlays):
        fc += f";[v{k}][{n + k}:v]overlay={x}:{y}:enable='between(t,{s:.2f},{e:.2f})'[v{k + 1}]"
    fc += f";[a0]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
    os.makedirs(os.path.dirname(os.path.abspath(spec["out"])), exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc,
         "-map", f"[v{len(overlays)}]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium",
         "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", spec["out"]])
    shutil.rmtree(work, ignore_errors=True)
    print(f"rendered {spec['out']} ({total:.1f}s, {len(caps)} captions, {len(spec.get('stickers', []))} stickers)")


if __name__ == "__main__":
    main()
