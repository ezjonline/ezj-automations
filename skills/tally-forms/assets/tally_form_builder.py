"""
Reusable Tally form creator. Builds a Tally form from a simple Python
question list, calls the Tally API, returns the responder URL.

EVERY form built through this module ships branded by default (see BRAND_STYLE
below): dark background, white text, one accent colour on links, focus rings and
buttons, your logo in the header, and a multi-step progress bar. The shipped
palette is EZJ Online's. Change BRAND_ACCENT, BRAND_BG and BRAND_LOGO_URL to make
it yours. Pass styles=None, logo=None for a plain unbranded Tally form.

Block types supported by the `questions` list:

  Structure
    {"type": "page_break"}                      real multi-step Next/Back split
    {"type": "heading",     "title": "..."}     big section header (HEADING_2)
    {"type": "subheading",  "title": "..."}     smaller header (HEADING_3)
    {"type": "label",       "title": "..."}     small bold label (LABEL)
    {"type": "instruction", "title": "..."}     prose / helper copy (TEXT, HTML ok)
    {"type": "divider"}                         horizontal rule
    {"type": "thank_you",   "title": "..."}     custom thank-you screen

  Inputs (all take "title", optional "placeholder", "required")
    short_text, long_text, email, number, phone, website, date, file_upload
    {"type": "multiple_choice", "options": [...]}   radio list
    {"type": "checkboxes",      "options": [...]}   multi-select
    {"type": "dropdown",        "options": [...]}   dropdown
    {"type": "linear_scale", "min": 1, "max": 10, "min_label": "", "max_label": ""}
    {"type": "rating",       "max": 5, "shape": "STAR"}

Usage from another script:

    from scripts.create_tally_form import create_form
    form_id, responder_url = create_form(
        title="🚀 My Form",
        questions=[...],
        status="PUBLISHED",
        description=None,
    )

Needs TALLY_API_KEY in the environment, or in a .env file in the directory you
run from. Get one at tally.so, Settings, then API keys.
"""

import os
import uuid
import json
import sys
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

TALLY_API_BASE = "https://api.tally.so"


def _api_key_from_env() -> Optional[str]:
    """TALLY_API_KEY from the environment, or a .env in the working directory."""
    load_dotenv()
    return os.environ.get("TALLY_API_KEY")

# ---------------------------------------------------------------------------
# Brand style. Edit these three values and every form you build follows them.
# ---------------------------------------------------------------------------
# Verified live against the Tally respond-page renderer 2026-09-20. The custom
# palette ONLY applies when theme is "CUSTOM" and the colours sit under the
# nested "color" key. Flat keys (backgroundColor, accentColor, ...) are stored
# by the API but silently ignored by the renderer, and unknown keys inside
# `styles` make the respond page 500. Do not "tidy" this shape.
#
# The shipped palette is EZJ Online's, true black and orange. Swap in your own.
# Keep the background a true near-black rather than a warm brown-black, and never
# put a gradient here, Tally renders it badly.
BRAND_ACCENT = "#F47C20"
BRAND_BG = "#0d0d0d"
BRAND_LOGO_URL = "https://www.ezjonline.com/assets/logo-icon.png"

BRAND_STYLE = {
    "theme": "CUSTOM",
    "color": {
        "background": BRAND_BG,
        "text": "#FFFFFF",
        "accent": BRAND_ACCENT,
        "buttonBackground": BRAND_ACCENT,
        "buttonText": BRAND_BG,
    },
}

# Progress bar + resume + partial capture are what make a long multi-step form
# feel light. pageAutoJump stays off so a mis-click never skips a step.
BRAND_SETTINGS = {
    "language": "en",
    "hasProgressBar": True,
    "hasPartialSubmissions": True,
    "pageAutoJump": False,
    "saveForLater": True,
}



def _u() -> str:
    return str(uuid.uuid4())


def _block(block_type: str, group_uuid: str, group_type: str, payload: dict) -> dict:
    return {
        "uuid": _u(),
        "type": block_type,
        "groupUuid": group_uuid,
        "groupType": group_type,
        "payload": payload,
    }


def _build_question(q: dict, is_first: bool = False) -> list[dict]:
    """One question becomes a TITLE block plus one or more input/option blocks,
    all sharing the same groupUuid. Tally validation requires an `isFirst` flag
    inside the payload of the FIRST option in dropdown/multiple-choice groups
    (and `isFirst: false` on subsequent options).

    The special `instruction` type renders prose between questions with no input
    field. Use it for setup steps, links, and explanations the person filling it in needs to read.

    The special `page_break` type splits the form into a real multi-step Tally
    form (Next/Back buttons, one screen per step) instead of one long scroll.
    Verified against Tally's real block shape (a standalone PAGE_BREAK block,
    same generic shape as TEXT, its own groupUuid, groupType == type, empty
    payload). Put one before each new phase/section."""
    qtype = q["type"]

    if qtype == "instruction":
        # Pure prose block, no input expected. Use Tally's TEXT block type.
        return [_block(
            "TEXT", _u(), "TEXT",
            {"html": q["title"]},
        )]

    if qtype in ("heading", "subheading", "label"):
        # Section furniture. HEADING_2 is the section header carrying the
        # emoji, HEADING_3 a sub-header, LABEL a small bold line above a
        # cluster of inputs. All three are plain HTML blocks like TEXT.
        block_type = {
            "heading": "HEADING_2",
            "subheading": "HEADING_3",
            "label": "LABEL",
        }[qtype]
        return [_block(block_type, _u(), block_type, {"html": q["title"]})]

    if qtype == "divider":
        return [_block("DIVIDER", _u(), "DIVIDER", {})]

    if qtype == "thank_you":
        # Tally has no THANK_YOU_PAGE block type. A thank-you screen is a
        # PAGE_BREAK flagged isThankYouPage, with the copy in blocks after it.
        return [
            _block("PAGE_BREAK", _u(), "PAGE_BREAK", {
                "isThankYouPage": True,
                "isQualifiedForThankYouPage": True,
            }),
            _block("HEADING_2", _u(), "HEADING_2", {
                "html": q.get("title", "Got it. 🎉"),
            }),
        ] + ([_block("TEXT", _u(), "TEXT", {"html": q["body"]})] if q.get("body") else [])

    if qtype == "page_break":
        # index/isFirst/isLast are filled in by _finalise_page_breaks once the
        # whole block list is known, so the step counter reads "2 of 5".
        return [_block("PAGE_BREAK", _u(), "PAGE_BREAK", {
            "isQualifiedForThankYouPage": False,
            "isThankYouPage": False,
        })]

    title = q["title"]
    required = q.get("required", False)
    placeholder = q.get("placeholder", "")
    group_uuid = _u()

    title_block = _block(
        "TITLE",
        group_uuid,
        "QUESTION",
        {"html": title},
    )
    # Input/option blocks get a SEPARATE groupUuid from the title block per
    # current Tally validation (changed sometime in May 2026: "TITLE block must
    # not share groupUuid with an input block").
    input_group_uuid = _u()

    if qtype == "short_text":
        return [title_block, _block(
            "INPUT_TEXT", input_group_uuid, "INPUT_TEXT",
            {"isRequired": required, "placeholder": placeholder},
        )]

    if qtype == "long_text":
        return [title_block, _block(
            "TEXTAREA", input_group_uuid, "TEXTAREA",
            {"isRequired": required, "placeholder": placeholder},
        )]

    if qtype == "email":
        return [title_block, _block(
            "INPUT_EMAIL", input_group_uuid, "INPUT_EMAIL",
            {"isRequired": required, "placeholder": placeholder or "your@email.com"},
        )]

    if qtype == "multiple_choice":
        opts = q["options"]
        # Tally renders option groups correctly only when option blocks share a
        # groupUuid that is DIFFERENT from the title block's groupUuid.
        options_group_uuid = _u()
        option_blocks = [
            _block(
                "MULTIPLE_CHOICE_OPTION", options_group_uuid, "MULTIPLE_CHOICE",
                {
                    "index": i,
                    "text": opt,
                    "isFirst": (i == 0),
                    "isLast": (i == len(opts) - 1),
                    "isRequired": required if i == 0 else False,
                },
            )
            for i, opt in enumerate(opts)
        ]
        return [title_block, *option_blocks]

    if qtype == "dropdown":
        opts = q["options"]
        options_group_uuid = _u()
        option_blocks = [
            _block(
                "DROPDOWN_OPTION", options_group_uuid, "DROPDOWN",
                {
                    "index": i,
                    "text": opt,
                    "isFirst": (i == 0),
                    "isLast": (i == len(opts) - 1),
                    "isRequired": required if i == 0 else False,
                },
            )
            for i, opt in enumerate(opts)
        ]
        return [title_block, *option_blocks]

    simple_inputs = {
        "number": ("INPUT_NUMBER", ""),
        "phone": ("INPUT_PHONE_NUMBER", "+1 555 000 0000"),
        "website": ("INPUT_LINK", "https://"),
        "url": ("INPUT_LINK", "https://"),
        "date": ("INPUT_DATE", ""),
    }
    if qtype in simple_inputs:
        block_type, default_placeholder = simple_inputs[qtype]
        return [title_block, _block(
            block_type, input_group_uuid, block_type,
            {"isRequired": required, "placeholder": placeholder or default_placeholder},
        )]

    if qtype == "file_upload":
        return [title_block, _block(
            "FILE_UPLOAD", input_group_uuid, "FILE_UPLOAD",
            {"isRequired": required},
        )]

    if qtype == "linear_scale":
        # The API rejects unknown payload keys outright, and the end labels are
        # gated behind their has* flags: sending leftLabel without hasLeftLabel
        # is a 400, and sending hasLeftLabel without leftLabel is too.
        payload = {
            "isRequired": required,
            "start": q.get("min", 1),
            "end": q.get("max", 10),
            "step": q.get("step", 1),
        }
        if q.get("min_label"):
            payload["hasLeftLabel"] = True
            payload["leftLabel"] = q["min_label"]
        if q.get("max_label"):
            payload["hasRightLabel"] = True
            payload["rightLabel"] = q["max_label"]
        return [title_block, _block(
            "LINEAR_SCALE", input_group_uuid, "LINEAR_SCALE", payload,
        )]

    if qtype == "rating":
        return [title_block, _block(
            "RATING", input_group_uuid, "RATING",
            {"isRequired": required, "stars": q.get("stars", q.get("max", 5))},
        )]

    if qtype == "checkboxes":
        opts = q["options"]
        options_group_uuid = _u()
        option_blocks = [
            _block(
                "CHECKBOX", options_group_uuid, "CHECKBOXES",
                {
                    "index": i,
                    "text": opt,
                    "isFirst": (i == 0),
                    "isLast": (i == len(opts) - 1),
                    "isRequired": required if i == 0 else False,
                },
            )
            for i, opt in enumerate(opts)
        ]
        return [title_block, *option_blocks]

    raise ValueError(f"Unknown question type: {qtype}")


def _finalise_page_breaks(blocks: list[dict]) -> list[dict]:
    """Number the PAGE_BREAK blocks so Tally's step counter and Back button
    behave. Tally reads index/isFirst/isLast off each break; leaving them out
    renders the form but the progress bar has nothing to count against."""
    breaks = [
        b for b in blocks
        if b["type"] == "PAGE_BREAK" and not b["payload"].get("isThankYouPage")
    ]
    for i, b in enumerate(breaks):
        b["payload"].update({
            "index": i,
            "isFirst": (i == 0),
            "isLast": (i == len(breaks) - 1),
        })
    return blocks


def _assemble_blocks(
    title: str,
    questions: list[dict],
    description: Optional[str],
    logo: Optional[str],
) -> list[dict]:
    """FORM_TITLE (carrying the logo) + optional intro prose + every question,
    with the page breaks numbered. Shared by create_form and update_form so the
    two can never drift apart."""
    form_title_payload = {"html": title, "title": title}
    if logo:
        form_title_payload["logo"] = logo

    blocks: list[dict] = [{
        "uuid": _u(),
        "type": "FORM_TITLE",
        "groupUuid": _u(),
        "groupType": "TEXT",
        "payload": form_title_payload,
    }]

    if description:
        blocks.append({
            "uuid": _u(),
            "type": "TEXT",
            "groupUuid": _u(),
            "groupType": "TEXT",
            "payload": {"html": description},
        })

    for i, q in enumerate(questions):
        blocks.extend(_build_question(q, is_first=(i == 0)))

    return _finalise_page_breaks(blocks)


def _assemble_settings(
    styles: Optional[dict],
    settings_extra: Optional[dict],
) -> dict:
    settings = dict(BRAND_SETTINGS)
    if styles:
        settings["styles"] = styles
    if settings_extra:
        settings.update(settings_extra)
    return settings


def create_form(
    title: str,
    questions: list[dict],
    status: str = "PUBLISHED",
    description: Optional[str] = None,
    api_key: Optional[str] = None,
    logo: Optional[str] = BRAND_LOGO_URL,
    styles: Optional[dict] = BRAND_STYLE,
    settings_extra: Optional[dict] = None,
) -> tuple[str, str]:
    """Create a Tally form, return (form_id, responder_url).

    Defaults to the brand style above. Pass logo=None, styles=None for a plain
    Tally form, for example when it has to carry a client's branding."""
    if api_key is None:
        api_key = _api_key_from_env()
    if not api_key:
        raise RuntimeError("TALLY_API_KEY not set in env")

    blocks = _assemble_blocks(title, questions, description, logo)
    body = {
        "status": status,
        "blocks": blocks,
        "settings": _assemble_settings(styles, settings_extra),
    }

    resp = requests.post(
        f"{TALLY_API_BASE}/forms",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=body,
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"Tally API error {resp.status_code}: {resp.text}")

    data = resp.json()
    form_id = data.get("id") or data.get("formId")
    # Responder URL on Tally is canonically https://tally.so/r/<formId>
    responder_url = data.get("url") or f"https://tally.so/r/{form_id}"
    return form_id, responder_url


def update_form(
    form_id: str,
    title: str,
    questions: list[dict],
    status: str = "PUBLISHED",
    api_key: Optional[str] = None,
    description: Optional[str] = None,
    logo: Optional[str] = BRAND_LOGO_URL,
    styles: Optional[dict] = BRAND_STYLE,
    settings_extra: Optional[dict] = None,
) -> str:
    """Update an existing Tally form's blocks in place, same responder URL,
    no need to delete-and-recreate for edits. PATCH /forms/{formId}, blocks
    shape is identical to create_form's. Returns the responder URL.

    A PATCH that omits `settings` wipes the theme back to Tally's default
    light/purple, so the house style is re-sent on every update."""
    if api_key is None:
        api_key = _api_key_from_env()
    if not api_key:
        raise RuntimeError("TALLY_API_KEY not set in env")

    blocks = _assemble_blocks(title, questions, description, logo)

    resp = requests.patch(
        f"{TALLY_API_BASE}/forms/{form_id}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "status": status,
            "blocks": blocks,
            "settings": _assemble_settings(styles, settings_extra),
        },
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"Tally API error {resp.status_code}: {resp.text}")
    return f"https://tally.so/r/{form_id}"


def restyle_form(
    form_id: str,
    api_key: Optional[str] = None,
    logo: Optional[str] = BRAND_LOGO_URL,
    styles: Optional[dict] = BRAND_STYLE,
) -> str:
    """Repaint an EXISTING form in the house style without touching its
    questions. Reads the current blocks back, drops the logo into FORM_TITLE,
    re-sends them with the house settings. Use this to retrofit forms built
    before the style existed. Returns the responder URL."""
    if api_key is None:
        api_key = _api_key_from_env()
    if not api_key:
        raise RuntimeError("TALLY_API_KEY not set in env")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    current = requests.get(f"{TALLY_API_BASE}/forms/{form_id}", headers=headers, timeout=30)
    if not current.ok:
        raise RuntimeError(f"Tally API error {current.status_code}: {current.text}")
    form = current.json()

    blocks = form["blocks"]
    if logo:
        for b in blocks:
            if b["type"] == "FORM_TITLE":
                b["payload"]["logo"] = logo

    settings = dict(form.get("settings") or {})
    settings.update(BRAND_SETTINGS)
    if styles:
        settings["styles"] = styles

    resp = requests.patch(
        f"{TALLY_API_BASE}/forms/{form_id}",
        headers=headers,
        json={"status": form.get("status", "PUBLISHED"), "blocks": blocks, "settings": settings},
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"Tally API error {resp.status_code}: {resp.text}")
    return f"https://tally.so/r/{form_id}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_tally_form.py <questions.json>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        spec = json.load(f)
    form_id, url = create_form(
        title=spec["title"],
        questions=spec["questions"],
        status=spec.get("status", "PUBLISHED"),
        description=spec.get("description"),
    )
    print(f"Form ID: {form_id}")
    print(f"Responder URL: {url}")


# Submissions go wherever you point them: your own n8n, Make, Zapier or app
# endpoint. Pick ONE endpoint per kind of form and reuse it, rather than
# building a separate automation for every form you make.


def list_webhooks(api_key: Optional[str] = None) -> list:
    """Every webhook on the Tally account. GET /webhooks takes NO formId param
    (it 400s) and returns the list under a "webhooks" key."""
    if api_key is None:
        api_key = _api_key_from_env()
    r = requests.get(
        f"{TALLY_API_BASE}/webhooks",
        headers={"Authorization": f"Bearer {api_key}"}, timeout=30,
    )
    r.raise_for_status()
    d = r.json()
    return d if isinstance(d, list) else d.get("webhooks", [])


def create_webhook(
    form_id: str,
    url: str,
    api_key: Optional[str] = None,
) -> dict:
    """Register a Tally webhook on a form so submissions POST to n8n.

    Idempotent: if the same URL is already wired to this form, the existing
    webhook is returned instead of stacking duplicates (which would double-post
    to Slack and double-write to Notion).
    """
    if api_key is None:
        api_key = _api_key_from_env()
    if not api_key:
        raise RuntimeError("TALLY_API_KEY not set in env")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # GET /webhooks REJECTS a formId query param ("formId is not allowed", 400).
    # Filter client-side instead. Getting this wrong is expensive: a failed
    # dedupe check silently falls through to POST and stacks a second webhook
    # on the form, which double-posts to Slack and writes the Notion page twice.
    existing = requests.get(f"{TALLY_API_BASE}/webhooks", headers=headers, timeout=30)
    if existing.ok:
        payload = existing.json()
        # The list lives under "webhooks". Reading the wrong key returns an
        # empty list, which looks like "no duplicate" and quietly creates one.
        items = payload if isinstance(payload, list) else payload.get("webhooks", [])
        for w in items:
            if w.get("formId") == form_id and w.get("url") == url:
                return w
    else:
        raise RuntimeError(
            f"Could not list Tally webhooks to check for duplicates "
            f"({existing.status_code}: {existing.text[:200]}). Refusing to create "
            f"one blindly, that risks a duplicate. Check the API and retry."
        )

    resp = requests.post(
        f"{TALLY_API_BASE}/webhooks",
        headers=headers,
        json={
            "formId": form_id,
            "url": url,
            "eventTypes": ["FORM_RESPONSE"],
            "isEnabled": True,
        },
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"Tally webhook error {resp.status_code}: {resp.text}")
    return resp.json()
