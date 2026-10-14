# Requirements Specification: Tamil Nadu College Outreach Workflow

## 1. Functional Requirements

### 1.1 Data Source & Ingestion
- **Single Source of Truth (SSOT):** The workflow must support data stored in either a **Google Sheet** (connected via Google Workspace connector) or an **uploaded CSV file**.
- **Supported Fields & Schema:**
  | Field Name | Data Type | Required? | Description / Allowed Values |
  | :--- | :--- | :--- | :--- |
  | `State` | String | Yes | Fixed as `"Tamil Nadu"` |
  | `City` | String | Yes | E.g., Chennai, Coimbatore, Madurai, Tiruchirappalli |
  | `College_Name` | String | Yes | Full institutional name |
  | `Official_Website_URL`| URL String | Yes | Official college domain (e.g., `https://annauniv.edu`) |
  | `Department_Or_Contact`| String | Optional | E.g., `"Head of Training & Placement"`, `"Dr. S. Raman"`, or blank |
  | `Official_Email` | Email String | Conditional | Verified institutional email. If missing, flagged for manual review |
  | `Source_Page_URL` | URL String | Yes | Direct page URL where the email was located (e.g., `/contact-us`, `/placement`) |
  | `Status` | Enum String | Yes | Allowed values: `Pending`, `Sent`, `Failed`, `Flagged` |
  | `Sent_Timestamp` | DateTime | Optional | Timestamp of successful transmission |
  | `Notes_Or_Error` | String | Optional | Diagnostic messages (e.g., `"Invalid email format"`, `"SMTP 429 quota"`) |

### 1.2 Data Hygiene & Collection Standards
- Contact details must originate exclusively from official domains (no scrape dumps or unverified third-party scraping).
- Any record lacking a verified email address must automatically be flagged (`Status = "Flagged"`, Notes = `"Missing official email"`).
- Duplicate URLs or duplicate email addresses across rows must be deduplicated prior to sending.

### 1.3 Trigger & Dispatch Control
- **Manual Trigger Only:** Workflow execution occurs strictly on manual trigger ("Send Selected Outreach Campaign" button).
- **Recipient Scope:** Allows user to execute across either all `Pending` rows or an explicitly selected subset of rows.

### 1.4 Dynamic Template Personalization & Fallback Logic
- **Subject Line:** Support dynamic merge variables with fallbacks.
  - Template: `Collaboration & Academic Initiative for {{College_Name}}`
- **Greeting & Body Personalization:**
  - If `Department_Or_Contact` is populated and contains a named person: `"Dear {{Department_Or_Contact}},"`
  - If `Department_Or_Contact` is populated with a department/office title: `"Dear {{Department_Or_Contact}} Team at {{College_Name}},"`
  - If `Department_Or_Contact` is blank/null: `"Dear Academic Leadership and Placement Team at {{College_Name}},"`
- Under no circumstance should a placeholder render empty punctuation or syntax (e.g. `"Dear ,"`).

### 1.5 Delivery & Service Integration
- **Integration:** Native Antigravity Gmail Action Connector using OAuth2.
- **Delivery Mode:** Individual, 1-to-1 personalized emails (no batch BCC/CC).
- **Rate Throttling:** 2 to 5-second staggering delay between consecutive sends to avoid triggering spam heuristics or burst rate limiting.

### 1.6 Tracking & Idempotency Safeguards
- **Idempotency Guard:** Rows where `Status == "Sent"` must be strictly excluded from the execution payload.
- **State Updates:** Upon send response from Gmail API:
  - `HTTP 200 / Success` -> Set `Status = "Sent"`, `Sent_Timestamp = NOW()`.
  - `Error / Exception` -> Set `Status = "Failed"`, `Notes_Or_Error = <error_message>`.

---

## 2. Non-Functional & Operational Requirements

### 2.1 Quotas & Sending Limits
- **Personal Gmail accounts (`@gmail.com`):** 500 emails / rolling 24 hours.
- **Google Workspace accounts:** 2,000 emails / rolling 24 hours.
- The workflow must maintain a send counter per execution batch to warn or halt when approaching safety limits.

### 2.2 Error Handling & Edge Cases
| Scenario | Behavior / Mitigation |
| :--- | :--- |
| **Missing Email** | Pre-send validation skips row; marks `Status = "Flagged"`. |
| **Duplicate Row** | Evaluates unique `Official_Email`; marks subsequent duplicate rows as `Flagged (Duplicate)`. |
| **Gmail Auth Token Expired** | Workflow stops immediately, alerts user to re-authenticate Gmail plugin before continuing; no rows marked falsely as sent. |
| **Rate Limit / Quota Exceeded (429 / 550)** | Stops execution immediately, flags current row as `Failed (Quota exceeded)`, retains remaining rows as `Pending`. |
