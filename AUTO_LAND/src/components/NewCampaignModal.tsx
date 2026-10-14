import React, { useState } from 'react';
import { EmailTemplate, Campaign } from '../types';

interface NewCampaignModalProps {
  isOpen: boolean;
  onClose: () => void;
  templates: EmailTemplate[];
  onScheduleCampaign: (campaign: Partial<Campaign>) => void;
}

export const NewCampaignModal: React.FC<NewCampaignModalProps> = ({
  isOpen,
  onClose,
  templates,
  onScheduleCampaign
}) => {
  const [targetZone, setTargetZone] = useState('All Tamil Nadu (38 Districts — 125 Colleges)');
  const [templateId, setTemplateId] = useState(templates[0]?.id || 'tpl-1');
  const [onlyVerified, setOnlyVerified] = useState(true);
  const [throttle, setThrottle] = useState(45);
  const [campaignName, setCampaignName] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const selectedTemplate = templates.find(t => t.id === templateId);
    
    // Calculate targeted count based on selection
    let count = 125;
    if (targetZone.includes('Zone 01')) count = 28;
    else if (targetZone.includes('Zone 04')) count = 24;
    else if (targetZone.includes('Zone 07')) count = 18;
    else if (targetZone.includes('Zone 05')) count = 16;

    onScheduleCampaign({
      name: campaignName.trim() || `Wave 05: ${selectedTemplate?.title.slice(0, 32)}...`,
      targetZone,
      templateId,
      templateName: selectedTemplate?.title || 'Selected Directorate Template',
      targetCount: count,
      velocityThrottle: throttle,
      status: 'In Progress'
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#213145]/40 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div 
        className="fixed inset-0"
        onClick={onClose}
      />
      <div className="relative bg-surface-container-lowest rounded-xl shadow-2xl max-w-lg w-full p-space-lg mx-space-md border border-[#cbd5e1] z-10 animate-in zoom-in-95 duration-200">
        <div className="flex items-center justify-between mb-space-md">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary-container text-on-primary flex items-center justify-center">
              <span className="material-symbols-outlined text-[20px]">send</span>
            </div>
            <div>
              <h3 className="font-headline-sm text-headline-sm text-on-surface font-bold">
                Launch Regional Campaign
              </h3>
              <span className="font-label-sm text-label-sm text-secondary">
                Batch dispatch engine
              </span>
            </div>
          </div>
          <button 
            className="text-secondary hover:text-on-surface p-1 rounded-lg" 
            onClick={onClose}
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-space-md">
          {/* Demo notice pill */}
          <div className="bg-secondary-fixed/40 p-space-sm rounded-lg flex items-start gap-2 border border-[#bec6e0]/60">
            <span className="material-symbols-outlined text-[18px] text-on-secondary-fixed shrink-0 mt-0.5">
              notification_important
            </span>
            <p className="font-body-sm text-body-sm text-on-secondary-fixed leading-tight">
              <strong>Demonstration Instance:</strong> Outreach invitations will be recorded into the mock analytics table. Real outbound SMTP packets remain suspended.
            </p>
          </div>

          <div>
            <label className="block font-label-md text-label-md text-on-surface mb-1">
              Campaign Name (Optional)
            </label>
            <input
              type="text"
              value={campaignName}
              onChange={(e) => setCampaignName(e.target.value)}
              placeholder="e.g. Wave 05: Special Academic Grant Roster"
              className="w-full bg-surface-container-low px-3 py-2 rounded-lg font-body-sm text-body-sm text-on-surface border border-[#e2e8f0] focus:outline-none focus:bg-surface-container-lowest focus:border-primary"
            />
          </div>

          <div>
            <label className="block font-label-md text-label-md text-on-surface mb-1">
              Target Zone / District Cluster
            </label>
            <select 
              value={targetZone}
              onChange={(e) => setTargetZone(e.target.value)}
              className="w-full bg-surface-container-low px-3 py-2 rounded-lg font-body-sm text-body-sm text-on-surface border border-[#e2e8f0] focus:outline-none focus:bg-surface-container-lowest focus:border-primary"
            >
              <option value="All Tamil Nadu (38 Districts — 125 Colleges)">
                All Tamil Nadu (38 Districts — 125 Colleges)
              </option>
              <option value="Chennai Metropolitan & Kanchipuram (Zone 01 — 28 Colleges)">
                Chennai Metropolitan & Kanchipuram (Zone 01 — 28 Colleges)
              </option>
              <option value="Western Belt: Coimbatore, Salem, Erode (Zone 04 — 24 Colleges)">
                Western Belt: Coimbatore, Salem, Erode (Zone 04 — 24 Colleges)
              </option>
              <option value="Southern Region: Madurai, Tirunelveli (Zone 07 — 18 Colleges)">
                Southern Region: Madurai, Tirunelveli (Zone 07 — 18 Colleges)
              </option>
              <option value="Central Cauvery Delta: Trichy, Thanjavur (Zone 05 — 16 Colleges)">
                Central Cauvery Delta: Trichy, Thanjavur (Zone 05 — 16 Colleges)
              </option>
            </select>
          </div>

          <div>
            <label className="block font-label-md text-label-md text-on-surface mb-1">
              Select Email Template
            </label>
            <select 
              value={templateId}
              onChange={(e) => setTemplateId(e.target.value)}
              className="w-full bg-surface-container-low px-3 py-2 rounded-lg font-body-sm text-body-sm text-on-surface border border-[#e2e8f0] focus:outline-none focus:bg-surface-container-lowest focus:border-primary"
            >
              {templates.map((tpl) => (
                <option key={tpl.id} value={tpl.id}>
                  {tpl.title}
                </option>
              ))}
            </select>
          </div>

          {/* Verification Check & Throttling */}
          <div className="flex items-center justify-between p-space-sm bg-surface-container-low rounded-lg border border-[#e2e8f0]">
            <div>
              <span className="font-label-md text-label-md text-on-surface block font-semibold">
                Verification Check
              </span>
              <span className="font-body-sm text-body-sm text-secondary">
                Dispatch solely to deliverability certified institutional records
              </span>
            </div>
            <input 
              checked={onlyVerified}
              onChange={(e) => setOnlyVerified(e.target.checked)}
              className="w-4 h-4 accent-primary rounded cursor-pointer" 
              type="checkbox"
            />
          </div>

          <div className="flex items-center justify-between px-space-sm py-2 bg-surface-container-low rounded-lg border border-[#e2e8f0]">
            <div>
              <span className="font-label-md text-label-md text-on-surface block font-semibold">
                Dispatcher Velocity Throttle
              </span>
              <span className="font-body-sm text-body-sm text-secondary text-[12px]">
                UGC / AICTE Outreach Protocol 2024 compliance
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-code-sm text-primary font-bold text-[13px]">{throttle} msgs/min</span>
            </div>
          </div>

          <div className="mt-space-lg flex items-center justify-end gap-space-sm pt-2">
            <button 
              type="button"
              className="px-space-md py-2 rounded-lg text-secondary hover:text-on-surface hover:bg-surface-container-low font-label-lg text-label-lg font-semibold transition-colors" 
              onClick={onClose}
            >
              Cancel
            </button>
            <button 
              type="submit"
              className="px-space-md py-2 rounded-lg bg-primary-container text-on-primary hover:opacity-95 font-label-lg text-label-lg font-semibold flex items-center gap-1.5 shadow-sm active:scale-[0.98] transition-all cursor-pointer"
            >
              <span className="material-symbols-outlined text-[18px]">rocket_launch</span>
              <span>Schedule Mock Send</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
