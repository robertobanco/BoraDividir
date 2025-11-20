
import React, { useRef, useMemo, useState } from 'react';
import type { BillSplitEvent, Transaction } from '../types';
import { ShareIcon } from './icons/ShareIcon';
import { DetailedSummary } from './DetailedSummary';
import { CheckCircleIcon } from './icons/CheckCircleIcon';

declare global {
  interface Window {
    html2canvas: any;
  }
}

interface ShareSummaryModalProps {
  event: BillSplitEvent;
  settlements: Transaction[];
  onClose: () => void;
  onShowAlert: (title: string, message: string) => void;
}

const formatCurrency = (value: number) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);

const formatDate = (dateString: string) => {
    try {
        const date = new Date(dateString);
        const userTimezoneOffset = date.getTimezoneOffset() * 60000;
        return new Date(date.getTime() + userTimezoneOffset).toLocaleDateString('pt-BR');
    } catch (e) {
        return "Data inválida";
    }
};

// General Summary Styled for "Paper Receipt"
const GeneralSummary: React.FC<{ event: BillSplitEvent, settlements: Transaction[] }> = ({ event, settlements }) => {
    if (event.type === 'SHARED_EXPENSES') {
        const totalExpenses = event.expenses.reduce((sum, exp) => sum + exp.amount, 0);
        const costPerPerson = event.participants.length > 0 ? totalExpenses / event.participants.length : 0;

        return (
            <div className="text-slate-800">
                <div className="mb-6 border-b border-slate-800 pb-4 space-y-3">
                    <div className="flex justify-between items-center">
                         <p className="text-xs text-slate-500 uppercase tracking-widest">Total Geral</p>
                         <p className="text-2xl font-bold text-slate-900 font-mono">{formatCurrency(totalExpenses)}</p>
                    </div>
                    <div className="flex justify-between items-center">
                         <p className="text-xs text-slate-500 uppercase tracking-widest">Por Pessoa</p>
                         <p className="text-xl font-bold text-slate-900 font-mono">{formatCurrency(costPerPerson)}</p>
                    </div>
                </div>
                
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-widest mb-4 flex items-center gap-2">
                    <span className="w-full h-px bg-slate-300"></span>
                    <span className="whitespace-nowrap">Acerto Final</span>
                    <span className="w-full h-px bg-slate-300"></span>
                </h3>

                {settlements.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-6 bg-emerald-50 border border-emerald-100 rounded-lg">
                         <CheckCircleIcon className="h-8 w-8 text-emerald-500 mb-2" />
                         <p className="text-sm font-bold text-emerald-700">Contas Equilibradas</p>
                    </div>
                ) : (
                    <ul className="space-y-2 font-mono text-sm">
                        {settlements.map((s, index) => (
                            <li key={index} className="flex items-center justify-between p-2 bg-slate-50 rounded border-l-4 border-violet-500">
                                <div className="flex items-center gap-2">
                                    <span className="font-bold text-slate-700">{s.from}</span>
                                    <span className="text-slate-400 text-xs">paga</span>
                                    <span className="font-bold text-slate-700">{s.to}</span>
                                </div>
                                <span className="font-bold text-slate-900">{formatCurrency(s.amount)}</span>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        )
    }

    if (event.type === 'ITEMIZED_BILL') {
        const calculation = useMemo(() => {
            const participantSubtotals = new Map<string, number>(event.participants.map(p => [p.id, 0]));
            const itemsSubtotal = event.items.reduce((sum, item) => sum + item.amount, 0);
            
            event.items.forEach(item => {
                if (item.consumedByIds.length > 0) {
                    const costPerPerson = item.amount / item.consumedByIds.length;
                    item.consumedByIds.forEach(id => {
                        participantSubtotals.set(id, (participantSubtotals.get(id) || 0) + costPerPerson);
                    });
                }
            });

            const tipAmount = event.tip.type === 'PERCENT' ? itemsSubtotal * (event.tip.value / 100) : event.tip.value;
            const totalFees = tipAmount + event.tax;
            
            const participantTotals = event.participants.map(p => {
                const individualSubtotal = participantSubtotals.get(p.id) || 0;
                const proportionalFees = itemsSubtotal > 0 ? (individualSubtotal / itemsSubtotal) * totalFees : 0;
                const total = individualSubtotal + proportionalFees;
                return { participantId: p.id, name: p.name, total };
            });
            
            const billTotal = itemsSubtotal + totalFees;
            const totalPaid = event.actualPayments.reduce((sum, p) => sum + p.amount, 0);
            const remainingToPay = billTotal - totalPaid;

            return { billTotal, participantTotals, totalPaid, remainingToPay, itemsSubtotal, totalFees };
        }, [event]);
        
        return (
            <div className="space-y-6 text-slate-800">
                <div className="space-y-2 font-mono text-sm border-b border-slate-300 pb-4">
                    <div className="flex justify-between items-center">
                        <span className="font-bold uppercase">Total Conta</span> 
                        <span className="font-bold text-lg">{formatCurrency(calculation.billTotal)}</span>
                    </div>

                    {/* Detalhamento solicitado */}
                    <div className="pl-2 text-xs text-slate-500 space-y-1 pb-2 border-b border-dotted border-slate-200">
                         <div className="flex justify-between items-center">
                            <span>Total Itens</span>
                            <span>{formatCurrency(calculation.itemsSubtotal)}</span>
                         </div>
                         <div className="flex justify-between items-center">
                            <span>Total Taxas/Serviço</span>
                            <span>{formatCurrency(calculation.totalFees)}</span>
                         </div>
                    </div>

                    <div className="flex justify-between items-center text-slate-600 pt-1">
                        <span>Total Pago</span> 
                        <span>{formatCurrency(calculation.totalPaid)}</span>
                    </div>
                    {Math.abs(calculation.remainingToPay) > 0.01 && (
                         <div className="flex justify-between items-center font-bold">
                            <span>{calculation.remainingToPay > 0 ? 'Falta' : 'Troco'}</span> 
                            <span className={`${calculation.remainingToPay > 0 ? 'text-red-600' : 'text-blue-600'}`}>{formatCurrency(Math.abs(calculation.remainingToPay))}</span>
                        </div>
                    )}
                </div>
                
                <div>
                    <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-3 text-center">Resumo Individual</h3>
                     <ul className="space-y-2">
                        {calculation.participantTotals.map(p => {
                            const actualPayment = event.actualPayments.find(ap => ap.participantId === p.participantId)?.amount || 0;
                            const balance = actualPayment - p.total;
                            const isSettled = Math.abs(balance) < 0.01;

                            return (
                                <li key={p.participantId} className="flex justify-between items-center border-b border-dashed border-slate-200 last:border-0 py-1">
                                    <div>
                                        <span className="font-bold text-slate-800 text-sm">{p.name}</span>
                                    </div>
                                    
                                    <div className="text-right flex items-center gap-2">
                                        <span className="text-xs text-slate-500">{formatCurrency(p.total)}</span>
                                         {isSettled && actualPayment > 0 ? (
                                             <CheckCircleIcon className="h-4 w-4 text-emerald-500" />
                                        ) : (
                                            <span className={`font-mono text-xs font-bold px-1.5 py-0.5 rounded ${balance >= 0 ? 'bg-blue-100 text-blue-700' : 'bg-red-100 text-red-700'}`}>
                                                {balance >= 0 ? '+' : ''}{formatCurrency(balance)}
                                            </span>
                                        )}
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
                </div>
            </div>
        );
    }

    return null;
}


export const ShareSummaryModal: React.FC<ShareSummaryModalProps> = ({ event, settlements, onClose, onShowAlert }) => {
  const summaryRef = useRef<HTMLDivElement>(null);
  const [isSharing, setIsSharing] = useState(false);

  const handleShare = async (mode: 'summary' | 'full') => {
    if (!window.html2canvas) {
        onShowAlert('Aguarde', 'A biblioteca de imagem ainda está carregando. Aguarde alguns segundos e tente novamente.');
        return;
    }

    if (!summaryRef.current) return;

    setIsSharing(true);
    const elementToCapture = summaryRef.current;

    try {
        // 1. Clone the element
        const clone = elementToCapture.cloneNode(true) as HTMLElement;

        // 2. Remove Detailed section if mode is summary
        if (mode === 'summary') {
            const detailedSection = clone.querySelector('.detailed-section');
            if (detailedSection) {
                detailedSection.remove();
            }
        }

        // 3. Style the clone
        clone.style.position = 'fixed';
        clone.style.left = '-9999px';
        clone.style.top = '0';
        clone.style.width = '380px'; 
        clone.style.height = 'auto';
        clone.style.overflow = 'visible';
        clone.style.borderRadius = '0'; 
        clone.style.boxShadow = 'none';
        clone.classList.add('receipt-jagged-bottom');

        // 4. Append to body
        document.body.appendChild(clone);

        // 5. Capture the clone
        const canvas = await window.html2canvas(clone, {
            useCORS: true,
            backgroundColor: '#ffffff', 
            scale: 3, 
            logging: false,
            windowHeight: clone.scrollHeight + 100, 
        });
        
        // 6. Remove clone
        document.body.removeChild(clone);
        
        canvas.toBlob(async (blob: Blob | null) => {
            if (blob) {
                const fileName = `resumo-${mode}-${event.name.replace(/\s+/g, '-').toLowerCase()}.png`;
                const file = new File([blob], fileName, { type: 'image/png' });
                
                if (navigator.canShare && navigator.canShare({ files: [file] })) {
                    try {
                        await navigator.share({
                            title: `Resumo: ${event.name}`,
                            text: `Confira o resumo da divisão de contas do evento ${event.name}.`,
                            files: [file],
                        });
                    } catch (shareError) {
                        console.info("Share dismissed", shareError);
                    }
                } else {
                    try {
                        const url = URL.createObjectURL(blob);
                        const link = document.createElement('a');
                        link.href = url;
                        link.download = fileName;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        URL.revokeObjectURL(url);
                    } catch (downloadError) {
                         console.error('Download failed:', downloadError);
                         onShowAlert('Erro', 'Erro ao baixar imagem.');
                    }
                }
            }
            setIsSharing(false);
        }, 'image/png'); 
    } catch (error) {
        console.error('Capture failed:', error);
        onShowAlert('Erro', 'Não foi possível gerar a imagem.');
        setIsSharing(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in" onClick={onClose}>
      <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl w-full max-w-md flex flex-col max-h-[90vh] overflow-hidden border border-slate-200 dark:border-slate-700" onClick={(e) => e.stopPropagation()}>
        
        {/* Header of Modal */}
        <div className="pt-6 px-6 pb-2 bg-white dark:bg-slate-900">
           <h2 className="text-xl font-bold text-center text-slate-900 dark:text-white">Compartilhar</h2>
           <p className="text-center text-xs text-slate-500 dark:text-slate-400 mt-1">Escolha o formato de envio</p>
        </div>

        {/* Scrollable Preview Area */}
        <div className="overflow-y-auto flex-grow bg-slate-200/50 dark:bg-slate-950 p-6 flex justify-center">
             {/* The Receipt Container */}
             <div 
                id="capture-container"
                ref={summaryRef} 
                className="bg-white w-full max-w-xs shadow-lg relative receipt-jagged-bottom"
                style={{ minHeight: '400px', height: 'max-content' }} 
             >
                {/* Receipt Header */}
                <div className="p-6 pb-4 text-center border-b-2 border-slate-900">
                    <div className="flex justify-center mb-2">
                        <div className="h-8 w-8 bg-slate-900 rounded-full flex items-center justify-center text-white font-bold text-xs">SB</div>
                    </div>
                    <h2 className="text-2xl font-black text-slate-900 uppercase tracking-tighter leading-none">{event.name}</h2>
                    <p className="text-[10px] text-slate-500 uppercase tracking-[0.2em] mt-2 font-mono">{formatDate(event.date || event.createdAt)}</p>
                </div>
                
                {/* Receipt Body */}
                <div className="p-6 pb-0">
                    <GeneralSummary event={event} settlements={settlements} />
                </div>

                {/* Detailed Section */}
                <div className="detailed-section px-6 pb-6">
                     <div className="my-6 flex items-center text-slate-300">
                        <div className="flex-grow border-t border-dashed border-slate-300"></div>
                        <span className="mx-2 text-[10px] uppercase tracking-widest font-bold text-slate-400">Detalhes</span>
                        <div className="flex-grow border-t border-dashed border-slate-300"></div>
                     </div>
                    <DetailedSummary event={event} />
                </div>
                
                {/* Receipt Footer */}
                <div className="pb-8 pt-4 px-6 text-center">
                     <p className="text-[10px] text-slate-400 font-mono uppercase">*** Fim do Recibo ***</p>
                     <p className="text-[9px] text-slate-300 mt-1">Gerado por SplitBill App</p>
                     <div className="h-8 w-full mt-3 bg-[url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAABCAYAAAD5PA/NAAAAFklEQVR4AWP4z8DwHwwDhuEBIA0TBAA8hQME923qOAAAAABJRU5ErkJggg==')] bg-repeat-x opacity-20"></div>
                </div>
            </div>
        </div>

        {/* Footer Actions */}
        <div className="p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex-shrink-0 z-10 space-y-3">
          
          {/* Image Section */}
          <div className="grid grid-cols-2 gap-3">
            <button
                onClick={() => handleShare('summary')}
                disabled={isSharing}
                className="inline-flex items-center justify-center px-4 py-3 border border-slate-300 dark:border-slate-600 text-xs font-bold rounded-xl text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-70 transition-all"
            >
                <ShareIcon className="h-4 w-4 mr-2" />
                Imagem (Resumo)
            </button>
            <button
                onClick={() => handleShare('full')}
                disabled={isSharing}
                className="inline-flex items-center justify-center px-4 py-3 border border-transparent text-xs font-bold rounded-xl text-white bg-violet-600 hover:bg-violet-700 disabled:opacity-70 transition-all"
            >
                <ShareIcon className="h-4 w-4 mr-2" />
                Imagem (Completo)
            </button>
          </div>
           <button onClick={onClose} className="w-full text-center text-xs font-semibold uppercase tracking-wider text-slate-400 hover:text-slate-800 dark:hover:text-white transition-colors p-2">Fechar</button>
        </div>
      </div>
    </div>
  );
};
