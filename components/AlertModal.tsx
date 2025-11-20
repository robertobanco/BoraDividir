
import React from 'react';

interface AlertModalProps {
  isOpen: boolean;
  type: 'alert' | 'confirm';
  title: string;
  message: string;
  onClose: () => void;
  onConfirm?: () => void;
}

export const AlertModal: React.FC<AlertModalProps> = ({ isOpen, type, title, message, onClose, onConfirm }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 animate-fade-in">
      <div className="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" onClick={onClose}></div>
      <div className="relative w-full max-w-sm bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 p-6 animate-scale-in overflow-hidden transform transition-all">
         {/* Decorative background blobs */}
         <div className="absolute top-0 right-0 -mt-8 -mr-8 w-24 h-24 bg-violet-500/20 rounded-full blur-xl pointer-events-none"></div>
         <div className="absolute bottom-0 left-0 -mb-8 -ml-8 w-24 h-24 bg-indigo-500/20 rounded-full blur-xl pointer-events-none"></div>

        <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2 relative z-10">{title}</h3>
        <p className="text-slate-600 dark:text-slate-300 text-sm mb-6 relative z-10 leading-relaxed">
          {message}
        </p>
        
        <div className="flex justify-end gap-3 relative z-10">
          {type === 'confirm' && (
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
            >
              Cancelar
            </button>
          )}
          <button
            onClick={() => {
              if (onConfirm) onConfirm();
              onClose();
            }}
            className="px-4 py-2 text-sm font-bold text-white bg-violet-600 hover:bg-violet-700 rounded-lg shadow-md shadow-violet-500/20 transition-all active:scale-95 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900"
          >
            {type === 'confirm' ? 'Confirmar' : 'Entendi'}
          </button>
        </div>
      </div>
    </div>
  );
};
