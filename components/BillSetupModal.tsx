
import React, { useState, useMemo } from 'react';

type BillDetails = {
    billSubtotal: number;
    tip: { value: number; type: 'PERCENT' | 'FIXED' };
    tax: number;
}

interface BillSetupModalProps {
  onConfirm: (details: BillDetails) => void;
  onCancel: () => void;
  initialData?: BillDetails;
}

const handleCurrencyInput = (val: string) => {
    const raw = val.replace(/\D/g, "");
    if (!raw) return "";
    return (parseInt(raw) / 100).toFixed(2);
};

export const BillSetupModal: React.FC<BillSetupModalProps> = ({ onConfirm, onCancel, initialData }) => {
    const [subtotal, setSubtotal] = useState(String(initialData?.billSubtotal ? initialData.billSubtotal.toFixed(2) : ''));
    const [tipType, setTipType] = useState<'PERCENT' | 'FIXED'>(initialData?.tip.type || 'PERCENT');
    const [tipValue, setTipValue] = useState(String(initialData?.tip.value !== undefined ? (initialData.tip.type === 'PERCENT' ? initialData.tip.value : initialData.tip.value.toFixed(2)) : ''));
    const [tax, setTax] = useState(String(initialData?.tax ? initialData.tax.toFixed(2) : ''));
    
    const numericSubtotal = parseFloat(subtotal) || 0;
    const numericTip = parseFloat(tipValue) || 0;
    const numericTax = parseFloat(tax) || 0;

    const calculatedTotal = useMemo(() => {
        const tipAmount = tipType === 'PERCENT' ? numericSubtotal * (numericTip / 100) : numericTip;
        return numericSubtotal + tipAmount + numericTax;
    }, [numericSubtotal, tipType, numericTip, numericTax]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (numericSubtotal > 0) {
            onConfirm({
                billSubtotal: numericSubtotal,
                tip: {
                    type: tipType,
                    value: numericTip
                },
                tax: numericTax
            });
        }
    };

    const handleTipChange = (val: string) => {
        if (tipType === 'PERCENT') {
             setTipValue(val); 
        } else {
             setTipValue(handleCurrencyInput(val));
        }
    }
    
    return (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
            <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-xl w-full max-w-sm">
                <h3 className="text-lg font-semibold mb-2 text-slate-900 dark:text-slate-100">{initialData ? 'Editar Detalhes da Conta' : 'Detalhes da Conta'}</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">Insira os valores da nota para o cálculo.</p>
                
                <div className="space-y-4">
                    <div>
                        <label htmlFor="subtotal" className="block text-sm font-medium text-slate-700 dark:text-slate-300">Total dos Produtos (R$)</label>
                        <input 
                            id="subtotal" 
                            type="text" 
                            inputMode="numeric"
                            value={subtotal} 
                            onChange={(e) => setSubtotal(handleCurrencyInput(e.target.value))} 
                            placeholder="0.00" 
                            className="mt-1 block w-full px-3 py-2 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-md text-sm shadow-sm placeholder-slate-400 dark:placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-slate-900 dark:text-slate-100" 
                            required 
                            autoFocus 
                        />
                    </div>

                    <div>
                        <label htmlFor="tip" className="block text-sm font-medium text-slate-700 dark:text-slate-300">Taxa de Serviço</label>
                         <div className="mt-1 flex rounded-md shadow-sm">
                            <input 
                                id="tip" 
                                type={tipType === 'PERCENT' ? "number" : "text"}
                                inputMode={tipType === 'PERCENT' ? undefined : "numeric"}
                                value={tipValue} 
                                onChange={(e) => handleTipChange(e.target.value)} 
                                placeholder={tipType === 'PERCENT' ? "10" : "0.00"} 
                                step={tipType === 'PERCENT' ? "0.1" : undefined}
                                min="0" 
                                className="block w-full px-3 py-2 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-none rounded-l-md text-sm placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-slate-900 dark:text-slate-100" 
                            />
                            <div className="relative -ml-px flex">
                                <button 
                                    type="button" 
                                    onClick={() => {
                                        setTipType('PERCENT');
                                        setTipValue('');
                                    }} 
                                    className={`px-4 py-2 text-sm font-medium border ${tipType === 'PERCENT' ? 'bg-indigo-600 text-white border-indigo-600 z-10' : 'bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-200 border-slate-300 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-600'}`}
                                >%</button>
                                <button 
                                    type="button" 
                                    onClick={() => {
                                        setTipType('FIXED');
                                        setTipValue('');
                                    }} 
                                    className={`px-4 py-2 text-sm font-medium border rounded-r-md ${tipType === 'FIXED' ? 'bg-indigo-600 text-white border-indigo-600 z-10' : 'bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-200 border-slate-300 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-600'}`}
                                >R$</button>
                            </div>
                        </div>
                    </div>

                     <div>
                        <label htmlFor="tax" className="block text-sm font-medium text-slate-700 dark:text-slate-300">Outras Taxas (R$)</label>
                        <input 
                            id="tax" 
                            type="text" 
                            inputMode="numeric"
                            value={tax} 
                            onChange={(e) => setTax(handleCurrencyInput(e.target.value))} 
                            placeholder="0.00" 
                            className="mt-1 block w-full px-3 py-2 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-md text-sm shadow-sm placeholder-slate-400 dark:placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-slate-900 dark:text-slate-100" 
                        />
                    </div>

                    <div className="pt-2 border-t border-slate-200 dark:border-slate-700">
                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">Valor Total da Nota (Calculado)</label>
                        <p className="mt-1 text-2xl font-bold text-slate-800 dark:text-slate-100 bg-slate-100 dark:bg-slate-700/50 p-2 rounded-md text-center">
                            {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(calculatedTotal)}
                        </p>
                    </div>
                </div>

                <div className="mt-6 flex justify-end gap-2">
                    <button type="button" onClick={onCancel} className="px-4 py-2 text-sm text-slate-600 dark:text-slate-300 hover:text-slate-800 dark:hover:text-slate-100 rounded-md">Cancelar</button>
                    <button type="submit" className="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-400 dark:disabled:bg-slate-600">Confirmar</button>
                </div>
            </form>
        </div>
    )
}
