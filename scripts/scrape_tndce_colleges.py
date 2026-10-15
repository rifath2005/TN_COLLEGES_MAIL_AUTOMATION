#!/usr/bin/env python3
"""
TNDCE (Directorate of Collegiate Education, Tamil Nadu) Scraper & Ingestion Engine.
Scrapes official collegiate listings directly from https://tndce.tn.gov.in/ and /Colleges.
Parses all colleges across Government, Government Aided, and Self-Financing categories.
Maintains completeness metrics (detecting missing phone numbers, missing websites, missing emails),
cross-references existing verified contacts, and writes structured outputs to:
1. tndce_colleges.csv (Complete scraped Directorate of Collegiate Education dataset)
2. contacts.csv (Updated master dataset with missing-data metadata)
"""

import os
import re
import csv
import ssl
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
TNDCE_CSV = os.path.join(ROOT_DIR, "tndce_colleges.csv")
MASTER_CSV = os.path.join(ROOT_DIR, "contacts.csv")

def get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_url(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    with urllib.request.urlopen(req, context=get_ssl_context(), timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def clean_college_name_and_address(raw_str):
    # Format e.g.: "3120043 - Arun Krishna College., Of Arts & Sci,, Valaiyampattu Vil., Rd, Chengam - 606 701."
    raw = raw_str.strip()
    
    # Extract code if present
    code = ""
    code_match = re.match(r"^(\d{5,8})\s*-\s*(.+)$", raw)
    if code_match:
        code = code_match.group(1).strip()
        raw = code_match.group(2).strip()
        
    # Extract pincode if present
    pincode = ""
    pin_match = re.search(r"\b(\d{3}\s?\d{3})\b", raw)
    if pin_match:
        pincode = pin_match.group(1).replace(" ", "")

    # Clean up excess dots and commas
    cleaned = re.sub(r"\s+", " ", raw)
    cleaned = re.sub(r"\.,", ",", cleaned)
    cleaned = re.sub(r",\s*,+", ",", cleaned)
    
    # Heuristic to separate college title from street address
    parts = [p.strip() for p in cleaned.split(",") if p.strip()]
    if len(parts) > 1 and any(k in parts[0].lower() for k in ["college", "institute", "university", "academy", "school"]):
        name = parts[0]
        address = ", ".join(parts[1:])
    elif len(parts) > 2 and any(k in parts[1].lower() for k in ["college", "institute", "university", "academy"]):
        name = f"{parts[0]}, {parts[1]}"
        address = ", ".join(parts[2:])
    else:
        name = parts[0] if parts else cleaned
        address = ", ".join(parts[1:]) if len(parts) > 1 else ""
        
    return code, name.strip(), address.strip(), pincode

def load_verified_contacts():
    lookup = {}
    if os.path.exists(MASTER_CSV):
        with open(MASTER_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("College_Name") or "").strip().lower()
                norm_name = re.sub(r"[^a-z0-9]", "", name)
                if norm_name:
                    lookup[norm_name] = row
    return lookup

def scrape_tndce():
    print("[*] Connecting to TNDCE Portal: https://tndce.tn.gov.in/ ...")
    html_home = fetch_url("https://tndce.tn.gov.in/")
    
    print("[*] Connecting to TNDCE Directory: https://tndce.tn.gov.in/Colleges ...")
    html_colleges = fetch_url("https://tndce.tn.gov.in/Colleges")
    
    verified_lookup = load_verified_contacts()
    print(f"[*] Loaded {len(verified_lookup)} existing verified reference records from contacts.csv")

    scraped_records = []
    seen_codes = set()
    seen_names = set()

    # 1. Parse homepage table (Table 0 has 1,719 rows with college IDs & course detail links)
    tables_home = re.findall(r"<table[^>]*>(.*?)</table>", html_home, re.DOTALL | re.IGNORECASE)
    if tables_home:
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", tables_home[0], re.DOTALL | re.IGNORECASE)
        print(f"[*] Parsing {len(rows)-1} collegiate entries from homepage table...")
        for r in rows[1:]:
            cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.DOTALL | re.IGNORECASE)]
            if len(cells) >= 5:
                sno = cells[0]
                raw_name = cells[1]
                district = cells[2]
                region = cells[3]
                ctype = cells[4]
                
                m = re.search(r"course_details/(\d+)", r)
                course_id = m.group(1) if m else ""
                
                code, name, address, pincode = clean_college_name_and_address(raw_name)
                code_key = code or course_id or raw_name.lower()
                
                if code_key in seen_codes:
                    continue
                seen_codes.add(code_key)
                
                norm_key = re.sub(r"[^a-z0-9]", "", name.lower())
                seen_names.add(norm_key)

                # Cross-reference existing verified contacts
                matched = verified_lookup.get(norm_key)
                
                phone = matched.get("Phone_Number", "") if matched else ""
                website = matched.get("Official_Website_URL", "") if matched else ""
                email = matched.get("Official_Email", "") if matched else ""
                dept = matched.get("Department_Or_Contact", "Office of the Principal") if matched else "Office of the Principal"
                
                source_url = f"https://tndce.tn.gov.in/Home/course_details/{course_id}" if course_id else "https://tndce.tn.gov.in/Colleges"

                # Check missing flags
                missing_items = []
                if not phone:
                    missing_items.append("No Phone")
                if not website:
                    missing_items.append("No Website")
                if not email:
                    missing_items.append("No Email")
                    
                status = "Pending" if email else "Flagged"
                notes = "Verified complete institutional contact" if not missing_items else f"Incomplete details: Missing {', '.join(missing_items)} from TNDCE directory"

                record = {
                    "State": "Tamil Nadu",
                    "City": district,
                    "College_Name": name if name else raw_name,
                    "Official_Website_URL": website,
                    "Department_Or_Contact": dept,
                    "Official_Email": email,
                    "Phone_Number": phone,
                    "Source_Page_URL": source_url,
                    "Status": status,
                    "Sent_Timestamp": matched.get("Sent_Timestamp", "") if matched else "",
                    "Notes_Or_Error": notes,
                    "TNDCE_Code": code or course_id,
                    "Region": region,
                    "College_Type": ctype,
                    "Full_Address": address,
                    "Pincode": pincode
                }
                scraped_records.append(record)

    # 2. Parse /Colleges table (Table 0 has 1,566 entries, check for any uncaptured colleges)
    tables_dir = re.findall(r"<table[^>]*>(.*?)</table>", html_colleges, re.DOTALL | re.IGNORECASE)
    if tables_dir:
        rows_dir = re.findall(r"<tr[^>]*>(.*?)</tr>", tables_dir[0], re.DOTALL | re.IGNORECASE)
        print(f"[*] Cross-checking {len(rows_dir)-1} entries from /Colleges master table...")
        for r in rows_dir[1:]:
            cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.DOTALL | re.IGNORECASE)]
            if len(cells) >= 5:
                raw_name = cells[1]
                district = cells[2]
                region = cells[3]
                ctype = cells[4]
                
                code, name, address, pincode = clean_college_name_and_address(raw_name)
                norm_key = re.sub(r"[^a-z0-9]", "", name.lower())
                
                if norm_key in seen_names:
                    continue
                seen_names.add(norm_key)

                matched = verified_lookup.get(norm_key)
                phone = matched.get("Phone_Number", "") if matched else ""
                website = matched.get("Official_Website_URL", "") if matched else ""
                email = matched.get("Official_Email", "") if matched else ""
                dept = matched.get("Department_Or_Contact", "Office of the Principal") if matched else "Office of the Principal"

                missing_items = []
                if not phone:
                    missing_items.append("No Phone")
                if not website:
                    missing_items.append("No Website")
                if not email:
                    missing_items.append("No Email")

                status = "Pending" if email else "Flagged"
                notes = "Verified complete institutional contact" if not missing_items else f"Incomplete details: Missing {', '.join(missing_items)} from TNDCE directory"

                record = {
                    "State": "Tamil Nadu",
                    "City": district,
                    "College_Name": name if name else raw_name,
                    "Official_Website_URL": website,
                    "Department_Or_Contact": dept,
                    "Official_Email": email,
                    "Phone_Number": phone,
                    "Source_Page_URL": "https://tndce.tn.gov.in/Colleges",
                    "Status": status,
                    "Sent_Timestamp": matched.get("Sent_Timestamp", "") if matched else "",
                    "Notes_Or_Error": notes,
                    "TNDCE_Code": code,
                    "Region": region,
                    "College_Type": ctype,
                    "Full_Address": address,
                    "Pincode": pincode
                }
                scraped_records.append(record)

    print(f"\n[+] Total TNDCE colleges successfully scraped: {len(scraped_records)}")
    
    # Calculate Missing Statistics
    no_phone_count = sum(1 for c in scraped_records if not c["Phone_Number"])
    no_website_count = sum(1 for c in scraped_records if not c["Official_Website_URL"])
    no_email_count = sum(1 for c in scraped_records if not c["Official_Email"])
    any_missing_count = sum(1 for c in scraped_records if not c["Phone_Number"] or not c["Official_Website_URL"] or not c["Official_Email"])
    complete_count = len(scraped_records) - any_missing_count

    print("=" * 65)
    print(" TNDCE DATA COMPLETENESS AUDIT")
    print(f" Total Institutions Scraped     : {len(scraped_records)}")
    print(f" ⚠️ Without Phone Number        : {no_phone_count} ({no_phone_count/len(scraped_records)*100:.1f}%)")
    print(f" ⚠️ Without Official Website    : {no_website_count} ({no_website_count/len(scraped_records)*100:.1f}%)")
    print(f" ⚠️ Without Official Email ID   : {no_email_count} ({no_email_count/len(scraped_records)*100:.1f}%)")
    print(f" ⚠️ Total Incomplete Profiles   : {any_missing_count} ({any_missing_count/len(scraped_records)*100:.1f}%)")
    print(f" ✅ Complete Verified Profiles  : {complete_count}")
    print("=" * 65)

    # 1. Write tndce_colleges.csv (Extended fields)
    tndce_headers = [
        "State", "City", "College_Name", "Official_Website_URL",
        "Department_Or_Contact", "Official_Email", "Phone_Number",
        "Source_Page_URL", "Status", "Sent_Timestamp", "Notes_Or_Error",
        "TNDCE_Code", "Region", "College_Type", "Full_Address", "Pincode"
    ]
    with open(TNDCE_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tndce_headers)
        writer.writeheader()
        writer.writerows(scraped_records)
    print(f"[+] Saved complete TNDCE directory to: {TNDCE_CSV}")

    # 2. Write/Update contacts.csv (Standard 11-field schema)
    # Merge existing 296 verified colleges with TNDCE records so none are lost
    existing_contacts = []
    existing_names_set = set()
    if os.path.exists(MASTER_CSV):
        with open(MASTER_CSV, "r", encoding="utf-8") as f:
            existing_contacts = list(csv.DictReader(f))
            for r in existing_contacts:
                existing_names_set.add(re.sub(r"[^a-z0-9]", "", (r.get("College_Name") or "").lower()))

    contacts_headers = [
        "State", "City", "College_Name", "Official_Website_URL",
        "Department_Or_Contact", "Official_Email", "Phone_Number",
        "Source_Page_URL", "Status", "Sent_Timestamp", "Notes_Or_Error"
    ]

    merged_contacts = list(existing_contacts)
    new_tndce_added = 0

    for rec in scraped_records:
        norm_rec_name = re.sub(r"[^a-z0-9]", "", rec["College_Name"].lower())
        if norm_rec_name not in existing_names_set:
            existing_names_set.add(norm_rec_name)
            merged_contacts.append({
                "State": rec["State"],
                "City": rec["City"],
                "College_Name": rec["College_Name"],
                "Official_Website_URL": rec["Official_Website_URL"],
                "Department_Or_Contact": rec["Department_Or_Contact"],
                "Official_Email": rec["Official_Email"],
                "Phone_Number": rec["Phone_Number"],
                "Source_Page_URL": rec["Source_Page_URL"],
                "Status": rec["Status"],
                "Sent_Timestamp": rec["Sent_Timestamp"],
                "Notes_Or_Error": rec["Notes_Or_Error"]
            })
            new_tndce_added += 1

    with open(MASTER_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=contacts_headers)
        writer.writeheader()
        writer.writerows(merged_contacts)

    print(f"[+] Added {new_tndce_added} newly discovered TNDCE colleges into {MASTER_CSV}")
    print(f"[+] Total colleges in master dataset: {len(merged_contacts)}")
    return scraped_records, merged_contacts

if __name__ == "__main__":
    scrape_tndce()
