"""
Worked example: a client project kickoff form that collects every bit of access
a build needs in one pass, instead of chasing people for a fortnight.

This is the real shape of a form that worked, with the client's details swapped
out. Read it for the pattern, not the questions: the questions should always come
from the actual project.

Three things in here are worth copying every time.

1. It asks for CONFIRMATION that access was granted, never for the credential
   itself. "Invited as an admin user" is a checkbox. The password is not a field.
2. It routes real credentials through a one time secret link, said twice, near
   the top and again at the end.
3. Almost nothing is required, because it gets filled in live on a call and a
   required field nobody can answer yet stops the whole thing dead.

Run it:
    TALLY_API_KEY=... python example_client_kickoff.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from tally_form_builder import create_form

QUESTIONS = [
    {"type": "instruction", "title": "Everything we need to start building, in one place. About 10 minutes. Your answers save as you go, so leave anything you need to look up and come back to it. Almost nothing here is required. ⚡"},
    {"type": "page_break"},

    {"type": "heading", "title": "🔑 The systems we build in"},
    {"type": "instruction", "title": "Wherever you can, <b>invite us as our own user with admin rights</b> rather than sharing a password. You can remove us any time. <b>Never type a password or an API key into this form.</b> There is a secure one time link at the end for those."},
    {"type": "checkboxes", "title": "Your CRM: what is done so far?",
     "options": ["Invited as an admin user", "That invite has been accepted", "API key generated", "Nothing yet, we will do it on the call"]},
    {"type": "short_text", "title": "Which plan are you on, and who is your account rep?",
     "placeholder": "The rep matters, they are who we ask about add ons"},
    {"type": "checkboxes", "title": "Which paid add ons do you already have?",
     "options": ["Automation and sequences", "AI assistant", "Forms and landing pages", "None of these", "Not sure, please check for us"]},
    {"type": "checkboxes", "title": "Your email tool: what is done so far?",
     "options": ["Invited as an admin", "That invite has been accepted", "Still pending", "Nothing yet"]},
    {"type": "page_break"},

    {"type": "heading", "title": "📅 The deadline that comes first"},
    {"type": "instruction", "title": "Anything with a date attached jumps the queue, ahead of the slower structural work. Tell us the real dates."},
    {"type": "long_text", "title": "The campaign or event: date, time, place, and anything that must appear in it"},
    {"type": "short_text", "title": "How do people respond?", "placeholder": "A link, a reply, a phone call"},
    {"type": "date", "title": "Last date this can go out and still be useful"},
    {"type": "file_upload", "title": "Any list or spreadsheet this needs to go to"},
    {"type": "page_break"},

    {"type": "heading", "title": "📬 Sending: texts, domain, email"},
    {"type": "checkboxes", "title": "Your texting platform",
     "options": ["We have been invited to the account", "The sending number is ready", "A2P 10DLC is already registered", "Not sure what 10DLC is, please check for us"]},
    {"type": "short_text", "title": "Who controls DNS for your domain?", "placeholder": "The registrar, or the person who handles it"},
    {"type": "long_text", "title": "Do you own any other domains?",
     "placeholder": "One you already own may work as a sending domain, which saves buying one"},
    {"type": "long_text", "title": "Consent records: do you know who opted in, and roughly when?",
     "placeholder": "An honest 'we have no idea' is a fine answer and actually helps us"},
    {"type": "page_break"},

    {"type": "heading", "title": "🔌 The rest of the stack"},
    {"type": "checkboxes", "title": "Which of these can we be invited to?",
     "options": ["Your automation tool", "Your database or spreadsheets", "Your forms tool", "Your shared inbox", "Your project boards", "Your ad accounts", "The website admin", "Email admin"]},
    {"type": "short_text", "title": "Who owns the website, and who can add a form or change DNS?"},
    {"type": "long_text", "title": "Anything in the stack we have not named yet?"},
    {"type": "file_upload", "title": "Any process docs, flowcharts or exports you already have"},
    {"type": "page_break"},

    {"type": "heading", "title": "👥 Your team and your rules"},
    {"type": "file_upload", "title": "Your team list", "placeholder": "Name, email, mobile, role"},
    {"type": "long_text", "title": "What must NEVER go out automatically?",
     "placeholder": "The single most important answer on this form. Anything that would embarrass you or upset a customer if a robot sent it"},
    {"type": "checkboxes", "title": "Who should get the weekly report?",
     "options": ["The owner", "The manager", "Operations", "The whole team", "Someone else, named below"]},
    {"type": "dropdown", "title": "Where should the weekly report land?", "options": ["Email", "Slack", "Both"]},
    {"type": "long_text", "title": "Any routing rules we should know before the mapping call?",
     "placeholder": "Who gets what, and anything that is not obvious from the outside"},
    {"type": "page_break"},

    {"type": "heading", "title": "🎨 Brand, approvals and the last bits"},
    {"type": "short_text", "title": "Who approves copy before anything sends?",
     "placeholder": "Nothing goes out without a yes from this person"},
    {"type": "short_text", "title": "Sender name and reply to address"},
    {"type": "file_upload", "title": "Logo, brand colours, or something that looks the way you want this to look"},
    {"type": "long_text", "title": "Anything you are worried about, or anything we have missed?"},
    {"type": "instruction", "title": "<b>Passwords and API keys:</b> do not put them in this form. Go to <a href='https://onetimesecret.com'>onetimesecret.com</a>, paste the credential, and send us the link. It self destructs after it is opened once."},
    {"type": "thank_you", "title": "Got it. 🔥",
     "body": "That is everything we need to start. Anything you left blank, we will pick up on the mapping call."},
]

if __name__ == "__main__":
    form_id, url = create_form(
        title="🚀 Project Kickoff",
        description="Everything we need access to, in one pass. About 10 minutes. ⚡",
        questions=QUESTIONS,
    )
    print("Form ID:", form_id)
    print("URL:", url)
