import React from 'react';
import { NavScreen } from '../types';

interface SidebarProps {
  currentScreen: NavScreen;
  onNavigate: (screen: NavScreen) => void;
  sheetsConnected?: boolean;
  gmailActive?: boolean;
  isOpenMobile?: boolean;
  onCloseMobile?: () => void;
  collegeCount?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentScreen,
  onNavigate,
  sheetsConnected = false,
  gmailActive = false,
  isOpenMobile = false,
  onCloseMobile,
  collegeCount = 125
}) => {
  const navItems: { id: NavScreen; label: string; icon: string; countBadge?: number }[] = [
    { id: 'dashboard', label: 'Dashboard', icon: 'dashboard' },
    { id: 'college-contacts', label: 'College Contacts', icon: 'school', countBadge: collegeCount },
    { id: 'import-contacts', label: 'Import Contacts', icon: 'cloud_upload' },
    { id: 'website-research', label: 'Website Research', icon: 'travel_explore' },
    { id: 'email-templates', label: 'Email Templates', icon: 'mark_email_read' },
    { id: 'campaigns', label: 'Campaigns', icon: 'campaign' },
    { id: 'send-history', label: 'Send History', icon: 'schedule_send' },
    { id: 'settings', label: 'Settings', icon: 'tune' },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpenMobile && (
        <div 
          className="fixed inset-0 bg-black/40 z-40 lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={`fixed left-0 top-0 h-full w-64 bg-surface-container-lowest z-50 flex flex-col justify-between shadow-[0_1px_8px_rgba(0,0,0,0.04)] border-r border-[#e2e8f0] transition-transform duration-200 lg:translate-x-0 ${
          isOpenMobile ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="flex flex-col">
          {/* Logo Brand Header */}
          <div className="h-16 px-space-md flex items-center justify-between bg-surface-container-lowest border-b border-[#f1f5f9]">
            <div className="flex items-center gap-space-sm cursor-pointer" onClick={() => onNavigate('dashboard')}>
              <img
                alt="TN Outreach Logo"
                className="h-8 w-auto object-contain"
                src="https://lh3.googleusercontent.com/aida/AEtjO1UDvUPKsHO2eCbKhZ_OUdz1hYZLKRyxRPgWH_b0hwKoiKW4kh3-aodYHT8bFRNyxo2cFhlaN_qifljSj0xXudYJxFU_VQADcbdipXxZjdK8i0tmpgqB_WYlVCPzQILKxNtZw8pM7X05SN6-w32oB-6OZCMStnxT3omx9Ty9bXOjrmBWERFwrJ8Z_eatDpO1_oxiMFbivr1zi9euSxJ96b8IDpcRLmMRn6MY0fAjzEkIqaChuxlzi-pD-g"
              />
              <div className="flex flex-col">
                <span className="font-headline-sm text-headline-sm text-primary tracking-tight leading-none font-bold">
                  TN Outreach
                </span>
                <span className="font-label-sm text-label-sm text-secondary">
                  Higher Ed Directorate
                </span>
              </div>
            </div>

            {/* Mobile close button */}
            <button
              onClick={onCloseMobile}
              className="lg:hidden p-1 text-secondary hover:text-on-surface"
            >
              <span className="material-symbols-outlined text-[20px]">close</span>
            </button>
          </div>

          {/* Nav List */}
          <nav className="flex flex-col gap-space-xs px-space-sm pt-space-md">
            {navItems.map((item) => {
              const isActive = currentScreen === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onNavigate(item.id);
                    if (onCloseMobile) onCloseMobile();
                  }}
                  className={`w-full flex items-center justify-between px-space-sm py-2 rounded-lg transition-all text-left group ${
                    isActive
                      ? 'bg-primary-container text-on-primary-container font-semibold shadow-sm'
                      : 'text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface'
                  }`}
                >
                  <div className="flex items-center gap-space-sm">
                    <span className={`material-symbols-outlined text-[20px] ${
                      isActive ? 'text-on-primary-container' : 'text-secondary group-hover:text-on-surface'
                    }`}>
                      {item.icon}
                    </span>
                    <span className="font-label-lg text-label-lg">{item.label}</span>
                  </div>
                  {item.countBadge && !isActive && (
                    <span className="font-code-sm text-[10px] text-secondary bg-surface-container px-1.5 py-0.5 rounded">
                      {item.countBadge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Bottom Integrations Widget */}
        <div className="p-space-sm">
          <div className="bg-surface-container-low p-space-sm rounded-lg flex flex-col gap-space-sm border border-[#e2e8f0]/60">
            <div className="flex items-center justify-between">
              <span className="font-label-sm text-label-sm text-secondary uppercase font-semibold">
                Integrations Status
              </span>
              <span className="material-symbols-outlined text-[16px] text-secondary">
                hub
              </span>
            </div>
            
            <div className="flex flex-col gap-space-xs">
              <div 
                className="flex items-center justify-between py-1 cursor-pointer hover:bg-surface-container-lowest/50 px-1 rounded transition-colors"
                onClick={() => onNavigate('settings')}
              >
                <span className="font-body-sm text-body-sm text-on-surface">Google Sheets</span>
                <span className={`px-2 py-0.5 rounded text-[11px] font-semibold ${
                  sheetsConnected 
                    ? 'bg-emerald-100 text-emerald-800' 
                    : 'bg-surface-container text-secondary'
                }`}>
                  {sheetsConnected ? 'Active Sync' : 'Not configured'}
                </span>
              </div>

              <div 
                className="flex flex-col gap-0.5 py-1 cursor-pointer hover:bg-surface-container-lowest/50 px-1 rounded transition-colors"
                onClick={() => onNavigate('settings')}
              >
                <div className="flex items-center justify-between">
                  <span className="font-body-sm text-body-sm text-on-surface">Gmail API</span>
                  <span className={`px-2 py-0.5 rounded text-[11px] font-semibold ${
                    gmailActive 
                      ? 'bg-sky-100 text-sky-800' 
                      : 'bg-error-container text-on-error-container'
                  }`}>
                    {gmailActive ? 'Sandbox Live' : 'Demo Mode'}
                  </span>
                </div>
                <span className="font-label-sm text-label-sm text-secondary">
                  {gmailActive ? 'Simulated SMTP Active' : 'Gateway disconnected'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};
