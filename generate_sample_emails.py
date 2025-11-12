"""
generate_sample_emails.py - Comprehensive Email Generation & Storage System

This script:
1. Generates emails for all 7 days of Russell Brunson framework
2. Organizes them by day and recipient
3. Exports individual email files as .txt files
4. Creates a master index with all emails
5. Generates a summary report
"""

import sys
import types
import os
import json
from datetime import datetime

# Inject a dummy 'groq' module to avoid import errors
mod = types.ModuleType("groq")
class Groq:
    def __init__(self, api_key=None, *a, **k):
        self.api_key = api_key
        class Chat:
            class completions:
                @staticmethod
                def create(*a, **k):
                    raise RuntimeError("Dummy Groq client called in offline mode")
        self.chat = Chat()
mod.Groq = Groq
sys.modules["groq"] = mod

import brain

# =============================
# Configuration
# =============================
EMAILS_FOLDER = "sample_emails"
DAYS = ["0", "1", "3", "5", "6", "7a", "7b"]
DAY_NAMES = {
    "0": "Day 0: Registration Confirmation",
    "1": "Day 1: Indoctrination",
    "3": "Day 3: Social Proof",
    "5": "Day 5: Objection Handling",
    "6": "Day 6: Final Push",
    "7a": "Day 7a: Morning Reminder",
    "7b": "Day 7b: Final Warning"
}

# =============================
# Helper Functions
# =============================
def create_folder_structure():
    """Create organized folder structure for emails"""
    os.makedirs(EMAILS_FOLDER, exist_ok=True)
    for day in DAYS:
        os.makedirs(os.path.join(EMAILS_FOLDER, f"day_{day}"), exist_ok=True)
    print(f"✅ Created folder structure in '{EMAILS_FOLDER}'")

def sanitize_filename(text):
    """Convert text to safe filename"""
    import re
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text)[:50]

def save_email_as_text(day, recipient_name, event_title, subject, body, recipient_id, event_id):
    """Save individual email as .txt file"""
    filename = f"{sanitize_filename(recipient_name)}_{sanitize_filename(event_title)}.txt"
    filepath = os.path.join(EMAILS_FOLDER, f"day_{day}", filename)
    
    content = f"""{'='*80}
EMAIL: Day {day} - {DAY_NAMES.get(day, 'Unknown Day')}
{'='*80}

RECIPIENT: {recipient_name}
EVENT: {event_title}
RECIPIENT_ID: {recipient_id}
EVENT_ID: {event_id}
GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
SUBJECT
{'='*80}
{subject}

{'='*80}
BODY
{'='*80}
{body}

{'='*80}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def save_email_as_json(day, email_data):
    """Save email data as JSON"""
    filename = f"emails_day_{day}.json"
    filepath = os.path.join(EMAILS_FOLDER, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(email_data, f, indent=2, ensure_ascii=False)
    
    return filepath

def generate_all_emails():
    """Generate emails for all days"""
    print("\n" + "="*80)
    print("🚀 GENERATING SAMPLE EMAILS FOR ALL DAYS")
    print("="*80)
    
    # Generate emails using brain.py
    print("\n📧 Running email generation (AI disabled)...")
    brain.generate_batch(days=DAYS, use_ai=False)
    
    # Load generated JSON files and process them
    generated_data = {}
    generated_count = 0
    
    print("\n📂 Processing generated emails...\n")
    
    for day in DAYS:
        generated_data[day] = {
            "day": day,
            "day_name": DAY_NAMES.get(day, "Unknown"),
            "emails": []
        }
        
        json_file = os.path.join("data", "generated", f"day_{day}_emails.json")
        
        if not os.path.exists(json_file):
            print(f"⚠️  No file found for day {day}")
            continue
        
        with open(json_file, 'r', encoding='utf-8') as f:
            day_data = json.load(f)
        
        emails = day_data.get("emails", [])
        day_generated = 0
        
        for item in emails:
            if item.get("meta", {}).get("status") == "generated":
                email_obj = item.get("email", {})
                subject = email_obj.get("subject", "")
                body = email_obj.get("body", "")
                recipient_id = item.get("meta", {}).get("recipient_id", "")
                event_id = item.get("meta", {}).get("event_id", "")
                
                # Get recipient and event names from the data
                recipient_name = ""
                event_title = ""
                
                # Load recipient data to get name
                with open("data/recipients.json", 'r', encoding='utf-8') as f:
                    recipients = json.load(f)
                    for r in recipients:
                        if r.get("recipient_id") == recipient_id:
                            recipient_name = r.get("name", "Unknown")
                            break
                
                # Load event data to get title
                with open("data/grant_events.json", 'r', encoding='utf-8') as f:
                    events = json.load(f)
                    for e in events:
                        if e.get("event_id") == event_id:
                            event_title = e.get("title", "Unknown")
                            break
                
                # Save as individual text file
                filepath = save_email_as_text(
                    day, recipient_name, event_title, subject, body, recipient_id, event_id
                )
                
                # Store in data structure
                generated_data[day]["emails"].append({
                    "recipient": recipient_name,
                    "recipient_id": recipient_id,
                    "event": event_title,
                    "event_id": event_id,
                    "subject": subject,
                    "body": body,
                    "file": filepath
                })
                
                day_generated += 1
                generated_count += 1
                
                print(f"✅ Day {day}: {recipient_name} → {event_title}")
        
        # Save day's emails as JSON
        save_email_as_json(day, generated_data[day])
        
        if day_generated == 0:
            print(f"⛔ Day {day}: No emails generated")
    
    return generated_data, generated_count

def create_master_index(generated_data, total_count):
    """Create a master index file with all emails"""
    index_content = f"""{'='*80}
MASTER EMAIL INDEX - Russell Brunson 7-Day Framework
{'='*80}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Emails Generated: {total_count}

{'='*80}
EMAILS BY DAY
{'='*80}

"""
    
    for day in DAYS:
        day_data = generated_data.get(day, {})
        emails = day_data.get("emails", [])
        day_name = DAY_NAMES.get(day, "Unknown")
        
        index_content += f"\n{'─'*80}\n"
        index_content += f"📧 {day_name}\n"
        index_content += f"{'─'*80}\n\n"
        
        if not emails:
            index_content += "⛔ No emails generated for this day\n\n"
        else:
            for i, email in enumerate(emails, 1):
                index_content += f"{i}. {email['recipient']} → {email['event']}\n"
                index_content += f"   📄 File: {email['file']}\n"
                index_content += f"   📌 Subject: {email['subject'][:60]}...\n\n"
    
    index_file = os.path.join(EMAILS_FOLDER, "INDEX.txt")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    return index_file

def create_summary_report(generated_data, total_count):
    """Create a summary report"""
    report_content = f"""{'='*80}
EMAIL GENERATION SUMMARY REPORT
{'='*80}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

STATISTICS
──────────────────────────────────────────────────────────────────────────────
Total Emails Generated: {total_count}
Folder Structure: {EMAILS_FOLDER}/
Days Covered: {len(DAYS)}

BREAKDOWN BY DAY
──────────────────────────────────────────────────────────────────────────────
"""
    
    for day in DAYS:
        day_data = generated_data.get(day, {})
        emails = day_data.get("emails", [])
        day_name = DAY_NAMES.get(day, "Unknown")
        count = len(emails)
        
        report_content += f"\n{day_name}:\n"
        report_content += f"  • Emails: {count}\n"
        
        if count > 0:
            report_content += f"  • Location: sample_emails/day_{day}/\n"
            for email in emails:
                report_content += f"    - {email['recipient']} ({email['event']})\n"
        else:
            report_content += f"  • Status: ⛔ None generated\n"
    
    report_content += f"""

FOLDER STRUCTURE
──────────────────────────────────────────────────────────────────────────────
{EMAILS_FOLDER}/
├── day_0/          (Registration Confirmation emails)
├── day_1/          (Indoctrination emails)
├── day_3/          (Social Proof emails)
├── day_5/          (Objection Handling emails)
├── day_6/          (Final Push emails)
├── day_7a/         (Morning Reminder emails)
├── day_7b/         (Final Warning emails)
├── emails_day_*.json   (JSON backup for each day)
├── INDEX.txt       (Master index of all emails)
└── REPORT.txt      (This file)

HOW TO USE THESE EMAILS
──────────────────────────────────────────────────────────────────────────────
1. Each email is stored as a separate .txt file with formatted content
2. JSON files are available for programmatic access
3. The INDEX.txt file provides a quick reference
4. Each email includes:
   - Recipient name
   - Event title
   - Email subject
   - Email body (fully personalized)
   - Metadata (IDs, generation date)

FRAMEWORK INFORMATION
──────────────────────────────────────────────────────────────────────────────
This email generation follows Russell Brunson's 7-Day Email Framework:

Day 0: Registration Confirmation
  Purpose: Set expectations and build excitement
  Tone: Welcoming, informative

Day 1: Indoctrination
  Purpose: Create curiosity and establish authority
  Tone: Problem-focused, engaging

Day 3: Social Proof
  Purpose: Build credibility through results
  Tone: Authoritative, confidence-building

Day 5: Objection Handling
  Purpose: Address skepticism and common fears
  Tone: Empathetic, logical

Day 6: Final Push
  Purpose: Create urgency before event day
  Tone: Urgent, motivating

Day 7a: Morning Reminder
  Purpose: Build excitement and prevent no-shows
  Tone: High-energy, supportive

Day 7b: Final Warning
  Purpose: Last chance urgency
  Tone: Ultra-urgent, direct

NEXT STEPS
──────────────────────────────────────────────────────────────────────────────
1. Review emails in each day folder
2. Customize as needed for your use case
3. Test with a small sample of recipients
4. Monitor open rates and engagement per day
5. Iterate and optimize based on metrics

Generated by: Email Generator (brain.py)
{'='*80}
"""
    
    report_file = os.path.join(EMAILS_FOLDER, "REPORT.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return report_file

def display_summary(generated_data, total_count, index_file, report_file):
    """Display summary in terminal"""
    print("\n" + "="*80)
    print("✅ EMAIL GENERATION COMPLETE")
    print("="*80)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total emails generated: {total_count}")
    print(f"   Storage location: {EMAILS_FOLDER}/")
    print(f"\n📂 BREAKDOWN BY DAY:")
    
    for day in DAYS:
        day_data = generated_data.get(day, {})
        emails = day_data.get("emails", [])
        count = len(emails)
        status = f"✅ {count} email(s)" if count > 0 else "⛔ None"
        print(f"   Day {day}: {status}")
    
    print(f"\n📄 FILES CREATED:")
    print(f"   📋 Master Index: {index_file}")
    print(f"   📊 Summary Report: {report_file}")
    print(f"   📁 Individual emails: sample_emails/day_*/")
    print(f"   📊 JSON backups: sample_emails/emails_day_*.json")
    
    print("\n" + "="*80)
    print("🎉 All emails are ready to use!")
    print("="*80 + "\n")

# =============================
# Main Execution
# =============================
def main():
    try:
        # Step 1: Create folder structure
        create_folder_structure()
        
        # Step 2: Generate all emails
        generated_data, total_count = generate_all_emails()
        
        # Step 3: Create master index
        index_file = create_master_index(generated_data, total_count)
        
        # Step 4: Create summary report
        report_file = create_summary_report(generated_data, total_count)
        
        # Step 5: Display summary
        display_summary(generated_data, total_count, index_file, report_file)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
