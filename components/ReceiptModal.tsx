import React from 'react';

interface ReceiptModalProps {
  imageUrl: string;
  onClose: () => void;
}

export const ReceiptModal: React.FC<ReceiptModalProps> = ({ imageUrl, onClose }) => {
  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div 
        className="relative bg-white dark:bg-slate-800 p-4 rounded-lg shadow-xl max-w-4xl max-h-[90vh]"
        onClick={(e) => e.stopPropagation()} // Prevent closing when clicking on the image
      >
        <button 
          onClick={onClose}
          className="absolute -top-4 -right-4 bg-white dark:bg-slate-700 rounded-full p-1 text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white"
          aria-label="Fechar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <img src={imageUrl} alt="Comprovante" className="max-w-full max-h-[85vh] object-contain rounded" />
      </div>
    </div>
  );
};