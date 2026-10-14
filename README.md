# Tamil Nadu Higher Education Email Outreach Automation System

A production-grade institutional outreach platform connecting an automated **Python SMTP dispatch engine** with a modern **React 19 / TypeScript Web Operations Portal (`AUTO_LAND`)**. 

Designed for structured, verified outreach across collegiate campuses in **Tamil Nadu**, this platform maintains an audited roster of **125 accredited institutions across all 38 educational districts**, strictly excluding any college without a verified official institutional email.

---

## 📑 Quick Navigation
- 🚀 [Quick Start Guide](#-quick-start-guide)
- 📁 [Repository & Directory Structure](#-repository--directory-structure)
- 🌐 [Deployment Guide (Netlify + Render/VPS/Docker)](DEPLOYMENT_GUIDE.md)
- 📊 [Architecture & System Overview](docs/overview.md)
- 📋 [Implementation Tasks & Audit](docs/tasks.md)
- 🔒 [Environment Variables Setup](#-environment-variables-setup)

---

## 🌟 Key Features

1. **Audited Institutional Database (`contacts.csv`)**:
   - **125 Verified Campuses**: Spanning Anna University, autonomous engineering institutes, arts & sciences colleges, polytechnics, and medical colleges.
   - **Strict Verification Filter**: 100% of campuses have verified official institutional email addresses and official website URLs. Zero unverified records.
   - **All 38 TN Districts Covered**: High-density educational clusters mapped across 9 regional zones.

2. **Safe & Compliant SMTP Engine (`run_outreach.py`)**:
   - Authenticated Gmail / Google Workspace SMTP transport over secure TLS (port 587).
   - Rate-limiting throttle delay (default 1.5s - 5s) to preserve sender domain reputation.
   - **Dry-Run Simulation Mode (`--dry-run`)**: Test message merges and recipient lists without sending actual emails or modifying the database.
   - **Single-Target Override Mode (`--test-target <email>`)**: Direct all outgoing messages to an internal test inbox (e.g. `babsword6@gmail.com`) for verification before launching campaigns.
   - **Dynamic Personalization with Smart Fallbacks**: Context-aware greetings preventing broken placeholder tags like `"Dear ,"`.

3. **Web Operations Portal (`AUTO_LAND`)**:
   - Built with **React 19, TypeScript, Tailwind CSS, and Vite**.
   - **Zero Mock Numbers**: All historical mock data (`1,482`, `1,420`, `1,180`) purged; metrics, badges, and progress bars compute dynamically from the live database.
   - **Live Top District Density Chart**: Dynamically groups and sorts campus distribution across Tamil Nadu districts.
   - **Institutional Classifications Matrix**: Real-time breakdown across AICTE, UGC, and DOTE categories.
   - **Officer Profile Persistence**: Administrator details persist locally across browser sessions.
   - **Integrated REST API Bridge (`AUTO_LAND/server_api.mjs`)**: Mounts directly inside Vite / Express to handle dispatch commands and CSV updates.

---

## 📁 Repository & Directory Structure

```
.
├── README.md                 # Primary project documentation & quick start
├── DEPLOYMENT_GUIDE.md       # Full deployment manual (Netlify Frontend + Render/VPS Backend)
├── Dockerfile                # Production multi-runtime container (Node.js 20 + Python 3)
├── netlify.toml              # Netlify build rules & backend API proxy configuration
├── package.json              # Root npm runner & development scripts
├── contacts.csv              # Master institutional ledger (125 verified TN colleges)
├── test_contacts.csv         # Isolated test database fixture
├── email_template.json       # Email subject & body templates with dynamic placeholders
├── run_outreach.py           # Core Python SMTP outreach engine
├── .env.example              # Safe template for credentials configuration
├── .gitignore                # Comprehensive ignore rules (excluding .env, node_modules, dist)
│
├── AUTO_LAND/                # Web Operations Portal (Frontend & API Bridge)
│   ├── index.html            # Application entry HTML
│   ├── vite.config.ts        # Vite configuration with embedded API plugin
│   ├── package.json          # Frontend dependencies & scripts
│   ├── server.ts             # Express production server
│   ├── server_api.mjs        # Backend API middleware (CORS enabled)
│   ├── netlify.toml          # Subdirectory Netlify build configuration
│   ├── public/
│   │   └── _redirects        # Netlify SPA client routing fallback (/* /index.html 200)
│   └── src/
│       ├── App.tsx           # Main application shell & state coordinator
│       ├── types.ts          # TypeScript domain interfaces
│       ├── components/       # Reusable UI components (Sidebar, Header, Modals, Toast)
│       ├── views/            # Screen views (Dashboard, College Contacts, Campaigns, etc.)
│       └── data/mockData.ts  # Fallback default constants
│
├── docs/                     # Detailed architectural documentation
│   ├── overview.md           # In-depth architectural & operational overview
│   ├── requirements.md       # System specifications & requirements
│   └── tasks.md              # Phase tracking & milestone audit
│
└── scripts/                  # Data extraction & database expansion utilities
    ├── add_fifty_colleges.py         # Utility script for expanding collegiate database
    └── scrape_and_update_colleges.py # Automated portal verification scraper
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Node.js**: v18.x or v20.x ([Download](https://nodejs.org/))
- **Python**: v3.9+ ([Download](https://www.python.org/))
- **npm**: v9.x+

### 2. Setup & Installation
Clone or navigate to the repository directory:
```bash
# 1. Install root dependencies
npm install

# 2. Install frontend dependencies
cd AUTO_LAND && npm install && cd ..

# 3. Configure your environment credentials
cp .env.example .env
```

Open `.env` and configure your Gmail credentials:
```env
SENDER_EMAIL=your-email@gmail.com
GMAIL_SENDER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
PORT=3000
NODE_ENV=development
```
*(See [Obtaining a Gmail App Password](#-obtaining-a-gmail-app-password) below if you need one).*

### 3. Launching the Web Portal
Start the live development server with the integrated backend API:
```bash
npm run dev
```
Open **`http://localhost:3000`** in your browser. The dashboard will load the active roster of 125 colleges directly from `contacts.csv`.

To run the production server:
```bash
npm run build
npm run serve
```

---

## ⚡ CLI Outreach Operations

You can also trigger dispatches directly from the terminal using `run_outreach.py`:

```bash
# 1. Dry-Run Simulation (Safe: renders next pending email preview without sending)
python3 run_outreach.py --dry-run

# 2. Single-Target Test Override (Test send or preview strictly for a specific email)
python3 run_outreach.py --dry-run --target babsword6@gmail.com --force
python3 run_outreach.py --target babsword6@gmail.com --force

# 3. Batch Outreach Wave (Sends to all pending colleges in contacts.csv)
python3 run_outreach.py --all

# 4. Use Alternative Test Dataset
python3 run_outreach.py --csv test_contacts.csv --dry-run
```

---

## 🌐 Deployment (Frontend on Netlify + Cloud Backend)

For complete instructions on deploying the frontend to **Netlify** and hosting the Python/Node backend on **Render.com**, **Railway**, **Docker**, or a **VPS**, please read the dedicated deployment manual:

👉 **[Read the Full Deployment Guide (DEPLOYMENT_GUIDE.md)](DEPLOYMENT_GUIDE.md)**

### Brief Deployment Summary:
- **Frontend on Netlify**: Connect your GitHub repository to Netlify. Set **Base directory** to `AUTO_LAND`, **Build command** to `npm run build`, and **Publish directory** to `dist`.
- **Backend on Render**: Create a free Web Service on Render with Build command `npm install && cd AUTO_LAND && npm install && npm run build` and Start command `node --loader tsx AUTO_LAND/server.ts`.
- **Zero CORS Proxy**: In `netlify.toml`, uncomment the redirect proxy so all `/api/*` traffic transparently forwards to your backend without any CORS errors!

---

## 🔒 Obtaining a Gmail App Password

To dispatch emails through Gmail SMTP:
1. Navigate to your [Google Account Security Settings](https://myaccount.google.com/security).
2. Enable **2-Step Verification** (required by Google for SMTP access).
3. In the search bar at the top, type **"App passwords"**.
4. Create a new App Password (e.g. name it `TN Outreach System`).
5. Copy the generated **16-character code** (format: `xxxx xxxx xxxx xxxx`).
6. Paste it into your `.env` file as `GMAIL_APP_PASSWORD`.

---

## 📦 How to Push to Git

To push this project cleanly to your Git repository:

```bash
# 1. Initialize git repository (if not already initialized)
git init

# 2. Check that .env is ignored and files are clean
git status

# 3. Stage all clean project files
git add .

# 4. Commit changes
git commit -m "feat: complete Tamil Nadu outreach platform with 125 colleges and deployment guide"

# 5. Add your GitHub remote repository
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>.git
git branch -M main

# 6. Push to GitHub
git push -u origin main
```

---

## 📄 License & Attribution
Developed for academic partnership and collegiate collaboration outreach in Tamil Nadu. Ensure institutional outreach conforms with UGC, AICTE, and university communications guidelines.
