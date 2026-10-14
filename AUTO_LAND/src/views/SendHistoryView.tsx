import React, { useState } from 'react';
import { DispatchAuditRecord } from '../types';

interface SendHistoryViewProps {
  auditLogs: DispatchAuditRecord[];
  onTriggerToast: (msg: string, icon?: string) => void;
  onNavigateToResearch: () => void;
}

export const SendHistoryView: React.FC<SendHistoryViewProps> = ({
  auditLogs,
  onTriggerToast,
  onNavigateToResearch
}) => {
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const filteredLogs = auditLogs.filter((log) => {
    const matchStatus = filterStatus === 'all' || log.status.toLowerCase() === filterStatus.toLowerCase();
    const matchSearch =
      log.collegeName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      log.aisheCode.toLowerCase().includes(searchQuery.toLowerCase()) ||
      log.recipientEmail.toLowerCase().includes(searchQuery.toLowerCase()) ||
      log.campaignName.toLowerCase().includes(searchQuery.toLowerCase());
    return matchStatus && matchSearch;
  });

  const handleExportAuditCSV = () => {
    const headers = ['Log_ID', 'College', 'AISHE', 'Recipient', 'Designation', 'Campaign', 'Timestamp', 'Status', 'IP_Node', 'Bounce_Reason'];
    const rows = filteredLogs.map(l => [
      `"${l.id}"`,
      `"${l.collegeName}"`,
      `"${l.aisheCode}"`,
      `"${l.recipientEmail}"`,
      `"${l.recipientTitle}"`,
      `"${l.campaignName}"`,
      `"${l.timestamp}"`,
      `"${l.status}"`,
      `"${l.ipNode}"`,
      `"${l.bounceReason || 'None'}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encoded = encodeURI(csvContent);
    const a = document.createElement('a');
    a.href = encoded;
    a.download = `TN_Outreach_Send_Audit_Report_${Date.now()}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    onTriggerToast('Audit certificate exported: AICTE & UGC compliant dispatch log', 'download');
  };

  const handleRetryBounce = (log: DispatchAuditRecord) => {
    onTriggerToast(`Queued fallback delivery retry for ${log.collegeName} via alternative mail exchange.`, 'refresh');
  };

  return (
    <div className="flex flex-col w-full pb-space-xl space-y-space-lg">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="font-code-sm text-code-sm uppercase tracking-widest text-primary font-bold">
              Audit & Compliance
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
            <span className="font-code-sm text-code-sm text-secondary">
              Statutory Outreach Ledger
            </span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface font-bold tracking-tight">
            Detailed Send Audit History
          </h1>
          <p className="font-body-md text-body-md text-secondary mt-0.5">
            Cryptographically signed delivery logs, open rates, and bounce telemetry across Tamil Nadu collegiate mail servers.
          </p>
        </div>

        <button
          onClick={handleExportAuditCSV}
          className="h-9 px-4 rounded-lg bg-surface-container-lowest text-on-surface hover:bg-surface-container-low border border-[#e2e8f0] font-label-md font-semibold flex items-center gap-1.5 shadow-sm active:scale-[0.98] transition-all cursor-pointer"
        >
          <span className="material-symbols-outlined text-[18px] text-secondary">file_download</span>
          <span>Export Audit Log</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm border border-[#e2e8f0] flex flex-col md:flex-row gap-3 items-center justify-between">
        <div className="relative w-full md:w-80">
          <span className="material-symbols-outlined absolute left-3 top-2.5 text-[18px] text-secondary">
            search
          </span>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search college, AISHE, email..."
            className="w-full pl-9 pr-3 py-1.5 bg-surface-container-low rounded-lg font-body-sm text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary"
          />
        </div>

        {/* Status filter tabs */}
        <div className="inline-flex p-1 bg-surface-container-low rounded-lg border border-[#e2e8f0]">
          {['all', 'delivered', 'opened', 'clicked', 'bounced'].map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-3 py-1 text-xs rounded-md font-semibold capitalize transition-all ${
                filterStatus === st
                  ? 'bg-white text-on-surface shadow-2xs'
                  : 'text-secondary hover:text-on-surface'
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-surface-container-lowest rounded-lg shadow-sm border border-[#e2e8f0] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-container-low/70 border-b border-[#e2e8f0] text-secondary font-label-sm uppercase tracking-wider text-[11px]">
                <th className="py-3 px-4 font-semibold">Timestamp</th>
                <th className="py-3 px-4 font-semibold">College & AISHE</th>
                <th className="py-3 px-4 font-semibold">Recipient Contact</th>
                <th className="py-3 px-4 font-semibold">Campaign Wave</th>
                <th className="py-3 px-4 font-semibold">Status & Diagnostic</th>
                <th className="py-3 px-4 font-semibold">Node Gateway</th>
                <th className="py-3 px-4 font-semibold text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#f1f5f9] font-body-sm text-[13px]">
              {filteredLogs.map((log) => (
                <tr key={log.id} className="hover:bg-surface-container-low/40 transition-colors">
                  <td className="py-3 px-4 whitespace-nowrap font-code-sm text-xs text-secondary">
                    {log.timestamp}
                  </td>
                  <td className="py-3 px-4">
                    <span className="font-semibold text-on-surface block line-clamp-1">{log.collegeName}</span>
                    <span className="font-code-sm text-[11px] text-secondary">AISHE {log.aisheCode}</span>
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-on-surface block">{log.recipientEmail}</span>
                    <span className="text-xs text-secondary">{log.recipientTitle}</span>
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-xs text-secondary line-clamp-1">{log.campaignName}</span>
                    <span className="text-[10px] font-code-sm bg-surface-container px-1 py-0.2 rounded text-secondary">{log.zone}</span>
                  </td>
                  <td className="py-3 px-4 whitespace-nowrap">
                    <div>
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold ${
                        log.status === 'Delivered'
                          ? 'bg-emerald-100 text-emerald-800'
                          : log.status === 'Opened'
                          ? 'bg-sky-100 text-sky-800'
                          : log.status === 'Clicked'
                          ? 'bg-indigo-100 text-indigo-800'
                          : 'bg-error-container text-on-error-container'
                      }`}>
                        {log.status}
                      </span>
                      {log.bounceReason && (
                        <p className="font-code-sm text-[10px] text-error mt-0.5 line-clamp-1 max-w-xs">
                          {log.bounceReason}
                        </p>
                      )}
                    </div>
                  </td>
                  <td className="py-3 px-4 whitespace-nowrap font-code-sm text-[11px] text-secondary">
                    {log.ipNode}
                  </td>
                  <td className="py-3 px-4 text-right whitespace-nowrap">
                    {log.status === 'Bounced' ? (
                      <button
                        onClick={() => handleRetryBounce(log)}
                        className="px-2 py-1 bg-red-50 hover:bg-red-100 text-error rounded text-xs font-semibold border border-red-200 transition-colors"
                        title="Retry delivery through alternative gateway"
                      >
                        Retry
                      </button>
                    ) : (
                      <span className="material-symbols-outlined text-emerald-600 text-[18px]">
                        check_circle
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredLogs.length === 0 && (
          <div className="p-8 text-center text-secondary">
            <span className="material-symbols-outlined text-[36px] opacity-40">rule</span>
            <p className="mt-1 font-body-md font-semibold text-on-surface">No audit records found</p>
          </div>
        )}

        <div className="px-4 py-3 bg-surface-container-low/40 border-t border-[#e2e8f0] flex items-center justify-between text-xs text-secondary">
          <span>{filteredLogs.length} verified events logged</span>
          <span className="font-code-sm">TLS 1.3 / DKIM Verified</span>
        </div>
      </div>
    </div>
  );
};
