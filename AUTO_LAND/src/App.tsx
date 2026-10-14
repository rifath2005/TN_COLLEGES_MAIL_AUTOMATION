import React, { useState, useEffect } from 'react';
import { 
  NavScreen, 
  CollegeContact, 
  SystemStats, 
  ActivityFeedItem, 
  EmailTemplate, 
  Campaign, 
  DispatchAuditRecord 
} from './types';
import { 
  initialColleges, 
  initialSystemStats, 
  initialActivities, 
  initialTemplates, 
  initialCampaigns, 
  initialAuditLogs 
} from './data/mockData';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { Toast, ToastMessage } from './components/Toast';
import { CommandPalette } from './components/CommandPalette';
import { NewCampaignModal } from './components/NewCampaignModal';
import { CollegeDetailModal } from './components/CollegeDetailModal';

// Views
import { DashboardView } from './views/DashboardView';
import { CollegeContactsView } from './views/CollegeContactsView';
import { ImportContactsView } from './views/ImportContactsView';
import { WebsiteResearchView } from './views/WebsiteResearchView';
import { EmailTemplatesView } from './views/EmailTemplatesView';
import { CampaignsView } from './views/CampaignsView';
import { SendHistoryView } from './views/SendHistoryView';
import { SettingsView } from './views/SettingsView';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<NavScreen>('dashboard');
  const [colleges, setColleges] = useState<CollegeContact[]>(initialColleges);
  const [stats, setStats] = useState<SystemStats>(initialSystemStats);
  const [activities, setActivities] = useState<ActivityFeedItem[]>(initialActivities);
  const [templates, setTemplates] = useState<EmailTemplate[]>(initialTemplates);
  const [campaigns, setCampaigns] = useState<Campaign[]>(initialCampaigns);
  const [auditLogs, setAuditLogs] = useState<DispatchAuditRecord[]>(initialAuditLogs);

  // Modals & Drawers
  const [isCampaignModalOpen, setIsCampaignModalOpen] = useState(false);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
  const [selectedCollegeModal, setSelectedCollegeModal] = useState<CollegeContact | null>(null);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [toast, setToast] = useState<ToastMessage | null>(null);
  const [contactsFilter, setContactsFilter] = useState<string>('');

  // Integrations state & Live Backend
  const [sheetsConnected, setSheetsConnected] = useState(false);
  const [gmailActive, setGmailActive] = useState(true);
  const [activeCsv, setActiveCsv] = useState<string>('contacts.csv');
  const [senderEmail, setSenderEmail] = useState<string>('babsword3@gmail.com');
  const [isDispatching, setIsDispatching] = useState<boolean>(false);

  // Officer Profile State (persisted to localStorage)
  const [officerName, setOfficerName] = useState<string>(() => {
    return localStorage.getItem('tn_outreach_officer_name') || 'Karthik Raja';
  });
  const [officerEmail, setOfficerEmail] = useState<string>(() => {
    return localStorage.getItem('tn_outreach_officer_email') || 'karthik.raja@tn.gov.in';
  });
  const [officerZone, setOfficerZone] = useState<string>(() => {
    return localStorage.getItem('tn_outreach_officer_zone') || 'Chennai Central (Zone 01)';
  });

  const handleUpdateOfficer = (name: string, email: string, zone: string) => {
    setOfficerName(name);
    setOfficerEmail(email);
    setOfficerZone(zone);
    try {
      localStorage.setItem('tn_outreach_officer_name', name);
      localStorage.setItem('tn_outreach_officer_email', email);
      localStorage.setItem('tn_outreach_officer_zone', zone);
    } catch (e) {}
  };

  // Global toast trigger
  const triggerToast = (message: string, icon: string = 'info') => {
    setToast({
      id: String(Date.now()),
      message,
      icon
    });
  };

  // Fetch live state from backend
  const loadBackendData = (csvToLoad: string = activeCsv) => {
    fetch(`/api/init?csv=${csvToLoad}`)
      .then(res => res.json())
      .then(data => {
        if (data.colleges && data.colleges.length > 0) {
          setColleges(data.colleges);
        }
        if (data.stats) {
          setStats(data.stats);
        }
        if (data.templates && data.templates.length > 0) {
          setTemplates(data.templates);
        }
        if (data.auditLogs && data.auditLogs.length > 0) {
          setAuditLogs(data.auditLogs);
        }
        if (data.activities && data.activities.length > 0) {
          setActivities(data.activities);
        }
        if (data.config) {
          if (data.config.senderEmail) setSenderEmail(data.config.senderEmail);
          if (data.config.gmailActive !== undefined) setGmailActive(data.config.gmailActive);
        }
      })
      .catch(err => {
        console.warn('Backend live sync notice:', err);
      });
  };

  useEffect(() => {
    loadBackendData(activeCsv);
  }, [activeCsv]);

  // Keyboard shortcut ⌘K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Auto-dismiss toast
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => {
      setToast(null);
    }, 3800);
    return () => clearTimeout(timer);
  }, [toast]);

  // Navigate handler with optional filter
  const handleNavigate = (screen: NavScreen, filter?: string) => {
    setCurrentScreen(screen);
    if (filter) {
      setContactsFilter(filter);
    } else {
      setContactsFilter('');
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Select college by name (e.g. from live feed)
  const handleSelectCollegeByName = (name: string) => {
    const found = colleges.find(c => 
      c.name.toLowerCase().includes(name.toLowerCase()) || 
      (c.shortName && c.shortName.toLowerCase().includes(name.toLowerCase()))
    );
    if (found) {
      setSelectedCollegeModal(found);
    } else {
      triggerToast(`Showing records for ${name}`, 'info');
      handleNavigate('college-contacts', name);
    }
  };

  // Schedule / Create Campaign
  const handleScheduleCampaign = (newCamp: Partial<Campaign>) => {
    const id = `cmp-${Date.now()}`;
    const targetCount = newCamp.targetCount || colleges.length;
    const campaignRecord: Campaign = {
      id,
      name: newCamp.name || 'Shortfundly Campus Outreach Wave',
      targetZone: newCamp.targetZone || 'Tamil Nadu Higher Education Institutions',
      templateId: newCamp.templateId || 'tpl-shortfundly',
      templateName: newCamp.templateName || 'Shortfundly Campus Collaboration Proposal',
      status: 'In Progress',
      targetCount,
      sentCount: 0,
      deliveredCount: 0,
      bouncedCount: 0,
      createdAt: 'Just now',
      velocityThrottle: newCamp.velocityThrottle || 45
    };

    setCampaigns(prev => [campaignRecord, ...prev]);

    const newActivity: ActivityFeedItem = {
      id: `act-${Date.now()}`,
      collegeName: `Campaign Launched: ${campaignRecord.name}`,
      action: 'Batch Dispatched',
      description: `Targeting ${targetCount} institutions with 2-second rate throttling`,
      timeAgo: 'Just now',
      statusBadge: 'Active',
      statusType: 'sent',
      subBadge: campaignRecord.targetZone.slice(0, 24),
      icon: 'rocket_launch',
      iconBg: 'bg-primary-container',
      iconColor: 'text-on-primary'
    };
    setActivities(prev => [newActivity, ...prev]);

    triggerToast(`Campaign Scheduled! Triggering live batch delivery engine...`, 'mark_email_read');
    handleRunBatch(false);
  };

  // Single test email (Live transmission via Gmail SMTP)
  const handleSendTestEmail = async (college: CollegeContact, templateTitle?: string) => {
    triggerToast(`Dispatching live outreach to ${college.principalEmail}...`, 'send');
    setIsDispatching(true);
    try {
      const res = await fetch('/api/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: college.principalEmail,
          collegeName: college.name,
          templateTitle: templateTitle || 'Shortfundly Campus Proposal',
          csv: activeCsv,
          force: true
        })
      });
      const data = await res.json();
      if (data.success) {
        triggerToast(`Email delivered successfully to ${college.principalEmail}!`, 'mark_email_read');
        loadBackendData(activeCsv);
      } else {
        triggerToast(`Transmission notice: ${data.error || data.output || 'Complete'}`, 'info');
        loadBackendData(activeCsv);
      }
    } catch (err) {
      triggerToast(`Network error: ${(err as Error).message}`, 'error');
    } finally {
      setIsDispatching(false);
    }
  };

  // Quick test send to babsword6@gmail.com
  const handleQuickTestSend = async () => {
    triggerToast('Sending real test email to babsword6@gmail.com...', 'send');
    setIsDispatching(true);
    try {
      const res = await fetch('/api/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: 'babsword6@gmail.com',
          collegeName: 'MR Test College of Engineering',
          templateTitle: 'Shortfundly Campus Collaboration Test',
          csv: 'test_contacts.csv',
          force: true
        })
      });
      const data = await res.json();
      if (data.success) {
        triggerToast('Test email successfully delivered to babsword6@gmail.com!', 'mark_email_read');
        loadBackendData(activeCsv);
      } else {
        triggerToast(`Test dispatch notice: ${data.error || 'Check server logs'}`, 'info');
        loadBackendData(activeCsv);
      }
    } catch (err) {
      triggerToast(`Error: ${(err as Error).message}`, 'error');
    } finally {
      setIsDispatching(false);
    }
  };

  // Real Batch Outreach
  const handleRunBatch = async (dryRun: boolean = false) => {
    triggerToast(dryRun ? 'Running dry-run simulation across dataset...' : 'Launching production batch outreach...', 'rocket_launch');
    setIsDispatching(true);
    try {
      const res = await fetch('/api/send-batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dryRun,
          csv: activeCsv,
          force: false
        })
      });
      const data = await res.json();
      if (data.success) {
        triggerToast(dryRun ? 'Dry run completed successfully!' : 'Batch outreach completed!', 'check_circle');
        loadBackendData(activeCsv);
      } else {
        triggerToast(`Batch notice: ${data.error || 'Check logs'}`, 'info');
        loadBackendData(activeCsv);
      }
    } catch (err) {
      triggerToast(`Error: ${(err as Error).message}`, 'error');
    } finally {
      setIsDispatching(false);
    }
  };

  // Save template to backend
  const handleSaveTemplate = async (tpl: EmailTemplate) => {
    setTemplates(prev => prev.map(t => t.id === tpl.id ? tpl : t));
    try {
      await fetch('/api/save-template', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject: tpl.subject,
          body: tpl.body
        })
      });
      triggerToast(`Template "${tpl.title}" saved to disk and backend engine!`, 'save');
    } catch (err) {
      triggerToast(`Saved locally. Network notice: ${(err as Error).message}`, 'info');
    }
  };

  // Add new college to active CSV
  const handleAddCollege = async (newCollege: CollegeContact) => {
    setColleges(prev => [newCollege, ...prev]);
    try {
      await fetch('/api/add-contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newCollege.name,
          district: newCollege.district,
          email: newCollege.principalEmail,
          phone: newCollege.phone,
          website: newCollege.website,
          principalName: newCollege.principalName,
          csv: activeCsv
        })
      });
      loadBackendData(activeCsv);
      triggerToast(`Added ${newCollege.name} to ${activeCsv}!`, 'check_circle');
    } catch (e) {
      triggerToast(`Added locally.`, 'info');
    }
  };

  // Simulate Campaign progress stream
  const handleSimulateBatch = (campaignId: string, count: number) => {
    setCampaigns(prev => prev.map(c => {
      if (c.id === campaignId) {
        const nextSent = Math.min(c.targetCount, c.sentCount + count);
        const isFinished = nextSent >= c.targetCount;
        return {
          ...c,
          sentCount: nextSent,
          deliveredCount: c.deliveredCount + count,
          status: isFinished ? 'Completed' : 'In Progress'
        };
      }
      return c;
    }));

    setStats(prev => ({
      ...prev,
      dispatched: prev.dispatched + count
    }));
  };

  // Update college in list
  const handleUpdateCollege = (updated: CollegeContact) => {
    setColleges(prev => prev.map(c => c.id === updated.id ? updated : c));
    if (selectedCollegeModal?.id === updated.id) {
      setSelectedCollegeModal(updated);
    }
  };

  // Refresh data
  const handleRefreshData = () => {
    loadBackendData(activeCsv);
  };

  return (
    <div className="bg-background min-h-screen text-on-surface flex flex-col font-body-md antialiased selection:bg-[#ffdad6] selection:text-[#410002]">
      {/* Toast Notification Container */}
      <Toast toast={toast} onClose={() => setToast(null)} />

      {/* Sidebar Navigation Rail */}
      <Sidebar
        currentScreen={currentScreen}
        onNavigate={handleNavigate}
        sheetsConnected={sheetsConnected}
        gmailActive={gmailActive}
        isOpenMobile={isMobileSidebarOpen}
        onCloseMobile={() => setIsMobileSidebarOpen(false)}
        collegeCount={colleges.length || stats.totalColleges}
      />

      {/* Main Layout Area */}
      <div className="pl-0 lg:pl-64 flex flex-col min-h-screen transition-all">
        {/* Global Header */}
        <Header
          onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
          onNavigate={handleNavigate}
          onOpenMobileMenu={() => setIsMobileSidebarOpen(true)}
          onTriggerToast={triggerToast}
          officerName={officerName}
          officerEmail={officerEmail}
        />

        {/* Content Canvas */}
        <main className="w-full pt-16 bg-background px-space-md lg:px-space-lg min-h-screen flex-1">
          <div className="pt-space-md">
            {currentScreen === 'dashboard' && (
              <DashboardView
                stats={stats}
                activities={activities}
                colleges={colleges}
                onOpenCampaignModal={() => setIsCampaignModalOpen(true)}
                onNavigate={handleNavigate}
                onTriggerToast={triggerToast}
                onSelectCollegeByName={handleSelectCollegeByName}
                onRefreshData={handleRefreshData}
                gmailActive={gmailActive}
                senderEmail={senderEmail}
                activeCsv={activeCsv}
                onSwitchCsv={(csv) => setActiveCsv(csv)}
                onQuickTestSend={handleQuickTestSend}
                onRunBatch={handleRunBatch}
                isDispatching={isDispatching}
                officerName={officerName}
              />
            )}

            {currentScreen === 'college-contacts' && (
              <CollegeContactsView
                colleges={colleges}
                initialFilter={contactsFilter}
                onSelectCollege={(c) => setSelectedCollegeModal(c)}
                onSendTestEmail={handleSendTestEmail}
                onAddCollege={handleAddCollege}
                onTriggerToast={triggerToast}
                onOpenCampaignModal={() => setIsCampaignModalOpen(true)}
              />
            )}

            {currentScreen === 'import-contacts' && (
              <ImportContactsView
                onImportSuccess={(count) => {
                  setSheetsConnected(true);
                  loadBackendData(activeCsv);
                }}
                onTriggerToast={triggerToast}
              />
            )}

            {currentScreen === 'website-research' && (
              <WebsiteResearchView
                colleges={colleges}
                onEnrichCollege={handleUpdateCollege}
                onTriggerToast={triggerToast}
              />
            )}

            {currentScreen === 'email-templates' && (
              <EmailTemplatesView
                templates={templates}
                colleges={colleges}
                onSaveTemplate={handleSaveTemplate}
                onSendTestEmail={handleSendTestEmail}
                onTriggerToast={triggerToast}
              />
            )}

            {currentScreen === 'campaigns' && (
              <CampaignsView
                campaigns={campaigns}
                colleges={colleges}
                onOpenCampaignModal={() => setIsCampaignModalOpen(true)}
                onSimulateBatch={handleSimulateBatch}
                onTriggerToast={triggerToast}
              />
            )}

            {currentScreen === 'send-history' && (
              <SendHistoryView
                auditLogs={auditLogs}
                onTriggerToast={triggerToast}
                onNavigateToResearch={() => handleNavigate('website-research')}
              />
            )}

            {currentScreen === 'settings' && (
              <SettingsView
                stats={stats}
                onUpdateStats={(newSt) => setStats(prev => ({ ...prev, ...newSt }))}
                sheetsConnected={sheetsConnected}
                onToggleSheets={setSheetsConnected}
                gmailActive={gmailActive}
                onToggleGmail={setGmailActive}
                onTriggerToast={triggerToast}
                officerName={officerName}
                officerEmail={officerEmail}
                officerZone={officerZone}
                onUpdateOfficer={handleUpdateOfficer}
              />
            )}
          </div>
        </main>
      </div>

      {/* Global Interactive Modals */}
      <NewCampaignModal
        isOpen={isCampaignModalOpen}
        onClose={() => setIsCampaignModalOpen(false)}
        templates={templates}
        onScheduleCampaign={handleScheduleCampaign}
      />

      <CollegeDetailModal
        college={selectedCollegeModal}
        onClose={() => setSelectedCollegeModal(null)}
        onUpdate={handleUpdateCollege}
        onSendTestEmail={handleSendTestEmail}
      />

      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        colleges={colleges}
        onSelectCollege={(c) => setSelectedCollegeModal(c)}
        onNavigate={handleNavigate}
        onOpenCampaignModal={() => setIsCampaignModalOpen(true)}
      />
    </div>
  );
}
