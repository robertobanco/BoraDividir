
import React, { useMemo } from 'react';
import type { BillSplitEvent } from '../types';
import { CheckCircleIcon } from './icons/CheckCircleIcon';
import { ExclamationTriangleIcon } from './icons/ExclamationTriangleIcon';

interface DetailedSummaryProps {
  event: BillSplitEvent;
}

const formatCurrency = (value: number) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);

// Note: This component is styled specifically to look like a paper receipt (Light Mode styles ONLY)
// regardless of the app's theme, to ensure the generated image is clean and printable.

const SharedExpensesDetailed: React.FC<{ event: Extract<BillSplitEvent, {type: 'SHARED_EXPENSES'}> }> = ({ event }) => {
    const totalExpenses = useMemo(() => event.expenses.reduce((sum, exp) => sum + exp.amount, 0), [event.expenses]);
    const costPerPerson = useMemo(() => event.participants.length > 0 ? totalExpenses / event.participants.length : 0, [totalExpenses, event.participants.length]);

    if (event.participants.length === 0) {
        return <p className="text-sm text-slate-400 text-center py-4 italic">Sem dados para exibir.</p>;
    }

    return (
        <div className="space-y-6">
            {event.participants.map(participant => {
                const paidExpenses = event.expenses.filter(e => e.paidById === participant.id);
                const totalPaid = paidExpenses.reduce((sum, e) => sum + e.amount, 0);
                const balance = totalPaid - costPerPerson;
                const isSettled = Math.abs(balance) < 0.01;
                
                return (
                    <div key={participant.id} className="border-b border-dashed border-slate-200 last:border-0 pb-4 last:pb-0">
                        <div className="flex justify-between items-baseline mb-2">
                            <h4 className="font-bold text-slate-800 text-lg">{participant.name}</h4>
                            <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${balance >= 0 ? 'bg-blue-50 text-blue-600' : 'bg-red-50 text-red-600'}`}>
                                {isSettled ? 'Zerado' : (balance >= 0 ? 'Recebe' : 'Paga')}
                            </span>
                        </div>
                        
                        <div className="space-y-1 text-sm">
                             {paidExpenses.length > 0 && (
                                <div className="mb-2 bg-slate-50 p-2 rounded border border-slate-100">
                                    <p className="text-xs font-semibold text-slate-500 mb-1 uppercase tracking-wider">Pagamentos Realizados</p>
                                    <ul className="space-y-1">
                                        {paidExpenses.map(e => (
                                            <li key={e.id} className="flex justify-between text-slate-600 text-xs">
                                                <span>{e.description}</span>
                                                <span className="font-mono">{formatCurrency(e.amount)}</span>
                                            </li>
                                        ))}
                                    </ul>
                                    <div className="border-t border-slate-200 mt-2 pt-1 flex justify-between font-medium text-slate-700">
                                        <span>Total Pago</span>
                                        <span>{formatCurrency(totalPaid)}</span>
                                    </div>
                                </div>
                            )}
                            
                            <div className="flex justify-between text-slate-500 text-xs">
                                <span>Quota individual</span>
                                <span>- {formatCurrency(costPerPerson)}</span>
                            </div>

                             <div className="flex justify-between items-center pt-2 mt-1">
                                <span className="font-semibold text-slate-800">Saldo</span>
                                {isSettled ? (
                                    <span className="font-bold text-emerald-600 flex items-center gap-1 text-sm">0,00 <CheckCircleIcon className="h-4 w-4" /></span>
                                ) : (
                                    <span className={`font-bold font-mono text-base ${balance > 0 ? 'text-blue-600' : 'text-red-600'}`}>
                                        {balance > 0 ? '+' : ''}{formatCurrency(balance)}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                )
            })}
        </div>
    )
};

const ItemizedBillDetailed: React.FC<{ event: Extract<BillSplitEvent, {type: 'ITEMIZED_BILL'}> }> = ({ event }) => {
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
        
        const participantDetails = event.participants.map(p => {
            const subtotal = participantSubtotals.get(p.id) || 0;
            const fees = itemsSubtotal > 0 ? (subtotal / itemsSubtotal) * totalFees : 0;
            const total = subtotal + fees;
            return { participantId: p.id, name: p.name, subtotal, fees, total };
        });
        
        return { participantDetails };
    }, [event]);

    if (event.participants.length === 0) {
        return <p className="text-sm text-slate-400 text-center py-4 italic">Sem dados.</p>;
    }
     if (event.items.some(item => item.consumedByIds.length === 0)) {
        return <p className="text-sm text-amber-700 text-center py-4 bg-amber-50 border border-amber-100 rounded-lg flex items-center justify-center gap-2"><ExclamationTriangleIcon className="h-5 w-5" /> Itens não atribuídos.</p>;
    }

    return (
         <div className="space-y-6">
            {calculation.participantDetails.map(p => {
                const consumedItems = event.items.filter(item => item.consumedByIds.includes(p.participantId));
                const actualPayment = event.actualPayments.find(ap => ap.participantId === p.participantId);
                const balance = actualPayment ? actualPayment.amount - p.total : -p.total;
                const isSettled = Math.abs(balance) < 0.01;

                return (
                    <div key={p.participantId} className="border-b border-dashed border-slate-200 last:border-0 pb-4 last:pb-0">
                         <div className="flex justify-between items-baseline mb-2">
                            <h4 className="font-bold text-slate-800 text-lg">{p.name}</h4>
                            <span className="text-xs font-medium text-slate-400">Consumidor</span>
                        </div>

                        <div className="space-y-1 text-sm">
                            {consumedItems.length > 0 ? (
                                <div className="mb-2 bg-slate-50 p-2 rounded border border-slate-100">
                                    <ul className="space-y-1">
                                        {consumedItems.map(item => (
                                            <li key={item.id} className="flex justify-between text-slate-600 text-xs">
                                                <span>{item.description} <span className="text-slate-400 text-[10px] ml-1">{item.consumedByIds.length > 1 ? `(1/${item.consumedByIds.length})` : ''}</span></span>
                                                <span className="font-mono">{formatCurrency(item.amount / item.consumedByIds.length)}</span>
                                            </li>
                                        ))}
                                    </ul>
                                    <div className="border-t border-slate-200 mt-2 pt-1 flex justify-between font-medium text-slate-700 text-xs">
                                        <span>Soma Itens</span>
                                        <span>{formatCurrency(p.subtotal)}</span>
                                    </div>
                                </div>
                            ) : <p className="text-xs text-slate-400 italic">Nenhum consumo direto.</p>}

                            <div className="flex justify-between text-slate-500 text-xs">
                                <span>Taxas / Gorjeta (Prop.)</span>
                                <span>+ {formatCurrency(p.fees)}</span>
                            </div>
                            
                            <div className="flex justify-between font-bold text-slate-900 text-base pt-1">
                                <span>Total da Parte</span>
                                <span>{formatCurrency(p.total)}</span>
                            </div>

                             {actualPayment && (
                                <div className="flex justify-between text-emerald-600 text-xs mt-1 font-medium">
                                    <span>Valor Pago</span>
                                    <span>- {formatCurrency(actualPayment.amount)}</span>
                                </div>
                             )}

                            <div className="flex justify-between items-center pt-2 border-t border-slate-100 mt-2">
                                <span className="font-semibold text-slate-800">Situação</span>
                                {isSettled && actualPayment ? (
                                    <span className="font-bold text-emerald-600 flex items-center gap-1 text-sm">Pago <CheckCircleIcon className="h-4 w-4" /></span>
                                ) : (
                                    <span className={`font-bold font-mono ${balance >= 0 ? 'text-blue-600' : 'text-red-600'}`}>
                                        {balance >= 0 ? 'Troco: ' : 'Falta: '} {formatCurrency(Math.abs(balance))}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                )
            })}
        </div>
    )
};


export const DetailedSummary: React.FC<DetailedSummaryProps> = ({ event }) => {
  return (
    <div>
        {event.type === 'SHARED_EXPENSES' && <SharedExpensesDetailed event={event} />}
        {event.type === 'ITEMIZED_BILL' && <ItemizedBillDetailed event={event} />}
    </div>
  );
};
