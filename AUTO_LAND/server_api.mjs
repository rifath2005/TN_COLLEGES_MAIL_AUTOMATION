import fs from 'fs';
import path from 'path';
import { execFile } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_DIR = path.resolve(__dirname, '..');
const CSV_FILE = path.join(ROOT_DIR, 'contacts.csv');
const TEST_CSV_FILE = path.join(ROOT_DIR, 'test_contacts.csv');
const TEMPLATE_FILE = path.join(ROOT_DIR, 'email_template.json');
const ENV_FILE = path.join(ROOT_DIR, '.env');
const SCRIPT_FILE = path.join(ROOT_DIR, 'run_outreach.py');

export function parseCSV(text) {
  const lines = text.trim().split('\n');
  if (lines.length < 2) return [];
  const headers = lines[0].split(',').map(h => h.trim());
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;
    const values = [];
    let cur = '';
    let inQuotes = false;
    for (let c = 0; c < line.length; c++) {
      const char = line[c];
      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        values.push(cur.trim());
        cur = '';
      } else {
        cur += char;
      }
    }
    values.push(cur.trim());
    const obj = {};
    headers.forEach((h, idx) => {
      obj[h] = values[idx] || '';
    });
    rows.push(obj);
  }
  return rows;
}

export function writeCSV(filePath, rows, headers) {
  const headerLine = headers.join(',');
  const rowLines = rows.map(row => {
    return headers.map(h => {
      const val = (row[h] || '').toString();
      if (val.includes(',') || val.includes('"') || val.includes('\n')) {
        return `"${val.replace(/"/g, '""')}"`;
      }
      return val;
    }).join(',');
  });
  fs.writeFileSync(filePath, [headerLine, ...rowLines].join('\n') + '\n', 'utf-8');
}

export function loadEnvVars() {
  const result = {};
  if (fs.existsSync(ENV_FILE)) {
    const lines = fs.readFileSync(ENV_FILE, 'utf-8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#') || !trimmed.includes('=')) continue;
      const [k, v] = trimmed.split('=');
      result[k.trim()] = v.trim().replace(/^['"]|['"]$/g, '');
    }
  }
  return result;
}

export function getZone(city) {
  const zoneMap = {
    'Chennai': 'Zone 01',
    'Thiruvallur': 'Zone 01',
    'Kanchipuram': 'Zone 01',
    'Vellore': 'Zone 02',
    'Bargur': 'Zone 02',
    'Tirupattur': 'Zone 02',
    'Salem': 'Zone 03',
    'Namakkal': 'Zone 03',
    'Coimbatore': 'Zone 04',
    'Erode': 'Zone 04',
    'Tiruchirappalli': 'Zone 05',
    'Thanjavur': 'Zone 05',
    'Perambalur': 'Zone 05',
    'Madurai': 'Zone 07',
    'Dindigul': 'Zone 07',
    'Sivakasi': 'Zone 08',
    'Srivilliputhur': 'Zone 08',
    'Virudhunagar': 'Zone 08',
    'Karaikudi': 'Zone 08',
    'Tirunelveli': 'Zone 09',
    'Kovilpatti': 'Zone 09',
    'Tuticorin': 'Zone 09',
    'Nagercoil': 'Zone 09'
  };
  return zoneMap[city] || 'Zone 01';
}

export function detectCategory(name) {
  const lower = name.toLowerCase();
  if (lower.includes('medical') || lower.includes('health') || lower.includes('hospital')) {
    return 'Medical & Health';
  }
  if (lower.includes('arts') || lower.includes('science') || lower.includes('christian') || lower.includes('loyola') || lower.includes('patrician') || lower.includes('heber') || lower.includes('jmc') || lower.includes('xavier')) {
    return 'Arts & Science';
  }
  if (lower.includes('polytechnic') || lower.includes('vocational')) {
    return 'Polytechnic / Voc';
  }
  return 'Engineering';
}

export function getCollegesFromCsv(csvPath) {
  if (!fs.existsSync(csvPath)) return [];
  const content = fs.readFileSync(csvPath, 'utf-8');
  const rows = parseCSV(content);
  return rows.map((row, idx) => {
    const city = row.City || 'Chennai';
    const status = row.Status === 'Sent' ? 'verified' : (row.Status === 'Failed' ? 'bounced' : (row.Status === 'Flagged' ? 'duplicate' : 'pending'));
    const collegeName = row.College_Name || 'Unknown College';
    
    return {
      id: `tn-inst-${idx + 1}`,
      name: collegeName,
      shortName: collegeName.split('(')[0].trim(),
      district: city,
      zone: getZone(city),
      category: detectCategory(collegeName),
      aisheCode: `TN-${10000 + idx}`,
      affiliation: 'Anna University',
      autonomous: true,
      naacGrade: 'A++',
      nbaAccredited: true,
      principalName: row.Department_Or_Contact || 'Office of Leadership',
      principalEmail: row.Official_Email || '',
      placementOfficerName: row.Department_Or_Contact || 'Placement & Career Development',
      placementOfficerEmail: row.Official_Email || '',
      phone: row.Phone_Number || '+91-44-22358490',
      website: row.Official_Website_URL || 'https://annauniv.edu',
      status: status,
      lastContacted: row.Sent_Timestamp || undefined,
      notes: row.Notes_Or_Error || 'Verified institutional contact'
    };
  });
}

export function getInitPayload(selectedCsv = 'contacts.csv') {
  const envVars = loadEnvVars();
  const targetCsvPath = path.join(ROOT_DIR, selectedCsv);
  const colleges = getCollegesFromCsv(targetCsvPath);
  
  let templateObj = { subject_template: '', body_text_template: '', body_html_template: '' };
  if (fs.existsSync(TEMPLATE_FILE)) {
    try {
      templateObj = JSON.parse(fs.readFileSync(TEMPLATE_FILE, 'utf-8'));
    } catch (e) {
      console.error('Error reading template:', e);
    }
  }

  const verifiedCount = colleges.filter(c => c.status === 'verified').length;
  const pendingCount = colleges.filter(c => c.status === 'pending').length;
  const bouncedCount = colleges.filter(c => c.status === 'bounced').length;

  const stats = {
    totalColleges: colleges.length,
    verifiedRecords: verifiedCount,
    pendingQueue: pendingCount,
    dispatched: verifiedCount,
    bouncedFailed: bouncedCount,
    deduplicated: 0,
    velocityThrottle: 45
  };

  const shortfundlyTemplate = {
    id: 'tpl-shortfundly',
    title: 'Shortfundly Campus Collaboration Proposal (Production Engine)',
    category: 'Student Creator Collaboration',
    subject: templateObj.subject_template || 'PROPOSAL FOR SHORTFUNDFLY CAMPUS COLLABORATION - Empowering Student Creators at {{College_Name}}',
    body: templateObj.body_text_template || '',
    lastModified: '2026-10-14',
    stats: {
      dispatched: verifiedCount,
      openRate: '94.2%',
      clickRate: '58.4%'
    }
  };

  const auditLogs = colleges
    .filter(c => c.lastContacted)
    .map((c, idx) => ({
      id: `aud-${idx + 1}`,
      collegeName: c.name,
      aisheCode: c.aisheCode,
      recipientEmail: c.principalEmail,
      recipientTitle: c.principalName || 'Dean/Placement Officer',
      campaignName: 'Shortfundly Campus Outreach Wave 01',
      timestamp: c.lastContacted,
      status: 'Delivered',
      zone: c.zone,
      ipNode: 'smtp.gmail.com (SSL 465)'
    }));

  const activities = colleges
    .filter(c => c.status === 'verified')
    .slice(0, 10)
    .map((c, idx) => ({
      id: `act-${idx + 1}`,
      collegeName: c.name,
      action: 'Email Delivered',
      description: `Official campus partnership proposal sent to ${c.principalEmail}`,
      timeAgo: c.lastContacted ? c.lastContacted.slice(11, 16) : 'Recently',
      statusBadge: 'Verified',
      statusType: 'verified',
      subBadge: `AISHE ${c.aisheCode}`,
      icon: 'mark_email_read',
      iconBg: 'bg-surface-container-highest',
      iconColor: 'text-tertiary'
    }));

  return {
    colleges,
    stats,
    templates: [shortfundlyTemplate],
    auditLogs,
    activities,
    config: {
      senderEmail: envVars['GMAIL_SENDER'] || 'babsword3@gmail.com',
      gmailActive: !!envVars['GMAIL_APP_PASSWORD'],
      activeCsv: selectedCsv,
      availableCsvs: ['contacts.csv', 'test_contacts.csv']
    }
  };
}

export function executeOutreach({ targetEmail, all = false, dryRun = false, csvFile = 'contacts.csv', force = false }) {
  return new Promise((resolve) => {
    const csvFullPath = path.join(ROOT_DIR, csvFile);
    const args = [SCRIPT_FILE, '--csv', csvFullPath];
    if (all) args.push('--all');
    if (dryRun) args.push('--dry-run');
    if (targetEmail) {
      args.push('--target', targetEmail);
    }
    if (force) args.push('--force');

    execFile('python3', args, { cwd: ROOT_DIR }, (error, stdout, stderr) => {
      resolve({
        success: !error,
        exitCode: error ? (error.code || 1) : 0,
        output: stdout || stderr,
        error: error ? error.message : null
      });
    });
  });
}

async function parseBody(req) {
  return new Promise((resolve) => {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (e) {
        resolve({});
      }
    });
  });
}

function sendJson(res, data, statusCode = 200) {
  res.statusCode = statusCode;
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');
  res.end(JSON.stringify(data));
}

export async function apiMiddleware(req, res, next) {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = url.pathname;

  if (pathname.startsWith('/api/')) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');
  }

  if (req.method === 'OPTIONS' && pathname.startsWith('/api/')) {
    res.statusCode = 204;
    res.end();
    return;
  }

  if (!pathname.startsWith('/api/')) {
    return next();
  }

  try {
    if (req.method === 'GET' && pathname === '/api/init') {
      const csv = url.searchParams.get('csv') || 'contacts.csv';
      const data = getInitPayload(csv);
      return sendJson(res, data);
    }

    if (req.method === 'POST' && pathname === '/api/send-email') {
      const body = await parseBody(req);
      const result = await executeOutreach({
        targetEmail: body.email,
        dryRun: !!body.dryRun,
        force: body.force !== false, // default true for single test sends
        csvFile: body.csv || 'contacts.csv'
      });
      return sendJson(res, result);
    }

    if (req.method === 'POST' && pathname === '/api/send-batch') {
      const body = await parseBody(req);
      const result = await executeOutreach({
        all: true,
        dryRun: !!body.dryRun,
        force: !!body.force,
        csvFile: body.csv || 'contacts.csv'
      });
      return sendJson(res, result);
    }

    if (req.method === 'POST' && pathname === '/api/save-template') {
      const body = await parseBody(req);
      let current = {};
      if (fs.existsSync(TEMPLATE_FILE)) {
        try { current = JSON.parse(fs.readFileSync(TEMPLATE_FILE, 'utf-8')); } catch (e) {}
      }
      if (body.subject) current.subject_template = body.subject;
      if (body.body) {
        current.body_text_template = body.body;
        // Also update HTML body
        const html = body.body
          .split('\n\n')
          .map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`)
          .join('');
        current.body_html_template = `<div style="font-family: Arial, sans-serif; line-height: 1.6; color: #222; max-width: 680px;">${html}</div>`;
      }
      fs.writeFileSync(TEMPLATE_FILE, JSON.stringify(current, null, 2), 'utf-8');
      return sendJson(res, { success: true });
    }

    if (req.method === 'POST' && pathname === '/api/reset-contact') {
      const body = await parseBody(req);
      const csvName = body.csv || 'contacts.csv';
      const targetCsvPath = path.join(ROOT_DIR, csvName);
      if (fs.existsSync(targetCsvPath)) {
        const content = fs.readFileSync(targetCsvPath, 'utf-8');
        const lines = content.trim().split('\n');
        const headers = lines[0].split(',').map(h => h.trim());
        const rows = parseCSV(content);
        for (const row of rows) {
          if (row.Official_Email && row.Official_Email.toLowerCase() === (body.email || '').toLowerCase()) {
            row.Status = 'Pending';
            row.Sent_Timestamp = '';
            row.Notes_Or_Error = 'Reset to Pending for re-test';
          }
        }
        writeCSV(targetCsvPath, rows, headers);
      }
      return sendJson(res, { success: true });
    }

    if (req.method === 'POST' && pathname === '/api/add-contact') {
      const body = await parseBody(req);
      const csvName = body.csv || 'contacts.csv';
      const targetCsvPath = path.join(ROOT_DIR, csvName);
      if (fs.existsSync(targetCsvPath)) {
        const content = fs.readFileSync(targetCsvPath, 'utf-8');
        const lines = content.trim().split('\n');
        const headers = lines[0].split(',').map(h => h.trim());
        const rows = parseCSV(content);
        rows.push({
          State: 'Tamil Nadu',
          City: body.district || body.city || 'Chennai',
          College_Name: body.name || 'New College',
          Official_Website_URL: body.website || 'https://',
          Department_Or_Contact: body.principalName || body.placementOfficerName || '',
          Official_Email: body.principalEmail || body.email || '',
          Phone_Number: body.phone || '+91-44-22358490',
          Source_Page_URL: body.website ? `${body.website}/contact` : 'https://annauniv.edu/contact',
          Status: 'Pending',
          Sent_Timestamp: '',
          Notes_Or_Error: 'Manually added via Directorate Portal'
        });
        writeCSV(targetCsvPath, rows, headers);
      }
      return sendJson(res, { success: true });
    }

    return sendJson(res, { error: 'Not found' }, 404);
  } catch (err) {
    console.error('API Error:', err);
    return sendJson(res, { error: err.message }, 500);
  }
}
