import React, { useState } from 'react';
import { CollegeContact } from '../types';

interface CollegeDetailModalProps {
  college: CollegeContact | null;
  onClose: () => void;
  onUpdate: (updated: CollegeContact) => void;
  onSendTestEmail: (college: CollegeContact) => void;
}

export const CollegeDetailModal: React.FC<CollegeDetailModalProps> = ({
  college,
  onClose,
  onUpdate,
  onSendTestEmail
}) => {
  if (!college) return null;

  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState<CollegeContact>({ ...college });

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdate(formData);
    setIsEditing(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#213145]/40 backdrop-blur-sm p-4 animate-in fade-in duration-150">
      <div className="fixed inset-0" onClick={onClose} />
      <div className="relative bg-surface-container-lowest rounded-xl shadow-2xl max-w-2xl w-full border border-[#cbd5e1] z-10 max-h-[90vh] flex flex-col overflow-hidden animate-in zoom-in-95 duration-150">
        
        {/* Header */}
        <div className="flex items-start justify-between p-space-md border-b border-[#e2e8f0] bg-surface-container-low/40">
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-primary shrink-0 border border-[#e2e8f0]">
              <span className="material-symbols-outlined text-[24px]">account_balance</span>
            </div>
            <div className="min-w-0">
              <h3 className="font-headline-sm text-headline-sm text-on-surface font-bold truncate">
                {college.name}
              </h3>
              <div className="flex items-center gap-2 mt-0.5 flex-wrap">
                <span className="font-code-sm text-code-sm text-primary font-bold bg-primary-fixed/50 px-2 py-0.5 rounded">
                  AISHE {college.aisheCode}
                </span>
                <span className="font-label-sm text-secondary bg-surface-container px-2 py-0.5 rounded">
                  {college.district} District ({college.zone})
                </span>
                <span className="font-label-sm text-secondary bg-surface-container px-2 py-0.5 rounded">
                  {college.category}
                </span>
                {college.autonomous && (
                  <span className="font-label-sm text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-semibold border border-emerald-200">
                    Autonomous
                  </span>
                )}
              </div>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="text-secondary hover:text-on-surface p-1 rounded-lg shrink-0 ml-2"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Content Body */}
        <div className="p-space-md overflow-y-auto space-y-4 flex-1">
          {/* Status & Deliverability Bar */}
          <div className="p-space-sm bg-surface-container-low rounded-lg border border-[#e2e8f0] flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${
                college.status === 'verified' 
                  ? 'bg-emerald-500' 
                  : college.status === 'pending'
                  ? 'bg-amber-500'
                  : 'bg-red-500'
              }`} />
              <div>
                <span className="font-label-md text-on-surface font-semibold capitalize">
                  Status: {college.status} Delivery Record
                </span>
                <p className="font-label-sm text-secondary">
                  {college.status === 'verified' 
                    ? 'MX server certified. Direct SMTP handshake validated.' 
                    : college.status === 'bounced' 
                    ? '550 5.1.1 Hard bounce logged on last delivery wave.' 
                    : 'Awaiting secondary directory confirmation.'}
                </p>
              </div>
            </div>

            <button
              onClick={() => onSendTestEmail(college)}
              className="h-8 px-3 rounded-lg bg-surface-container-lowest text-primary hover:bg-primary-fixed font-label-md font-semibold border border-[#e2e8f0] flex items-center gap-1.5 transition-colors cursor-pointer shadow-2xs"
            >
              <span className="material-symbols-outlined text-[16px]">forward_to_inbox</span>
              <span>Send Single Test</span>
            </button>
          </div>

          {isEditing ? (
            <form onSubmit={handleSave} className="space-y-3">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-label-sm text-secondary mb-1">Principal / Head Name</label>
                  <input
                    type="text"
                    value={formData.principalName}
                    onChange={(e) => setFormData({ ...formData, principalName: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg font-body-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                    required
                  />
                </div>
                <div>
                  <label className="block font-label-sm text-secondary mb-1">Principal Email</label>
                  <input
                    type="email"
                    value={formData.principalEmail}
                    onChange={(e) => setFormData({ ...formData, principalEmail: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg font-body-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                    required
                  />
                </div>
                <div>
                  <label className="block font-label-sm text-secondary mb-1">Placement Officer</label>
                  <input
                    type="text"
                    value={formData.placementOfficerName || ''}
                    onChange={(e) => setFormData({ ...formData, placementOfficerName: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg font-body-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
                <div>
                  <label className="block font-label-sm text-secondary mb-1">Placement Email</label>
                  <input
                    type="email"
                    value={formData.placementOfficerEmail || ''}
                    onChange={(e) => setFormData({ ...formData, placementOfficerEmail: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg font-body-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
                <div>
                  <label className="block font-label-sm text-secondary mb-1">Campus Phone</label>
                  <input
                    type="text"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg font-body-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
                <div>
                  <label className="block font-label-sm text-secondary mb-1">Official Website</label>
                  <input
                    type="url"
                    value={formData.website}
                    onChange={(e) => setFormData({ ...formData, website: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg font-body-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
              </div>

              <div>
                <label className="block font-label-sm text-secondary mb-1">Registry Notes</label>
                <textarea
                  value={formData.notes || ''}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  rows={2}
                  className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg font-body-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="px-3 py-1.5 rounded-lg text-secondary hover:bg-surface-container-low font-label-md"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-lg bg-primary text-white font-label-md font-semibold"
                >
                  Save Changes
                </button>
              </div>
            </form>
          ) : (
            <div className="space-y-4">
              {/* Leadership & Contacts Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="p-3 bg-surface-container-low/60 rounded-lg border border-[#e2e8f0]">
                  <span className="font-label-sm text-secondary uppercase font-semibold">Head of Institution</span>
                  <p className="font-body-md font-semibold text-on-surface mt-1">{college.principalName}</p>
                  <a 
                    href={`mailto:${college.principalEmail}`} 
                    className="font-code-sm text-primary hover:underline block mt-0.5"
                  >
                    {college.principalEmail}
                  </a>
                  <p className="font-label-sm text-secondary mt-1">{college.phone}</p>
                </div>

                <div className="p-3 bg-surface-container-low/60 rounded-lg border border-[#e2e8f0]">
                  <span className="font-label-sm text-secondary uppercase font-semibold">Placement & Industry Liaison</span>
                  <p className="font-body-md font-semibold text-on-surface mt-1">
                    {college.placementOfficerName || 'Placement Cell Secretariat'}
                  </p>
                  <a 
                    href={`mailto:${college.placementOfficerEmail || college.principalEmail}`} 
                    className="font-code-sm text-tertiary hover:underline block mt-0.5"
                  >
                    {college.placementOfficerEmail || 'Not specified'}
                  </a>
                  <p className="font-label-sm text-secondary mt-1">Direct Industry Desk</p>
                </div>
              </div>

              {/* Affiliation & Accreditation Meta */}
              <div className="p-3 bg-surface-container-low/40 rounded-lg border border-[#e2e8f0] text-sm space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-secondary font-label-sm">Affiliated University:</span>
                  <span className="font-semibold text-on-surface">{college.affiliation}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-secondary font-label-sm">NAAC Accreditation:</span>
                  <span className="font-semibold text-on-surface">{college.naacGrade ? `Grade ${college.naacGrade}` : 'Non-Accredited'}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-secondary font-label-sm">Official Web Portal:</span>
                  <a 
                    href={college.website} 
                    target="_blank" 
                    rel="noreferrer" 
                    className="text-primary hover:underline flex items-center gap-1 font-body-sm"
                  >
                    <span>{college.website}</span>
                    <span className="material-symbols-outlined text-[14px]">open_in_new</span>
                  </a>
                </div>
                {college.notes && (
                  <div className="pt-2 border-t border-[#e2e8f0]/80">
                    <span className="text-secondary font-label-sm block mb-0.5">Directorate Dossier Notes:</span>
                    <p className="text-on-surface font-body-sm italic">{college.notes}</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-space-md border-t border-[#e2e8f0] bg-surface-container-low/30 flex items-center justify-between">
          <span className="font-code-sm text-[11px] text-secondary">
            Last synchronization: {college.lastContacted || 'Recent'}
          </span>
          <div className="flex items-center gap-2">
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className="px-3 py-1.5 rounded-lg border border-[#cbd5e1] text-on-surface hover:bg-surface-container-low font-label-md flex items-center gap-1"
              >
                <span className="material-symbols-outlined text-[16px]">edit</span>
                <span>Edit Record</span>
              </button>
            )}
            <button
              onClick={onClose}
              className="px-4 py-1.5 rounded-lg bg-surface-container text-on-surface hover:bg-surface-container-high font-label-md font-semibold"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
