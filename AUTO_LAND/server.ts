import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { apiMiddleware } from './server_api.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = Number(process.env.PORT) || 3000;

// API routes
app.use(apiMiddleware);

// Static assets in production
const distPath = path.join(__dirname, 'dist');
app.use(express.static(distPath));

app.get('*', (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`[TN Outreach Directorate Server] Running at http://localhost:${PORT}`);
});
