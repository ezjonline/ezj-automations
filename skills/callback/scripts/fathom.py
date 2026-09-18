#!/usr/bin/env python3
"""Pull calls out of Fathom for Callback.

  python3 fathom.py list [--days 14]
  python3 fathom.py transcript <recording_id> [--out call.txt]
  python3 fathom.py download <recording_id> [--out call.mp4]

Needs FATHOM_API_KEY in the environment (Fathom > Settings > API Access).
`download` needs yt-dlp and a public share link on the recording
(Fathom > the call > Share > anyone with the link).
"""
import argparse
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.fathom.ai/external/v1"

try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()


def get(path, params=None):
    key = os.environ.get("FATHOM_API_KEY")
    if not key:
        sys.exit("FATHOM_API_KEY is not set. Make one in Fathom > Settings > API Access, then: export FATHOM_API_KEY=...")
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"X-Api-Key": key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            sys.exit(f"Fathom said {e.code}. The API key is wrong or revoked.")
        sys.exit(f"Fathom said {e.code} on {path}: {e.read()[:300]!r}")


def meetings(days):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    cursor, out = None, []
    while True:
        data = get("/meetings", {"limit": 50, **({"cursor": cursor} if cursor else {})})
        for m in data.get("items") or []:
            if (m.get("recording_start_time") or "") < cutoff:
                return out
            out.append(m)
        cursor = data.get("next_cursor")
        if not cursor:
            return out


def find(recording_id):
    for m in meetings(365):
        if str(m.get("recording_id")) == str(recording_id):
            return m
    sys.exit(f"No recording {recording_id} in the last year. Run `list` to see the ids.")


def secs(ts):
    parts = [float(p) for p in str(ts).split(":")]
    total = 0.0
    for p in parts:
        total = total * 60 + p
    return total


def cmd_list(a):
    for m in meetings(a.days):
        who = ", ".join(i.get("name") or i.get("email") or "?" for i in m.get("calendar_invitees") or [])
        when = (m.get("recording_start_time") or "")[:16].replace("T", " ")
        print(f"{m.get('recording_id')}  {when}  {m.get('title') or m.get('meeting_title')}  [{who}]")


def cmd_transcript(a):
    data = get(f"/recordings/{a.recording_id}/transcript")
    segs = data.get("transcript") if isinstance(data, dict) else data
    if not segs:
        sys.exit("Fathom returned no transcript for that recording yet. Try again once it finishes processing.")
    lines = []
    for s in segs:
        sp = s.get("speaker") or {}
        name = sp.get("display_name") if isinstance(sp, dict) else str(sp)
        lines.append(f"[{secs(s.get('timestamp') or 0):8.1f}] {name}: {s.get('text', '').strip()}")
    text = "\n".join(lines) + "\n"
    if a.out:
        open(a.out, "w").write(text)
        print(f"wrote {len(lines)} lines to {a.out}")
    else:
        sys.stdout.write(text)


def cmd_download(a):
    if not shutil.which("yt-dlp"):
        sys.exit("yt-dlp is not installed. Mac: brew install yt-dlp. Anywhere: pip install yt-dlp")
    m = find(a.recording_id)
    url = m.get("share_url")
    if not url:
        sys.exit("This recording has no share link. In Fathom open the call, click Share, allow anyone with the link, then rerun.")
    out = a.out or re.sub(r"[^a-z0-9]+", "_", (m.get("title") or str(a.recording_id)).lower()).strip("_") + ".mp4"
    subprocess.run(["yt-dlp", "--no-progress", "-o", out, url], check=True)
    print(f"saved {out}")


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("list"); s.add_argument("--days", type=int, default=14); s.set_defaults(fn=cmd_list)
s = sub.add_parser("transcript"); s.add_argument("recording_id"); s.add_argument("--out"); s.set_defaults(fn=cmd_transcript)
s = sub.add_parser("download"); s.add_argument("recording_id"); s.add_argument("--out"); s.set_defaults(fn=cmd_download)
a = p.parse_args()
a.fn(a)
