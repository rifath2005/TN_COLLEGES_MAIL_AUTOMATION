import React, { useState, useEffect, useRef } from 'react';
import { CollegeContact, NavScreen } from '../types';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  colleges: CollegeContact[];
  onSelectCollege: (college: CollegeContact) => void;
  onNavigate: (screen: NavScreen) => void;
  onOpenCampaignModal: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  colleges,
  onSelectCollege,
  onNavigate,
  onOpenCampaignModal
}) => {
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
    }
  }, [isOpen]);

  // Handle ESC
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const filteredColleges = colleges.filter((c) =>
    c.name.toLowerCase().includes(query.toLowerCase()) ||
    c.district.toLowerCase().includes(query.toLowerCase()) ||
    c.aisheCode.toLowerCase().includes(query.toLowerCase()) ||
    c.principalName.toLowerCase().includes(query.toLowerCase())
  ).slice(0, 5);

  const quickActions = [
    {
      title: 'New Outreach Campaign',
      desc: 'Launch institutional batch dispatch',
      icon: 'campaign',
      action: () => {
        onClose();
        onOpenCampaignModal();
      }
    },
    {
      title: 'College Contacts Roster',
      desc: 'Browse all verified colleges & AISHE codes',
      icon: 'school',
      action: () => {
        onClose();
        onNavigate('college-contacts');
      }
    },
    {
      title: 'Website Research & Contact Scraper',
      desc: 'Extract Dean & Placement Officer emails automatically',
      icon: 'travel_explore',
      action: () => {
        onClose();
        onNavigate('website-research');
      }
    },
    {
      title: 'Import Contacts from Google Sheets',
      desc: 'Reconcile roster and run MX validation checks',
      icon: 'cloud_upload',
      action: () => {
        onClose();
        onNavigate('import-contacts');
      }
    },
    {
      title: 'Send History & Audit Trail',
      desc: 'Inspect bounce telemetry and delivery speed',
      icon: 'schedule_send',
      action: () => {
        onClose();
        onNavigate('send-history');
      }
    }
  ].filter(a => a.title.toLowerCase().includes(query.toLowerCase()) || a.desc.toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/40 backdrop-blur-sm animate-in fade-in duration-150">
      <div 
        className="fixed inset-0"
        onClick={onClose}
      />
      <div className="relative bg-surface-container-lowest rounded-xl shadow-2xl max-w-xl w-full border border-[#cbd5e1] overflow-hidden z-10 animate-in zoom-in-95 duration-150">
        {/* Search Input */}
        <div className="flex items-center px-4 py-3 border-b border-[#e2e8f0] gap-2">
          <span className="material-symbols-outlined text-[20px] text-secondary">search</span>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search Tamil Nadu colleges, AISHE codes, districts, or actions..."
            className="w-full bg-transparent text-on-surface placeholder:text-secondary focus:outline-none font-body-sm text-sm"
          />
          {query && (
            <button onClick={() => setQuery('')} className="text-secondary hover:text-on-surface">
              <span className="material-symbols-outlined text-[18px]">close</span>
            </button>
          )}
          <span className="font-code-sm text-[11px] text-secondary bg-surface-container px-2 py-0.5 rounded border border-[#e2e8f0]">
            ESC
          </span>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-2 divide-y divide-[#f1f5f9]">
          {/* Colleges */}
          {filteredColleges.length > 0 && (
            <div className="py-2">
              <div className="px-3 pb-1 text-[11px] font-label-sm uppercase font-semibold text-secondary tracking-wider">
                Colleges & Institutions ({filteredColleges.length})
              </div>
              {filteredColleges.map((college) => (
                <div
                  key={college.id}
                  onClick={() => {
                    onClose();
                    onSelectCollege(college);
                  }}
                  className="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center text-primary shrink-0 group-hover:bg-primary-fixed">
                      <span className="material-symbols-outlined text-[18px]">account_balance</span>
                    </div>
                    <div className="min-w-0">
                      <p className="font-body-sm font-semibold text-on-surface truncate">
                        {college.name}
                      </p>
                      <p className="font-label-sm text-secondary truncate text-[12px]">
                        {college.district} District • {college.category} • {college.principalName}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className="font-code-sm text-[11px] text-secondary bg-surface-container px-1.5 py-0.5 rounded">
                      AISHE {college.aisheCode}
                    </span>
                    <span className="material-symbols-outlined text-[16px] text-secondary group-hover:text-primary">
                      chevron_right
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Quick Actions */}
          {quickActions.length > 0 && (
            <div className="py-2">
              <div className="px-3 pb-1 text-[11px] font-label-sm uppercase font-semibold text-secondary tracking-wider">
                Quick Actions
              </div>
              {quickActions.map((action, i) => (
                <div
                  key={i}
                  onClick={action.action}
                  className="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center text-on-surface shrink-0 group-hover:bg-primary-fixed group-hover:text-primary">
                      <span className="material-symbols-outlined text-[18px]">{action.icon}</span>
                    </div>
                    <div>
                      <p className="font-body-sm font-semibold text-on-surface">{action.title}</p>
                      <p className="font-label-sm text-secondary text-[12px]">{action.desc}</p>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-[16px] text-secondary group-hover:text-primary">
                    arrow_forward
                  </span>
                </div>
              ))}
            </div>
          )}

          {filteredColleges.length === 0 && quickActions.length === 0 && (
            <div className="py-8 text-center text-secondary">
              <span className="material-symbols-outlined text-[36px] mb-2 opacity-50">search_off</span>
              <p className="font-body-sm">No institutions found matching "{query}"</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-2 bg-surface-container-low border-t border-[#e2e8f0] flex items-center justify-between text-[11px] text-secondary font-label-sm">
          <span>Navigate with mouse or arrow keys</span>
          <span>Tamil Nadu Higher Ed Registry 2024–25</span>
        </div>
      </div>
    </div>
  );
};
