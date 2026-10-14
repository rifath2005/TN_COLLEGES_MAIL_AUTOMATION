export type NavScreen = 
  | 'dashboard' 
  | 'college-contacts' 
  | 'import-contacts' 
  | 'website-research' 
  | 'email-templates' 
  | 'campaigns' 
  | 'send-history' 
  | 'settings';

export type CollegeStatus = 'verified' | 'pending' | 'bounced' | 'duplicate';

export type CollegeCategory = 'Engineering' | 'Arts & Science' | 'Polytechnic / Voc' | 'Medical & Health';

export interface CollegeContact {
  id: string;
  name: string;
  shortName?: string;
  district: string;
  zone: string;
  category: CollegeCategory;
  aisheCode: string;
  affiliation: string;
  autonomous: boolean;
  naacGrade?: string;
  nbaAccredited?: boolean;
  principalName: string;
  principalEmail: string;
  placementOfficerName?: string;
  placementOfficerEmail?: string;
  phone: string;
  website: string;
  status: CollegeStatus;
  lastContacted?: string;
  notes?: string;
}

export interface ActivityFeedItem {
  id: string;
  collegeName: string;
  action: string;
  description: string;
  timeAgo: string;
  statusBadge: string;
  statusType: 'verified' | 'pending' | 'sent' | 'duplicate' | 'bounced';
  subBadge: string;
  icon: string;
  iconBg: string;
  iconColor: string;
}

export interface EmailTemplate {
  id: string;
  title: string;
  category: string;
  subject: string;
  body: string;
  lastModified: string;
  stats: {
    dispatched: number;
    openRate: string;
    clickRate: string;
  };
}

export interface Campaign {
  id: string;
  name: string;
  targetZone: string;
  templateId: string;
  templateName: string;
  status: 'Draft' | 'Scheduled' | 'In Progress' | 'Completed';
  targetCount: number;
  sentCount: number;
  deliveredCount: number;
  bouncedCount: number;
  createdAt: string;
  scheduledFor?: string;
  velocityThrottle: number; // e.g. 45 msgs/min
}

export interface DispatchAuditRecord {
  id: string;
  collegeName: string;
  aisheCode: string;
  recipientEmail: string;
  recipientTitle: string;
  campaignName: string;
  timestamp: string;
  status: 'Delivered' | 'Opened' | 'Clicked' | 'Bounced' | 'Queued';
  bounceReason?: string;
  zone: string;
  ipNode: string;
}

export interface SystemStats {
  totalColleges: number;
  verifiedRecords: number;
  pendingQueue: number;
  dispatched: number;
  bouncedFailed: number;
  deduplicated: number;
  velocityThrottle: number;
}
