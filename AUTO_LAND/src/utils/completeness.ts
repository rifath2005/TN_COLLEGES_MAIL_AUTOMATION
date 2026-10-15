import { CollegeContact } from '../types';

export const isMissingPhone = (c: CollegeContact): boolean => {
  if (!c.phone) return true;
  const p = c.phone.trim().toLowerCase();
  return p === '' || p === '-' || p === 'n/a' || p === 'none' || p === 'null';
};

export const isMissingWebsite = (c: CollegeContact): boolean => {
  if (!c.website) return true;
  const w = c.website.trim().toLowerCase();
  return (
    w === '' ||
    w === '-' ||
    w === 'https://' ||
    w === 'http://' ||
    w === 'n/a' ||
    w === 'none' ||
    w === 'null' ||
    w === 'https://-' ||
    w === 'http://-'
  );
};

export const isMissingEmail = (c: CollegeContact): boolean => {
  if (!c.principalEmail) return true;
  const e = c.principalEmail.trim().toLowerCase();
  return (
    e === '' ||
    e === '-' ||
    e === 'n/a' ||
    e === 'none' ||
    e === 'null' ||
    !e.includes('@')
  );
};

export const isMissingAny = (c: CollegeContact): boolean => {
  return isMissingPhone(c) || isMissingWebsite(c) || isMissingEmail(c);
};

export const isCompleteProfile = (c: CollegeContact): boolean => {
  return !isMissingPhone(c) && !isMissingWebsite(c) && !isMissingEmail(c);
};

export const getMissingDetailsList = (c: CollegeContact): ('Phone' | 'Website' | 'Email')[] => {
  const missing: ('Phone' | 'Website' | 'Email')[] = [];
  if (isMissingPhone(c)) missing.push('Phone');
  if (isMissingWebsite(c)) missing.push('Website');
  if (isMissingEmail(c)) missing.push('Email');
  return missing;
};

export const getMissingDetailsCount = (c: CollegeContact): number => {
  let count = 0;
  if (isMissingPhone(c)) count++;
  if (isMissingWebsite(c)) count++;
  if (isMissingEmail(c)) count++;
  return count;
};
