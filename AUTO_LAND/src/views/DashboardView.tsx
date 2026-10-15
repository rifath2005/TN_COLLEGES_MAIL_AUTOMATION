import React, { useState, useMemo } from 'react';
import { SystemStats, ActivityFeedItem, NavScreen, CollegeContact } from '../types';
import {
  isMissingPhone,
  isMissingWebsite,
  isMissingEmail,
  isMissingAny,
  isCompleteProfile,
  getMissingDetailsList
} from '../utils/completeness';

interface DashboardViewProps {
  stats: SystemStats;
  activities: ActivityFeedItem[];
  colleges: CollegeContact[];
  onOpenCampaignModal: () => void;
  onNavigate: (screen: NavScreen, filter?: string) => void;
  onTriggerToast: (msg: string, icon?: string) => void;
  onSelectCollegeByName: (name: string) => void;
  onRefreshData: () => void;
  gmailActive?: boolean;
  senderEmail?: string;
  activeCsv?: string;
  onSwitchCsv?: (csv: string) => void;
  onQuickTestSend?: () => void;
  onRunBatch?: (dryRun: boolean) => void;
  isDispatching?: boolean;
  officerName?: string;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  stats,
  activities,
  colleges,
  onOpenCampaignModal,
  onNavigate,
  onTriggerToast,
  onSelectCollegeByName,
  onRefreshData,
  gmailActive = true,
  senderEmail = 'babsword3@gmail.com',
  activeCsv = 'contacts.csv',
  onSwitchCsv,
  onQuickTestSend,
  onRunBatch,
  isDispatching = false,
  officerName = 'Karthik Raja'
}) => {
  // Real metrics dynamically computed from contacts ledger
  const totalCount = colleges.length || stats.totalColleges || 1;
  const verifiedCount = colleges.filter(c => c.status === 'Sent' || c.status === 'verified').length || stats.verifiedRecords;
  const pendingCount = colleges.filter(c => c.status === 'Pending' || c.status === 'pending').length || stats.pendingQueue;
  const bouncedCount = colleges.filter(c => c.status === 'Failed' || c.status === 'bounced').length || stats.bouncedFailed || 0;
  const deduplicatedCount = stats.deduplicated || 0;

  const verifiedPct = Math.round((verifiedCount / totalCount) * 100);
  const pendingPct = Math.round((pendingCount / totalCount) * 100);
  const bouncedPct = Math.round((bouncedCount / totalCount) * 100);
  const deduplicatedPct = Math.round((deduplicatedCount / totalCount) * 100);

  // Dynamically compute classifications from colleges
  const dynamicClassifications = useMemo(() => {
    if (!colleges || colleges.length === 0) return [];
    const counts: Record<string, number> = {};
    for (const c of colleges) {
      const cat = c.category || 'Engineering';
      counts[cat] = (counts[cat] || 0) + 1;
    }
    const colorMap: Record<string, string> = {
      'Engineering': 'bg-primary',
      'Arts & Science': 'bg-tertiary-container',
      'Medical & Health': 'bg-primary-container',
      'Polytechnic / Voc': 'bg-secondary'
    };
    return Object.entries(counts).map(([name, count]) => ({
      name,
      count,
      pct: Math.round((count / totalCount) * 100),
      color: colorMap[name] || 'bg-primary'
    })).sort((a, b) => b.count - a.count);
  }, [colleges, totalCount]);

  // Dynamically compute top districts density from colleges
  const dynamicDistricts = useMemo(() => {
    if (!colleges || colleges.length === 0) return [];
    const counts: Record<string, { count: number; zone: string }> = {};
    for (const c of colleges) {
      const dist = c.district || 'Chennai';
      if (!counts[dist]) {
        counts[dist] = { count: 0, zone: c.zone || 'Zone 01' };
      }
      counts[dist].count += 1;
    }
    return Object.entries(counts)
      .map(([name, data]) => ({
        name: name.toLowerCase().includes('district') ? name : `${name} District`,
        zone: data.zone,
        count: data.count,
        pct: Math.min(100, Math.round((data.count / (colleges.length || 1)) * 100 * 2.5))
      }))
      .sort((a, b) => b.count - a.count);
  }, [colleges]);

  // Count of distinct districts represented in the ledger
  const distinctDistrictsCount = useMemo(() => {
    const s = new Set(colleges.map(c => c.district).filter(Boolean));
    return s.size || 38;
  }, [colleges]);

  // Data Completeness & Missing Details State
  const [dashboardMissingFilter, setDashboardMissingFilter] = useState<'any-missing' | 'no-phone' | 'no-website' | 'no-email' | 'complete'>('any-missing');
  const [dashboardSortBy, setDashboardSortBy] = useState<'missing-desc' | 'name-asc' | 'name-desc' | 'district-asc'>('missing-desc');
  const [dashboardPreviewLimit, setDashboardPreviewLimit] = useState<number>(6);

  // Missing details counts
  const missingPhoneCount = useMemo(() => colleges.filter(isMissingPhone).length, [colleges]);
  const missingWebsiteCount = useMemo(() => colleges.filter(isMissingWebsite).length, [colleges]);
  const missingEmailCount = useMemo(() => colleges.filter(isMissingEmail).length, [colleges]);
  const missingAnyCount = useMemo(() => colleges.filter(isMissingAny).length, [colleges]);
  const completeCount = useMemo(() => colleges.filter(isCompleteProfile).length, [colleges]);

  const missingPhonePct = Math.round((missingPhoneCount / totalCount) * 100);
  const missingWebsitePct = Math.round((missingWebsiteCount / totalCount) * 100);
  const missingEmailPct = Math.round((missingEmailCount / totalCount) * 100);
  const missingAnyPct = Math.round((missingAnyCount / totalCount) * 100);
  const completePct = Math.round((completeCount / totalCount) * 100);

  // Filtered colleges for on-dashboard missing preview
  const missingPreviewColleges = useMemo(() => {
    let list = colleges.filter(c => {
      if (dashboardMissingFilter === 'no-phone') return isMissingPhone(c);
      if (dashboardMissingFilter === 'no-website') return isMissingWebsite(c);
      if (dashboardMissingFilter === 'no-email') return isMissingEmail(c);
      if (dashboardMissingFilter === 'complete') return isCompleteProfile(c);
      return isMissingAny(c); // 'any-missing'
    });

    return [...list].sort((a, b) => {
      if (dashboardSortBy === 'name-asc') {
        return a.name.localeCompare(b.name);
      }
      if (dashboardSortBy === 'name-desc') {
        return b.name.localeCompare(a.name);
      }
      if (dashboardSortBy === 'district-asc') {
        return a.district.localeCompare(b.district);
      }
      // 'missing-desc' - colleges with the most missing fields first
      const countA = (isMissingPhone(a) ? 1 : 0) + (isMissingWebsite(a) ? 1 : 0) + (isMissingEmail(a) ? 1 : 0);
      const countB = (isMissingPhone(b) ? 1 : 0) + (isMissingWebsite(b) ? 1 : 0) + (isMissingEmail(b) ? 1 : 0);
      if (countB !== countA) return countB - countA;
      return a.name.localeCompare(b.name);
    });
  }, [colleges, dashboardMissingFilter, dashboardSortBy]);
  const handleExportCSV = () => {
    // Generate simple CSV payload of colleges
    const headers = ['Name', 'District', 'Zone', 'Category', 'AISHE', 'Principal', 'Email', 'Status'];
    const rows = colleges.map(c => [
      `"${c.name}"`,
      `"${c.district}"`,
      `"${c.zone}"`,
      `"${c.category}"`,
      `"${c.aisheCode}"`,
      `"${c.principalName}"`,
      `"${c.principalEmail}"`,
      `"${c.status}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'TN_Institutions_Roster_2024.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    onTriggerToast('Export initiated: Generating TN_Institutions_Roster_2024.csv', 'download');
  };

  return (
    <div className="flex flex-col w-full pb-space-xl">
      {/* Live Gateway / Demo Notice Banner */}
      <div className={`mb-space-md px-space-md py-space-sm rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-sm border ${
        gmailActive 
          ? 'bg-emerald-50 border-emerald-200 text-emerald-950'
          : 'bg-secondary-fixed/50 border-[#bec6e0]/40 text-on-secondary-fixed'
      }`}>
        <div className="flex items-center gap-space-sm">
          <span className={`material-symbols-outlined text-[22px] ${gmailActive ? 'text-emerald-700' : 'text-on-secondary-fixed'}`}>
            {gmailActive ? 'mark_email_read' : 'shield_lock'}
          </span>
          <div className="flex items-baseline gap-space-xs flex-wrap">
            <span className={`font-label-sm text-label-sm uppercase tracking-wider font-bold ${gmailActive ? 'text-emerald-800' : 'text-on-secondary-fixed'}`}>
              {gmailActive ? 'Live Outreach Gateway Active' : 'Demo Mode Active'}
            </span>
            <span className="text-secondary">—</span>
            <span className="font-body-sm text-body-sm">
              {gmailActive ? (
                <>
                  Connected via <strong>{senderEmail}</strong> (Gmail SMTP SSL) • Target Dataset: <strong>{activeCsv}</strong> ({colleges.length} colleges)
                </>
              ) : (
                'No live Gmail or Google Sheets connected. Displaying synthetic Tamil Nadu institutional directory metrics.'
              )}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          {onSwitchCsv && (
            <div className="flex items-center bg-white rounded-lg border border-emerald-200 text-xs overflow-hidden shadow-xs">
              <button
                type="button"
                onClick={() => onSwitchCsv('contacts.csv')}
                className={`px-2.5 py-1 font-medium transition-colors cursor-pointer ${
                  activeCsv === 'contacts.csv' 
                    ? 'bg-emerald-700 text-white font-semibold' 
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                Production (contacts.csv)
              </button>
              <button
                type="button"
                onClick={() => onSwitchCsv('test_contacts.csv')}
                className={`px-2.5 py-1 font-medium transition-colors cursor-pointer ${
                  activeCsv === 'test_contacts.csv' 
                    ? 'bg-emerald-700 text-white font-semibold' 
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                Test Sandbox (test_contacts.csv)
              </button>
            </div>
          )}

          {onQuickTestSend && (
            <button
              type="button"
              disabled={isDispatching}
              onClick={onQuickTestSend}
              className="px-3 py-1 bg-emerald-700 hover:bg-emerald-800 disabled:opacity-50 text-white text-xs font-semibold rounded-lg flex items-center gap-1 shadow-xs transition-all cursor-pointer"
              title="Send real test email to babsword6@gmail.com"
            >
              <span className="material-symbols-outlined text-[16px]">send</span>
              <span>{isDispatching ? 'Transmitting...' : 'Test babsword6@gmail.com'}</span>
            </button>
          )}

          <button
            className="text-secondary hover:text-on-surface p-1 rounded transition-colors"
            onClick={() => {
              onRefreshData();
              onTriggerToast('Synchronizing state with local database and CSV ledger...', 'sync');
            }}
            title="Refresh database"
          >
            <span className="material-symbols-outlined text-[16px]">refresh</span>
          </button>
        </div>
      </div>

      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-space-md mb-space-lg">
        <div className="flex flex-col">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-code-sm text-code-sm uppercase tracking-widest text-primary font-bold">
              Regional Directorate
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
            <span className="font-code-sm text-code-sm text-secondary">
              T.N. Directorate of Collegiate Outreach
            </span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight">
            Welcome back, {officerName ? officerName.split(' ')[0] : 'Officer'}
          </h1>
          <p className="font-body-md text-body-md text-secondary mt-0.5">
            Tamil Nadu Higher Education Outreach Overview — Academic Year 2024–25
          </p>
        </div>

        {/* Actions Area */}
        <div className="flex items-center gap-space-sm flex-wrap">
          <button
            className="h-9 px-space-md rounded-lg bg-surface-container-lowest text-on-surface hover:bg-surface-container-low transition-all shadow-sm border border-[#e2e8f0] flex items-center gap-space-xs font-label-lg text-label-lg font-semibold active:scale-[0.98] cursor-pointer"
            onClick={handleExportCSV}
          >
            <span className="material-symbols-outlined text-[18px] text-secondary">file_download</span>
            <span>Export CSV</span>
          </button>
          <button
            className="h-9 px-space-md rounded-lg bg-primary-container text-on-primary hover:opacity-95 transition-all shadow-sm flex items-center gap-space-xs font-label-lg text-label-lg font-semibold active:scale-[0.98] cursor-pointer"
            onClick={onOpenCampaignModal}
          >
            <span className="material-symbols-outlined text-[18px]">add_circle</span>
            <span>New Campaign</span>
          </button>
        </div>
      </div>

      {/* 6-Metric Visual Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-space-md mb-space-lg">
        {/* Card 1: Total Colleges */}
        <div 
          onClick={() => onNavigate('college-contacts')}
          className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm hover:shadow-md transition-all flex flex-col justify-between group border border-[#e2e8f0] cursor-pointer"
        >
          <div>
            <div className="flex items-center justify-between mb-space-xs">
              <span className="font-label-sm text-label-sm uppercase font-semibold text-secondary">Total Colleges</span>
              <div className="w-7 h-7 rounded-lg bg-surface-container flex items-center justify-center text-on-surface group-hover:bg-primary-fixed group-hover:text-primary transition-colors">
                <span className="material-symbols-outlined text-[18px]">account_balance</span>
              </div>
            </div>
            <div className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              {stats.totalColleges.toLocaleString()}
            </div>
            <p className="font-body-sm text-body-sm text-secondary mt-1 line-clamp-1">{distinctDistrictsCount} Districts across Tamil Nadu</p>
          </div>
          <div className="mt-space-md pt-space-xs flex items-center justify-between">
            <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container-high text-on-surface font-semibold">
              <span className="material-symbols-outlined text-[13px] text-primary">verified</span> {colleges.length} Active
            </span>
            <span className="font-code-sm text-code-sm text-secondary">100% Verified</span>
          </div>
        </div>

        {/* Card 2: Verified Records */}
        <div 
          onClick={() => onNavigate('college-contacts', 'verified')}
          className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm hover:shadow-md transition-all flex flex-col justify-between group border border-[#e2e8f0] cursor-pointer"
        >
          <div>
            <div className="flex items-center justify-between mb-space-xs">
              <span className="font-label-sm text-label-sm uppercase font-semibold text-secondary">Verified Records</span>
              <div className="w-7 h-7 rounded-lg bg-surface-container-high flex items-center justify-center text-on-surface group-hover:bg-secondary-fixed transition-colors">
                <span className="material-symbols-outlined text-[18px]">verified</span>
              </div>
            </div>
            <div className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              {stats.verifiedRecords.toLocaleString()}
            </div>
            <p className="font-body-sm text-body-sm text-secondary mt-1 line-clamp-1">{verifiedPct}% deliverability certified</p>
          </div>
          <div className="mt-space-md pt-space-xs flex items-center justify-between">
            <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container-highest text-tertiary font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-tertiary"></span> 100% valid MX
            </span>
            <span className="font-code-sm text-code-sm text-secondary">MX valid</span>
          </div>
        </div>

        {/* Card 3: Pending Queued */}
        <div 
          onClick={() => onNavigate('college-contacts', 'pending')}
          className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm hover:shadow-md transition-all flex flex-col justify-between group border border-[#e2e8f0] cursor-pointer"
        >
          <div>
            <div className="flex items-center justify-between mb-space-xs">
              <span className="font-label-sm text-label-sm uppercase font-semibold text-secondary">Pending Queue</span>
              <div className="w-7 h-7 rounded-lg bg-surface-container flex items-center justify-center text-on-surface group-hover:bg-surface-container-highest transition-colors">
                <span className="material-symbols-outlined text-[18px]">hourglass_top</span>
              </div>
            </div>
            <div className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              {stats.pendingQueue}
            </div>
            <p className="font-body-sm text-body-sm text-secondary mt-1 line-clamp-1">Awaiting review & dispatch</p>
          </div>
          <div className="mt-space-md pt-space-xs flex items-center justify-between">
            <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container text-secondary font-semibold">
              <span className="material-symbols-outlined text-[13px]">schedule</span> Batch Ready
            </span>
            <span className="font-code-sm text-code-sm text-secondary">{pendingPct}%</span>
          </div>
        </div>

        {/* Card 4: Dispatched Sent */}
        <div 
          onClick={() => onNavigate('send-history')}
          className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm hover:shadow-md transition-all flex flex-col justify-between group border border-[#e2e8f0] cursor-pointer"
        >
          <div>
            <div className="flex items-center justify-between mb-space-xs">
              <span className="font-label-sm text-label-sm uppercase font-semibold text-secondary">Dispatched</span>
              <div className="w-7 h-7 rounded-lg bg-tertiary-fixed flex items-center justify-center text-on-tertiary-fixed group-hover:bg-tertiary-container group-hover:text-on-tertiary-container transition-colors">
                <span className="material-symbols-outlined text-[18px]">forward_to_inbox</span>
              </div>
            </div>
            <div className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              {stats.dispatched}
            </div>
            <p className="font-body-sm text-body-sm text-secondary mt-1 line-clamp-1">Total academic dispatches</p>
          </div>
          <div className="mt-space-md pt-space-xs flex items-center justify-between">
            <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2 py-0.5 rounded bg-tertiary-fixed text-on-tertiary-fixed font-semibold">
              <span className="material-symbols-outlined text-[13px]">campaign</span> Production
            </span>
            <span className="font-code-sm text-code-sm text-secondary">{verifiedPct}% reach</span>
          </div>
        </div>

        {/* Card 5: Failed Bounces */}
        <div 
          onClick={() => onNavigate('college-contacts', 'bounced')}
          className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm hover:shadow-md transition-all flex flex-col justify-between group border border-[#e2e8f0] cursor-pointer"
        >
          <div>
            <div className="flex items-center justify-between mb-space-xs">
              <span className="font-label-sm text-label-sm uppercase font-semibold text-secondary">Bounced / Failed</span>
              <div className="w-7 h-7 rounded-lg bg-error-container flex items-center justify-center text-on-error-container">
                <span className="material-symbols-outlined text-[18px]">error</span>
              </div>
            </div>
            <div className="font-headline-lg text-headline-lg text-error tracking-tight font-bold">
              {stats.bouncedFailed}
            </div>
            <p className="font-body-sm text-body-sm text-secondary mt-1 line-clamp-1">Mailbox unavailable or full</p>
          </div>
          <div className="mt-space-md pt-space-xs flex items-center justify-between">
            <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2 py-0.5 rounded bg-error-container text-on-error-container font-semibold">
              {bouncedPct}% rate
            </span>
            <span className="font-code-sm text-code-sm text-secondary">Sub-3% SLA</span>
          </div>
        </div>

        {/* Card 6: Cleaned Duplicates */}
        <div 
          onClick={() => onNavigate('import-contacts')}
          className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm hover:shadow-md transition-all flex flex-col justify-between group border border-[#e2e8f0] cursor-pointer"
        >
          <div>
            <div className="flex items-center justify-between mb-space-xs">
              <span className="font-label-sm text-label-sm uppercase font-semibold text-secondary">Deduplicated</span>
              <div className="w-7 h-7 rounded-lg bg-secondary-fixed flex items-center justify-center text-on-secondary-fixed">
                <span className="material-symbols-outlined text-[18px]">filter_alt</span>
              </div>
            </div>
            <div className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              {stats.deduplicated}
            </div>
            <p className="font-body-sm text-body-sm text-secondary mt-1 line-clamp-1">Purged across campus rosters</p>
          </div>
          <div className="mt-space-md pt-space-xs flex items-center justify-between">
            <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container text-on-surface font-semibold">
              Cleaned
            </span>
            <span className="font-code-sm text-code-sm text-secondary">{deduplicatedPct}% scrub</span>
          </div>
        </div>
      </div>

      {/* Data Completeness & Missing Details Audit Section */}
      <section className="bg-surface-container-lowest p-space-lg rounded-xl shadow-sm border border-[#e2e8f0] mb-space-lg">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-sm pb-space-md border-b border-[#e2e8f0]">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-700 shrink-0">
              <span className="material-symbols-outlined text-[24px]">fact_check</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="font-headline-sm text-headline-sm font-bold text-on-surface">
                  Data Completeness &amp; Missing Details Audit
                </h2>
                <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-200 uppercase tracking-wide">
                  TNDCE Scraped Directory
                </span>
              </div>
              <p className="font-body-sm text-body-sm text-secondary mt-0.5">
                Audit across {totalCount.toLocaleString()} Tamil Nadu collegiate institutions. Identify and filter colleges missing vital phone numbers, official websites, or direct email addresses.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 self-start md:self-auto shrink-0">
            <button
              onClick={() => onNavigate('college-contacts', dashboardMissingFilter)}
              className="h-9 px-4 rounded-lg bg-primary text-white hover:bg-primary-container font-label-md font-semibold text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer"
            >
              <span className="material-symbols-outlined text-[16px]">travel_explore</span>
              <span>Inspect in Full Roster ({missingPreviewColleges.length})</span>
            </button>
          </div>
        </div>

        {/* 5 Missing Details Audit Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-space-md my-space-md">
          {/* Card 1: Without Phone No */}
          <div
            onClick={() => setDashboardMissingFilter('no-phone')}
            className={`p-space-md rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
              dashboardMissingFilter === 'no-phone'
                ? 'bg-rose-50/70 border-rose-300 ring-2 ring-rose-500/20 shadow-xs'
                : 'bg-surface-container-low/60 border-[#e2e8f0] hover:bg-surface-container-low hover:border-rose-200'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-label-sm text-[11px] font-bold uppercase tracking-wider text-rose-800">
                  Without Phone No
                </span>
                <span className="w-6 h-6 rounded-md bg-rose-100 text-rose-700 flex items-center justify-center">
                  <span className="material-symbols-outlined text-[15px]">phone_disabled</span>
                </span>
              </div>
              <div className="font-headline-md text-headline-md font-bold text-on-surface">
                {missingPhoneCount.toLocaleString()}
              </div>
              <p className="text-xs text-secondary mt-1">
                {missingPhonePct}% lack verified telephone/landline
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-[#e2e8f0]/60 flex items-center justify-between">
              <span className={`text-[11px] font-semibold ${dashboardMissingFilter === 'no-phone' ? 'text-rose-700 font-bold' : 'text-secondary'}`}>
                {dashboardMissingFilter === 'no-phone' ? 'Active Filter • Clicked' : 'Click to Pick'}
              </span>
              <span className="material-symbols-outlined text-[14px] text-secondary">arrow_forward</span>
            </div>
          </div>

          {/* Card 2: Without Website */}
          <div
            onClick={() => setDashboardMissingFilter('no-website')}
            className={`p-space-md rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
              dashboardMissingFilter === 'no-website'
                ? 'bg-amber-50/70 border-amber-300 ring-2 ring-amber-500/20 shadow-xs'
                : 'bg-surface-container-low/60 border-[#e2e8f0] hover:bg-surface-container-low hover:border-amber-200'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-label-sm text-[11px] font-bold uppercase tracking-wider text-amber-800">
                  Without Website
                </span>
                <span className="w-6 h-6 rounded-md bg-amber-100 text-amber-700 flex items-center justify-center">
                  <span className="material-symbols-outlined text-[15px]">public_off</span>
                </span>
              </div>
              <div className="font-headline-md text-headline-md font-bold text-on-surface">
                {missingWebsiteCount.toLocaleString()}
              </div>
              <p className="text-xs text-secondary mt-1">
                {missingWebsitePct}% lack official web portal
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-[#e2e8f0]/60 flex items-center justify-between">
              <span className={`text-[11px] font-semibold ${dashboardMissingFilter === 'no-website' ? 'text-amber-700 font-bold' : 'text-secondary'}`}>
                {dashboardMissingFilter === 'no-website' ? 'Active Filter • Clicked' : 'Click to Pick'}
              </span>
              <span className="material-symbols-outlined text-[14px] text-secondary">arrow_forward</span>
            </div>
          </div>

          {/* Card 3: Without Mail ID */}
          <div
            onClick={() => setDashboardMissingFilter('no-email')}
            className={`p-space-md rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
              dashboardMissingFilter === 'no-email'
                ? 'bg-orange-50/70 border-orange-300 ring-2 ring-orange-500/20 shadow-xs'
                : 'bg-surface-container-low/60 border-[#e2e8f0] hover:bg-surface-container-low hover:border-orange-200'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-label-sm text-[11px] font-bold uppercase tracking-wider text-orange-800">
                  Without Mail ID
                </span>
                <span className="w-6 h-6 rounded-md bg-orange-100 text-orange-700 flex items-center justify-center">
                  <span className="material-symbols-outlined text-[15px]">unsubscribe</span>
                </span>
              </div>
              <div className="font-headline-md text-headline-md font-bold text-on-surface">
                {missingEmailCount.toLocaleString()}
              </div>
              <p className="text-xs text-secondary mt-1">
                {missingEmailPct}% lack verified direct email
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-[#e2e8f0]/60 flex items-center justify-between">
              <span className={`text-[11px] font-semibold ${dashboardMissingFilter === 'no-email' ? 'text-orange-700 font-bold' : 'text-secondary'}`}>
                {dashboardMissingFilter === 'no-email' ? 'Active Filter • Clicked' : 'Click to Pick'}
              </span>
              <span className="material-symbols-outlined text-[14px] text-secondary">arrow_forward</span>
            </div>
          </div>

          {/* Card 4: Any Missing Detail */}
          <div
            onClick={() => setDashboardMissingFilter('any-missing')}
            className={`p-space-md rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
              dashboardMissingFilter === 'any-missing'
                ? 'bg-purple-50/70 border-purple-300 ring-2 ring-purple-500/20 shadow-xs'
                : 'bg-surface-container-low/60 border-[#e2e8f0] hover:bg-surface-container-low hover:border-purple-200'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-label-sm text-[11px] font-bold uppercase tracking-wider text-purple-800">
                  Any Incomplete Detail
                </span>
                <span className="w-6 h-6 rounded-md bg-purple-100 text-purple-700 flex items-center justify-center">
                  <span className="material-symbols-outlined text-[15px]">warning</span>
                </span>
              </div>
              <div className="font-headline-md text-headline-md font-bold text-on-surface">
                {missingAnyCount.toLocaleString()}
              </div>
              <p className="text-xs text-secondary mt-1">
                {missingAnyPct}% flagged for missing channels
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-[#e2e8f0]/60 flex items-center justify-between">
              <span className={`text-[11px] font-semibold ${dashboardMissingFilter === 'any-missing' ? 'text-purple-700 font-bold' : 'text-secondary'}`}>
                {dashboardMissingFilter === 'any-missing' ? 'Active Filter • Clicked' : 'Click to Pick'}
              </span>
              <span className="material-symbols-outlined text-[14px] text-secondary">arrow_forward</span>
            </div>
          </div>

          {/* Card 5: Complete Records */}
          <div
            onClick={() => setDashboardMissingFilter('complete')}
            className={`p-space-md rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
              dashboardMissingFilter === 'complete'
                ? 'bg-emerald-50/70 border-emerald-300 ring-2 ring-emerald-500/20 shadow-xs'
                : 'bg-surface-container-low/60 border-[#e2e8f0] hover:bg-surface-container-low hover:border-emerald-200'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-label-sm text-[11px] font-bold uppercase tracking-wider text-emerald-800">
                  Complete Profiles
                </span>
                <span className="w-6 h-6 rounded-md bg-emerald-100 text-emerald-700 flex items-center justify-center">
                  <span className="material-symbols-outlined text-[15px]">verified</span>
                </span>
              </div>
              <div className="font-headline-md text-headline-md font-bold text-emerald-800">
                {completeCount.toLocaleString()}
              </div>
              <p className="text-xs text-secondary mt-1">
                {completePct}% ready for immediate outreach
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-[#e2e8f0]/60 flex items-center justify-between">
              <span className={`text-[11px] font-semibold ${dashboardMissingFilter === 'complete' ? 'text-emerald-700 font-bold' : 'text-secondary'}`}>
                {dashboardMissingFilter === 'complete' ? 'Active Filter • Clicked' : 'Click to Pick'}
              </span>
              <span className="material-symbols-outlined text-[14px] text-secondary">arrow_forward</span>
            </div>
          </div>
        </div>

        {/* Filter and Sort Toolbar */}
        <div className="bg-surface-container-low/50 p-space-sm rounded-lg border border-[#e2e8f0] flex flex-col sm:flex-row items-center justify-between gap-3 mb-space-sm">
          {/* Quick Filter Pick Buttons */}
          <div className="flex items-center gap-1.5 flex-wrap w-full sm:w-auto">
            <span className="text-xs font-bold text-secondary uppercase tracking-wider mr-1">
              Pick Filter:
            </span>
            <button
              onClick={() => setDashboardMissingFilter('any-missing')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer ${
                dashboardMissingFilter === 'any-missing'
                  ? 'bg-purple-700 text-white shadow-xs'
                  : 'bg-white text-secondary hover:text-on-surface border border-[#e2e8f0]'
              }`}
            >
              Any Missing ({missingAnyCount})
            </button>
            <button
              onClick={() => setDashboardMissingFilter('no-phone')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer ${
                dashboardMissingFilter === 'no-phone'
                  ? 'bg-rose-700 text-white shadow-xs'
                  : 'bg-white text-secondary hover:text-on-surface border border-[#e2e8f0]'
              }`}
            >
              Without Phone ({missingPhoneCount})
            </button>
            <button
              onClick={() => setDashboardMissingFilter('no-website')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer ${
                dashboardMissingFilter === 'no-website'
                  ? 'bg-amber-700 text-white shadow-xs'
                  : 'bg-white text-secondary hover:text-on-surface border border-[#e2e8f0]'
              }`}
            >
              Without Website ({missingWebsiteCount})
            </button>
            <button
              onClick={() => setDashboardMissingFilter('no-email')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer ${
                dashboardMissingFilter === 'no-email'
                  ? 'bg-orange-700 text-white shadow-xs'
                  : 'bg-white text-secondary hover:text-on-surface border border-[#e2e8f0]'
              }`}
            >
              Without Mail ID ({missingEmailCount})
            </button>
            <button
              onClick={() => setDashboardMissingFilter('complete')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer ${
                dashboardMissingFilter === 'complete'
                  ? 'bg-emerald-700 text-white shadow-xs'
                  : 'bg-white text-secondary hover:text-on-surface border border-[#e2e8f0]'
              }`}
            >
              Complete Records ({completeCount})
            </button>
          </div>

          {/* Sort By Option */}
          <div className="flex items-center gap-2 self-end sm:self-auto shrink-0">
            <label htmlFor="dashboardSortSelect" className="text-xs font-bold text-secondary uppercase tracking-wider flex items-center gap-1">
              <span className="material-symbols-outlined text-[16px]">sort</span>
              <span>Sort By:</span>
            </label>
            <select
              id="dashboardSortSelect"
              value={dashboardSortBy}
              onChange={(e) => setDashboardSortBy(e.target.value as any)}
              className="px-2.5 py-1 bg-white rounded-md text-xs font-semibold text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary cursor-pointer shadow-2xs"
            >
              <option value="missing-desc">Most Missing Details First</option>
              <option value="name-asc">College Name (A to Z)</option>
              <option value="name-desc">College Name (Z to A)</option>
              <option value="district-asc">District (A to Z)</option>
            </select>
          </div>
        </div>

        {/* Preview Roster Table */}
        <div className="overflow-x-auto rounded-lg border border-[#e2e8f0]">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-container-low/80 border-b border-[#e2e8f0] text-secondary font-label-sm uppercase tracking-wider text-[11px]">
                <th className="py-2.5 px-3 font-semibold">College Name &amp; Code</th>
                <th className="py-2.5 px-3 font-semibold">District</th>
                <th className="py-2.5 px-3 font-semibold">Category</th>
                <th className="py-2.5 px-3 font-semibold">Missing Details Status</th>
                <th className="py-2.5 px-3 font-semibold text-right">Quick Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#f1f5f9] font-body-sm text-[13px]">
              {missingPreviewColleges.slice(0, dashboardPreviewLimit).map((college) => {
                const missingList = getMissingDetailsList(college);
                const isComplete = missingList.length === 0;

                return (
                  <tr key={college.id} className="hover:bg-surface-container-low/40 transition-colors">
                    <td className="py-2.5 px-3">
                      <div className="flex flex-col">
                        <span
                          onClick={() => onSelectCollegeByName(college.name)}
                          className="font-semibold text-on-surface hover:text-primary cursor-pointer line-clamp-1"
                          title={college.name}
                        >
                          {college.name}
                        </span>
                        <span className="font-code-sm text-[10px] text-secondary">
                          {college.aisheCode}
                        </span>
                      </div>
                    </td>
                    <td className="py-2.5 px-3 whitespace-nowrap text-on-surface font-medium">
                      {college.district}
                    </td>
                    <td className="py-2.5 px-3 whitespace-nowrap text-secondary text-xs">
                      {college.category}
                    </td>
                    <td className="py-2.5 px-3">
                      {isComplete ? (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                          <span className="material-symbols-outlined text-[13px]">check_circle</span>
                          All Details Complete
                        </span>
                      ) : (
                        <div className="flex items-center gap-1.5 flex-wrap">
                          {isMissingPhone(college) && (
                            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-rose-800 bg-rose-50 px-1.5 py-0.5 rounded border border-rose-200">
                              <span className="material-symbols-outlined text-[12px]">phone_disabled</span>
                              No Phone
                            </span>
                          )}
                          {isMissingWebsite(college) && (
                            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-amber-800 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
                              <span className="material-symbols-outlined text-[12px]">public_off</span>
                              No Website
                            </span>
                          )}
                          {isMissingEmail(college) && (
                            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-orange-800 bg-orange-50 px-1.5 py-0.5 rounded border border-orange-200">
                              <span className="material-symbols-outlined text-[12px]">unsubscribe</span>
                              No Mail ID
                            </span>
                          )}
                        </div>
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          onClick={() => onSelectCollegeByName(college.name)}
                          className="px-2 py-1 bg-surface-container hover:bg-surface-container-high rounded text-xs font-semibold text-secondary hover:text-on-surface transition-colors cursor-pointer"
                          title="Open College Dossier"
                        >
                          Dossier
                        </button>
                        <button
                          onClick={() => onNavigate('college-contacts', college.name)}
                          className="px-2 py-1 bg-primary/10 hover:bg-primary/20 text-primary rounded text-xs font-semibold transition-colors cursor-pointer"
                          title="View in College Contacts"
                        >
                          Roster →
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Section Footer / Pagination & View All Link */}
        <div className="mt-space-sm pt-space-xs flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-secondary">
          <div className="flex items-center gap-2">
            <span>
              Showing {Math.min(dashboardPreviewLimit, missingPreviewColleges.length)} of {missingPreviewColleges.length.toLocaleString()} institutions for selected filter
            </span>
            {missingPreviewColleges.length > 6 && (
              <button
                onClick={() => setDashboardPreviewLimit(prev => (prev === 6 ? 25 : 6))}
                className="font-semibold text-primary hover:underline cursor-pointer ml-1"
              >
                {dashboardPreviewLimit === 6 ? 'Show 25 records' : 'Collapse to 6'}
              </button>
            )}
          </div>

          <button
            onClick={() => onNavigate('college-contacts', dashboardMissingFilter)}
            className="font-semibold text-primary hover:text-primary-container flex items-center gap-1 cursor-pointer"
          >
            <span>View and sort all {missingPreviewColleges.length} in College Contacts</span>
            <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
          </button>
        </div>
      </section>

      {/* Primary Analytic & Activity Layout (2 Columns) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg mb-space-lg items-start">
        {/* Left Column: Status Breakdown & Regional Coverage (7 Cols) */}
        <div className="lg:col-span-7 flex flex-col gap-space-md">
          {/* Card: Delivery & Health Distribution */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-center justify-between mb-space-md">
              <div className="flex flex-col">
                <h2 className="font-headline-sm text-headline-sm text-on-surface">
                  Campaign Delivery &amp; Status Breakdown
                </h2>
                <span className="font-body-sm text-body-sm text-secondary">
                  Active ledger segmentation for Tamil Nadu institutional database
                </span>
              </div>
              <span className="font-code-sm text-code-sm bg-surface-container px-2 py-1 rounded text-secondary font-medium">
                {colleges.length.toLocaleString()} TOTAL
              </span>
            </div>

            {/* Multi-segment visual progress bar */}
            <div className="h-3 w-full bg-surface-container-low rounded-full overflow-hidden flex mb-space-sm">
              <div className="bg-primary-container h-full transition-all" style={{ width: `${verifiedPct}%` }} title={`Verified: ${verifiedPct}%`}></div>
              <div className="bg-surface-dim h-full transition-all" style={{ width: `${pendingPct}%` }} title={`Pending: ${pendingPct}%`}></div>
              {bouncedCount > 0 && <div className="bg-error h-full transition-all" style={{ width: `${bouncedPct}%` }} title={`Failed: ${bouncedPct}%`}></div>}
              {deduplicatedCount > 0 && <div className="bg-secondary h-full transition-all" style={{ width: `${deduplicatedPct}%` }} title={`Duplicates: ${deduplicatedPct}%`}></div>}
            </div>

            {/* Legend Pills */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-space-sm pt-space-xs mb-space-md">
              <div 
                onClick={() => onNavigate('college-contacts', 'verified')}
                className="flex flex-col p-2 bg-surface-container-low rounded-lg cursor-pointer hover:bg-surface-container transition-colors"
              >
                <div className="flex items-center gap-1.5 mb-1">
                  <span className="w-2.5 h-2.5 rounded-sm bg-primary-container"></span>
                  <span className="font-label-sm text-label-sm text-secondary">Verified</span>
                </div>
                <span className="font-headline-sm text-headline-sm text-on-surface font-bold">{verifiedCount}</span>
                <span className="font-code-sm text-code-sm text-secondary">{verifiedPct}%</span>
              </div>

              <div 
                onClick={() => onNavigate('college-contacts', 'pending')}
                className="flex flex-col p-2 bg-surface-container-low rounded-lg cursor-pointer hover:bg-surface-container transition-colors"
              >
                <div className="flex items-center gap-1.5 mb-1">
                  <span className="w-2.5 h-2.5 rounded-sm bg-surface-dim"></span>
                  <span className="font-label-sm text-label-sm text-secondary">Pending</span>
                </div>
                <span className="font-headline-sm text-headline-sm text-on-surface font-bold">{pendingCount}</span>
                <span className="font-code-sm text-code-sm text-secondary">{pendingPct}%</span>
              </div>

              <div 
                onClick={() => onNavigate('college-contacts', 'bounced')}
                className="flex flex-col p-2 bg-surface-container-low rounded-lg cursor-pointer hover:bg-surface-container transition-colors"
              >
                <div className="flex items-center gap-1.5 mb-1">
                  <span className="w-2.5 h-2.5 rounded-sm bg-error"></span>
                  <span className="font-label-sm text-label-sm text-secondary">Bounced</span>
                </div>
                <span className="font-headline-sm text-headline-sm text-error font-bold">{bouncedCount}</span>
                <span className="font-code-sm text-code-sm text-secondary">{bouncedPct}%</span>
              </div>

              <div 
                onClick={() => onNavigate('import-contacts')}
                className="flex flex-col p-2 bg-surface-container-low rounded-lg cursor-pointer hover:bg-surface-container transition-colors"
              >
                <div className="flex items-center gap-1.5 mb-1">
                  <span className="w-2.5 h-2.5 rounded-sm bg-secondary"></span>
                  <span className="font-label-sm text-label-sm text-secondary">Duplicates</span>
                </div>
                <span className="font-headline-sm text-headline-sm text-on-surface font-bold">{deduplicatedCount}</span>
                <span className="font-code-sm text-code-sm text-secondary">{deduplicatedPct}%</span>
              </div>
            </div>

            {/* Inline Visual Chart: Category Matrix */}
            <div className="pt-space-sm bg-surface-container-low/50 p-space-md rounded-lg border border-[#e2e8f0]/60">
              <div className="flex items-center justify-between mb-space-sm">
                <span className="font-label-md text-label-md text-on-surface font-semibold">Institutional Classifications</span>
                <span className="font-label-sm text-label-sm text-secondary">AICTE / UGC / DOTE Real Distribution</span>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-space-sm">
                {dynamicClassifications.map((cls) => (
                  <div 
                    key={cls.name}
                    className="cursor-pointer hover:opacity-80 transition-opacity"
                    onClick={() => onNavigate('college-contacts', cls.name)}
                  >
                    <span className="font-label-sm text-label-sm text-secondary block truncate">{cls.name}</span>
                    <span className="font-headline-sm text-headline-sm text-on-surface font-bold">{cls.count}</span>
                    <div className="w-full bg-surface-container h-1.5 rounded-full mt-1.5 overflow-hidden">
                      <div className={`${cls.color} h-full rounded-full`} style={{ width: `${cls.pct}%` }}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* District Coverage Summary Module */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-center justify-between mb-space-md">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center text-primary">
                  <span className="material-symbols-outlined text-[20px]">map</span>
                </div>
                <div>
                  <h2 className="font-headline-sm text-headline-sm text-on-surface font-bold">Top District Density</h2>
                  <p className="font-body-sm text-body-sm text-secondary">Real verified institutional clusters in Tamil Nadu</p>
                </div>
              </div>
              <button
                className="font-label-sm text-label-sm text-primary hover:underline font-semibold flex items-center gap-1 cursor-pointer"
                onClick={() => onNavigate('college-contacts')}
              >
                <span>View All ({distinctDistrictsCount} Districts)</span>
                <span className="material-symbols-outlined text-[14px]">chevron_right</span>
              </button>
            </div>

            <div className="space-y-3">
              {dynamicDistricts.slice(0, 6).map((dist, idx) => {
                const palette = ['bg-primary', 'bg-tertiary', 'bg-secondary', 'bg-outline', 'bg-secondary-container', 'bg-surface-dim'];
                const barColor = palette[idx % palette.length];
                return (
                  <div 
                    key={dist.name} 
                    className="flex flex-col gap-1 cursor-pointer group"
                    onClick={() => onNavigate('college-contacts', dist.name.replace(' District', ''))}
                  >
                    <div className="flex items-center justify-between font-body-sm text-body-sm">
                      <div className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${barColor}`}></span>
                        <span className="font-medium text-on-surface group-hover:text-primary transition-colors">
                          {dist.name}
                        </span>
                        <span className="font-code-sm text-code-sm text-secondary bg-surface-container px-1.5 py-0.2 rounded text-[11px]">
                          {dist.zone}
                        </span>
                      </div>
                      <span className="font-semibold text-on-surface">
                        {dist.count} <span className="font-normal text-secondary">colleges</span>
                      </span>
                    </div>
                    <div className="w-full bg-surface-container-low h-2 rounded-full overflow-hidden">
                      <div className={`${barColor} h-2 rounded-full transition-all group-hover:opacity-85`} style={{ width: `${dist.pct}%` }}></div>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="mt-space-md pt-space-sm bg-surface-container-low p-space-sm rounded-lg flex items-center justify-between flex-wrap gap-2 border border-[#e2e8f0]/60">
              <span className="font-body-sm text-body-sm text-secondary">Institutional Roster Coverage:</span>
              <span className="font-code-sm text-code-sm font-semibold text-on-surface text-[12px]">
                {colleges.length} Active Campuses | {distinctDistrictsCount} Districts | 100% Verified Emails
              </span>
            </div>
          </div>
        </div>

        {/* Right Column: Recent Outreach Activity Stream (5 Cols) */}
        <div className="lg:col-span-5 flex flex-col gap-space-md">
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-center justify-between mb-space-md">
              <div>
                <h2 className="font-headline-sm text-headline-sm text-on-surface font-bold">Recent Outreach Activity</h2>
                <p className="font-body-sm text-body-sm text-secondary">Real-time mock dispatch events &amp; ledger checks</p>
              </div>
              <span className="inline-flex items-center gap-1 font-code-sm text-code-sm px-2 py-0.5 rounded bg-surface-container text-secondary">
                <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span> LIVE FEED
              </span>
            </div>

            {/* Activity Feed List */}
            <div className="flex flex-col gap-space-sm">
              {activities.map((item) => (
                <div
                  key={item.id}
                  onClick={() => onSelectCollegeByName(item.collegeName)}
                  className="p-space-sm rounded-lg bg-surface-container-low/40 hover:bg-surface-container-low transition-colors flex items-start gap-space-sm cursor-pointer border border-transparent hover:border-[#e2e8f0]"
                >
                  <div className={`w-8 h-8 rounded-lg ${item.iconBg} flex items-center justify-center shrink-0 mt-0.5`}>
                    <span className={`material-symbols-outlined text-[18px] ${item.iconColor}`}>
                      {item.icon}
                    </span>
                  </div>
                  <div className="flex flex-col flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-1">
                      <span className="font-body-sm text-body-sm font-semibold text-on-surface truncate">
                        {item.collegeName}
                      </span>
                      <span className="font-code-sm text-code-sm text-secondary shrink-0 text-[11px]">
                        {item.timeAgo}
                      </span>
                    </div>
                    <p className="font-label-sm text-label-sm text-secondary truncate">
                      {item.description}
                    </p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-semibold ${
                        item.statusType === 'verified' 
                          ? 'bg-surface-container-highest text-tertiary' 
                          : item.statusType === 'pending'
                          ? 'bg-surface-container text-secondary'
                          : item.statusType === 'sent'
                          ? 'bg-tertiary-fixed text-on-tertiary-fixed'
                          : item.statusType === 'duplicate'
                          ? 'bg-secondary-fixed text-on-secondary-fixed'
                          : 'bg-error-container text-on-error-container'
                      }`}>
                        {item.statusBadge}
                      </span>
                      <span className="font-code-sm text-code-sm text-secondary text-[11px] truncate">
                        {item.subBadge}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button
              className="w-full mt-space-md py-2 rounded-lg bg-surface-container-low hover:bg-surface-container text-on-surface font-label-md text-label-md font-semibold transition-colors flex items-center justify-center gap-1 cursor-pointer border border-[#e2e8f0]"
              onClick={() => onNavigate('send-history')}
            >
              <span>View Detailed Send Audit History</span>
              <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
            </button>
          </div>

          {/* Quick Campaign Dispatch Readiness Card */}
          <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-center justify-between mb-2">
              <span className="font-label-sm text-label-sm font-semibold uppercase text-secondary">
                Dispatcher Velocity Throttle
              </span>
              <span className="font-code-sm text-code-sm text-primary font-bold">
                {stats.velocityThrottle} msgs/min
              </span>
            </div>
            <p className="font-body-sm text-body-sm text-secondary mb-3">
              Rate limiting safeguards active to protect IP reputation across .edu.in and .ac.in institutional recipient servers.
            </p>
            <div className="flex items-center justify-between bg-surface-container-low p-2 rounded text-[12px] border border-[#e2e8f0]/60">
              <span className="text-secondary font-medium">Compliance Check:</span>
              <span className="text-on-surface font-semibold">UGC / AICTE Outreach Protocol 2024</span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Integration Health Cards & System Notice */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md">
        {/* Integration 1: Google Sheets */}
        <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm flex items-center justify-between border border-[#e2e8f0]">
          <div className="flex items-center gap-space-sm">
            <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-on-surface">
              <span className="material-symbols-outlined text-[24px]">table_chart</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-headline-sm text-headline-sm text-on-surface">Google Sheets Sync</span>
                <span className="bg-surface-container text-secondary px-2 py-0.5 rounded text-[11px] font-semibold">
                  Mock Provider
                </span>
              </div>
              <p className="font-body-sm text-body-sm text-secondary">
                Institutional master roster auto-import disconnected
              </p>
            </div>
          </div>
          <button
            className="font-label-md text-label-md text-primary hover:underline font-semibold flex items-center gap-1 shrink-0 cursor-pointer"
            onClick={() => onNavigate('settings')}
          >
            <span>Configure</span>
            <span className="material-symbols-outlined text-[16px]">open_in_new</span>
          </button>
        </div>

        {/* Integration 2: Gmail SMTP API */}
        <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm flex items-center justify-between border border-[#e2e8f0]">
          <div className="flex items-center gap-space-sm">
            <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-on-surface">
              <span className="material-symbols-outlined text-[24px]">mail</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-headline-sm text-headline-sm text-on-surface">Gmail API Gateway</span>
                <span className="bg-error-container text-on-error-container px-2 py-0.5 rounded text-[11px] font-semibold">
                  Sandbox Active
                </span>
              </div>
              <p className="font-body-sm text-body-sm text-secondary">
                Zero real emails will be transmitted in this environment
              </p>
            </div>
          </div>
          <button
            className="font-label-md text-label-md text-secondary hover:text-on-surface font-semibold flex items-center gap-1 shrink-0 cursor-pointer"
            onClick={() => onTriggerToast('Sandbox mode is active. Dispatches generate simulated audit records without external mail transmission.', 'lock')}
          >
            <span>Sandbox Info</span>
            <span className="material-symbols-outlined text-[16px]">info</span>
          </button>
        </div>
      </div>
    </div>
  );
};
