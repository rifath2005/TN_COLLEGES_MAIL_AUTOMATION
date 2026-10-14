# Tamil Nadu Higher Education Email Outreach Automation System — Architecture & Operations Overview

## 1. Executive Summary
The **Tamil Nadu Higher Education Email Outreach Automation System** is an end-to-end institutional engagement and verification platform. It couples a secure **Python SMTP outreach engine** with a high-fidelity **React/TypeScript Web Operations Portal (`AUTO_LAND`)**. 

The system operates on an active, verified institutional database across all **38 educational districts and 9 regional zones of Tamil Nadu**. It enforces strict data verification rules: **only collegiate institutions with verified official institutional email addresses and official website URLs are maintained in the roster**. All outreach messages are dispatched via authenticated Google Workspace / Gmail SMTP with built-in rate-limiting safeguards, intelligent template fallback personalization, deduplication filters, and automated audit tracking.

---

## 2. High-Level System Architecture

```
                    ┌────────────────────────────────────────────────────────┐
                    │               Tamil Nadu College Roster                │
                    │                      contacts.csv                      │
                    │  (125 Verified Campuses, 38 Districts, 100% MX Valid)   │
                    └──────────────────────────┬─────────────────────────────┘
                                               │
                                               ▼
     ┌──────────────────────────────────────────────────────────────────────────────────┐
     │                             Core Dispatch Engine                                 │
     │                                run_outreach.py                                   │
     │  ├── Credentials: .env (SENDER_EMAIL, GMAIL_APP_PASSWORD)                        │
     │  ├── Template Merge: email_template.json with smart fallback greetings           │
     │  ├── Modes: --dry-run (simulation), --test-target (single email override)        │
     │  ├── Throttling: Delay interval (default 1.5s - 5s) protecting domain IP        │
     │  └── Ledger Persistence: Updates Status to 'Sent' / 'Failed' in contacts.csv     │
     └─────────────────────────────────────────▲────────────────────────────────────────┘
                                               │ (Child Process Invocations)
                                               │
     ┌─────────────────────────────────────────┴────────────────────────────────────────┐
     │                              API Middleware Layer                                │
     │                            AUTO_LAND/server_api.mjs                              │
     │  ├── /api/init          -> Dynamic stats, active template, and college records   │
     │  ├── /api/test-send     -> Dispatches test outreach email via Gmail SMTP         │
     │  ├── /api/send-batch    -> Triggers throttled outreach campaign wave             │
     │  ├── /api/colleges/add  -> Appends newly verified campus to contacts.csv         │
     │  ├── /api/colleges/update -> Updates contact person, email, or status in CSV     │
     │  ├── /api/save-template -> Updates subject & body in email_template.json         │
     │  └── Category & Zone Engine -> Auto-categorizes institutions & maps TN zones     │
     └─────────────────────────────────────────▲────────────────────────────────────────┘
                                               │ (REST API / CORS Enabled)
                                               │
     ┌─────────────────────────────────────────┴────────────────────────────────────────┐
     │                      Web Operations Portal (AUTO_LAND)                           │
     │                          (React 19, TypeScript, Vite)                            │
     │  ├── Dashboard View: Dynamic stats, delivery progress, Top District Density      │
     │  ├── College Contacts: Search, filter by district/zone/status, CSV export        │
     │  ├── Campaign Launcher: Target cluster scheduling with velocity throttle         │
     │  ├── Email Templates: Live preview with personalized merge variables             │
     │  ├── Send Audit Trail: Telemetry, timestamps, and bounce tracking                │
     │  └── Officer Profile: Zone Administrator settings persisted in local storage     │
     └──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Active Institutional Database (`contacts.csv`)

### 3.1 Data Validation Standard
In accordance with the operational directive:
> *"Extract Tamil Nadu colleges website and scrape email ID. If the email ID is not present, exclude the college rather than collecting uncontactable records."*

All records in `contacts.csv` must satisfy:
1. **Verified Official Email**: Regex-validated email syntax (`^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`).
2. **Official Institutional Website**: Resolving `.ac.in`, `.edu.in`, or official institutional URL.
3. **Geographic Grounding**: Mapped to an active Tamil Nadu district (Chennai, Coimbatore, Madurai, Tiruchirappalli, Salem, Tirunelveli, Erode, Vellore, Thanjavur, Dindigul, Sivakasi, Karaikudi, etc.).

### 3.2 Current Ledger Snapshot
- **Total Registered Campuses**: `125`
- **Verified Official Emails**: `125 / 125` (100% valid MX records)
- **Official Website URLs**: `125 / 125` (100% official institutional domains)
- **Current Status**:
  - `Sent` (Verified Dispatched): `15`
  - `Pending` (Outreach Queue): `110`
  - `Failed / Bounced`: `0`
  - `Duplicates`: `0`

### 3.3 CSV Column Schema
| Column Name | Purpose | Example |
| :--- | :--- | :--- |
| `State` | State identifier | `Tamil Nadu` |
| `City` | District / City location | `Chennai`, `Coimbatore`, `Madurai` |
| `College_Name` | Full official legal name of institution | `College of Engineering Guindy (Anna University)` |
| `Official_Website_URL` | Canonical campus portal | `https://ceg.annauniv.edu` |
| `Department_Or_Contact` | Target office or officer designation | `Office of the Principal / Dean` |
| `Official_Email` | Verified institutional mailbox | `dean@ceg.annauniv.edu` |
| `Phone_Number` | Campus phone or EPABX | `+91-44-22358490` |
| `Source_Page_URL` | Audit URL where contact was scraped | `https://ceg.annauniv.edu/contact.php` |
| `Status` | Lifecycle stage (`Pending`, `Sent`, `Failed`) | `Pending` |
| `Sent_Timestamp` | ISO/UTC timestamp of transmission | `2026-10-14 13:24:34` |
| `Notes_Or_Error` | Audit comment or SMTP response message | `Successfully sent via Gmail SMTP` |

---

## 4. Dispatch Engine Mechanics (`run_outreach.py`)

### 4.1 Authentication & Transport
Outreach messages are transmitted using Python’s native `smtplib` over secure TLS:
- **SMTP Host**: `smtp.gmail.com`
- **SMTP Port**: `587` (STARTTLS)
- **Sender Identity**: Loaded from `.env` via `SENDER_EMAIL`
- **Authentication**: Authenticated via Google App Password via `GMAIL_APP_PASSWORD`

### 4.2 Dynamic Personalization & Smart Fallbacks
The template merge engine (`email_template.json`) dynamically substitutes institutional placeholders while preventing awkward formatting:

- `{{College_Name}}` $\rightarrow$ Replaced with `row["College_Name"]`.
- `{{Department_Or_Contact}}` $\rightarrow$ Evaluated by `generate_greeting()`:
  - If a specific contact or office is present (e.g. `Office of the Principal`, `Dr. S. Ramanathan`):
    $\rightarrow$ *"Dear Principal / Leadership Team,"* or *"Respected Dr. S. Ramanathan,"*
  - If omitted or empty:
    $\rightarrow$ Professional fallback: *"Respected Principal / Directorate of {{College_Name}},"*

### 4.3 Safety Flags & Controls
| Flag | Behavior |
| :--- | :--- |
| `--dry-run` | Renders merged emails, simulates SMTP dispatch, displays recipient output in console, and leaves `contacts.csv` untouched. |
| `--test-target <email>` | Overrides all recipient emails and transmits test payloads strictly to the specified email (e.g. `babsword6@gmail.com`). |
| `--force` | Dispatches even if row status is marked `Sent` (used during targeted testing). |
| `--batch-size <N>` | Restricts outreach wave to a maximum of `N` pending campuses. |
| `--delay <seconds>` | Introduces a pause between transmissions (default: `1.5s`) to respect recipient MTA rate limits. |
| `--csv <filename>` | Targets an alternative CSV file (e.g. `test_contacts.csv`). |

---

## 5. Backend API Middleware (`AUTO_LAND/server_api.mjs`)

The API layer is implemented as an Express / Vite middleware, enabling zero-config local execution and cloud container deployments:

- `GET /api/init?csv=contacts.csv`: Dynamically parses the active CSV, applies zone mapping and institutional category classification, computes real ledger stats, and returns the complete directory payload.
- `POST /api/send-email`: Runs `run_outreach.py` targeting a single institution or test recipient.
- `POST /api/send-batch`: Runs `run_outreach.py` in batch mode with customizable dry-run and batch-size parameters.
- `POST /api/colleges/add`: Appends a new college with verified email, website, district, and contact info to `contacts.csv`.
- `POST /api/colleges/update`: In-place update of officer details, emails, or notes in the CSV.
- `POST /api/save-template`: Writes updated subject line and body text to `email_template.json`.
- `POST /api/reset-contact`: Reverts a contact’s status back to `Pending` for re-testing.

---

## 6. Frontend Operations Portal (`AUTO_LAND`)

The frontend is a single-page web application built with **React 19, TypeScript, Tailwind CSS, and Vite**:

1. **Purely Dynamic Metrics (Zero Mock Data)**:
   - All historical mock numbers (`1,482`, `1,420`, `1,180`) have been eradicated.
   - All counters, progress bars, and badges dynamically reflect the active records in `contacts.csv` (`125 Total`, `15 Verified`, `110 Pending`).
2. **Top District Density Visualization**:
   - Dynamically aggregates campuses by their district across Tamil Nadu.
   - Highlights educational hubs (Chennai, Coimbatore, Madurai, Tiruchirappalli, Salem, etc.) with proportional progress indicators.
3. **Institutional Classification Matrix**:
   - AICTE / UGC matrix dynamically groups colleges by category (`Engineering`, `Arts & Science`, `Medical & Health`, `Polytechnic / Voc`).
4. **Officer Profile Persistence**:
   - Directorate Officer identity (Name, Official Email, Zone) persists across browser reloads via `localStorage`.
5. **Real-Time Test Send & Batch Dispatch**:
   - One-click testing modal allowing live verification dispatches directly from the interface.

---

## 7. Operational Runbook

### 7.1 Running the Frontend & Backend Locally
From the project root:
```bash
# Start development server with live API backend (Port 3000)
npm run dev

# Or run the production server
npm run build
npm run serve
```
Open **`http://localhost:3000`** in any browser.

### 7.2 Testing Outreach from the Terminal
```bash
# 1. Run a Dry-Run Simulation (No emails sent, contacts.csv unchanged)
python3 run_outreach.py --dry-run --batch-size 3

# 2. Send a Single Real Test Email to a specific test mailbox
python3 run_outreach.py --test-target babsword6@gmail.com --batch-size 1 --force

# 3. Run a Real Batch Campaign (5 pending colleges with 2-second throttling)
python3 run_outreach.py --batch-size 5 --delay 2.0
```

### 7.3 Adding New Colleges
When adding colleges, maintain the strict quality filter:
1. Locate official institutional portal (`.ac.in` / `.edu.in`).
2. Extract the Dean, Principal, or Placement Officer official email.
3. Append via the **Web UI ("Add New Campus" button)** or append a row to `contacts.csv`.
4. Ensure `Status` is set to `Pending`.
