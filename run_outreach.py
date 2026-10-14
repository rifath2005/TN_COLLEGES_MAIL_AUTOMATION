#!/usr/bin/env python3
"""
Email Outreach Workflow Engine with Test Mode & Dry-Run Support.
Reads contacts directly from contacts.csv (or Google Sheet export),
loads sender credentials from .env, applies validation, deduplication,
fallback personalization, and sends emails via Gmail SMTP.
"""

import os
import sys
import csv
import json
import time
import smtplib
import argparse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "contacts.csv")
TEMPLATE_FILE = os.path.join(BASE_DIR, "email_template.json")
ENV_FILE = os.path.join(BASE_DIR, ".env")

def load_env():
    """Load environment variables from .env file if present."""
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = val

def load_template():
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_greeting(department_or_contact, college_name):
    """
    Fallback greeting logic:
    1. If specific contact person/dept is provided -> "Dear <Contact/Dept>,"
    2. If missing -> "Dear Sir/Madam," as per proposal template
    """
    dept = (department_or_contact or "").strip()
    if dept:
        return f"Dear {dept},"
    return "Dear Sir/Madam,"

def render_content(template_str, mapping):
    result = template_str
    for key, value in mapping.items():
        placeholder = f"{{{{{key}}}}}"
        result = result.replace(placeholder, str(value or ""))
    return result

def send_via_gmail_smtp(sender_email, app_password, recipient_email, subject, body_text, body_html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())

def run_workflow(test_mode=True, dry_run=False, target_email=None, csv_path=None, force=False):
    load_env()
    sender_email = os.environ.get("GMAIL_SENDER", "").strip()
    app_password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()

    template = load_template()
    active_csv = os.path.abspath(csv_path) if csv_path else CSV_FILE
    
    if not os.path.exists(active_csv):
        print(f"[ERROR] Contacts file not found at: {active_csv}")
        sys.exit(1)

    with open(active_csv, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        fieldnames = reader[0].keys() if reader else []

    if not reader:
        print("[WARNING] CSV file is empty.")
        return

    print("=" * 65)
    print(" TAMIL NADU COLLEGE OUTREACH WORKFLOW")
    print(f" Mode: {'TEST MODE (First pending recipient from dataset)' if test_mode else 'PRODUCTION BATCH'}")
    print(f" Dry Run: {'YES (Preview only, no emails dispatched)' if dry_run else 'NO (Live transmission)'}")
    print(f" Sender Configured: {sender_email if sender_email and sender_email != 'your_email@gmail.com' else '[NOT SET in .env]'}")
    if target_email:
        print(f" Target Filter: {target_email}")
    if force:
        print(" Force Send: ENABLED (Re-sending to previously sent recipients allowed)")
    print("=" * 65)

    updated_rows = []
    processed_count = 0
    seen_emails = set()

    for idx, row in enumerate(reader):
        email = (row.get("Official_Email") or "").strip()
        college = (row.get("College_Name") or "").strip()
        dept = (row.get("Department_Or_Contact") or "").strip()
        status = (row.get("Status") or "Pending").strip()

        # If a specific target filter is specified, skip non-matching
        if target_email and email.lower() != target_email.lower():
            updated_rows.append(row)
            continue

        # Safeguard 1: Skip if already Sent (unless force=True)
        if status == "Sent" and not force:
            print(f"[SKIP] {college} ({email}) - Already Sent on {row.get('Sent_Timestamp')}")
            updated_rows.append(row)
            continue

        # Safeguard 2: Flag missing email in dataset
        if not email:
            print(f"[FLAGGED] {college} - Missing official email address in dataset.")
            row["Status"] = "Flagged"
            row["Notes_Or_Error"] = "Missing official email address"
            updated_rows.append(row)
            continue

        # Safeguard 3: Check duplicate email across dataset in this run
        if email.lower() in seen_emails:
            print(f"[FLAGGED] {college} ({email}) - Duplicate recipient detected in dataset.")
            row["Status"] = "Flagged"
            row["Notes_Or_Error"] = "Duplicate recipient email in batch"
            updated_rows.append(row)
            continue

        seen_emails.add(email.lower())

        # Construct Greeting and merge mapping directly from dataset row
        greeting = generate_greeting(dept, college)
        mapping = {
            "College_Name": college,
            "Greeting": greeting,
            "Department_Or_Contact": dept,
            "State": row.get("State", "Tamil Nadu"),
            "City": row.get("City", ""),
            "Official_Website_URL": row.get("Official_Website_URL", ""),
            "Phone_Number": row.get("Phone_Number", "")
        }

        subject = render_content(template["subject_template"], mapping)
        body_text = render_content(template["body_text_template"], mapping)
        body_html = render_content(template["body_html_template"], mapping)

        print("\n" + "-" * 50)
        print(f"Preparing Email #{processed_count + 1} from Dataset:")
        print(f"  To (Recipient): {email}")
        print(f"  College: {college}")
        print(f"  Phone: {row.get('Phone_Number', 'N/A')}")
        print(f"  Department / Contact: {dept if dept else '[None - Using generic fallback]'}")
        print(f"  Greeting: {greeting}")
        print(f"  Subject: {subject}")
        print("-" * 50)

        if dry_run:
            print("[DRY-RUN] Preview complete. Email rendered successfully from dataset.")
            row["Notes_Or_Error"] = "Dry-run verified"
            updated_rows.append(row)
            processed_count += 1
            if test_mode:
                print("\n[TEST MODE] Single send test simulation completed.")
                updated_rows.extend(reader[idx + 1:])
                break
            continue

        # Check credentials before live send
        if not sender_email or not app_password or "your_" in sender_email or "your_" in app_password:
            print("[ERROR] Please set valid GMAIL_SENDER and GMAIL_APP_PASSWORD in .env")
            row["Status"] = "Failed"
            row["Notes_Or_Error"] = "Missing or unconfigured Gmail credentials in .env"
            updated_rows.append(row)
            if test_mode:
                updated_rows.extend(reader[idx + 1:])
                break
            continue

        try:
            send_via_gmail_smtp(sender_email, app_password, email, subject, body_text, body_html)
            row["Status"] = "Sent"
            row["Sent_Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row["Notes_Or_Error"] = "Successfully sent via Gmail SMTP"
            print(f"[SUCCESS] Email successfully delivered to {email}")
        except Exception as e:
            row["Status"] = "Failed"
            row["Notes_Or_Error"] = f"SMTP Send Error: {str(e)}"
            print(f"[FAILED] Error sending to {email}: {e}")

        updated_rows.append(row)
        processed_count += 1

        if test_mode:
            print("\n[TEST MODE COMPLETE] Tested single send successfully from dataset.")
            updated_rows.extend(reader[idx + 1:])
            break

        # Rate throttle between live production sends (safe pacing)
        time.sleep(2)

    # Write back updated status to CSV dataset
    with open(active_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print("\n" + "=" * 65)
    print(f" Workflow finished. Processed: {processed_count} records.")
    print(f" Updated tracking status saved to: {active_csv}")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Antigravity Outreach Workflow Runner")
    parser.add_argument("--csv", type=str, default=None, help="Path to custom CSV contacts file (defaults to contacts.csv)")
    parser.add_argument("--all", action="store_true", help="Run batch for all pending recipients in dataset")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without sending emails")
    parser.add_argument("--target", type=str, default=None, help="Target email filter (optional, default reads from dataset)")
    parser.add_argument("--force", action="store_true", help="Force send even if status is already Sent")

    args = parser.parse_args()
    is_test = not args.all

    run_workflow(
        test_mode=is_test,
        dry_run=args.dry_run,
        target_email=args.target,
        csv_path=args.csv,
        force=args.force
    )
