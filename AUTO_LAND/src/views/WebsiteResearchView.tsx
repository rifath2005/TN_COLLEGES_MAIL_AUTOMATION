import React, { useState } from 'react';
import { CollegeContact } from '../types';

interface WebsiteResearchViewProps {
  colleges: CollegeContact[];
  onEnrichCollege: (enriched: CollegeContact) => void;
  onTriggerToast: (msg: string, icon?: string) => void;
}

export const WebsiteResearchView: React.FC<WebsiteResearchViewProps> = ({
  colleges,
  onEnrichCollege,
  onTriggerToast
}) => {
  const [selectedCollegeId, setSelectedCollegeId] = useState<string>(colleges[1]?.id || colleges[0]?.id || '');
  const [customUrl, setCustomUrl] = useState('');
  const [isCrawling, setIsCrawling] = useState(false);
  const [crawledData, setCrawledData] = useState<{
    principalName: string;
    principalEmail: string;
    placementOfficer: string;
    placementEmail: string;
    phone: string;
    naacGrade: string;
    nirfRank: string;
    scannedPages: string[];
    confidenceScore: number;
  } | null>(null);

  const activeCollege = colleges.find(c => c.id === selectedCollegeId) || colleges[0];

  const handleStartCrawl = () => {
    setIsCrawling(true);
    setCrawledData(null);

    setTimeout(() => {
      setIsCrawling(false);
      // Realistic discovered data based on active college
      setCrawledData({
        principalName: activeCollege.principalName,
        principalEmail: activeCollege.principalEmail.includes('old') 
          ? 'principal.office@nec.edu.in' 
          : activeCollege.principalEmail,
        placementOfficer: activeCollege.placementOfficerName || 'Dr. K. Senthil Kumar (Head CDC)',
        placementEmail: activeCollege.placementOfficerEmail || 'careers@college.edu.in',
        phone: activeCollege.phone || '+91 44 2817 8200',
        naacGrade: activeCollege.naacGrade || 'A++',
        nirfRank: '#32 Engineering category (NIRF 2024)',
        scannedPages: [
          '/administration/leadership.html',
          '/contact-us/directory.php',
          '/training-and-placement/office.html',
          '/iqac/annual-quality-assurance-report.pdf'
        ],
        confidenceScore: 97
      });
      onTriggerToast(`Web crawl completed for ${activeCollege.name}: High confidence leadership emails found.`, 'travel_explore');
    }, 1400);
  };

  const handleApplyEnrichment = () => {
    if (!crawledData || !activeCollege) return;
    const updated: CollegeContact = {
      ...activeCollege,
      principalEmail: crawledData.principalEmail,
      placementOfficerName: crawledData.placementOfficer,
      placementOfficerEmail: crawledData.placementEmail,
      status: 'verified',
      lastContacted: 'Enriched via Web Scraper'
    };
    onEnrichCollege(updated);
    onTriggerToast(`Enriched "${updated.name}" record in central registry! Status updated to Verified.`, 'verified');
  };

  return (
    <div className="flex flex-col w-full pb-space-xl space-y-space-lg">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="font-code-sm text-code-sm uppercase tracking-widest text-primary font-bold">
            Autonomous Crawler
          </span>
          <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
          <span className="font-code-sm text-code-sm text-secondary">
            Collegiate Web Discovery &amp; Contact Extractor
          </span>
        </div>
        <h1 className="font-headline-lg text-headline-lg text-on-surface font-bold tracking-tight">
          Website Research &amp; Contact Scraper
        </h1>
        <p className="font-body-md text-body-md text-secondary mt-0.5">
          Scan official university and college web portals to extract verified dean, principal, and placement leadership mailboxes.
        </p>
      </div>

      {/* Target Selector Bar */}
      <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm border border-[#e2e8f0] flex flex-col md:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-3 w-full md:w-auto flex-1">
          <div className="w-9 h-9 rounded-lg bg-surface-container flex items-center justify-center text-primary shrink-0">
            <span className="material-symbols-outlined text-[20px]">language</span>
          </div>
          <div className="flex-1 max-w-md">
            <label className="block text-[11px] font-label-sm uppercase font-semibold text-secondary">
              Select Institution from Registry
            </label>
            <select
              value={selectedCollegeId}
              onChange={(e) => {
                setSelectedCollegeId(e.target.value);
                setCrawledData(null);
              }}
              className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-xs font-semibold text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary mt-0.5"
            >
              {colleges.map((col) => (
                <option key={col.id} value={col.id}>
                  {col.name} ({col.district} — AISHE {col.aisheCode}) [{col.status.toUpperCase()}]
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center gap-2 w-full md:w-auto">
          <button
            onClick={handleStartCrawl}
            disabled={isCrawling}
            className="w-full md:w-auto h-9 px-4 rounded-lg bg-primary-container text-on-primary hover:opacity-95 font-label-md font-semibold flex items-center justify-center gap-2 shadow-sm active:scale-[0.98] transition-all disabled:opacity-50 cursor-pointer"
          >
            <span className={`material-symbols-outlined text-[18px] ${isCrawling ? 'animate-spin' : ''}`}>
              {isCrawling ? 'autorenew' : 'travel_explore'}
            </span>
            <span>{isCrawling ? 'Crawling Portal...' : 'Crawl & Extract Contacts'}</span>
          </button>
        </div>
      </div>

      {/* Crawl Results & Inspection */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        {/* Left Column: Target Info & Live Crawl Telemetry (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-space-md">
          {/* Target Profile Card */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-start justify-between mb-3">
              <div>
                <span className="font-code-sm text-xs text-primary font-bold bg-primary-fixed/50 px-2 py-0.5 rounded">
                  AISHE {activeCollege.aisheCode}
                </span>
                <h2 className="font-headline-sm font-bold text-on-surface mt-1">
                  {activeCollege.name}
                </h2>
                <a
                  href={activeCollege.website}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs text-primary hover:underline flex items-center gap-1 mt-0.5"
                >
                  <span>{activeCollege.website}</span>
                  <span className="material-symbols-outlined text-[13px]">open_in_new</span>
                </a>
              </div>

              <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                activeCollege.status === 'verified'
                  ? 'bg-surface-container-highest text-tertiary'
                  : activeCollege.status === 'bounced'
                  ? 'bg-error-container text-on-error-container'
                  : 'bg-amber-100 text-amber-900'
              }`}>
                {activeCollege.status.toUpperCase()}
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 p-3 bg-surface-container-low rounded-lg text-xs border border-[#e2e8f0]/80 mb-3">
              <div>
                <span className="text-secondary block">District / Zone:</span>
                <span className="font-semibold text-on-surface">{activeCollege.district} ({activeCollege.zone})</span>
              </div>
              <div>
                <span className="text-secondary block">Category:</span>
                <span className="font-semibold text-on-surface">{activeCollege.category}</span>
              </div>
              <div>
                <span className="text-secondary block">Affiliation:</span>
                <span className="font-semibold text-on-surface truncate block">{activeCollege.affiliation}</span>
              </div>
            </div>

            {/* Crawl Status Console */}
            {isCrawling && (
              <div className="p-4 bg-slate-900 text-slate-100 rounded-lg font-code-sm text-xs space-y-2 border border-slate-800">
                <div className="flex items-center gap-2 text-primary-fixed">
                  <span className="w-2 h-2 rounded-full bg-primary animate-ping"></span>
                  <span>Connecting to {activeCollege.website}...</span>
                </div>
                <p className="text-slate-400">&gt; Fetching robots.txt: Crawl-delay 1s allowed</p>
                <p className="text-slate-400">&gt; Parsing DOM structure for semantic leadership schema...</p>
                <p className="text-emerald-400">&gt; Discovered mailto: regex matching institutional pattern</p>
              </div>
            )}

            {/* Extracted Data Card */}
            {crawledData && (
              <div className="p-4 bg-emerald-50/60 rounded-xl border border-emerald-200 space-y-3 animate-in fade-in duration-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-emerald-700 text-[20px]">verified_user</span>
                    <span className="font-label-md text-emerald-900 font-bold">
                      Extracted Contacts &amp; Accreditation ({crawledData.confidenceScore}% Confidence)
                    </span>
                  </div>
                  <span className="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">
                    4 pages indexed
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="p-2.5 bg-white rounded-lg border border-emerald-200">
                    <span className="text-secondary block">Principal / Head Office:</span>
                    <span className="font-bold text-on-surface block text-sm">{crawledData.principalName}</span>
                    <span className="font-code-sm text-primary block mt-0.5">{crawledData.principalEmail}</span>
                  </div>

                  <div className="p-2.5 bg-white rounded-lg border border-emerald-200">
                    <span className="text-secondary block">Placement &amp; Industry Officer:</span>
                    <span className="font-bold text-on-surface block text-sm">{crawledData.placementOfficer}</span>
                    <span className="font-code-sm text-tertiary block mt-0.5">{crawledData.placementEmail}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-2">
                  <span className="text-xs text-secondary">
                    Crawled Pages: {crawledData.scannedPages.join(', ')}
                  </span>
                  <button
                    onClick={handleApplyEnrichment}
                    className="px-4 py-1.5 bg-primary text-white rounded-lg text-xs font-semibold hover:bg-primary-container shadow-sm flex items-center gap-1"
                  >
                    <span className="material-symbols-outlined text-[16px]">sync_alt</span>
                    <span>Enrich into Registry</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Research Instructions & Capabilities (5 cols) */}
        <div className="lg:col-span-5 flex flex-col gap-space-md">
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0]">
            <h3 className="font-headline-sm font-bold text-on-surface mb-2">
              Autonomous Crawler Specs
            </h3>
            <p className="font-body-sm text-secondary mb-4">
              Designed specifically for Tamil Nadu state higher education web architectures (.edu.in / .ac.in).
            </p>

            <div className="space-y-3 text-xs">
              <div className="p-3 bg-surface-container-low rounded-lg border border-[#e2e8f0]">
                <span className="font-bold text-on-surface block mb-0.5">1. Leadership Email Discovery</span>
                <p className="text-secondary">
                  Scans `/administration`, `/governing-council`, and `/principal` sections to replace expired or bounced mailboxes.
                </p>
              </div>

              <div className="p-3 bg-surface-container-low rounded-lg border border-[#e2e8f0]">
                <span className="font-bold text-on-surface block mb-0.5">2. Training &amp; Placement Cell</span>
                <p className="text-secondary">
                  Extracts dedicated placement officer names and direct mobile numbers for recruitment and skilling drives.
                </p>
              </div>

              <div className="p-3 bg-surface-container-low rounded-lg border border-[#e2e8f0]">
                <span className="font-bold text-on-surface block mb-0.5">3. AICTE / NIRF Verification</span>
                <p className="text-secondary">
                  Cross-checks mandatory public disclosures (Mandatory Disclosure PDF) against AISHE database.
                </p>
              </div>
            </div>

            <button
              onClick={() => {
                onTriggerToast('Batch research queued for all 184 Pending Queue records.', 'hourglass_top');
              }}
              className="w-full mt-4 py-2 bg-surface-container text-on-surface hover:bg-surface-container-high rounded-lg text-xs font-semibold flex items-center justify-center gap-1 transition-colors"
            >
              <span className="material-symbols-outlined text-[16px]">auto_mode</span>
              <span>Enrich All 184 Pending Records</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
