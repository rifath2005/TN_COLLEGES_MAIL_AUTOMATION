import React, { useState } from 'react';
import { NavScreen } from '../types';

interface HeaderProps {
  onOpenCommandPalette: () => void;
  onNavigate: (screen: NavScreen) => void;
  onOpenMobileMenu: () => void;
  onTriggerToast: (msg: string, icon?: string) => void;
  officerName?: string;
  officerEmail?: string;
}

export const Header: React.FC<HeaderProps> = ({
  onOpenCommandPalette,
  onNavigate,
  onOpenMobileMenu,
  onTriggerToast,
  officerName = 'Karthik Raja',
  officerEmail = 'karthik.raja@tn.gov.in'
}) => {
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className="fixed top-0 left-0 lg:left-64 right-0 h-16 bg-surface-container-lowest/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)] z-40 flex items-center justify-between px-space-md lg:px-space-lg border-b border-[#e2e8f0]/80">
      {/* Left: Mobile Toggle & Breadcrumbs & Search */}
      <div className="flex items-center gap-space-sm lg:gap-space-md flex-1 max-w-2xl">
        <button
          onClick={onOpenMobileMenu}
          className="p-1.5 rounded-lg text-secondary hover:text-on-surface hover:bg-surface-container-high lg:hidden"
        >
          <span className="material-symbols-outlined text-[24px]">menu</span>
        </button>

        <div className="hidden sm:flex items-center gap-space-xs font-label-md text-label-md text-secondary whitespace-nowrap">
          <span
            className="hover:text-on-surface cursor-pointer transition-colors"
            onClick={() => onNavigate('dashboard')}
          >
            Higher Ed
          </span>
          <span>/</span>
          <span className="text-on-surface font-semibold truncate">
            Tamil Nadu Outreach Directorate
          </span>
        </div>

        {/* Global Quick Search */}
        <div 
          onClick={onOpenCommandPalette}
          className="relative flex items-center w-full max-w-sm sm:max-w-md cursor-pointer group ml-1"
        >
          <span className="material-symbols-outlined absolute left-3 text-[18px] text-secondary group-hover:text-primary transition-colors">
            search
          </span>
          <input
            readOnly
            className="w-full pl-9 pr-12 py-1.5 bg-surface-container-low hover:bg-surface-container/70 rounded-lg font-body-sm text-body-sm text-on-surface placeholder:text-secondary focus:outline-none cursor-pointer transition-colors border border-transparent hover:border-[#cbd5e1]"
            placeholder="Search 38 districts & verified TN colleges..."
            type="text"
          />
          <span className="absolute right-3 font-code-sm text-code-sm text-secondary bg-surface-container px-1.5 py-0.5 rounded shadow-2xs border border-[#cbd5e1]/40">
            ⌘K
          </span>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-space-sm lg:gap-space-md">
        {/* Live Status Badge */}
        <div className="hidden md:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container text-on-surface font-label-sm text-label-sm font-semibold border border-[#bec6e0]/60">
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
          Live Verified Roster
        </div>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => {
              setShowNotifications(!showNotifications);
              setShowProfileMenu(false);
            }}
            className="relative p-2 rounded-lg text-secondary hover:bg-surface-container-high hover:text-on-surface transition-colors"
            title="Notifications"
          >
            <span className="material-symbols-outlined text-[22px]">notifications</span>
            <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-primary ring-2 ring-white"></span>
          </button>

          {/* Notifications Dropdown */}
          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 bg-surface-container-lowest rounded-xl shadow-xl border border-[#e2e8f0] p-space-sm z-50 animate-in fade-in slide-in-from-top-2 duration-150">
              <div className="flex items-center justify-between pb-2 border-b border-[#f1f5f9] mb-2 px-1">
                <span className="font-label-md text-label-md font-semibold text-on-surface">Directorate Notifications</span>
                <span className="font-code-sm text-[11px] text-primary font-bold">3 New</span>
              </div>
              <div className="space-y-2 max-h-72 overflow-y-auto">
                <div 
                  className="p-2 rounded-lg hover:bg-surface-container-low transition-colors cursor-pointer text-left"
                  onClick={() => {
                    setShowNotifications(false);
                    onNavigate('send-history');
                  }}
                >
                  <p className="font-body-sm text-body-sm font-medium text-on-surface">Wave 04 Dispatches in progress</p>
                  <p className="font-label-sm text-label-sm text-secondary">15 of 125 institutions transmitted at 45 msgs/min</p>
                  <span className="font-code-sm text-[10px] text-secondary">10m ago</span>
                </div>
                <div 
                  className="p-2 rounded-lg hover:bg-surface-container-low transition-colors cursor-pointer text-left"
                  onClick={() => {
                    setShowNotifications(false);
                    onNavigate('college-contacts');
                  }}
                >
                  <p className="font-body-sm text-body-sm font-medium text-on-surface">AISHE Data Reconciled</p>
                  <p className="font-label-sm text-label-sm text-secondary">St. Joseph's College contacts refreshed via NIRF sync</p>
                  <span className="font-code-sm text-[10px] text-secondary">3h ago</span>
                </div>
                <div 
                  className="p-2 rounded-lg hover:bg-surface-container-low transition-colors cursor-pointer text-left"
                  onClick={() => {
                    setShowNotifications(false);
                    onNavigate('send-history');
                  }}
                >
                  <p className="font-body-sm text-body-sm font-medium text-error">1 Hard Bounce Detected</p>
                  <p className="font-label-sm text-label-sm text-secondary">NEC Kovilpatti: 550 5.1.1 user unknown</p>
                  <span className="font-code-sm text-[10px] text-secondary">8h ago</span>
                </div>
              </div>
              <div className="pt-2 border-t border-[#f1f5f9] mt-2 text-center">
                <button
                  onClick={() => {
                    setShowNotifications(false);
                    onNavigate('send-history');
                  }}
                  className="text-primary font-label-sm hover:underline font-semibold"
                >
                  View All Activity Feed
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Profile User Info */}
        <div className="relative">
          <div
            onClick={() => {
              setShowProfileMenu(!showProfileMenu);
              setShowNotifications(false);
            }}
            className="flex items-center gap-space-sm pl-space-xs sm:pl-space-sm cursor-pointer hover:opacity-85 transition-opacity"
          >
            <img
              alt="Profile"
              className="w-8 h-8 rounded-full object-cover ring-2 ring-primary/20"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuDVHYqUoO_9rJ7GYJL0n35V5UMR6MJwelYIa101n80Wx1IsH2qn1HqDfzryT-K76znV7z8nyAEkm7zGaXkXhco0S-ommzlRCeBOXzei1IjfWzbs0P6vrnank0lHfvJe4FyeSdHTSFTVsp3trR5RWaCgX8tXLzeDq6zDTAEv5FNnV2m8CWZJHsi3npw1T8wVE8-r1pn-ExhcexVOi6jzh-foNBGntadCd6beDuOkEDaI3EdC0BxCNopP"
            />
            <div className="hidden sm:flex flex-col text-left">
              <span className="font-label-md text-label-md text-on-surface font-semibold leading-tight">
                {officerName}
              </span>
              <span className="font-label-sm text-label-sm text-secondary leading-tight text-[11px]">
                Outreach Lead (Chennai Central)
              </span>
            </div>
            <span className="material-symbols-outlined text-[18px] text-secondary">
              expand_more
            </span>
          </div>

          {/* Profile Menu Dropdown */}
          {showProfileMenu && (
            <div className="absolute right-0 mt-2 w-56 bg-surface-container-lowest rounded-xl shadow-xl border border-[#e2e8f0] p-1.5 z-50 animate-in fade-in duration-150">
              <div className="px-3 py-2 border-b border-[#f1f5f9] mb-1">
                <p className="font-label-md text-on-surface font-semibold">{officerName}</p>
                <p className="font-label-sm text-secondary">{officerEmail}</p>
                <span className="inline-block mt-1 bg-surface-container text-secondary px-2 py-0.5 rounded text-[10px] font-code-sm">
                  Zone 01 Administrator
                </span>
              </div>
              <button
                onClick={() => {
                  setShowProfileMenu(false);
                  onNavigate('settings');
                }}
                className="w-full flex items-center gap-2 px-3 py-1.5 rounded-lg text-left text-on-surface hover:bg-surface-container-low text-body-sm"
              >
                <span className="material-symbols-outlined text-[18px] text-secondary">tune</span>
                Directorate Settings
              </button>
              <button
                onClick={() => {
                  setShowProfileMenu(false);
                  onTriggerToast('Switched to Zone 04 (Western Belt: Coimbatore)', 'swap_horiz');
                }}
                className="w-full flex items-center gap-2 px-3 py-1.5 rounded-lg text-left text-on-surface hover:bg-surface-container-low text-body-sm"
              >
                <span className="material-symbols-outlined text-[18px] text-secondary">swap_horiz</span>
                Switch Zone View
              </button>
              <button
                onClick={() => {
                  setShowProfileMenu(false);
                  onTriggerToast('Signed out of demo session. Session refreshed.', 'logout');
                }}
                className="w-full flex items-center gap-2 px-3 py-1.5 rounded-lg text-left text-error hover:bg-red-50 text-body-sm mt-1 border-t border-[#f1f5f9]"
              >
                <span className="material-symbols-outlined text-[18px]">logout</span>
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
