import React, { useState } from 'react';
import { SystemStats } from '../types';

interface SettingsViewProps {
  stats: SystemStats;
  onUpdateStats: (newStats: Partial<SystemStats>) => void;
  sheetsConnected: boolean;
  onToggleSheets: (connected: boolean) => void;
  gmailActive: boolean;
  onToggleGmail: (active: boolean) => void;
  onTriggerToast: (msg: string, icon?: string) => void;
  officerName?: string;
  officerEmail?: string;
  officerZone?: string;
  onUpdateOfficer?: (name: string, email: string, zone: string) => void;
}

export const SettingsView: React.FC<SettingsViewProps> = ({
  stats,
  onUpdateStats,
  sheetsConnected,
  onToggleSheets,
  gmailActive,
  onToggleGmail,
  onTriggerToast,
  officerName: initialOfficerName = 'Karthik Raja',
  officerEmail: initialOfficerEmail = 'karthik.raja@tn.gov.in',
  officerZone: initialOfficerZone = 'Chennai Central (Zone 01)',
  onUpdateOfficer
}) => {
  const [velocity, setVelocity] = useState(stats.velocityThrottle || 45);
  const [officerName, setOfficerName] = useState(initialOfficerName);
  const [officerEmail, setOfficerEmail] = useState(initialOfficerEmail);
  const [officerZone, setOfficerZone] = useState(initialOfficerZone);
  const [enforceUGCProtocol, setEnforceUGCProtocol] = useState(true);
  const [requireMXCheck, setRequireMXCheck] = useState(true);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdateStats({ velocityThrottle: velocity });
    if (onUpdateOfficer) {
      onUpdateOfficer(officerName, officerEmail, officerZone);
    }
    onTriggerToast(`Directorate settings updated. Welcome, ${officerName}!`, 'tune');
  };

  return (
    <div className="flex flex-col w-full pb-space-xl space-y-space-lg">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="font-code-sm text-code-sm uppercase tracking-widest text-primary font-bold">
            Administrative Control
          </span>
          <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
          <span className="font-code-sm text-code-sm text-secondary">
            Gateway &amp; Compliance Configuration
          </span>
        </div>
        <h1 className="font-headline-lg text-headline-lg text-on-surface font-bold tracking-tight">
          System &amp; Integration Settings
        </h1>
        <p className="font-body-md text-body-md text-secondary mt-0.5">
          Configure Google Sheets roster sync, Gmail API gateway credentials, velocity throttles, and statutory compliance.
        </p>
      </div>

      <form onSubmit={handleSave} className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        {/* Left Column (7 cols): Integrations & Dispatcher Velocity */}
        <div className="lg:col-span-7 flex flex-col gap-space-md">
          {/* Card 1: Velocity Throttle & Rate Limiting */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0] space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-primary">
                  <span className="material-symbols-outlined text-[24px]">speed</span>
                </div>
                <div>
                  <h3 className="font-headline-sm font-bold text-on-surface">Dispatcher Velocity Throttle</h3>
                  <p className="text-xs text-secondary">Institutional recipient rate limiting</p>
                </div>
              </div>
              <span className="font-code-sm text-lg font-bold text-primary bg-primary-fixed/50 px-3 py-1 rounded-lg">
                {velocity} msgs/min
              </span>
            </div>

            <p className="text-xs text-secondary">
              Protects state outreach IP reputation against spam filter greylisting across Tamil Nadu university domains (.edu.in and .ac.in).
            </p>

            <div>
              <div className="flex justify-between text-xs font-semibold text-secondary mb-1">
                <span>10 msgs/min (Conservative)</span>
                <span>45 msgs/min (Standard)</span>
                <span>120 msgs/min (Fast)</span>
              </div>
              <input
                type="range"
                min="10"
                max="120"
                step="5"
                value={velocity}
                onChange={(e) => setVelocity(Number(e.target.value))}
                className="w-full accent-primary cursor-pointer"
              />
            </div>
          </div>

          {/* Card 2: Google Sheets API Configuration */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0] space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center border border-emerald-200">
                  <span className="material-symbols-outlined text-[24px]">table_chart</span>
                </div>
                <div>
                  <h3 className="font-headline-sm font-bold text-on-surface">Google Sheets Sync</h3>
                  <p className="text-xs text-secondary">Roster auto-import gateway</p>
                </div>
              </div>

              <button
                type="button"
                onClick={() => {
                  onToggleSheets(!sheetsConnected);
                  onTriggerToast(
                    !sheetsConnected ? 'Google Sheets integration connected' : 'Google Sheets integration disconnected',
                    'hub'
                  );
                }}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  sheetsConnected
                    ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                    : 'bg-surface-container text-secondary hover:text-on-surface'
                }`}
              >
                {sheetsConnected ? 'Connected (Active)' : 'Click to Connect'}
              </button>
            </div>

            <div className="p-3 bg-surface-container-low rounded-lg text-xs space-y-2 border border-[#e2e8f0]/80">
              <div className="flex items-center justify-between">
                <span className="text-secondary">Spreadsheet ID:</span>
                <span className="font-code-sm font-semibold">1tN-TN_HigherEd_Roster_2024</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-secondary">Sync Target:</span>
                <span className="font-semibold text-on-surface">contacts.csv (125 Verified Campuses)</span>
              </div>
            </div>
          </div>

          {/* Card 3: Gmail API Gateway & Sandbox */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0] space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-primary">
                  <span className="material-symbols-outlined text-[24px]">mail</span>
                </div>
                <div>
                  <h3 className="font-headline-sm font-bold text-on-surface">Gmail API Gateway</h3>
                  <p className="text-xs text-secondary">SMTP sandbox simulation layer</p>
                </div>
              </div>

              <button
                type="button"
                onClick={() => {
                  onToggleGmail(!gmailActive);
                  onTriggerToast(
                    !gmailActive ? 'Gmail Sandbox Gateway enabled' : 'Gmail Sandbox returned to demo mode',
                    'mail'
                  );
                }}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  gmailActive
                    ? 'bg-sky-100 text-sky-800 border border-sky-300'
                    : 'bg-surface-container text-secondary hover:text-on-surface'
                }`}
              >
                {gmailActive ? 'Sandbox Live' : 'Demo Mode Active'}
              </button>
            </div>

            <div className="p-3 bg-surface-container-low rounded-lg text-xs space-y-2 border border-[#e2e8f0]/80">
              <div className="flex items-center justify-between">
                <span className="text-secondary">Daily Transmission Quota:</span>
                <span className="font-code-sm font-semibold text-on-surface">2,000 / day</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-secondary">Environment:</span>
                <span className="font-semibold text-on-surface">Government of Tamil Nadu Sandbox Domain</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column (5 cols): Officer Dossier & Compliance */}
        <div className="lg:col-span-5 flex flex-col gap-space-md">
          {/* Officer Dossier */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0] space-y-3">
            <h3 className="font-headline-sm font-bold text-on-surface">Outreach Officer Profile</h3>

            <div>
              <label className="block text-xs font-semibold text-secondary mb-1">Officer Name</label>
              <input
                type="text"
                value={officerName}
                onChange={(e) => setOfficerName(e.target.value)}
                className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-secondary mb-1">Official Email Address</label>
              <input
                type="email"
                value={officerEmail}
                onChange={(e) => setOfficerEmail(e.target.value)}
                className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-secondary mb-1">Assigned Directorate Zone</label>
              <select
                value={officerZone}
                onChange={(e) => setOfficerZone(e.target.value)}
                className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-xs text-on-surface border border-[#e2e8f0] focus:outline-none"
              >
                <option value="Chennai Central (Zone 01)">Chennai Central (Zone 01)</option>
                <option value="Western Belt: Coimbatore (Zone 04)">Western Belt: Coimbatore (Zone 04)</option>
                <option value="Southern Region: Madurai (Zone 07)">Southern Region: Madurai (Zone 07)</option>
                <option value="Cauvery Delta: Trichy (Zone 05)">Cauvery Delta: Trichy (Zone 05)</option>
              </select>
            </div>
          </div>

          {/* Compliance & Safeguards */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0] space-y-3">
            <h3 className="font-headline-sm font-bold text-on-surface">Statutory Compliance Safeguards</h3>

            <div className="flex items-start gap-3 p-2 rounded-lg bg-surface-container-low border border-[#e2e8f0]">
              <input
                type="checkbox"
                id="ugc-rule"
                checked={enforceUGCProtocol}
                onChange={(e) => setEnforceUGCProtocol(e.target.checked)}
                className="accent-primary mt-1"
              />
              <label htmlFor="ugc-rule" className="text-xs cursor-pointer">
                <span className="font-bold text-on-surface block">UGC / AICTE Outreach Protocol 2024</span>
                <span className="text-secondary text-[11px]">
                  Enforces mandatory unsubscribe links and institutional verification disclaimer in all outreach headers.
                </span>
              </label>
            </div>

            <div className="flex items-start gap-3 p-2 rounded-lg bg-surface-container-low border border-[#e2e8f0]">
              <input
                type="checkbox"
                id="mx-rule"
                checked={requireMXCheck}
                onChange={(e) => setRequireMXCheck(e.target.checked)}
                className="accent-primary mt-1"
              />
              <label htmlFor="mx-rule" className="text-xs cursor-pointer">
                <span className="font-bold text-on-surface block">Pre-dispatch DNS MX Verification</span>
                <span className="text-secondary text-[11px]">
                  Automatically drops unverified domains to maintain sub-3% bounce rate ceiling.
                </span>
              </label>
            </div>

            <button
              type="submit"
              className="w-full mt-2 py-2 bg-primary text-white rounded-lg font-label-md font-semibold hover:bg-primary-container shadow-sm flex items-center justify-center gap-1.5 transition-colors cursor-pointer"
            >
              <span className="material-symbols-outlined text-[18px]">save</span>
              <span>Save Configuration</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};
