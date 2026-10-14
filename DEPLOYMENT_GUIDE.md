# Netlify & Backend Deployment Guide: Tamil Nadu Outreach Automation

This guide provides complete, step-by-step instructions on **how to host the frontend on Netlify** and **how to host the Python/Node backend** so they work together seamlessly in production.

---

## 1. Architectural Strategy: Decoupling Frontend & Backend

Before deploying, it helps to understand why Netlify needs a backend companion for this system:

- **Frontend (`AUTO_LAND`)**: A Single-Page Application (SPA) built with React 19, TypeScript, and Vite. Netlify is **built specifically for this**—it distributes static assets globally across high-speed CDNs with free automated SSL.
- **Backend (`server.ts`, `server_api.mjs`, `run_outreach.py`)**: Responsible for connecting to Gmail SMTP over TLS, executing Python dispatch subprocesses, and updating `contacts.csv`. A static CDN cannot run long-lived Python scripts or persist writes to local disk files.

### The Recommended Setup (Zero CORS Proxy Architecture)
```
  [ User Browser ]
         │
         │ (Visits https://your-app.netlify.app)
         ▼
  ┌────────────────────────────────────────────────────────┐
  │                    Netlify Frontend                    │
  │  ├── Serves React 19 UI (dist/ bundle)                 │
  │  └── Automatically proxies /api/* requests to Backend  │
  └──────────────────────────┬─────────────────────────────┘
                             │ (Encrypted HTTPS Proxy Rewrite)
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │         Cloud Backend Service (Render / Railway / VPS)  │
  │  ├── Node.js Express Server (AUTO_LAND/server.ts)       │
  │  ├── Python 3 Dispatcher (run_outreach.py)              │
  │  ├── Institutional Database (contacts.csv)              │
  │  └── Secure Gmail SMTP Transport (smtp.gmail.com:587)  │
  └────────────────────────────────────────────────────────┘
```

> [!TIP]
> **Why this is the best setup:** By using Netlify's built-in redirect proxy rewrite, your frontend code **does not need to change at all**. Calls to `/api/init` or `/api/test-send` go to your Netlify domain and are transparently forwarded behind the scenes to your backend without any CORS errors!

---

## 2. Part 1: Hosting the Frontend on Netlify

### Step 2.1: Pre-configured Files (Already in Your Project)
We have already prepared your project with the essential Netlify files:
1. **`AUTO_LAND/public/_redirects`**:
   ```
   /*    /index.html   200
   ```
   *Guarantees client-side SPA routing works properly when users refresh on `/college-contacts` or `/settings` (prevents 404 errors).*
2. **`netlify.toml`**:
   *Configures automated build commands and deployment directories.*

---

### Step 2.2: Deploy via GitHub (Recommended)

1. **Push your code to GitHub**:
   If not already pushed, initialize and push your repository to your GitHub account:
   ```bash
   git init
   git add .
   git commit -m "feat: complete outreach system with 125 colleges and live backend"
   git branch -M main
   git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>.git
   git push -u origin main
   ```

2. **Log in to Netlify**:
   - Go to [https://app.netlify.com](https://app.netlify.com).
   - Sign in with your GitHub account.

3. **Import Project**:
   - Click **"Add new site"** $\rightarrow$ **"Import an existing project"**.
   - Select **GitHub** and pick your repository.

4. **Configure Build Settings**:
   Netlify will prompt for build configurations:
   - **Base directory**: `AUTO_LAND`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist` (or `AUTO_LAND/dist` if base is left at root)

5. **Deploy**:
   - Click **"Deploy site"**.
   - Netlify will build your application in ~30 seconds and provide a live URL like `https://peaceful-haven-12345.netlify.app`.

---

### Step 2.3: Deploy via Netlify CLI (Alternative Quick Deploy)
If you prefer deploying directly from your Linux terminal without linking GitHub:

```bash
# 1. Install Netlify CLI globally
sudo npm install -g netlify-cli

# 2. Build the production frontend assets
cd "/home/nabeel/Documents/Automation of emails/AUTO_LAND"
npm run build

# 3. Log in to Netlify
netlify login

# 4. Deploy to production
netlify deploy --prod --dir=dist
```
Follow the terminal prompt to create a new site or link an existing one.

---

## 3. Part 2: Hosting the Backend

You need a server environment with **Node.js (v18+)** and **Python 3**. Here are the two best options:

---

### Option A: Free/Low-Cost Cloud Container on Render.com (Recommended)
[Render.com](https://render.com) offers a native Node & Python environment with a generous free tier and free SSL certificates.

#### Step-by-Step on Render:
1. Go to [https://render.com](https://render.com) and create an account.
2. In the dashboard, click **"New +"** $\rightarrow$ **"Web Service"**.
3. Connect your GitHub repository.
4. Fill in the service configuration:
   - **Name**: `tn-outreach-backend`
   - **Region**: Singapore or Frankfurt (choose closest to India)
   - **Branch**: `main`
   - **Runtime**: `Node`
   - **Build Command**:
     ```bash
     npm install && cd AUTO_LAND && npm install && npm run build
     ```
   - **Start Command**:
     ```bash
     node --loader tsx AUTO_LAND/server.ts
     ```
   - **Instance Type**: `Free`

5. **Set Environment Variables**:
   Click **"Advanced"** $\rightarrow$ **"Add Environment Variable"**:
   - `PORT`: `3000`
   - `NODE_ENV`: `production`
   - `SENDER_EMAIL`: `your-email@gmail.com`
   - `GMAIL_APP_PASSWORD`: `your-16-char-app-password`

6. Click **"Create Web Service"**.
   - Render will build the project and launch the server.
   - You will receive a backend URL like:
     `https://tn-outreach-backend.onrender.com`

#### Step 6: Connect Netlify Frontend to Render Backend (The 1-Step Link)
Now, tell Netlify to route all `/api/*` requests to your Render backend!

Open `netlify.toml` in your repository and update the redirect rule:
```toml
[[redirects]]
  from = "/api/*"
  to = "https://tn-outreach-backend.onrender.com/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```
Commit and push this change to GitHub. Netlify will redeploy automatically. **Your Netlify frontend is now fully connected to your live backend!**

---

### Option B: Deploying on a Cloud VPS (Ubuntu DigitalOcean / AWS EC2 / Hetzner)
If you have a Linux virtual server (VPS) with a public IP:

1. **SSH into your server**:
   ```bash
   ssh root@your-server-ip
   ```

2. **Install Node.js 20 & Python 3**:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip git curl
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt install -y nodejs
   sudo npm install -g pm2
   ```

3. **Clone your repository**:
   ```bash
   git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>.git /opt/outreach
   cd /opt/outreach
   ```

4. **Install dependencies & build**:
   ```bash
   npm install
   cd AUTO_LAND && npm install && npm run build && cd ..
   ```

5. **Configure `.env`**:
   ```bash
   nano .env
   # Add your credentials:
   # SENDER_EMAIL=your-email@gmail.com
   # GMAIL_APP_PASSWORD=your-16-character-password
   ```

6. **Start service with PM2 (Auto-restart on reboot)**:
   ```bash
   pm2 start "node --loader tsx AUTO_LAND/server.ts" --name "tn-outreach"
   pm2 save
   pm2 startup
   ```

7. **Configure Nginx as Reverse Proxy**:
   ```nginx
   server {
       listen 80;
       server_name api.yourdomain.com; # or your IP

       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```
   Point Netlify's `netlify.toml` to `https://api.yourdomain.com/api/:splat`.

---

### Option C: Docker Container (Render / Railway / Fly.io / AWS ECS)
A production-ready `Dockerfile` is already created in your root directory.

To run with Docker:
```bash
# Build the container
docker build -t tn-outreach:latest .

# Run the container with your Gmail credentials
docker run -d \
  -p 3000:3000 \
  -e SENDER_EMAIL="your-email@gmail.com" \
  -e GMAIL_APP_PASSWORD="your-app-password" \
  --name tn-outreach-app \
  tn-outreach:latest
```

---

## 4. Environment Variables Checklist

Ensure these variables are set in your backend host (Render, Railway, or VPS):

| Variable | Description | Example |
| :--- | :--- | :--- |
| `SENDER_EMAIL` | Official sender Gmail / Google Workspace address | `babsword3@gmail.com` |
| `GMAIL_APP_PASSWORD` | 16-character Google App Password (not standard account password) | `abcd efgh ijkl mnop` |
| `PORT` | Listening port for Express API | `3000` |
| `NODE_ENV` | Environment identifier | `production` |

> [!IMPORTANT]
> **How to create a Gmail App Password:**
> 1. Log in to your Google Account at [myaccount.google.com](https://myaccount.google.com).
> 2. Go to **Security** $\rightarrow$ Enable **2-Step Verification** (if not already enabled).
> 3. Search for **"App passwords"** in the top search bar.
> 4. Create an App name (e.g. `TN Outreach`) and copy the generated 16-character code.
> 5. Paste this code as `GMAIL_APP_PASSWORD`.

---

## 5. End-to-End Verification Checklist

Once both frontend and backend are deployed:

- [ ] **Frontend Loads**: Navigate to your Netlify URL (`https://your-app.netlify.app`). Verify the dashboard loads without layout issues.
- [ ] **Live Ledger Loaded**: Check that the dashboard shows **125 Total Colleges**, **15 Verified**, and **110 Pending Queue** (fetched dynamically from `/api/init`).
- [ ] **SPA Routing Works**: Navigate to `College Contacts` or `Settings` and refresh the page (press `F5`). Verify that Netlify does not return a 404 error.
- [ ] **Test Email Dispatch**:
  1. Open the **Dashboard**.
  2. Click **"Quick Test Email (babsword6@gmail.com)"**.
  3. Verify the browser receives a success confirmation toast.
  4. Inspect the recipient mailbox to confirm receipt of the formatted outreach invitation.
- [ ] **Campaign Launch**: Test launching a batch wave using the "Launch Campaign" modal and verify status updates in the ledger.
