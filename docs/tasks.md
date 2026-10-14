# Implementation & Execution Tasks: Tamil Nadu College Outreach Workflow

This document tracks all tasks required to configure, test, and run the manual outreach workflow in Antigravity.

---

## Phase 1: Contact List Schema & Data Ingestion Setup
- [x] **Task 1.1: Create Contact Data Store (Google Sheet / CSV)**
  - Initialize the sheet or CSV with the standard schema:
    `State, City, College_Name, Official_Website_URL, Department_Or_Contact, Official_Email, Source_Page_URL, Status, Sent_Timestamp, Notes_Or_Error`
  - Populate default initial `Status` as `"Pending"`.
- [x] **Task 1.2: Connect Data Source in Antigravity**
  - If using Google Sheets: Add and authorize Google Drive/Sheets connector in Antigravity.
  - If using CSV: Upload CSV into workspace, configure File Intake step, and map headers.
- [x] **Task 1.3: Configure Deduplication and Hygiene Script/Filter**
  - Set pre-filtering rule: `WHERE Official_Email IS NOT EMPTY AND Status != 'Sent'`.
  - Flag empty email records with `Status = "Flagged"` and `Notes_Or_Error = "Missing email"`.
  - Deduplicate on unique `Official_Email`.

---

## Phase 2: Antigravity Workflow Configuration (Trigger & Actions)
- [x] **Task 2.1: Create Manual Trigger Node**
  - Name: `Manual Send Button ("Send Outreach Batch")`.
  - Input parameters: Selection mode (`All Pending Rows` vs. `Selected Rows Only`).
- [x] **Task 2.2: Add Data Iterator Node**
  - Loop over qualified records filtered from Phase 1.
- [x] **Task 2.3: Configure Data Transformation & Personalization Node**
  - Implement conditional merge logic for greetings:
    ```javascript
    let greeting = "";
    if (record.Department_Or_Contact && record.Department_Or_Contact.trim() !== "") {
      greeting = `Dear ${record.Department_Or_Contact},`;
    } else {
      greeting = `Dear Leadership & Placement Team at ${record.College_Name},`;
    }
    return { ...record, Greeting: greeting };
    ```
- [x] **Task 2.4: Configure Gmail Send Action Node**
  - Authenticate Gmail OAuth connection in Antigravity.
  - Map Recipient: `{{record.Official_Email}}`.
  - Map Subject: `Partnership & Student Opportunity Initiative — {{record.College_Name}}`.
  - Map HTML / Body: Use dynamic template with `{{record.Greeting}}`, `{{record.College_Name}}`, and institutional references.
- [x] **Task 2.5: Add Rate Throttling / Delay Node**
  - Insert a 3-second sleep/delay between loop iterations to safeguard Gmail account health.
- [x] **Task 2.6: Configure Result Logger Node (Status Update)**
  - On Success: Update spreadsheet row `Status = "Sent"`, `Sent_Timestamp = NOW()`.
  - On Error / Failure: Update spreadsheet row `Status = "Failed"`, `Notes_Or_Error = Error.message`.

---

## Phase 3: Email Template Design & Fallback Review
- [x] **Task 3.1: Finalize Email Subject and Body Copy**
  - Review copy for tone, professional appeal to TN universities/colleges, clear call-to-action (CTA), and sender signature.
- [x] **Task 3.2: Verify Fallback Strings**
  - Ensure zero undefined tokens (no `{{...}}` raw text or `Dear ,`).

---

## Phase 4: Safe Sandboxed Testing & Verification
- [x] **Task 4.1: Prepare Test Fixtures**
  - Row 1 (Standard): Internal test address with all fields filled.
  - Row 2 (Missing Department/Contact): Internal test address with `Department_Or_Contact` left blank.
  - Row 3 (Negative test / Missing Email): Record with blank `Official_Email` to verify auto-flagging.
  - Row 4 (Negative test / Bad Domain / Simulated Fail): Record with invalid email format to verify graceful failure handling and error column writing.
- [x] **Task 4.2: Execute Manual Test Run**
  - Trigger test run inside Antigravity.
  - Verify received emails in test inbox for formatting, links, and correct merge values.
  - Verify spreadsheet state updates (`Sent`, `Flagged`, `Failed`).

---

## Phase 5: Production Run & Monitoring
- [x] **Task 5.1: Upload/Link Verified Tamil Nadu College Contacts**
- [x] **Task 5.2: Execute Production Manual Trigger in Batches**
  - Observe progress, quota limits, and execution logs.
- [x] **Task 5.3: Post-Send Review & Tracking Audit**
  - Filter by `Failed` or `Flagged` to resolve any institutional bounces or missing data.
