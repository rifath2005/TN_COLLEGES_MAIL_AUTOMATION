import React, { useState, useEffect } from 'react';
import { Campaign, CollegeContact } from '../types';

interface CampaignsViewProps {
  campaigns: Campaign[];
  colleges: CollegeContact[];
  onOpenCampaignModal: () => void;
  onSimulateBatch: (campaignId: string, count: number) => void;
  onTriggerToast: (msg: string, icon?: string) => void;
}

export const CampaignsView: React.FC<CampaignsViewProps> = ({
  campaigns,
  colleges,
  onOpenCampaignModal,
  onSimulateBatch,
  onTriggerToast
}) => {
  const [activeSimulationId, setActiveSimulationId] = useState<string | null>(null);
  const [liveStreamLogs, setLiveStreamLogs] = useState<{ time: string; text: string; status: string }[]>([]);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    if (activeSimulationId) {
      interval = setInterval(() => {
        const randomCollege = colleges[Math.floor(Math.random() * colleges.length)];
        const isBounced = Math.random() < 0.03;
        
        onSimulateBatch(activeSimulationId, 1);
        
        setLiveStreamLogs(prev => [
          {
            time: new Date().toLocaleTimeString(),
            text: `[${randomCollege.aisheCode}] Dispatched to ${randomCollege.principalEmail} (${randomCollege.name})`,
            status: isBounced ? 'Bounced' : 'Delivered'
          },
          ...prev.slice(0, 15)
        ]);
      }, 1000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [activeSimulationId, colleges, onSimulateBatch]);

  const toggleSimulation = (campId: string) => {
    if (activeSimulationId === campId) {
      setActiveSimulationId(null);
      onTriggerToast('Batch dispatch simulator paused.', 'pause');
    } else {
      setActiveSimulationId(campId);
      onTriggerToast('Batch dispatch simulator active: Dispatching 45 msgs/min.', 'rocket_launch');
    }
  };

  return (
    <div className="flex flex-col w-full pb-space-xl space-y-space-lg">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="font-code-sm text-code-sm uppercase tracking-widest text-primary font-bold">
              Dispatch Operations
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
            <span className="font-code-sm text-code-sm text-secondary">
              Statewide Outreach Management
            </span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface font-bold tracking-tight">
            Campaigns &amp; Wave Dispatches
          </h1>
          <p className="font-body-md text-body-md text-secondary mt-0.5">
            Create, schedule, throttle, and monitor multi-district collegiate communication waves.
          </p>
        </div>

        <button
          onClick={onOpenCampaignModal}
          className="h-9 px-4 rounded-lg bg-primary-container text-on-primary hover:opacity-95 font-label-md font-semibold flex items-center gap-1.5 shadow-sm active:scale-[0.98] transition-all cursor-pointer"
        >
          <span className="material-symbols-outlined text-[18px]">add_circle</span>
          <span>New Campaign</span>
        </button>
      </div>

      {/* Campaign KPI Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-space-md">
        <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm border border-[#e2e8f0]">
          <span className="text-xs uppercase font-semibold text-secondary">Active Waves</span>
          <div className="font-headline-lg font-bold text-on-surface mt-1">
            {campaigns.filter(c => c.status === 'In Progress').length}
          </div>
          <span className="text-[11px] text-primary font-semibold">1 wave transmitting now</span>
        </div>

        <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm border border-[#e2e8f0]">
          <span className="text-xs uppercase font-semibold text-secondary">Cumulative Dispatched</span>
          <div className="font-headline-lg font-bold text-on-surface mt-1">
            {campaigns.reduce((acc, c) => acc + c.sentCount, 0).toLocaleString()}
          </div>
          <span className="text-[11px] text-emerald-700 font-semibold">56.8% directory reach</span>
        </div>

        <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm border border-[#e2e8f0]">
          <span className="text-xs uppercase font-semibold text-secondary">Global Bounce Rate</span>
          <div className="font-headline-lg font-bold text-error mt-1">
            2.5%
          </div>
          <span className="text-[11px] text-secondary font-code-sm">Sub-3% SLA compliant</span>
        </div>

        <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm border border-[#e2e8f0]">
          <span className="text-xs uppercase font-semibold text-secondary">Velocity Throttle</span>
          <div className="font-headline-lg font-bold text-on-surface mt-1">
            45 <span className="text-sm font-normal text-secondary">msgs/min</span>
          </div>
          <span className="text-[11px] text-secondary">AICTE IP Protection Protocol</span>
        </div>
      </div>

      {/* Campaign Cards List */}
      <div className="space-y-space-md">
        {campaigns.map((camp) => {
          const pct = Math.min(100, Math.round((camp.sentCount / (camp.targetCount || 1)) * 100));
          const isSimulating = activeSimulationId === camp.id;

          return (
            <div
              key={camp.id}
              className="bg-surface-container-lowest p-space-lg rounded-xl shadow-sm border border-[#e2e8f0] flex flex-col gap-4"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                    camp.status === 'In Progress' 
                      ? 'bg-primary-container text-on-primary' 
                      : 'bg-emerald-100 text-emerald-800'
                  }`}>
                    <span className="material-symbols-outlined text-[22px]">
                      {camp.status === 'In Progress' ? 'rocket_launch' : 'task_alt'}
                    </span>
                  </div>
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-headline-sm font-bold text-on-surface">
                        {camp.name}
                      </h3>
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                        camp.status === 'In Progress'
                          ? 'bg-primary-fixed text-on-primary-fixed'
                          : 'bg-emerald-100 text-emerald-800'
                      }`}>
                        {camp.status}
                      </span>
                    </div>
                    <p className="text-xs text-secondary mt-0.5">
                      Target Audience: <span className="font-semibold text-on-surface">{camp.targetZone}</span>
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {camp.status === 'In Progress' && (
                    <button
                      onClick={() => toggleSimulation(camp.id)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                        isSimulating
                          ? 'bg-amber-100 text-amber-900 border border-amber-300'
                          : 'bg-primary text-white hover:bg-primary-container shadow-sm'
                      }`}
                    >
                      <span className="material-symbols-outlined text-[16px]">
                        {isSimulating ? 'pause' : 'play_arrow'}
                      </span>
                      <span>{isSimulating ? 'Pause Dispatch Stream' : 'Run Live Dispatcher'}</span>
                    </button>
                  )}
                  <span className="text-xs font-code-sm text-secondary bg-surface-container px-2 py-1 rounded">
                    Created: {camp.createdAt}
                  </span>
                </div>
              </div>

              {/* Progress and numbers */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="font-semibold text-on-surface">
                    Progress: {camp.sentCount} of {camp.targetCount} delivered
                  </span>
                  <span className="font-code-sm font-bold text-primary">{pct}%</span>
                </div>
                <div className="w-full bg-surface-container-low h-2.5 rounded-full overflow-hidden">
                  <div
                    className={`h-full transition-all duration-300 ${
                      pct === 100 ? 'bg-emerald-500' : 'bg-primary-container'
                    }`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>

              {/* Campaign meta tags */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-[#f1f5f9] text-xs">
                <div>
                  <span className="text-secondary block">Email Template:</span>
                  <span className="font-semibold text-on-surface truncate block">{camp.templateName}</span>
                </div>
                <div>
                  <span className="text-secondary block">Delivered:</span>
                  <span className="font-semibold text-emerald-700">{camp.deliveredCount} institutions</span>
                </div>
                <div>
                  <span className="text-secondary block">Bounced / Rejected:</span>
                  <span className="font-semibold text-error">{camp.bouncedCount} records</span>
                </div>
                <div>
                  <span className="text-secondary block">Velocity Cap:</span>
                  <span className="font-semibold text-on-surface font-code-sm">{camp.velocityThrottle} msgs/min</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Live Dispatch Stream Log (When simulation is active) */}
      {activeSimulationId && (
        <div className="bg-[#0b1c30] text-slate-100 p-space-md rounded-xl shadow-lg border border-slate-800 space-y-2 animate-in fade-in duration-200">
          <div className="flex items-center justify-between pb-2 border-b border-slate-700/60">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="font-code-sm text-xs font-bold text-emerald-400">
                LIVE DISPATCH LOG STREAM (Simulated SMTP Packets)
              </span>
            </div>
            <span className="text-[11px] font-code-sm text-slate-400">Rate: 45 msgs/min</span>
          </div>

          <div className="space-y-1 font-code-sm text-[11px] max-h-48 overflow-y-auto">
            {liveStreamLogs.length === 0 && (
              <p className="text-slate-400 italic">Starting queue listener...</p>
            )}
            {liveStreamLogs.map((log, index) => (
              <div key={index} className="flex items-center justify-between text-slate-300">
                <span className="truncate">{log.time} {log.text}</span>
                <span className={`px-1.5 py-0.2 rounded text-[10px] shrink-0 font-bold ml-2 ${
                  log.status === 'Bounced' ? 'bg-red-900 text-red-200' : 'bg-emerald-900 text-emerald-200'
                }`}>
                  {log.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
