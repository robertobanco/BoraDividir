
import React, { useState, useEffect, useRef } from 'react';
import type { Participant, Expense } from '../types';
import { CurrencyDollarIcon } from './icons/CurrencyDollarIcon';
import { TrashIcon } from './icons/TrashIcon';
import { PencilIcon } from './icons/PencilIcon';
import { CameraIcon } from './icons/CameraIcon';
import { PaperClipIcon } from './icons/PaperClipIcon';
import { ReceiptModal } from './ReceiptModal';
import { ChevronDownIcon } from './icons/ChevronDownIcon';

interface ExpenseManagerProps {
  participants: Participant[];
  expenses: Expense[];
  onAddExpense: (expense: Omit<Expense, 'id'>) => void;
  onRemoveExpense: (id: string) => void;
  editingExpense: Expense | null;
  onUpdateExpense: (id: string, expense: Omit<Expense, 'id'>) => void;
  onStartEdit: (expense: Expense) => void;
  onCancelEdit: () => void;
  isExpanded: boolean;
  onToggle: () => void;
}

const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = error => reject(error);
  });
};

export const ExpenseManager: React.FC<ExpenseManagerProps> = ({ participants, expenses, onAddExpense, onRemoveExpense, editingExpense, onUpdateExpense, onStartEdit, onCancelEdit, isExpanded, onToggle }) => {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [paidById, setPaidById] = useState<string>('');
  const [receiptImage, setReceiptImage] = useState<string | null>(null);
  const [viewingReceipt, setViewingReceipt] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const descriptionInputRef = useRef<HTMLInputElement>(null);
  
  useEffect(() => {
    if (editingExpense) {
      setDescription(editingExpense.description);
      setAmount(editingExpense.amount.toFixed(2));
      setPaidById(editingExpense.paidById);
      setReceiptImage(editingExpense.receiptImage || null);
      if (!isExpanded) onToggle(); // Auto expand if editing
    } else {
      resetForm();
    }
  }, [editingExpense]);

  const resetForm = () => {
    setDescription('');
    setAmount('');
    setPaidById('');
    setReceiptImage(null);
    if(fileInputRef.current) fileInputRef.current.value = "";
    if(cameraInputRef.current) cameraInputRef.current.value = "";
    setTimeout(() => descriptionInputRef.current?.focus(), 100);
  }
  
  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const base64 = await fileToBase64(file);
      setReceiptImage(base64);
    }
  };

  const handleCurrencyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rawValue = e.target.value.replace(/\D/g, "");
    if (!rawValue) {
        setAmount("");
        return;
    }
    const value = (parseInt(rawValue) / 100).toFixed(2);
    setAmount(value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const numericAmount = parseFloat(amount);
    if (description.trim() && !isNaN(numericAmount) && numericAmount > 0 && paidById) {
      const expenseData = { description, amount: numericAmount, paidById, receiptImage };
      if(editingExpense) {
        onUpdateExpense(editingExpense.id, expenseData);
      } else {
        onAddExpense(expenseData);
      }
      resetForm();
    }
  };

  const getParticipantName = (id: string) => {
    return participants.find(p => p.id === id)?.name || 'Desconhecido';
  }

  const isFormValid = description.trim() && amount && parseFloat(amount) > 0 && paidById;

  const totalExpenses = expenses.reduce((sum, e) => sum + e.amount, 0);

  return (
    <>
    <div className="glass-card rounded-2xl transition-all duration-300 overflow-hidden">
      <div 
        onClick={onToggle} 
        className="p-5 sm:p-6 flex items-center justify-between cursor-pointer hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors select-none"
      >
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
                <span className="bg-violet-100 dark:bg-violet-900/30 text-violet-600 dark:text-violet-300 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">2</span>
                <h2 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">
                    Despesas
                </h2>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {!isExpanded && expenses.length > 0 && (
                <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 animate-fade-in">
                    <span className="hidden sm:inline font-medium">{expenses.length} itens</span>
                    <span className="hidden sm:inline h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-600"></span>
                    <span className="font-bold text-violet-600 dark:text-violet-400 bg-violet-50 dark:bg-violet-900/20 px-2 py-1 rounded-md">
                        {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(totalExpenses)}
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
                <p className="text-slate-500 dark:text-slate-400">Adicione participantes acima para começar a lançar despesas.</p>
            </div>
        ) : (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                <div className="lg:col-span-5 lg:order-2">
                    <div className="bg-slate-50 dark:bg-slate-800/50 p-4 sm:p-5 rounded-xl border border-slate-100 dark:border-slate-700 sticky top-24">
                        <h3 className="font-semibold text-slate-700 dark:text-slate-200 mb-4 text-sm uppercase tracking-wider">{editingExpense ? 'Editar Despesa' : 'Nova Despesa'}</h3>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">O que foi?</label>
                                <input ref={descriptionInputRef} type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Ex: Supermercado" className="w-full px-3 py-2 bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg text-sm focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-slate-900 dark:text-white" />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Valor (R$)</label>
                                <div className="relative">
                                    <span className="absolute left-3 top-2 text-slate-400 dark:text-slate-500 text-sm">R$</span>
                                    <input 
                                        type="text" 
                                        inputMode="numeric"
                                        value={amount} 
                                        onChange={handleCurrencyChange} 
                                        placeholder="0.00" 
                                        className="w-full pl-9 pr-3 py-2 bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg text-sm focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-slate-900 dark:text-white font-mono" 
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Quem pagou?</label>
                                <select value={paidById} onChange={(e) => setPaidById(e.target.value)} className="w-full px-3 py-2 bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg text-sm focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-slate-900 dark:text-white">
                                    <option value="" disabled>Selecione...</option>
                                    {participants.map((p) => (<option key={p.id} value={p.id}>{p.name}</option>))}
                                </select>
                            </div>
                            
                            <div className="pt-2">
                                <div className="flex gap-2">
                                    <button type="button" onClick={() => fileInputRef.current?.click()} className="flex-1 flex items-center justify-center gap-2 py-2 border border-dashed border-slate-300 dark:border-slate-600 rounded-lg text-xs text-slate-600 dark:text-slate-400 hover:bg-white dark:hover:bg-slate-600 transition-colors">
                                        <PaperClipIcon className="h-4 w-4"/> Anexar
                                    </button>
                                    <button type="button" onClick={() => cameraInputRef.current?.click()} className="flex-1 flex items-center justify-center gap-2 py-2 border border-dashed border-slate-300 dark:border-slate-600 rounded-lg text-xs text-slate-600 dark:text-slate-400 hover:bg-white dark:hover:bg-slate-600 transition-colors">
                                        <CameraIcon className="h-4 w-4"/> Foto
                                    </button>
                                    <input type="file" accept="image/*" ref={fileInputRef} onChange={handleFileChange} className="hidden" />
                                    <input type="file" accept="image/*" capture="environment" ref={cameraInputRef} onChange={handleFileChange} className="hidden" />
                                </div>
                                {receiptImage && (
                                    <div className="mt-2 relative group inline-block">
                                        <img src={receiptImage} alt="Preview" className="h-16 w-16 object-cover rounded-lg border border-slate-200 dark:border-slate-600" />
                                        <button type="button" onClick={() => setReceiptImage(null)} className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-0.5 shadow-sm hover:bg-red-600">
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" /></svg>
                                        </button>
                                    </div>
                                )}
                            </div>

                            <div className="pt-2 flex flex-col gap-2">
                                <button type="submit" disabled={!isFormValid} className="w-full py-2.5 px-4 bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium rounded-lg shadow-md shadow-violet-500/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 disabled:shadow-none transition-all">
                                    {editingExpense ? 'Salvar Alterações' : 'Adicionar Despesa'}
                                </button>
                                {editingExpense && (
                                    <button type="button" onClick={() => { onCancelEdit(); resetForm(); }} className="w-full py-2 text-sm text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200">
                                        Cancelar
                                    </button>
                                )}
                            </div>
                        </form>
                    </div>
                </div>

                <div className="lg:col-span-7 lg:order-1">
                    {expenses.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-full py-12 text-slate-400 dark:text-slate-500">
                            <CurrencyDollarIcon className="h-12 w-12 mb-3 opacity-20" />
                            <p className="text-sm">Nenhuma despesa lançada.</p>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {expenses.map((e) => (
                                <div key={e.id} className="group flex items-center justify-between p-3 sm:p-4 bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm hover:shadow-md transition-all hover:border-violet-200 dark:hover:border-violet-900/50">
                                    <div className="flex items-center gap-3 sm:gap-4 overflow-hidden">
                                        <div className="flex-shrink-0">
                                            {e.receiptImage ? (
                                                <button onClick={() => setViewingReceipt(e.receiptImage as string)} className="relative block group-img">
                                                    <img src={e.receiptImage} alt="recibo" className="h-10 w-10 sm:h-12 sm:w-12 object-cover rounded-lg border border-slate-200 dark:border-slate-600" />
                                                    <div className="absolute inset-0 bg-black/30 rounded-lg opacity-0 group-img-hover:opacity-100 transition-opacity flex items-center justify-center">
                                                        <span className="text-white text-xs">Ver</span>
                                                    </div>
                                                </button>
                                            ) : (
                                                <div className="h-10 w-10 sm:h-12 sm:w-12 rounded-lg bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-slate-400 dark:text-slate-500">
                                                    <CurrencyDollarIcon className="h-5 w-5 sm:h-6 sm:w-6" />
                                                </div>
                                            )}
                                        </div>
                                        <div className="min-w-0">
                                            <p className="font-semibold text-slate-900 dark:text-white truncate text-sm sm:text-base">{e.description}</p>
                                            <p className="text-xs text-slate-500 dark:text-slate-400 truncate">
                                                Pago por <span className="font-medium text-violet-600 dark:text-violet-400">{getParticipantName(e.paidById)}</span>
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex flex-col items-end gap-1 pl-2">
                                        <span className="font-bold text-slate-900 dark:text-white font-mono text-sm sm:text-base">
                                            {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(e.amount)}
                                        </span>
                                        <div className="flex gap-1 opacity-100 sm:opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button onClick={() => onStartEdit(e)} className="p-1 text-slate-400 hover:text-blue-500 transition-colors">
                                                <PencilIcon className="h-4 w-4" />
                                            </button>
                                            <button onClick={() => onRemoveExpense(e.id)} className="p-1 text-slate-400 hover:text-red-500 transition-colors">
                                                <TrashIcon className="h-4 w-4" />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        )}
      </div>
      )}
    </div>
    {viewingReceipt && <ReceiptModal imageUrl={viewingReceipt} onClose={() => setViewingReceipt(null)} />}
    </>
  );
};
