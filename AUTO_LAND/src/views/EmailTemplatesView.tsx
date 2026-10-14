import React, { useState } from 'react';
import { EmailTemplate, CollegeContact } from '../types';

interface EmailTemplatesViewProps {
  templates: EmailTemplate[];
  colleges: CollegeContact[];
  onSaveTemplate: (template: EmailTemplate) => void;
  onSendTestEmail: (college: CollegeContact, templateTitle: string) => void;
  onTriggerToast: (msg: string, icon?: string) => void;
}

export const EmailTemplatesView: React.FC<EmailTemplatesViewProps> = ({
  templates,
  colleges,
  onSaveTemplate,
  onSendTestEmail,
  onTriggerToast
}) => {
  const [selectedTemplateId, setSelectedTemplateId] = useState<string>(templates[0]?.id || 'tpl-1');
  const [previewCollegeId, setPreviewCollegeId] = useState<string>(colleges[0]?.id || '');
  
  const currentTemplate = templates.find(t => t.id === selectedTemplateId) || templates[0];
  const previewCollege = colleges.find(c => c.id === previewCollegeId) || colleges[0];

  const [editSubject, setEditSubject] = useState(currentTemplate?.subject || '');
  const [editBody, setEditBody] = useState(currentTemplate?.body || '');
  const [editTitle, setEditTitle] = useState(currentTemplate?.title || '');

  // Keep editor in sync when switching template
  const handleSelectTemplate = (tpl: EmailTemplate) => {
    setSelectedTemplateId(tpl.id);
    setEditTitle(tpl.title);
    setEditSubject(tpl.subject);
    setEditBody(tpl.body);
  };

  const handleInsertTag = (tag: string) => {
    setEditBody(prev => prev + ` {{${tag}}}`);
  };

  const handleSave = () => {
    const updated: EmailTemplate = {
      ...currentTemplate,
      title: editTitle,
      subject: editSubject,
      body: editBody,
      lastModified: new Date().toISOString().slice(0, 10)
    };
    onSaveTemplate(updated);
    onTriggerToast(`Saved template "${updated.title}" successfully`, 'save');
  };

  // Interpolate body for live preview
  const interpolatedBody = editBody
    .replace(/{{College_Name}}/g, previewCollege.name)
    .replace(/{{Principal_Name}}/g, previewCollege.principalName)
    .replace(/{{District}}/g, previewCollege.district)
    .replace(/{{Zone}}/g, previewCollege.zone)
    .replace(/{{AISHE_Code}}/g, previewCollege.aisheCode)
    .replace(/{{Placement_Officer}}/g, previewCollege.placementOfficerName || 'Placement Officer');

  const interpolatedSubject = editSubject
    .replace(/{{College_Name}}/g, previewCollege.name)
    .replace(/{{District}}/g, previewCollege.district)
    .replace(/{{AISHE_Code}}/g, previewCollege.aisheCode);

  return (
    <div className="flex flex-col w-full pb-space-xl space-y-space-lg">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="font-code-sm text-code-sm uppercase tracking-widest text-primary font-bold">
            Outreach Communications
          </span>
          <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
          <span className="font-code-sm text-code-sm text-secondary">
            Collegiate Message Standard
          </span>
        </div>
        <h1 className="font-headline-lg text-headline-lg text-on-surface font-bold tracking-tight">
          Official Email Templates
        </h1>
        <p className="font-body-md text-body-md text-secondary mt-0.5">
          Statutory notification formats, curriculum alignment requests, and grant announcements.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        {/* Left Column: Template Selector & Editor (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-space-md">
          {/* Template Tabs Carousel */}
          <div className="bg-surface-container-lowest p-space-sm rounded-lg shadow-sm border border-[#e2e8f0]">
            <span className="font-label-sm uppercase font-semibold text-secondary px-2 block mb-2">
              Template Repository ({templates.length})
            </span>
            <div className="space-y-1.5">
              {templates.map((tpl) => {
                const isSelected = tpl.id === selectedTemplateId;
                return (
                  <div
                    key={tpl.id}
                    onClick={() => handleSelectTemplate(tpl)}
                    className={`p-2.5 rounded-lg border transition-all cursor-pointer flex items-center justify-between ${
                      isSelected
                        ? 'bg-primary-50/70 border-primary/40 shadow-2xs'
                        : 'border-[#e2e8f0] hover:bg-surface-container-low'
                    }`}
                  >
                    <div className="min-w-0 pr-2">
                      <div className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${isSelected ? 'bg-primary' : 'bg-secondary'}`} />
                        <h4 className="font-body-sm font-semibold text-on-surface truncate">
                          {tpl.title}
                        </h4>
                      </div>
                      <p className="font-label-sm text-secondary truncate mt-0.5 text-[11px] pl-4">
                        {tpl.subject}
                      </p>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className="font-code-sm text-[10px] bg-surface-container px-1.5 py-0.5 rounded text-secondary">
                        {tpl.stats.openRate} open
                      </span>
                      <span className="material-symbols-outlined text-[16px] text-secondary">
                        {isSelected ? 'check' : 'chevron_right'}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Template Editor */}
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0] space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="font-headline-sm font-bold text-on-surface">Template Editor</h3>
              <span className="text-xs text-secondary font-code-sm">Last modified: {currentTemplate.lastModified}</span>
            </div>

            <div>
              <label className="block text-xs font-semibold text-secondary mb-1">Template Title</label>
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm font-semibold text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-secondary mb-1">Email Subject Line</label>
              <input
                type="text"
                value={editSubject}
                onChange={(e) => setEditSubject(e.target.value)}
                className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary"
              />
            </div>

            {/* Merge Tag Pills */}
            <div>
              <span className="block text-[11px] font-semibold text-secondary mb-1.5 uppercase">
                Available Dynamic Tags (Click to insert):
              </span>
              <div className="flex flex-wrap gap-1.5">
                {[
                  'College_Name',
                  'Principal_Name',
                  'District',
                  'Zone',
                  'AISHE_Code',
                  'Placement_Officer'
                ].map(tag => (
                  <button
                    key={tag}
                    type="button"
                    onClick={() => handleInsertTag(tag)}
                    className="px-2 py-0.5 bg-surface-container hover:bg-surface-container-high rounded text-xs font-code-sm text-on-surface border border-[#cbd5e1]/60 transition-colors"
                  >
                    + &#123;&#123;{tag}&#125;&#125;
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-secondary mb-1">Email Body Content</label>
              <textarea
                rows={11}
                value={editBody}
                onChange={(e) => setEditBody(e.target.value)}
                className="w-full bg-surface-container-low px-3 py-2 rounded-lg font-body-sm text-xs text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary font-mono leading-relaxed"
              />
            </div>

            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-secondary">
                Compliance: Standard Government of Tamil Nadu signature included
              </span>
              <button
                onClick={handleSave}
                className="px-4 py-2 bg-primary text-white rounded-lg font-label-md font-semibold hover:bg-primary-container shadow-sm flex items-center gap-1.5"
              >
                <span className="material-symbols-outlined text-[18px]">save</span>
                <span>Save Template</span>
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Live Interpolated Preview (5 cols) */}
        <div className="lg:col-span-5 flex flex-col gap-space-md">
          <div className="bg-surface-container-lowest p-space-lg rounded-lg shadow-sm border border-[#e2e8f0]">
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="font-headline-sm font-bold text-on-surface">Live Variable Preview</h3>
                <p className="text-xs text-secondary">See how email renders for target campus</p>
              </div>
              <span className="bg-surface-container text-secondary px-2 py-0.5 rounded text-[10px] font-bold uppercase">
                Render Test
              </span>
            </div>

            {/* Test College Selector */}
            <div className="mb-3">
              <label className="block text-xs text-secondary mb-1 font-semibold">Test against Institution:</label>
              <select
                value={previewCollegeId}
                onChange={(e) => setPreviewCollegeId(e.target.value)}
                className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-xs font-semibold text-on-surface border border-[#e2e8f0]"
              >
                {colleges.map(c => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.district})
                  </option>
                ))}
              </select>
            </div>

            {/* Simulated Email Envelope */}
            <div className="border border-[#cbd5e1] rounded-xl overflow-hidden bg-white shadow-sm">
              <div className="bg-surface-container-low p-3 border-b border-[#e2e8f0] text-xs space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-secondary font-medium">From:</span>
                  <span className="font-semibold text-on-surface">karthik.raja@tn.gov.in (TN Higher Ed Directorate)</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-secondary font-medium">To:</span>
                  <span className="font-code-sm text-primary font-bold">{previewCollege.principalEmail}</span>
                </div>
                <div className="flex items-start justify-between pt-1 border-t border-[#e2e8f0]/60">
                  <span className="text-secondary font-medium">Subject:</span>
                  <span className="font-semibold text-on-surface ml-2 text-right">{interpolatedSubject}</span>
                </div>
              </div>

              {/* Email Content Body */}
              <div className="p-4 text-xs font-body-sm text-[#0b1c30] whitespace-pre-wrap leading-relaxed max-h-96 overflow-y-auto">
                {interpolatedBody}
              </div>
            </div>

            <button
              onClick={() => onSendTestEmail(previewCollege, editTitle)}
              className="w-full mt-4 py-2 bg-primary-container text-on-primary hover:opacity-95 rounded-lg font-label-md font-semibold flex items-center justify-center gap-2 shadow-sm transition-all cursor-pointer"
            >
              <span className="material-symbols-outlined text-[18px]">send</span>
              <span>Send Test Preview Email</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
