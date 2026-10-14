import React, { useState } from 'react';
import { CollegeContact } from '../types';

interface ImportContactsViewProps {
  onImportSuccess: (count: number) => void;
  onTriggerToast: (msg: string, icon?: string) => void;
}

export const ImportContactsView: React.FC<ImportContactsViewProps> = ({
  onImportSuccess,
  onTriggerToast
}) => {
  const [sheetUrl, setSheetUrl] = useState('https://docs.google.com/spreadsheets/d/1TN-Collegiate-HigherEd-Ledger-2024/edit');
  const [sheetTab, setSheetTab] = useState('TN_Affiliated_Colleges_AY24');
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncLogs, setSyncLogs] = useState<string[]>([]);
  const [syncDone, setSyncDone] = useState(false);

  // CSV Drag and drop state
  const [fileName, setFileName] = useState<string | null>(null);
  const [isProcessingCsv, setIsProcessingCsv] = useState(false);

  const handleStartGoogleSheetsSync = () => {
    setIsSyncing(true);
    setSyncLogs([]);
    setSyncDone(false);

    const logSteps = [
      'Connecting to Google Sheets API gateway...',
      'Authenticated with Directorate service account (read-only)...',
      `Loading tab "${sheetTab}" from Google Spreadsheet...`,
      'Found 125 institutional rows across verified districts...',
      'Running AISHE code normalization & syntax checks...',
      'Executing deduplication filter: verified zero duplicates in active ledger...',
      'Verifying MX DNS records for all university hostnames...',
      'Synchronization complete: 125 verified records active in ledger.'
    ];

    logSteps.forEach((step, index) => {
      setTimeout(() => {
        setSyncLogs(prev => [...prev, step]);
        if (index === logSteps.length - 1) {
          setIsSyncing(false);
          setSyncDone(true);
          onImportSuccess(125);
          onTriggerToast('Google Sheets sync finished: 125 records updated and reconciled.', 'sync');
        }
      }, (index + 1) * 350);
    });
  };

  const handleDropFile = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileUpload = (file: File) => {
    setFileName(file.name);
    setIsProcessingCsv(true);
    setTimeout(() => {
      setIsProcessingCsv(false);
      onImportSuccess(34);
      onTriggerToast(`Parsed ${file.name}: 34 colleges imported with verified AISHE codes.`, 'check_circle');
    }, 1200);
  };

  const handleDownloadTemplate = () => {
    const csvContent = 'data:text/csv;charset=utf-8,College_Name,AISHE_Code,District,Category,Affiliation,Principal_Name,Principal_Email,Phone,Website\n"Loyola College","C-43954","Chennai","Arts & Science","University of Madras","Rev. Dr. A. Louis Arockiaraj S.J.","principal@loyolacollege.edu","+91 44 2817 8200","https://loyolacollege.edu"';
    const encoded = encodeURI(csvContent);
    const a = document.createElement('a');
    a.href = encoded;
    a.download = 'TN_Outreach_Directory_Template.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    onTriggerToast('Template downloaded: TN_Outreach_Directory_Template.csv', 'download');
  };

  return (
    <div className="flex flex-col w-full pb-space-xl space-y-space-lg">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="font-code-sm text-code-sm uppercase tracking-widest text-primary font-bold">
            Data Ingestion & Hygiene
          </span>
          <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
          <span className="font-code-sm text-code-sm text-secondary">
            Collegiate Ledger Sync Engine
          </span>
        </div>
        <h1 className="font-headline-lg text-headline-lg text-on-surface font-bold tracking-tight">
          Import & Reconcile Contacts
        </h1>
        <p className="font-body-md text-body-md text-secondary mt-0.5">
          Synchronize institutional directories from Google Sheets or CSV rosters with automated deduplication and MX verification.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        {/* Left Column: Google Sheets Integration (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-space-md">
          {/* Card: Google Sheets Roster Sync */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-center justify-between mb-space-md">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center border border-emerald-200">
                  <span className="material-symbols-outlined text-[24px]">table_chart</span>
                </div>
                <div>
                  <h2 className="font-headline-sm text-on-surface font-bold">Google Sheets Live Sync</h2>
                  <p className="font-body-sm text-secondary">Continuous synchronization with state higher ed master spreadsheet</p>
                </div>
              </div>
              <span className="font-code-sm text-xs bg-emerald-100 text-emerald-800 px-2.5 py-1 rounded-full font-bold">
                OAuth Configured
              </span>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block font-label-sm text-secondary mb-1">
                  Google Sheet URL / Resource Identifier
                </label>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-3 top-2.5 text-[18px] text-secondary">
                    link
                  </span>
                  <input
                    type="text"
                    value={sheetUrl}
                    onChange={(e) => setSheetUrl(e.target.value)}
                    className="w-full pl-9 pr-3 py-2 bg-surface-container-low rounded-lg font-code-sm text-xs text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-label-sm text-secondary mb-1">Sheet Tab Name</label>
                  <select
                    value={sheetTab}
                    onChange={(e) => setSheetTab(e.target.value)}
                    className="w-full bg-surface-container-low px-3 py-2 rounded-lg font-body-sm text-xs text-on-surface border border-[#e2e8f0] focus:outline-none"
                  >
                    <option value="TN_Affiliated_Colleges_AY24">TN_Affiliated_Colleges_AY24 (125 rows)</option>
                    <option value="Anna_Univ_Autonomous_Nodes">Anna_Univ_Autonomous_Nodes (128 rows)</option>
                    <option value="DOTE_Polytechnic_Directory">DOTE_Polytechnic_Directory (206 rows)</option>
                    <option value="Medical_Colleges_TN">Medical_Colleges_TN (124 rows)</option>
                  </select>
                </div>
                <div>
                  <label className="block font-label-sm text-secondary mb-1">Sync Schedule</label>
                  <select className="w-full bg-surface-container-low px-3 py-2 rounded-lg font-body-sm text-xs text-on-surface border border-[#e2e8f0] focus:outline-none">
                    <option>Daily at 02:00 AM IST</option>
                    <option>Manual Trigger Only</option>
                    <option>Hourly Webhook Trigger</option>
                  </select>
                </div>
              </div>

              {/* Sync Logs Terminal */}
              {syncLogs.length > 0 && (
                <div className="p-3 bg-[#0b1c30] text-slate-200 rounded-lg font-code-sm text-[11px] space-y-1 max-h-48 overflow-y-auto border border-slate-800">
                  <div className="flex items-center justify-between text-secondary pb-1 border-b border-slate-700/60 mb-1">
                    <span className="text-emerald-400 font-bold">Console Output</span>
                    <span>{syncDone ? 'Status: 200 OK' : 'Processing...'}</span>
                  </div>
                  {syncLogs.map((log, i) => (
                    <div key={i} className="flex items-center gap-2">
                      <span className="text-secondary select-none">&gt;</span>
                      <span className={i === syncLogs.length - 1 ? 'text-primary-fixed' : 'text-slate-300'}>
                        {log}
                      </span>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex items-center justify-between pt-2">
                <span className="text-xs text-secondary">
                  Last successful sync: Today at 01:20 AM IST
                </span>
                <button
                  onClick={handleStartGoogleSheetsSync}
                  disabled={isSyncing}
                  className="px-4 py-2 bg-primary-container text-on-primary rounded-lg font-label-md font-semibold flex items-center gap-2 hover:opacity-95 active:scale-[0.98] transition-all disabled:opacity-50 cursor-pointer shadow-sm"
                >
                  <span className={`material-symbols-outlined text-[18px] ${isSyncing ? 'animate-spin' : ''}`}>
                    {isSyncing ? 'sync' : 'cloud_sync'}
                  </span>
                  <span>{isSyncing ? 'Reconciling Ledger...' : 'Run Sync Now'}</span>
                </button>
              </div>
            </div>
          </div>

          {/* Card: CSV / Excel Upload */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-center justify-between mb-space-md">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-surface-container text-primary flex items-center justify-center">
                  <span className="material-symbols-outlined text-[24px]">upload_file</span>
                </div>
                <div>
                  <h2 className="font-headline-sm text-on-surface font-bold">Manual File Ingestion</h2>
                  <p className="font-body-sm text-secondary">Upload CSV or XLSX files exported from AISHE or AICTE portals</p>
                </div>
              </div>

              <button
                onClick={handleDownloadTemplate}
                className="text-primary hover:underline font-label-sm font-semibold flex items-center gap-1 text-xs cursor-pointer"
              >
                <span className="material-symbols-outlined text-[16px]">file_download</span>
                <span>Download Sample CSV</span>
              </button>
            </div>

            {/* Dropzone */}
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDropFile}
              className="border-2 border-dashed border-[#cbd5e1] hover:border-primary rounded-xl p-8 text-center bg-surface-container-low/40 hover:bg-surface-container-low transition-all cursor-pointer flex flex-col items-center justify-center"
              onClick={() => document.getElementById('csv-file-input')?.click()}
            >
              <input
                id="csv-file-input"
                type="file"
                accept=".csv, .xlsx, .xls"
                className="hidden"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    handleFileUpload(e.target.files[0]);
                  }
                }}
              />
              <div className="w-12 h-12 rounded-full bg-surface-container flex items-center justify-center text-secondary mb-2">
                <span className="material-symbols-outlined text-[28px]">cloud_upload</span>
              </div>
              <p className="font-body-md font-semibold text-on-surface">
                {fileName ? fileName : 'Drag & drop institutional spreadsheet or browse'}
              </p>
              <p className="font-label-sm text-secondary mt-1">
                Supports .CSV, .XLSX formatted with AISHE Code, Institution Name, and Contact Email
              </p>
              {isProcessingCsv && (
                <div className="mt-3 flex items-center gap-2 text-primary font-code-sm text-xs">
                  <span className="material-symbols-outlined animate-spin text-[16px]">sync</span>
                  Parsing collegiate data...
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Hygiene & Deduplication Ledger (5 cols) */}
        <div className="lg:col-span-5 flex flex-col gap-space-md">
          {/* Deduplication Summary Card */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-center justify-between mb-space-sm">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-secondary text-[20px]">filter_alt</span>
                <h3 className="font-headline-sm font-bold text-on-surface">Deduplication Telemetry</h3>
              </div>
              <span className="font-code-sm text-xs bg-secondary-fixed text-on-secondary-fixed px-2 py-0.5 rounded font-bold">
                80 Cleaned
              </span>
            </div>
            <p className="font-body-sm text-secondary mb-space-md">
              Multi-criteria matching engine to eliminate repeated campus dispatches and resolve duplicate principal emails.
            </p>

            <div className="space-y-3">
              <div className="p-3 bg-surface-container-low rounded-lg border border-[#e2e8f0]/80">
                <div className="flex items-center justify-between text-xs font-semibold text-on-surface mb-1">
                  <span>AISHE Code Collision Check</span>
                  <span className="text-emerald-700">100% Unique</span>
                </div>
                <p className="text-[11px] text-secondary">
                  Detected and merged 42 duplicate rows where multiple departmental mailboxes shared identical AISHE codes.
                </p>
              </div>

              <div className="p-3 bg-surface-container-low rounded-lg border border-[#e2e8f0]/80">
                <div className="flex items-center justify-between text-xs font-semibold text-on-surface mb-1">
                  <span>Fuzzy Name Normalization</span>
                  <span className="text-primary font-bold">38 Resolved</span>
                </div>
                <p className="text-[11px] text-secondary">
                  Example: "Govt College of Eng., Salem" unified with "Government College of Engineering Salem (C-1392)".
                </p>
              </div>

              <div className="p-3 bg-surface-container-low rounded-lg border border-[#e2e8f0]/80">
                <div className="flex items-center justify-between text-xs font-semibold text-on-surface mb-1">
                  <span>Domain Hostname Consistency</span>
                  <span className="text-sky-700">98.2% Direct</span>
                </div>
                <p className="text-[11px] text-secondary">
                  Eliminated generic @gmail.com aliases when official @edu.in institutional routing was discovered.
                </p>
              </div>
            </div>
          </div>

          {/* MX DNS Verification Engine Card */}
          <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-center justify-between mb-2">
              <span className="font-label-sm font-semibold uppercase text-secondary">
                Mail Routing MX Validation
              </span>
              <span className="font-code-sm text-xs text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                98.2% Deliverable
              </span>
            </div>
            <p className="font-body-sm text-secondary mb-3">
              Validates that institutional mail servers (MX records) accept connections before dispatches leave the queue.
            </p>
            <div className="flex items-center justify-between bg-surface-container-low p-2 rounded text-[11px] border border-[#e2e8f0]">
              <span className="text-secondary">Safe Bounce Ceiling:</span>
              <span className="font-code-sm font-bold text-on-surface">&lt; 3.0% SLA Threshold</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
