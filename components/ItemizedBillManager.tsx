
import React, { useState, useMemo, useRef } from 'react';
import type { Participant, BillItem, ActualPayment } from '../types';
import { TrashIcon } from './icons/TrashIcon';
import { CurrencyDollarIcon } from './icons/CurrencyDollarIcon';
import { ShareIcon } from './icons/ShareIcon';
import { PencilIcon } from './icons/PencilIcon';
import { CheckCircleIcon } from './icons/CheckCircleIcon';
import { ArrowPathIcon } from './icons/ArrowPathIcon';
import { ExclamationTriangleIcon } from './icons/ExclamationTriangleIcon';
import { ChevronDownIcon } from './icons/ChevronDownIcon';

interface ItemizedBillManagerProps {
  participants: Participant[];
  items: BillItem[];
  tip: { value: number, type: 'PERCENT' | 'FIXED' };
  tax: number;
  billSubtotal: number;
  actualPayments: ActualPayment[];
  onUpdateItems: (items: BillItem[]) => void;
  onUpdateActualPayments: (payments: ActualPayment[]) => void;
  onOpenSummary: () => void;
  isExpanded: boolean;
  onToggle: () => void;
}

const formatCurrency = (val: number) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

const handleCurrencyInput = (val: string) => {
    const raw = val.replace(/\D/g, "");
    if (!raw) return "";
    return (parseInt(raw) / 100).toFixed(2);
};

// Subcomponent for Settlement (Refined for new design)
const ItemizedSettlementManager: React.FC<{
    participants: Participant[],
    items: BillItem[],
    tip: { value: number, type: 'PERCENT' | 'FIXED' },
    tax: number,
    actualPayments: ActualPayment[],
    onUpdateActualPayments: (payments: ActualPayment[]) => void,
    isValid: boolean,
    onOpenSummary: () => void;
    unassignedItemsCount: number;
}> = ({ participants, items, tip, tax, actualPayments, onUpdateActualPayments, isValid, onOpenSummary, unassignedItemsCount }) => {
    
    const [editingPaymentId, setEditingPaymentId] = useState<string | null>(null);
    const [editingAmount, setEditingAmount] = useState('');

    const originalCalculation = useMemo(() => {
        const participantSubtotals = new Map<string, number>(participants.map(p => [p.id, 0]));
        const itemsSubtotal = items.reduce((sum, item) => sum + item.amount, 0);
        
        items.forEach(item => {
            if (item.consumedByIds.length > 0) {
                const costPerPerson = item.amount / item.consumedByIds.length;
                item.consumedByIds.forEach(id => {
                    participantSubtotals.set(id, (participantSubtotals.get(id) || 0) + costPerPerson);
                });
            }
        });

        const tipAmount = tip.type === 'PERCENT' ? itemsSubtotal * (tip.value / 100) : tip.value;
        const totalFees = tipAmount + tax;
        
        const participantTotals = participants.map(p => {
            const individualSubtotal = participantSubtotals.get(p.id) || 0;
            const proportionalFees = itemsSubtotal > 0 ? (individualSubtotal / itemsSubtotal) * totalFees : 0;
            const total = individualSubtotal + proportionalFees;
            return { participantId: p.id, name: p.name, total, subtotal: individualSubtotal };
        });
        
        return { billTotal: itemsSubtotal + totalFees, participantTotals, itemsSubtotal, totalFees };
    }, [participants, items, tip, tax]);

    const dynamicPaymentStatus = useMemo(() => {
        const totalPaid = actualPayments.reduce((sum, p) => sum + p.amount, 0);
        const remainingBill = originalCalculation.billTotal - totalPaid;

        const unpaidParticipants = originalCalculation.participantTotals.filter(
            p => !actualPayments.some(ap => ap.participantId === p.participantId)
        );

        const totalSubtotalOfUnpaid = unpaidParticipants.reduce((sum, p) => sum + p.subtotal, 0);
        const paymentStatusMap = new Map<string, { toPay: number }>();

        if (totalSubtotalOfUnpaid > 0) {
            unpaidParticipants.forEach(p => {
                const proportionalShare = p.subtotal / totalSubtotalOfUnpaid;
                const amountToPay = proportionalShare * remainingBill;
                paymentStatusMap.set(p.participantId, { toPay: Math.max(0, amountToPay) });
            });
        } else if (unpaidParticipants.length > 0) {
            const amountToPay = remainingBill / unpaidParticipants.length;
            unpaidParticipants.forEach(p => {
                paymentStatusMap.set(p.participantId, { toPay: Math.max(0, amountToPay) });
            });
        }
        return paymentStatusMap;
    }, [actualPayments, originalCalculation]);

    const handleConfirmPayment = (participantId: string, amount: number) => {
        const existingPayment = actualPayments.find(p => p.participantId === participantId);
        if (existingPayment) {
            onUpdateActualPayments(actualPayments.map(p => p.participantId === participantId ? { ...p, amount } : p));
        } else {
            onUpdateActualPayments([...actualPayments, { participantId, amount }]);
        }
        setEditingPaymentId(null);
        setEditingAmount('');
    };
    
    const handleStartEdit = (participantId: string, currentAmountToPay: number) => {
        setEditingPaymentId(participantId);
        const currentPaidAmount = actualPayments.find(p => p.participantId === participantId)?.amount;
        setEditingAmount(currentPaidAmount ? currentPaidAmount.toFixed(2) : currentAmountToPay.toFixed(2));
    };

    if(participants.length === 0 || items.length === 0) return null;

    // --- Lógica de validação e mensagens de erro/sucesso ---
    const totalPaid = actualPayments.reduce((sum, p) => sum + p.amount, 0);
    const remainingTotal = originalCalculation.billTotal - totalPaid;
    
    // Tolerância para ponto flutuante
    const isOverPaid = remainingTotal < -0.01;
    const isUnderPaid = remainingTotal > 0.01;

    // Verifica se cobriu pelo menos os itens
    const itemsOnlyTotal = originalCalculation.itemsSubtotal;
    // Use a slightly smaller number than itemsOnlyTotal to avoid float precision issues blocking "Exact" item payment
    const coversItems = totalPaid >= (itemsOnlyTotal - 0.1);
    
    // Condição para liberar o botão: Não falta nada OU falta mas já cobriu os itens
    const canGenerateReceipt = !isUnderPaid || coversItems;
    
    const missingFees = coversItems && isUnderPaid;

    let statusMessage = null;
    let statusColor = "";

    if (isOverPaid) {
        statusMessage = `Sobrou dinheiro! Haverá troco de ${formatCurrency(Math.abs(remainingTotal))}.`;
        statusColor = "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300 border-blue-200 dark:border-blue-800";
    } else if (missingFees) {
        statusMessage = `O valor cobre os itens, mas faltam ${formatCurrency(remainingTotal)} (Taxas). Recibo liberado.`;
        statusColor = "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300 border-amber-200 dark:border-amber-800";
    } else if (isUnderPaid) {
        statusMessage = `Faltam ${formatCurrency(remainingTotal)} para fechar a conta.`;
        statusColor = "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300 border-red-200 dark:border-red-800";
    } else {
        statusMessage = "Conta fechada com sucesso!";
        statusColor = "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800";
    }

    if (unassignedItemsCount > 0) {
        return (
            <div className="glass-card rounded-2xl p-6 mt-8 animate-fade-in">
                <h2 className="text-xl font-bold mb-4 text-slate-900 dark:text-white">Resultado</h2>
                <div className="flex items-center gap-3 bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-300 p-4 rounded-xl border border-amber-200 dark:border-amber-800">
                    <ExclamationTriangleIcon className="h-6 w-6 flex-shrink-0" />
                    <p className="font-medium text-sm">
                        Existem {unassignedItemsCount} item(ns) não atribuídos. Atribua todos para calcular.
                    </p>
                </div>
            </div>
        );
    }
    
    return (
        <div className="glass-card rounded-2xl p-6 mt-8 animate-fade-in border-t-4 border-t-emerald-500">
             <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <span className="bg-violet-100 dark:bg-violet-900/30 text-violet-600 dark:text-violet-400 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">3</span>
                    Pagamento
                </h2>
                {actualPayments.length > 0 && (
                    <button onClick={() => onUpdateActualPayments([])} className="flex items-center gap-1.5 text-xs font-medium text-slate-500 hover:text-indigo-600 transition-colors">
                        <ArrowPathIcon className="h-4 w-4" />
                        Reiniciar
                    </button>
                )}
             </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                 <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-700">
                     <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">Total Calculado</p>
                     <p className="text-xl font-bold text-slate-900 dark:text-white mt-1">{formatCurrency(originalCalculation.billTotal)}</p>
                 </div>
                 <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-700">
                     <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">Total Pago</p>
                     <p className="text-xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">{formatCurrency(totalPaid)}</p>
                 </div>
                  <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-700">
                     <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">{remainingTotal >= 0 ? 'Falta' : 'Troco'}</p>
                     <p className={`text-xl font-bold mt-1 ${remainingTotal > 0.01 ? 'text-red-500' : 'text-blue-500'}`}>{formatCurrency(Math.abs(remainingTotal))}</p>
                 </div>
            </div>

            <div className={`mb-6 p-4 rounded-xl border flex items-start gap-3 ${statusColor}`}>
                {isUnderPaid ? <ExclamationTriangleIcon className="h-5 w-5 flex-shrink-0 mt-0.5"/> : <CheckCircleIcon className="h-5 w-5 flex-shrink-0 mt-0.5"/>}
                <p className="font-medium text-sm">{statusMessage}</p>
            </div>

            <div className="space-y-3">
                {originalCalculation.participantTotals.map(p => {
                    const actualPayment = actualPayments.find(ap => ap.participantId === p.participantId);
                    const dynamicStatus = dynamicPaymentStatus.get(p.participantId);
                    const amountToPay = dynamicStatus?.toPay ?? 0;
                    const paymentDifference = actualPayment ? actualPayment.amount - p.total : 0;
                    const isExact = Math.abs(paymentDifference) < 0.01;
                    const isOver = paymentDifference > 0;

                    return (
                    <div key={p.participantId} className={`flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl border transition-all ${actualPayment ? 'bg-emerald-50/50 dark:bg-emerald-900/10 border-emerald-100 dark:border-emerald-800/30' : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700'}`}>
                        <div className="mb-2 sm:mb-0">
                            <p className="font-bold text-slate-900 dark:text-white">{p.name}</p>
                            <p className="text-xs text-slate-500 dark:text-slate-400">Deveria pagar: {formatCurrency(p.total)}</p>
                        </div>

                        <div className="flex items-center justify-end gap-3">
                            {editingPaymentId === p.participantId ? (
                                    <div className="flex items-center gap-2 animate-fade-in">
                                    <input 
                                        type="text" 
                                        inputMode="numeric"
                                        value={editingAmount} 
                                        onChange={e => setEditingAmount(handleCurrencyInput(e.target.value))} 
                                        onKeyDown={e => e.key === 'Enter' && handleConfirmPayment(p.participantId, parseFloat(editingAmount) || 0)} 
                                        className="w-24 text-right px-2 py-1 bg-white dark:bg-slate-900 border border-violet-500 rounded-lg text-sm shadow-sm focus:outline-none" 
                                        autoFocus
                                    />
                                    <button onClick={() => handleConfirmPayment(p.participantId, parseFloat(editingAmount) || 0)} className="p-1.5 bg-violet-600 text-white rounded-lg text-xs font-bold shadow-sm">OK</button>
                                </div>
                            ) : (
                                <>
                                    {actualPayment ? (
                                        <div className="text-right mr-2">
                                            <p className="font-bold text-emerald-700 dark:text-emerald-400">{formatCurrency(actualPayment.amount)}</p>
                                            {!isExact && (
                                                 <p className={`text-xs font-medium ${isOver ? 'text-blue-500' : 'text-red-500'}`}>
                                                    {isOver ? '+' : ''}{formatCurrency(paymentDifference)}
                                                </p>
                                            )}
                                        </div>
                                    ) : (
                                         <span className="font-mono font-medium text-slate-400 dark:text-slate-500 mr-2">
                                            Sugestão: {formatCurrency(amountToPay)}
                                         </span>
                                    )}

                                    <div className="flex gap-1">
                                        {!actualPayment && (
                                            <button onClick={() => handleConfirmPayment(p.participantId, amountToPay)} className="p-2 rounded-lg bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400 hover:bg-emerald-200 dark:hover:bg-emerald-900/50 transition-colors" title="Confirmar pagamento sugerido">
                                                <CheckCircleIcon className="h-5 w-5"/>
                                            </button>
                                        )}
                                        <button onClick={() => handleStartEdit(p.participantId, amountToPay)} className="p-2 rounded-lg bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors" title="Editar valor">
                                            <PencilIcon className="h-5 w-5"/>
                                        </button>
                                    </div>
                                </>
                            )}
                        </div>
                    </div>
                )})}
            </div>
            
             {/* Show Generate Receipt button if it can generate receipt (either fully paid or covers items) */}
             {canGenerateReceipt ? (
                <div className="mt-8 flex justify-center">
                    <button
                        onClick={onOpenSummary}
                        className="inline-flex items-center justify-center px-6 py-2.5 border border-slate-300 dark:border-slate-600 rounded-full text-sm font-medium text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 shadow-sm transition-all hover:scale-105 active:scale-95"
                    >
                        <ShareIcon className="h-4 w-4 mr-2" />
                        Gerar Recibo
                    </button>
                </div>
             ) : (
                 <div className="mt-6 text-center">
                     <p className="text-sm text-slate-400 dark:text-slate-500 italic">Complete os pagamentos dos itens para gerar o recibo.</p>
                 </div>
             )}
        </div>
    );
};


export const ItemizedBillManager: React.FC<ItemizedBillManagerProps> = ({ participants, items, tip, tax, billSubtotal, actualPayments, onUpdateItems, onUpdateActualPayments, onOpenSummary, isExpanded, onToggle }) => {
  const [itemDescription, setItemDescription] = useState('');
  const [itemAmount, setItemAmount] = useState('');
  const [editingItemId, setEditingItemId] = useState<string | null>(null);
  const [editingItemData, setEditingItemData] = useState({ description: '', amount: '' });
  const itemDescriptionRef = useRef<HTMLInputElement>(null);

  const itemsSubtotal = useMemo(() => items.reduce((sum, item) => sum + item.amount, 0), [items]);
  const difference = billSubtotal - itemsSubtotal;
  const isSubtotalValid = Math.abs(difference) < 0.01;

  const handleAddItem = (e: React.FormEvent) => {
    e.preventDefault();
    const amount = parseFloat(itemAmount);
    if(itemDescription.trim() && !isNaN(amount) && amount > 0) {
      const newItem: BillItem = {
        id: crypto.randomUUID(),
        description: itemDescription.trim(),
        amount,
        consumedByIds: []
      }
      const newItems = [...items, newItem];
      onUpdateItems(newItems);
      setItemDescription('');
      setItemAmount('');

      const newItemsSubtotal = newItems.reduce((sum, item) => sum + item.amount, 0);
      if (billSubtotal > newItemsSubtotal) {
          itemDescriptionRef.current?.focus();
      }
    }
  };
  
  const handleRemoveItem = (id: string) => {
    onUpdateItems(items.filter(item => item.id !== id));
  };

  const handleStartEditItem = (item: BillItem) => {
    setEditingItemId(item.id);
    setEditingItemData({ description: item.description, amount: item.amount.toFixed(2) });
  }

  const handleCancelEditItem = () => {
    setEditingItemId(null);
    setEditingItemData({ description: '', amount: '' });
  }

  const handleSaveEditItem = (id: string) => {
    const amount = parseFloat(editingItemData.amount);
    if (editingItemData.description.trim() && !isNaN(amount) && amount > 0) {
      onUpdateItems(items.map(item => item.id === id ? { ...item, description: editingItemData.description.trim(), amount } : item));
      handleCancelEditItem();
    }
  }

  const handleToggleConsumer = (itemId: string, participantId: string) => {
    const updatedItems = items.map(item => {
      if (item.id === itemId) {
        const isConsuming = item.consumedByIds.includes(participantId);
        const newConsumedByIds = isConsuming
          ? item.consumedByIds.filter(id => id !== participantId)
          : [...item.consumedByIds, participantId];
        return { ...item, consumedByIds: newConsumedByIds };
      }
      return item;
    });
    onUpdateItems(updatedItems);
  };
  
  const handleToggleAllConsumers = (itemId: string) => {
     const updatedItems = items.map(item => {
      if (item.id === itemId) {
        const allAreConsumers = item.consumedByIds.length === participants.length;
        return { ...item, consumedByIds: allAreConsumers ? [] : participants.map(p => p.id) };
      }
      return item;
    });
    onUpdateItems(updatedItems);
  }

  return (
    <div className="space-y-6">
        {/* Main Items List Container */}
        <div className="glass-card rounded-2xl transition-all duration-300 overflow-hidden">
            <div 
              onClick={onToggle} 
              className="p-5 sm:p-6 flex items-center justify-between cursor-pointer hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors select-none"
            >
                <div className="flex items-center gap-3">
                   <div className="flex items-center gap-2">
                        <span className="bg-violet-100 dark:bg-violet-900/30 text-violet-600 dark:text-violet-300 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">2</span>
                        <h2 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">
                            Consumo
                        </h2>
                    </div>
                </div>
                
                <div className="flex items-center gap-3">
                    {/* Always show summary when collapsed */}
                    {!isExpanded && items.length > 0 && (
                        <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 animate-fade-in">
                             <span className="hidden sm:inline font-medium">{items.length} itens</span>
                             <span className="hidden sm:inline h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-600"></span>
                             <span className="font-bold text-violet-600 dark:text-violet-400 bg-violet-50 dark:bg-violet-900/20 px-2 py-1 rounded-md">
                                {formatCurrency(itemsSubtotal)}
                             </span>
                        </div>
                    )}
                    <ChevronDownIcon className={`h-5 w-5 text-slate-400 transition-transform duration-300 flex-shrink-0 ${isExpanded ? 'rotate-180' : ''}`} />
                </div>
            </div>

            {isExpanded && (
            <div className="px-4 pb-6 sm:px-6 animate-fade-in">
                {participants.length < 1 ? (
                    <div className="text-center py-8 bg-slate-50 dark:bg-slate-800/30 rounded-xl border border-dashed border-slate-200 dark:border-slate-700">
                        <p className="text-slate-500 dark:text-slate-400">Adicione participantes para registrar o consumo.</p>
                    </div>
                ) : (
                    <>
                        <form onSubmit={handleAddItem} className="flex gap-2 mb-6">
                            <input ref={itemDescriptionRef} type="text" value={itemDescription} onChange={e => setItemDescription(e.target.value)} placeholder="Item (ex: Suco)" className="flex-grow px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm focus:ring-2 focus:ring-violet-500" />
                            <input 
                                type="text" 
                                inputMode="numeric"
                                value={itemAmount} 
                                onChange={e => setItemAmount(handleCurrencyInput(e.target.value))} 
                                placeholder="R$" 
                                className="w-20 sm:w-24 px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm focus:ring-2 focus:ring-violet-500" 
                            />
                            <button type="submit" disabled={!itemDescription.trim() || !itemAmount} className="bg-violet-600 hover:bg-violet-700 text-white p-2 rounded-lg transition-colors disabled:opacity-50 flex-shrink-0">
                                <CurrencyDollarIcon className="h-5 w-5"/>
                            </button>
                        </form>

                        <div className="space-y-3">
                            {items.length === 0 ? <p className="text-sm text-slate-400 text-center italic">Nenhum item adicionado.</p> : items.map(item => (
                                <div key={item.id} className={`p-3 sm:p-4 bg-white dark:bg-slate-800 border rounded-xl transition-all ${item.consumedByIds.length === 0 ? 'border-red-300 dark:border-red-500/50 shadow-sm shadow-red-100 dark:shadow-none' : 'border-slate-200 dark:border-slate-700 shadow-sm'}`}>
                                {editingItemId === item.id ? (
                                    <div className="space-y-2">
                                        <div className="flex gap-2">
                                            <input type="text" value={editingItemData.description} onChange={e => setEditingItemData({...editingItemData, description: e.target.value})} className="flex-grow px-2 py-1 bg-white dark:bg-slate-900 border border-violet-500 rounded-md text-sm" />
                                            <input 
                                                type="text" 
                                                inputMode="numeric"
                                                value={editingItemData.amount} 
                                                onChange={e => setEditingItemData({...editingItemData, amount: handleCurrencyInput(e.target.value)})} 
                                                className="w-24 px-2 py-1 bg-white dark:bg-slate-900 border border-violet-500 rounded-md text-sm" 
                                            />
                                        </div>
                                        <div className="flex justify-end gap-2">
                                            <button onClick={() => handleSaveEditItem(item.id)} className="text-xs font-bold text-violet-600 dark:text-violet-400">Salvar</button>
                                            <button onClick={handleCancelEditItem} className="text-xs text-slate-400">Cancelar</button>
                                        </div>
                                    </div>
                                ) : (
                                    <>
                                        <div className="flex justify-between items-start mb-3">
                                            <div>
                                                <p className="font-semibold text-slate-900 dark:text-white text-sm sm:text-base">{item.description}</p>
                                                <p className="text-sm text-slate-500 dark:text-slate-400 font-mono">{formatCurrency(item.amount)}</p>
                                            </div>
                                            <div className="flex items-center gap-1">
                                                <button onClick={() => handleStartEditItem(item)} className="p-2 text-slate-400 hover:text-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-full transition-colors"><PencilIcon className="h-4 w-4"/></button>
                                                <button onClick={() => handleRemoveItem(item.id)} className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-full transition-colors"><TrashIcon className="h-4 w-4"/></button>
                                            </div>
                                        </div>
                                        
                                        <div>
                                            <div className="flex flex-wrap gap-1.5">
                                                <button onClick={() => handleToggleAllConsumers(item.id)} className={`px-2 py-0.5 text-xs rounded-full border transition-all ${item.consumedByIds.length === participants.length ? 'bg-slate-800 text-white border-slate-800 dark:bg-slate-200 dark:text-slate-900 dark:border-slate-200' : 'bg-transparent text-slate-500 border-slate-200 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700'}`}>
                                                    Todos
                                                </button>
                                                {participants.map(p => (
                                                    <button key={p.id} onClick={() => handleToggleConsumer(item.id, p.id)} className={`px-2 py-0.5 text-xs rounded-full border transition-all ${item.consumedByIds.includes(p.id) ? 'bg-violet-100 text-violet-700 border-violet-200 dark:bg-violet-900/40 dark:text-violet-300 dark:border-violet-800' : 'bg-transparent text-slate-500 border-slate-200 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700'}`}>
                                                    {p.name}
                                                    </button>
                                                ))}
                                            </div>
                                        </div>
                                    </>
                                )}
                                </div>
                            ))}
                        </div>
                    </>
                )}
            </div>
            )}
        </div>

      {isSubtotalValid ? (
         <ItemizedSettlementManager participants={participants} items={items} tip={tip} tax={tax} actualPayments={actualPayments} onUpdateActualPayments={onUpdateActualPayments} isValid={isSubtotalValid} onOpenSummary={onOpenSummary} unassignedItemsCount={items.filter(i => i.consumedByIds.length === 0).length} />
      ) : (
         <div className="glass-card rounded-2xl p-8 mt-8 text-center border-t-4 border-t-amber-400">
            <ExclamationTriangleIcon className="h-12 w-12 text-amber-400 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-1">Validação Pendente</h3>
            <p className="text-slate-500 dark:text-slate-400 max-w-md mx-auto">
                A soma dos itens lançados ({formatCurrency(itemsSubtotal)}) deve ser exatamente igual ao Subtotal da nota ({formatCurrency(billSubtotal)}) para prosseguir para o pagamento.
            </p>
            <p className="mt-4 font-mono font-bold text-amber-600 dark:text-amber-400">
                Diferença: {formatCurrency(difference)}
            </p>
         </div>
      )}
    </div>
  );
};
