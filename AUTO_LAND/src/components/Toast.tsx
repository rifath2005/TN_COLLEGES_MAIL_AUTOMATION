import React from 'react';

export interface ToastMessage {
  id: string;
  message: string;
  icon?: string;
  type?: 'info' | 'success' | 'warning' | 'error';
}

interface ToastProps {
  toast: ToastMessage | null;
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ toast, onClose }) => {
  if (!toast) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-center gap-space-sm bg-surface-container-lowest text-on-surface px-space-md py-space-sm rounded-lg shadow-2xl border border-[#e2e8f0] animate-in fade-in slide-in-from-bottom-5 duration-200">
      <span className="material-symbols-outlined text-[20px] text-primary">
        {toast.icon || 'info'}
      </span>
      <span className="font-body-sm text-body-sm font-semibold text-on-surface">
        {toast.message}
      </span>
      <button 
        onClick={onClose}
        className="ml-2 text-secondary hover:text-on-surface p-0.5 rounded transition-colors"
      >
        <span className="material-symbols-outlined text-[16px]">close</span>
      </button>
    </div>
  );
};
