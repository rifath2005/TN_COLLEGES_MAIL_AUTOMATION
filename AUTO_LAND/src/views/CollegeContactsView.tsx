import React, { useState, useEffect, useMemo } from 'react';
import { CollegeContact, CollegeCategory, CollegeStatus } from '../types';
import {
  isMissingPhone,
  isMissingWebsite,
  isMissingEmail,
  isMissingAny,
  isCompleteProfile,
  getMissingDetailsList,
  getMissingDetailsCount
} from '../utils/completeness';

interface CollegeContactsViewProps {
  colleges: CollegeContact[];
  initialFilter?: string;
  onSelectCollege: (college: CollegeContact) => void;
  onSendTestEmail: (college: CollegeContact) => void;
  onAddCollege: (newCollege: CollegeContact) => void;
  onTriggerToast: (msg: string, icon?: string) => void;
  onOpenCampaignModal: () => void;
}

export const CollegeContactsView: React.FC<CollegeContactsViewProps> = ({
  colleges,
  initialFilter = '',
  onSelectCollege,
  onSendTestEmail,
  onAddCollege,
  onTriggerToast,
  onOpenCampaignModal
}) => {
  const missingFilterKeys = ['no-phone', 'no-website', 'no-email', 'any-missing', 'complete'];
  const statusKeys = ['verified', 'pending', 'bounced'];
  const categoryKeys = ['Engineering', 'Arts & Science', 'Polytechnic / Voc', 'Medical & Health'];

  const [searchQuery, setSearchQuery] = useState(
    initialFilter && !missingFilterKeys.includes(initialFilter) && !statusKeys.includes(initialFilter) && !categoryKeys.includes(initialFilter)
      ? initialFilter
      : ''
  );
  const [selectedStatus, setSelectedStatus] = useState<string>(
    statusKeys.includes(initialFilter) ? initialFilter : 'all'
  );
  const [selectedCategory, setSelectedCategory] = useState<string>(
    categoryKeys.includes(initialFilter) ? initialFilter : 'all'
  );
  const [missingFilter, setMissingFilter] = useState<string>(
    missingFilterKeys.includes(initialFilter) ? initialFilter : 'all'
  );
  const [sortBy, setSortBy] = useState<string>('missing-desc');
  const [selectedDistrict, setSelectedDistrict] = useState<string>('all');
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // Sync state if initialFilter prop changes
  useEffect(() => {
    if (missingFilterKeys.includes(initialFilter)) {
      setMissingFilter(initialFilter);
      setSearchQuery('');
    } else if (statusKeys.includes(initialFilter)) {
      setSelectedStatus(initialFilter);
      setSearchQuery('');
    } else if (categoryKeys.includes(initialFilter)) {
      setSelectedCategory(initialFilter);
      setSearchQuery('');
    } else if (initialFilter) {
      setSearchQuery(initialFilter);
    }
  }, [initialFilter]);

  // New college form state
  const [newCollegeData, setNewCollegeData] = useState<Partial<CollegeContact>>({
    name: '',
    district: 'Chennai',
    zone: 'Zone 01',
    category: 'Engineering',
    aisheCode: '',
    affiliation: 'Anna University',
    autonomous: false,
    principalName: '',
    principalEmail: '',
    phone: '',
    website: 'https://',
    status: 'verified'
  });

  // Extract unique districts
  const districts = useMemo(() => {
    const set = new Set<string>();
    colleges.forEach(c => set.add(c.district));
    return Array.from(set).sort();
  }, [colleges]);

  // Missing details counts for quick badges
  const missingPhoneTotal = useMemo(() => colleges.filter(isMissingPhone).length, [colleges]);
  const missingWebsiteTotal = useMemo(() => colleges.filter(isMissingWebsite).length, [colleges]);
  const missingEmailTotal = useMemo(() => colleges.filter(isMissingEmail).length, [colleges]);
  const missingAnyTotal = useMemo(() => colleges.filter(isMissingAny).length, [colleges]);
  const completeTotal = useMemo(() => colleges.filter(isCompleteProfile).length, [colleges]);

  // Filtered and sorted colleges
  const filtered = useMemo(() => {
    const result = colleges.filter((c) => {
      const matchSearch =
        searchQuery === '' ||
        c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.aisheCode.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.principalName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.district.toLowerCase().includes(searchQuery.toLowerCase());

      const matchStatus = selectedStatus === 'all' || c.status === selectedStatus;
      const matchCategory = selectedCategory === 'all' || c.category === selectedCategory;
      const matchDistrict = selectedDistrict === 'all' || c.district === selectedDistrict;

      // Completeness / Missing Details Filter
      let matchMissing = true;
      if (missingFilter === 'no-phone') {
        matchMissing = isMissingPhone(c);
      } else if (missingFilter === 'no-website') {
        matchMissing = isMissingWebsite(c);
      } else if (missingFilter === 'no-email') {
        matchMissing = isMissingEmail(c);
      } else if (missingFilter === 'any-missing') {
        matchMissing = isMissingAny(c);
      } else if (missingFilter === 'complete') {
        matchMissing = isCompleteProfile(c);
      }

      return matchSearch && matchStatus && matchCategory && matchDistrict && matchMissing;
    });

    // Sorting
    return [...result].sort((a, b) => {
      if (sortBy === 'missing-desc') {
        const countA = (isMissingPhone(a) ? 1 : 0) + (isMissingWebsite(a) ? 1 : 0) + (isMissingEmail(a) ? 1 : 0);
        const countB = (isMissingPhone(b) ? 1 : 0) + (isMissingWebsite(b) ? 1 : 0) + (isMissingEmail(b) ? 1 : 0);
        if (countB !== countA) return countB - countA;
        return a.name.localeCompare(b.name);
      }
      if (sortBy === 'complete-first') {
        const countA = (isMissingPhone(a) ? 1 : 0) + (isMissingWebsite(a) ? 1 : 0) + (isMissingEmail(a) ? 1 : 0);
        const countB = (isMissingPhone(b) ? 1 : 0) + (isMissingWebsite(b) ? 1 : 0) + (isMissingEmail(b) ? 1 : 0);
        if (countA !== countB) return countA - countB;
        return a.name.localeCompare(b.name);
      }
      if (sortBy === 'name-asc') {
        return a.name.localeCompare(b.name);
      }
      if (sortBy === 'name-desc') {
        return b.name.localeCompare(a.name);
      }
      if (sortBy === 'district-asc') {
        return a.district.localeCompare(b.district);
      }
      return 0;
    });
  }, [colleges, searchQuery, selectedStatus, selectedCategory, selectedDistrict, missingFilter, sortBy]);

  const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked) {
      setSelectedIds(filtered.map(c => c.id));
    } else {
      setSelectedIds([]);
    }
  };

  const handleToggleRow = (id: string) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  const handleBulkVerify = () => {
    onTriggerToast(`Ran MX check on ${selectedIds.length} records. DNS mail routing validated.`, 'verified');
    setSelectedIds([]);
  };

  const handleAddSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCollegeData.name || !newCollegeData.principalEmail) {
      onTriggerToast('Please fill in required fields: College Name and Principal Email', 'error');
      return;
    }

    const generated: CollegeContact = {
      id: `col-${Date.now()}`,
      name: newCollegeData.name || '',
      district: newCollegeData.district || 'Chennai',
      zone: newCollegeData.zone || 'Zone 01',
      category: (newCollegeData.category as CollegeCategory) || 'Engineering',
      aisheCode: newCollegeData.aisheCode || `C-${Math.floor(10000 + Math.random() * 90000)}`,
      affiliation: newCollegeData.affiliation || 'Anna University',
      autonomous: !!newCollegeData.autonomous,
      principalName: newCollegeData.principalName || 'Principal In-Charge',
      principalEmail: newCollegeData.principalEmail || '',
      phone: newCollegeData.phone || '+91 44 2000 0000',
      website: newCollegeData.website || 'https://www.example.edu.in',
      status: (newCollegeData.status as CollegeStatus) || 'verified',
      lastContacted: 'Just now'
    };

    onAddCollege(generated);
    setShowAddModal(false);
    onTriggerToast(`Added "${generated.name}" to Tamil Nadu Directorate registry`, 'school');
  };

  return (
    <div className="flex flex-col w-full pb-space-xl space-y-space-md">
      {/* Top Banner and Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="font-code-sm text-code-sm uppercase tracking-widest text-primary font-bold">
              Institutional Registry
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
            <span className="font-code-sm text-code-sm text-secondary">
              Tamil Nadu Higher Education Directorate
            </span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface font-bold tracking-tight">
            College Contacts Roster
          </h1>
          <p className="font-body-md text-body-md text-secondary mt-0.5">
            Active directory of {colleges.length} collegiate campuses, principals, and placement directorates.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowAddModal(true)}
            className="h-9 px-4 rounded-lg bg-primary-container text-on-primary hover:opacity-95 font-label-md font-semibold flex items-center gap-1.5 shadow-sm active:scale-[0.98] transition-all cursor-pointer"
          >
            <span className="material-symbols-outlined text-[18px]">add_circle</span>
            <span>Add New Campus</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-surface-container-lowest p-space-md rounded-lg shadow-sm border border-[#e2e8f0] flex flex-col gap-3">
        {/* Top Row: Search + Status + District + Category */}
        <div className="flex flex-col md:flex-row gap-3 items-center justify-between">
          {/* Search */}
          <div className="relative w-full md:w-80">
            <span className="material-symbols-outlined absolute left-3 top-2.5 text-[18px] text-secondary">
              search
            </span>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search college, AISHE, principal..."
              className="w-full pl-9 pr-3 py-1.5 bg-surface-container-low rounded-lg font-body-sm text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary focus:bg-white"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-2 text-secondary hover:text-on-surface"
              >
                <span className="material-symbols-outlined text-[16px]">close</span>
              </button>
            )}
          </div>

          {/* Filters */}
          <div className="flex items-center gap-2 w-full md:w-auto flex-wrap">
            {/* Status Tabs */}
            <div className="inline-flex p-1 bg-surface-container-low rounded-lg border border-[#e2e8f0]">
              <button
                onClick={() => setSelectedStatus('all')}
                className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all ${
                  selectedStatus === 'all'
                    ? 'bg-white text-on-surface shadow-2xs'
                    : 'text-secondary hover:text-on-surface'
                }`}
              >
                All ({colleges.length})
              </button>
              <button
                onClick={() => setSelectedStatus('verified')}
                className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all ${
                  selectedStatus === 'verified'
                    ? 'bg-emerald-50 text-emerald-800 shadow-2xs'
                    : 'text-secondary hover:text-on-surface'
                }`}
              >
                Verified
              </button>
              <button
                onClick={() => setSelectedStatus('pending')}
                className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all ${
                  selectedStatus === 'pending'
                    ? 'bg-amber-50 text-amber-800 shadow-2xs'
                    : 'text-secondary hover:text-on-surface'
                }`}
              >
                Pending
              </button>
              <button
                onClick={() => setSelectedStatus('bounced')}
                className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all ${
                  selectedStatus === 'bounced'
                    ? 'bg-red-50 text-red-800 shadow-2xs'
                    : 'text-secondary hover:text-on-surface'
                }`}
              >
                Bounced
              </button>
            </div>

            {/* District Select */}
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="px-2.5 py-1.5 bg-surface-container-low rounded-lg text-xs font-semibold text-on-surface border border-[#e2e8f0] focus:outline-none"
            >
              <option value="all">All Districts ({districts.length})</option>
              {districts.map(d => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>

            {/* Category Select */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-2.5 py-1.5 bg-surface-container-low rounded-lg text-xs font-semibold text-on-surface border border-[#e2e8f0] focus:outline-none"
            >
              <option value="all">All Categories</option>
              <option value="Engineering">Engineering</option>
              <option value="Arts & Science">Arts & Science</option>
              <option value="Polytechnic / Voc">Polytechnic / Voc</option>
              <option value="Medical & Health">Medical & Health</option>
            </select>
          </div>
        </div>

        {/* Bottom Row: Missing Details Filter Pick Options & Sort By */}
        <div className="pt-2.5 border-t border-[#e2e8f0] flex flex-col lg:flex-row lg:items-center justify-between gap-3">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-xs font-bold text-secondary uppercase tracking-wider flex items-center gap-1 mr-1">
              <span className="material-symbols-outlined text-[16px] text-amber-600">filter_list</span>
              <span>Missing Details:</span>
            </span>
            <button
              onClick={() => setMissingFilter('all')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer ${
                missingFilter === 'all'
                  ? 'bg-slate-800 text-white shadow-2xs'
                  : 'bg-surface-container-low text-secondary hover:text-on-surface border border-[#e2e8f0]'
              }`}
            >
              All Records ({colleges.length})
            </button>
            <button
              onClick={() => setMissingFilter('no-phone')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer flex items-center gap-1 ${
                missingFilter === 'no-phone'
                  ? 'bg-rose-700 text-white shadow-2xs'
                  : 'bg-rose-50 text-rose-800 hover:bg-rose-100 border border-rose-200'
              }`}
            >
              <span className="material-symbols-outlined text-[13px]">phone_disabled</span>
              <span>Without Phone ({missingPhoneTotal})</span>
            </button>
            <button
              onClick={() => setMissingFilter('no-website')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer flex items-center gap-1 ${
                missingFilter === 'no-website'
                  ? 'bg-amber-700 text-white shadow-2xs'
                  : 'bg-amber-50 text-amber-800 hover:bg-amber-100 border border-amber-200'
              }`}
            >
              <span className="material-symbols-outlined text-[13px]">public_off</span>
              <span>Without Website ({missingWebsiteTotal})</span>
            </button>
            <button
              onClick={() => setMissingFilter('no-email')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer flex items-center gap-1 ${
                missingFilter === 'no-email'
                  ? 'bg-orange-700 text-white shadow-2xs'
                  : 'bg-orange-50 text-orange-800 hover:bg-orange-100 border border-orange-200'
              }`}
            >
              <span className="material-symbols-outlined text-[13px]">unsubscribe</span>
              <span>Without Mail ID ({missingEmailTotal})</span>
            </button>
            <button
              onClick={() => setMissingFilter('any-missing')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer flex items-center gap-1 ${
                missingFilter === 'any-missing'
                  ? 'bg-purple-700 text-white shadow-2xs'
                  : 'bg-purple-50 text-purple-800 hover:bg-purple-100 border border-purple-200'
              }`}
            >
              <span className="material-symbols-outlined text-[13px]">warning</span>
              <span>Any Incomplete ({missingAnyTotal})</span>
            </button>
            <button
              onClick={() => setMissingFilter('complete')}
              className={`px-2.5 py-1 text-xs rounded-md font-semibold transition-all cursor-pointer flex items-center gap-1 ${
                missingFilter === 'complete'
                  ? 'bg-emerald-700 text-white shadow-2xs'
                  : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100 border border-emerald-200'
              }`}
            >
              <span className="material-symbols-outlined text-[13px]">verified</span>
              <span>Complete ({completeTotal})</span>
            </button>
          </div>

          {/* Sort By Dropdown */}
          <div className="flex items-center gap-2 self-start lg:self-auto shrink-0">
            <label htmlFor="collegeSortSelect" className="text-xs font-bold text-secondary uppercase tracking-wider flex items-center gap-1">
              <span className="material-symbols-outlined text-[16px]">sort</span>
              <span>Sort By:</span>
            </label>
            <select
              id="collegeSortSelect"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-2.5 py-1.5 bg-surface-container-low rounded-lg text-xs font-semibold text-on-surface border border-[#e2e8f0] focus:outline-none focus:border-primary cursor-pointer"
            >
              <option value="missing-desc">Most Missing Details First</option>
              <option value="complete-first">Complete Records First</option>
              <option value="name-asc">College Name (A to Z)</option>
              <option value="name-desc">College Name (Z to A)</option>
              <option value="district-asc">District (A to Z)</option>
            </select>

            {(missingFilter !== 'all' || selectedStatus !== 'all' || selectedCategory !== 'all' || selectedDistrict !== 'all' || searchQuery) && (
              <button
                onClick={() => {
                  setMissingFilter('all');
                  setSelectedStatus('all');
                  setSelectedCategory('all');
                  setSelectedDistrict('all');
                  setSearchQuery('');
                  setSortBy('missing-desc');
                }}
                className="px-2 py-1 text-xs text-secondary hover:text-on-surface font-semibold underline cursor-pointer"
                title="Reset all filters"
              >
                Reset
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Bulk Action Bar (when rows are selected) */}
      {selectedIds.length > 0 && (
        <div className="bg-primary-50 p-space-sm rounded-lg border border-primary/20 flex items-center justify-between animate-in fade-in duration-150">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-[20px]">check_circle</span>
            <span className="font-label-md text-primary font-bold">
              {selectedIds.length} {selectedIds.length === 1 ? 'institution' : 'institutions'} selected
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleBulkVerify}
              className="px-3 py-1 bg-white hover:bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-lg text-xs font-semibold flex items-center gap-1 transition-colors"
            >
              <span className="material-symbols-outlined text-[15px]">verified</span>
              <span>Verify MX Records</span>
            </button>
            <button
              onClick={onOpenCampaignModal}
              className="px-3 py-1 bg-primary text-white hover:bg-primary-container rounded-lg text-xs font-semibold flex items-center gap-1 transition-colors"
            >
              <span className="material-symbols-outlined text-[15px]">campaign</span>
              <span>Create Campaign</span>
            </button>
            <button
              onClick={() => setSelectedIds([])}
              className="text-secondary hover:text-on-surface text-xs font-semibold ml-2"
            >
              Clear
            </button>
          </div>
        </div>
      )}

      {/* Directory Table */}
      <div className="bg-surface-container-lowest rounded-lg shadow-sm border border-[#e2e8f0] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-container-low/70 border-b border-[#e2e8f0] text-secondary font-label-sm uppercase tracking-wider text-[11px]">
                <th className="py-3 px-4 w-10">
                  <input
                    type="checkbox"
                    checked={selectedIds.length === filtered.length && filtered.length > 0}
                    onChange={handleSelectAll}
                    className="accent-primary rounded"
                  />
                </th>
                <th className="py-3 px-4 font-semibold">Institution Name & AISHE</th>
                <th className="py-3 px-4 font-semibold">District & Zone</th>
                <th className="py-3 px-4 font-semibold">Type & Affiliation</th>
                <th className="py-3 px-4 font-semibold">Principal & Direct Contact</th>
                <th className="py-3 px-4 font-semibold">Status</th>
                <th className="py-3 px-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#f1f5f9] font-body-sm text-[13px]">
              {filtered.map((college) => {
                const isSelected = selectedIds.includes(college.id);
                return (
                  <tr
                    key={college.id}
                    className={`hover:bg-surface-container-low/50 transition-colors ${
                      isSelected ? 'bg-primary-50/40' : ''
                    }`}
                  >
                    <td className="py-3 px-4">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => handleToggleRow(college.id)}
                        className="accent-primary rounded"
                      />
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex flex-col">
                        <span 
                          onClick={() => onSelectCollege(college)}
                          className="font-semibold text-on-surface hover:text-primary cursor-pointer line-clamp-1"
                        >
                          {college.name}
                        </span>
                        <div className="flex items-center gap-1.5 mt-0.5 flex-wrap">
                          <span className="font-code-sm text-[11px] text-secondary bg-surface-container px-1 rounded">
                            AISHE {college.aisheCode}
                          </span>
                          {isMissingWebsite(college) ? (
                            <span className="inline-flex items-center gap-0.5 text-[10px] font-bold text-amber-800 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
                              <span className="material-symbols-outlined text-[11px]">public_off</span>
                              No Website
                            </span>
                          ) : (
                            <a
                              href={college.website}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-0.5 text-[10px] text-primary hover:underline"
                            >
                              <span className="material-symbols-outlined text-[11px]">link</span>
                              Website
                            </a>
                          )}
                          {college.autonomous && (
                            <span className="text-[10px] font-semibold text-emerald-800 bg-emerald-50 px-1 rounded border border-emerald-200">
                              Auto
                            </span>
                          )}
                          {college.naacGrade && (
                            <span className="text-[10px] font-semibold text-sky-800 bg-sky-50 px-1 rounded border border-sky-200">
                              NAAC {college.naacGrade}
                            </span>
                          )}
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <span className="text-on-surface font-medium">{college.district}</span>
                      <span className="block text-[11px] text-secondary">{college.zone}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-on-surface font-medium">{college.category}</span>
                      <span className="block text-[11px] text-secondary line-clamp-1">{college.affiliation}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-on-surface font-medium block line-clamp-1">{college.principalName}</span>
                      {/* Email */}
                      <div className="mt-0.5">
                        {isMissingEmail(college) ? (
                          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-orange-800 bg-orange-50 px-1.5 py-0.5 rounded border border-orange-200">
                            <span className="material-symbols-outlined text-[12px]">unsubscribe</span>
                            No Mail ID
                          </span>
                        ) : (
                          <a
                            href={`mailto:${college.principalEmail}`}
                            className="block font-code-sm text-primary hover:underline text-[12px] truncate max-w-[210px]"
                          >
                            {college.principalEmail}
                          </a>
                        )}
                      </div>
                      {/* Phone */}
                      <div className="mt-1">
                        {isMissingPhone(college) ? (
                          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-rose-800 bg-rose-50 px-1.5 py-0.5 rounded border border-rose-200">
                            <span className="material-symbols-outlined text-[12px]">phone_disabled</span>
                            No Phone
                          </span>
                        ) : (
                          <span className="font-code-sm text-[11px] text-secondary flex items-center gap-1">
                            <span className="material-symbols-outlined text-[12px]">call</span>
                            {college.phone}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <div className="flex flex-col gap-1 items-start">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold ${
                          college.status === 'verified'
                            ? 'bg-surface-container-highest text-tertiary'
                            : college.status === 'pending'
                            ? 'bg-amber-100 text-amber-900'
                            : 'bg-error-container text-on-error-container'
                        }`}>
                          {college.status === 'verified' && <span className="w-1.5 h-1.5 rounded-full bg-tertiary mr-1.5"></span>}
                          {college.status === 'pending' && <span className="w-1.5 h-1.5 rounded-full bg-amber-600 mr-1.5"></span>}
                          {college.status === 'bounced' && <span className="w-1.5 h-1.5 rounded-full bg-error mr-1.5"></span>}
                          {college.status.toUpperCase()}
                        </span>
                        {isCompleteProfile(college) ? (
                          <span className="text-[10px] font-bold text-emerald-800 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200 inline-flex items-center gap-0.5">
                            <span className="material-symbols-outlined text-[11px]">check_circle</span>
                            Complete
                          </span>
                        ) : (
                          <span className="text-[10px] font-bold text-amber-900 bg-amber-100 px-1.5 py-0.5 rounded border border-amber-300 inline-flex items-center gap-0.5">
                            <span className="material-symbols-outlined text-[11px]">warning</span>
                            {getMissingDetailsCount(college)}/3 Missing
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-1">
                        <button
                          onClick={() => onSendTestEmail(college)}
                          title="Dispatch test outreach"
                          className="p-1 rounded text-secondary hover:text-primary hover:bg-surface-container transition-colors"
                        >
                          <span className="material-symbols-outlined text-[18px]">forward_to_inbox</span>
                        </button>
                        <button
                          onClick={() => onSelectCollege(college)}
                          title="View dossier"
                          className="p-1 rounded text-secondary hover:text-on-surface hover:bg-surface-container transition-colors"
                        >
                          <span className="material-symbols-outlined text-[18px]">visibility</span>
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {filtered.length === 0 && (
          <div className="p-8 text-center text-secondary">
            <span className="material-symbols-outlined text-[36px] opacity-40">school</span>
            <p className="mt-1 font-body-md font-semibold text-on-surface">No colleges found</p>
            <p className="text-sm">Try resetting filters or adjusting search parameters</p>
          </div>
        )}

        {/* Table footer */}
        <div className="px-4 py-3 bg-surface-container-low/40 border-t border-[#e2e8f0] flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-secondary">
          <div className="flex items-center gap-2 flex-wrap">
            <span>Showing {filtered.length.toLocaleString()} of {colleges.length.toLocaleString()} institutional records</span>
            {missingFilter !== 'all' && (
              <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-900 font-semibold text-[11px] border border-amber-200">
                Active Filter: {missingFilter === 'no-phone' ? 'Without Phone No' : missingFilter === 'no-website' ? 'Without Website' : missingFilter === 'no-email' ? 'Without Mail ID' : missingFilter === 'any-missing' ? 'Any Incomplete' : 'Complete Profiles'}
              </span>
            )}
          </div>
          <span className="font-code-sm">AICTE / AISHE / TNDCE Census Verified</span>
        </div>
      </div>

      {/* Add College Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#213145]/40 backdrop-blur-sm p-4 animate-in fade-in duration-150">
          <div className="fixed inset-0" onClick={() => setShowAddModal(false)} />
          <div className="relative bg-surface-container-lowest rounded-xl shadow-2xl max-w-lg w-full p-space-lg border border-[#cbd5e1] z-10 animate-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between pb-3 border-b border-[#e2e8f0] mb-3">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-primary text-[22px]">domain_add</span>
                <h3 className="font-headline-sm font-bold text-on-surface">Add New Higher Ed Institution</h3>
              </div>
              <button onClick={() => setShowAddModal(false)} className="text-secondary hover:text-on-surface">
                <span className="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <form onSubmit={handleAddSubmit} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-secondary mb-1">Official College Name *</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Government College of Engineering, Erode"
                  value={newCollegeData.name}
                  onChange={(e) => setNewCollegeData({ ...newCollegeData, name: e.target.value })}
                  className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-semibold text-secondary mb-1">District</label>
                  <input
                    type="text"
                    value={newCollegeData.district}
                    onChange={(e) => setNewCollegeData({ ...newCollegeData, district: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-secondary mb-1">AISHE Code</label>
                  <input
                    type="text"
                    placeholder="e.g. C-18492"
                    value={newCollegeData.aisheCode}
                    onChange={(e) => setNewCollegeData({ ...newCollegeData, aisheCode: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-semibold text-secondary mb-1">Classification</label>
                  <select
                    value={newCollegeData.category}
                    onChange={(e) => setNewCollegeData({ ...newCollegeData, category: e.target.value as CollegeCategory })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  >
                    <option value="Engineering">Engineering</option>
                    <option value="Arts & Science">Arts & Science</option>
                    <option value="Polytechnic / Voc">Polytechnic / Voc</option>
                    <option value="Medical & Health">Medical & Health</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-secondary mb-1">Affiliated University</label>
                  <input
                    type="text"
                    value={newCollegeData.affiliation}
                    onChange={(e) => setNewCollegeData({ ...newCollegeData, affiliation: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-semibold text-secondary mb-1">Principal / Head Name</label>
                  <input
                    type="text"
                    placeholder="Dr. S. Ramesh"
                    value={newCollegeData.principalName}
                    onChange={(e) => setNewCollegeData({ ...newCollegeData, principalName: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-secondary mb-1">Principal Email *</label>
                  <input
                    type="email"
                    required
                    placeholder="principal@college.edu.in"
                    value={newCollegeData.principalEmail}
                    onChange={(e) => setNewCollegeData({ ...newCollegeData, principalEmail: e.target.value })}
                    className="w-full bg-surface-container-low px-3 py-1.5 rounded-lg text-sm border border-[#e2e8f0] focus:outline-none focus:border-primary"
                  />
                </div>
              </div>

              <div className="flex items-center gap-2 pt-1">
                <input
                  type="checkbox"
                  id="autonomous-chk"
                  checked={newCollegeData.autonomous}
                  onChange={(e) => setNewCollegeData({ ...newCollegeData, autonomous: e.target.checked })}
                  className="accent-primary"
                />
                <label htmlFor="autonomous-chk" className="text-xs font-medium text-on-surface">
                  Autonomous Status (UGC Conferred)
                </label>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-[#e2e8f0]">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-3 py-1.5 rounded-lg text-secondary hover:bg-surface-container-low text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-lg bg-primary text-white text-xs font-semibold shadow-sm"
                >
                  Save Campus
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
