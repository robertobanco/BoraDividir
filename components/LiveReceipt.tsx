
import React, { useMemo } from 'react';
import type { BillItem } from '../types';
import { PencilIcon } from './icons/PencilIcon';
import { CheckCircleIcon } from './icons/CheckCircleIcon';
import { ExclamationTriangleIcon } from './icons/ExclamationTriangleIcon';

interface LiveReceiptProps {
    items: BillItem[];
    tip: { value: number; type: 'PERCENT' | 'FIXED' };
    tax: number;
    billSubtotal: number;
    onEditDetails: () => void;
}

const formatCurrency = (val: number) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

export const LiveReceipt: React.FC<LiveReceiptProps> = ({ items, tip, tax, billSubtotal, onEditDetails }) => {
    const itemsSubtotal = useMemo(() => items.reduce((sum, item) => sum + item.amount, 0), [items]);
  
    const tipAmount = useMemo(() => {
        if (tip.type === 'PERCENT') {
            return itemsSubtotal * (tip.value / 100);
        }
        return tip.value;
    }, [itemsSubtotal, tip]);

    const calculatedTotal = itemsSubtotal + tipAmount + tax;
    const difference = billSubtotal - itemsSubtotal;
    const isSubtotalValid = Math.abs(difference) < 0.01;

    const getStatusStyles = () => {
        if (billSubtotal === 0) return { colorClass: 'text-slate-400', text: 'Meta não definida' };
        if (isSubtotalValid) return { colorClass: 'text-emerald-500', text: 'Completo' };
        if (difference > 0) return { colorClass: 'text-amber-500', text: 'Falta lançar' };
        return { colorClass: 'text-red-500', text: 'Passou do valor' };
    };
    const status = getStatusStyles();

    return (
        <div className="mb-6">
            <div className="bg-white dark:bg-slate-800 shadow-lg rounded-lg overflow-hidden receipt-jagged-bottom dark:receipt-jagged-bottom dark-receipt max-w-2xl mx-auto">
                <div className="bg-slate-50 dark:bg-slate-900/50 p-3 border-b border-slate-200 dark:border-slate-700 flex justify-between items-center">
                    <h3 className="font-bold text-slate-700 dark:text-slate-200 uppercase tracking-widest text-xs">Recibo Fiscal</h3>
                    <button onClick={onEditDetails} className="text-slate-400 hover:text-violet-600 dark:hover:text-violet-400 transition-colors flex items-center gap-1 text-xs">
                        <PencilIcon className="h-3 w-3" /> Editar
                    </button>
                </div>
                
                <div className="p-4 grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm font-mono">
                    <div className="flex flex-col justify-center">
                        <span className="text-xs text-slate-500 dark:text-slate-400">Itens</span>
                        <span className="font-bold text-slate-700 dark:text-slate-200">{formatCurrency(itemsSubtotal)}</span>
                    </div>
                    <div className="flex flex-col justify-center border-l border-slate-100 dark:border-slate-700 pl-4">
                        <span className="text-xs text-slate-500 dark:text-slate-400">Taxas</span>
                        <span className="text-slate-600 dark:text-slate-300">{formatCurrency(tipAmount + tax)}</span>
                    </div>
                    <div className="flex flex-col justify-center border-l border-slate-100 dark:border-slate-700 pl-4 col-span-2 sm:col-span-1">
                        <span className="text-xs text-slate-500 dark:text-slate-400 font-bold">TOTAL</span>
                        <span className="font-bold text-lg text-slate-900 dark:text-white leading-tight">{formatCurrency(calculatedTotal)}</span>
                    </div>
                    <div className="flex flex-col justify-center items-end border-l border-slate-100 dark:border-slate-700 pl-4 sm:items-center col-span-2 sm:col-span-1">
                         <div className="text-right sm:text-center">
                            <div className={`text-xs font-bold uppercase ${status.colorClass}`}>{status.text}</div>
                            {!isSubtotalValid && billSubtotal > 0 && (
                                <div className="text-xs text-slate-400">{formatCurrency(Math.abs(difference))}</div>
                            )}
                         </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
