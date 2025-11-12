import sysimport sys

import typesimport types

import osimport os

import jsonimport json



# Inject a dummy 'groq' module so importing brain.py won't fail if the real package isn't installed.# Inject a dummy 'groq' module so importing brain.py won't fail if the real package isn't installed.

mod = types.ModuleType("groq")mod = types.ModuleType("groq")

class Groq:class Groq:

    def __init__(self, api_key=None, *a, **k):    def __init__(self, api_key=None, *a, **k):

        self.api_key = api_key        self.api_key = api_key

        # Minimal client stub (not used because we'll run with use_ai=False)        # Minimal client stub (not used because we'll run with use_ai=False)

        class Chat:        class Chat:

            class completions:            class completions:

                @staticmethod                @staticmethod

                def create(*a, **k):                def create(*a, **k):

                    raise RuntimeError("Dummy Groq client called in offline mode")                    raise RuntimeError("Dummy Groq client called in offline mode")

        self.chat = Chat()        self.chat = Chat()

mod.Groq = Groqmod.Groq = Groq

sys.modules["groq"] = modsys.modules["groq"] = mod



# Now import the main module# Now import the main module

import brainimport brain



# Ensure output dir is writable# Ensure output dir is writable

out_dir = os.path.join("data", "generated")out_dir = os.path.join("data", "generated")

os.makedirs(out_dir, exist_ok=True)os.makedirs(out_dir, exist_ok=True)



# Run generation with AI disabled to avoid external API calls# Run generation with AI disabled to avoid external API calls

print("Running generation for all days (AI disabled)...")print("Running generation for all days (AI disabled)...")

brain.generate_batch(days=["0", "1", "3", "5", "6", "7a", "7b"], use_ai=False)brain.generate_batch(days=["0", "1", "3", "5", "6", "7a", "7b"], use_ai=False)



# Load and display emails for each day# Load and display emails for each day

days = ["0", "1", "3", "5", "6", "7a", "7b"]days = ["0", "1", "3", "5", "6", "7a", "7b"]

day_names = {day_names = {

    "0": "Day 0: Registration Confirmation",    "0": "Day 0: Registration Confirmation",

    "1": "Day 1: Indoctrination",    "1": "Day 1: Indoctrination",

    "3": "Day 3: Social Proof",    "3": "Day 3: Social Proof",

    "5": "Day 5: Objection Handling",    "5": "Day 5: Objection Handling",

    "6": "Day 6: Final Push",    "6": "Day 6: Final Push",

    "7a": "Day 7a: Morning Reminder",    "7a": "Day 7a: Morning Reminder",

    "7b": "Day 7b: Final Warning"    "7b": "Day 7b: Final Warning"

}}



for day in days:for day in days:

    out_file = os.path.join(out_dir, f"day_{day}_emails.json")    out_file = os.path.join(out_dir, f"day_{day}_emails.json")

    if not os.path.exists(out_file):    if not os.path.exists(out_file):

        print(f"\n❌ No output file created: {out_file}")        print(f"\n❌ No output file created: {out_file}")

        continue        continue

        

    print(f"\n{'='*80}")    print(f"\n{'='*80}")

    print(f"📧 {day_names[day]}")    print(f"📧 {day_names[day]}")

    print(f"{'='*80}\n")    print(f"{'='*80}\n")

        

    with open(out_file, 'r', encoding='utf-8') as f:    with open(out_file, 'r', encoding='utf-8') as f:

        data = json.load(f)        data = json.load(f)

        

    emails = data.get("emails", [])    emails = data.get("emails", [])

        

    # Find and display the first generated email for this day    # Find and display the first generated email for this day

    found = False    found = False

    for item in emails:    for item in emails:

        if item.get("meta", {}).get("status") == "generated":        if item.get("meta", {}).get("status") == "generated":

            email_obj = item.get("email", {})            email_obj = item.get("email", {})

            subject = email_obj.get("subject", "")            subject = email_obj.get("subject", "")

            body = email_obj.get("body", "")            body = email_obj.get("body", "")

                        

            print(f"📌 SUBJECT: {subject}\n")            print(f"📌 SUBJECT: {subject}\n")

            print(f"📝 BODY:\n{body}\n")            print(f"📝 BODY:\n{body}\n")

                        

            found = True            found = True

            break            break

        

    if not found:    if not found:

        print("⛔ No generated emails for this day (all blocked).")        print("⛔ No generated emails for this day (all blocked).")

