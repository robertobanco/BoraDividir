import React, { useState, useMemo } from 'react';
import * as XLSX from 'xlsx';
import {
    ArrowLeftRight, Calendar, TrendingUp, Plus, Trash2, Pencil,
    ChevronLeft, ChevronRight, Share2, Copy, Settings
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import type { DomesticExpense, UserSettings, Payer } from '../types';
import { formatCurrency, getCategoryInfo, getMonthKey, addMonths, calculateMonthlyBalance } from '../domesticUtils';

interface DomesticExpensesManagerProps {
    expenses: DomesticExpense[];
    userSettings: UserSettings;
    onUpdateExpenses: (expenses: DomesticExpense[]) => void;
    onUpdateSettings: (settings: UserSettings) => void;
    isExpanded: boolean;
    onToggle: () => void;
}

export const DomesticExpensesManager: React.FC<DomesticExpensesManagerProps> = ({
    expenses, userSettings, onUpdateExpenses, onUpdateSettings
}) => {
    const [currentMonth, setCurrentMonth] = useState(getMonthKey(new Date()));
    const [showAddModal, setShowAddModal] = useState(false);
    const [showSettingsModal, setShowSettingsModal] = useState(false);
    const [showExportModal, setShowExportModal] = useState(false);
    const [editingExpense, setEditingExpense] = useState<DomesticExpense | null>(null);

    const [description, setDescription] = useState('');
    const [amount, setAmount] = useState('');
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [category, setCategory] = useState<'CASA' | 'MERCADO' | 'TRANSPORTE' | 'LAZER' | 'SAUDE' | 'OUTROS'>('MERCADO');
    const [payer, setPayer] = useState<Payer>('USER1');
    const [ownershipPercentage, setOwnershipPercentage] = useState(50);
    const [frequency, setFrequency] = useState<'UNICA' | 'MENSAL' | 'PARCELADA'>('UNICA');
    const [installmentsCount, setInstallmentsCount] = useState('2');

    const monthlyBalance = useMemo(() =>
        calculateMonthlyBalance(expenses, userSettings, currentMonth),
        [expenses, userSettings, currentMonth]
    );

    const projectionData = useMemo(() => {
        const data = [];
        const [y, m] = currentMonth.split('-').map(Number);
        const startDate = new Date(y, m - 1, 1, 12, 0, 0);

        for (let i = 0; i < 6; i++) {
            const currentMonthDate = addMonths(startDate, i);
            const monthKey = getMonthKey(currentMonthDate);
            const balance = calculateMonthlyBalance(expenses, userSettings, monthKey);
            const monthLabel = currentMonthDate.toLocaleDateString('pt-BR', { month: 'short', year: '2-digit' });

            data.push({
                month: monthLabel,
                user1Spend: balance.user1Share,
                user2Spend: balance.user2Share,
                total: balance.total
            });
        }
        return data;
    }, [expenses, userSettings, currentMonth]);

    const changeMonth = (delta: number) => {
        const [y, m] = currentMonth.split('-').map(Number);
        const date = new Date(y, m - 1, 1, 12, 0, 0);
        setCurrentMonth(getMonthKey(addMonths(date, delta)));
    };

    const handleAddExpense = (e: React.FormEvent) => {
        e.preventDefault();
        if (!description.trim() || !amount) return;

        const expenseData: DomesticExpense = {
            id: crypto.randomUUID(),
            description: description.trim(),
            amount: parseFloat(amount),
            category,
            payer,
            date,
            ownershipPercentage,
            frequency,
            installmentsCount: frequency === 'PARCELADA' ? parseInt(installmentsCount) : undefined
        };

        if (editingExpense) {
            onUpdateExpenses(expenses.map(e => e.id === editingExpense.id ? { ...expenseData, id: editingExpense.id } : e));
        } else {
            onUpdateExpenses([...expenses, expenseData]);
        }

        resetForm();
    };

    const resetForm = () => {
        setDescription('');
        setAmount('');
        setDate(new Date().toISOString().split('T')[0]);
        setCategory('MERCADO');
        setPayer('USER1');
        setOwnershipPercentage(50);
        setFrequency('UNICA');
        setInstallmentsCount('2');
        setEditingExpense(null);
        setShowAddModal(false);
    };

    const handleEditExpense = (expense: DomesticExpense) => {
        setEditingExpense(expense);
        setDescription(expense.description);
        setAmount(expense.amount.toString());
        setDate(expense.date);
        setCategory(expense.category as any);
        setPayer(expense.payer);
        setOwnershipPercentage(expense.ownershipPercentage);
        setFrequency(expense.frequency);
        setInstallmentsCount(expense.installmentsCount?.toString() || '2');
        setShowAddModal(true);
    };

    const handleShareSummary = async () => {
        const monthName = new Date(currentMonth + '-01T12:00:00').toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
        let settlementText = "Contas zeradas.";
        if (monthlyBalance.settlement) {
            settlementText = `${monthlyBalance.settlement.from} deve R$ ${monthlyBalance.settlement.amount.toFixed(2)} a ${monthlyBalance.settlement.to}`;
        }

        const lines = [
            `📊 *Resumo Contas Domésticas - ${monthName}*`,
            `-----------------------------`,
            `💰 Total Gastos: ${formatCurrency(monthlyBalance.total)}`,
            `👤 ${userSettings.user1Name} pagou: ${formatCurrency(monthlyBalance.user1Paid)}`,
            `👤 ${userSettings.user2Name} pagou: ${formatCurrency(monthlyBalance.user2Paid)}`,
            `-----------------------------`,
            `👉 *Resultado: ${settlementText}*`,
            `-----------------------------`,
            `📝 *Detalhamento:*`,
            ...monthlyBalance.items.map(e => {
                const payer = e.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name;
                const responsibility = e.ownershipPercentage !== 50 
                    ? ` (${userSettings.user1Name} ${e.ownershipPercentage}% / ${100 - e.ownershipPercentage}% ${userSettings.user2Name})` 
                    : '';
                return `- ${e.description}: ${formatCurrency(e.amount)} (Pago por ${payer}${responsibility})`;
            })
        ];

        const text = lines.join('\n');
        if (navigator.share) {
            try {
                await navigator.share({ title: `Resumo Financeiro - ${monthName}`, text });
            } catch (err) {
                console.log('Error sharing', err);
            }
        } else {
            navigator.clipboard.writeText(text);
            alert('Resumo copiado para a área de transferência!');
        }
    };

    const [yearStr, monthStrVal] = currentMonth.split('-');
    const dateObj = new Date(parseInt(yearStr), parseInt(monthStrVal) - 1, 1, 12, 0, 0);
    const longDate = isNaN(dateObj.getTime()) ? 'Data Inválida' : dateObj.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });

    let settlementTextShort = "Tudo certo! ✅";
    if (monthlyBalance.settlement) {
        settlementTextShort = `${monthlyBalance.settlement.from} deve pagar a ${monthlyBalance.settlement.to}`;
    }

    // Sort expenses by date (most recent first)
    const sortedExpenses = [...monthlyBalance.items].sort((a, b) =>
        new Date(b.date).getTime() - new Date(a.date).getTime()
    );


    // Helper para calcular qual parcela está sendo exibida
    const getCurrentInstallment = (expense: DomesticExpense, currentMonthKey: string): number | null => {
        if (expense.frequency !== 'PARCELADA' || !expense.installmentsCount) return null;
        
        const [expenseYear, expenseMonth] = expense.date.split('-').map(Number);
        const [currentYear, currentMonth] = currentMonthKey.split('-').map(Number);
        
        const monthsDiff = (currentYear - expenseYear) * 12 + (currentMonth - expenseMonth);
        
        if (monthsDiff < 0 || monthsDiff >= expense.installmentsCount) return null;
        
        return monthsDiff + 1; // Parcela atual (1-indexed)
    };


    const handleExportExcel = () => {
        const monthName = new Date(currentMonth + '-01T12:00:00').toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
        
        // Preparar dados para o Excel
        const data = monthlyBalance.items.map(item => ({
            Data: new Date(item.date).toLocaleDateString('pt-BR'),
            Descrição: item.description,
            Categoria: item.category,
            Valor: item.amount,
            'Quem Pagou': item.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name,
            'Responsabilidade': item.ownershipPercentage !== 50 
                ? `${userSettings.user1Name} ${item.ownershipPercentage}% / ${userSettings.user2Name} ${100 - item.ownershipPercentage}%`
                : 'Meio a Meio',
            'Recorrência': item.frequency === 'UNICA' ? 'Única' : item.frequency === 'MENSAL' ? 'Mensal' : `Parcelada (${item.installmentsCount}x)`
        }));

        // Adicionar resumo no final
        data.push({} as any); // Linha em branco
        data.push({
            Data: 'RESUMO',
            Descrição: 'Total Gastos',
            Valor: monthlyBalance.total
        } as any);
        data.push({
            Data: '',
            Descrição: `${userSettings.user1Name} Pagou`,
            Valor: monthlyBalance.user1Paid
        } as any);
        data.push({
            Data: '',
            Descrição: `${userSettings.user2Name} Pagou`,
            Valor: monthlyBalance.user2Paid
        } as any);
        
        if (monthlyBalance.settlement) {
            data.push({
                Data: 'RESULTADO',
                Descrição: `${monthlyBalance.settlement.from} deve a ${monthlyBalance.settlement.to}`,
                Valor: monthlyBalance.settlement.amount
            } as any);
        }

        const ws = XLSX.utils.json_to_sheet(data);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Despesas");
        
        // Ajustar largura das colunas
        const wscols = [
            {wch: 12}, // Data
            {wch: 30}, // Descrição
            {wch: 15}, // Categoria
            {wch: 12}, // Valor
            {wch: 15}, // Quem Pagou
            {wch: 30}, // Responsabilidade
            {wch: 20}  // Recorrência
        ];
        ws['!cols'] = wscols;

        XLSX.writeFile(wb, `BoraDividir_${monthName.replace(' ', '_')}.xlsx`);
        setShowExportModal(false);
    };
    return (
        <div className="space-y-8">
            {/* Month Navigation */}
            <div className="flex items-center justify-between bg-slate-900 dark:bg-slate-800/50 rounded-xl p-4 border border-slate-800 dark:border-slate-700">
                <div className="flex items-center gap-2">
                    <button onClick={() => changeMonth(-1)} className="p-2 hover:bg-slate-800 dark:hover:bg-slate-700 rounded-lg transition text-slate-400 hover:text-white">
                        <ChevronLeft size={20} />
                    </button>
                    <div className="relative">
                        <span className="text-lg font-semibold text-slate-200 dark:text-white capitalize px-4 cursor-pointer hover:text-pink-400 transition-colors">
                            {longDate}
                        </span>
                        <input
                            type="month"
                            value={currentMonth}
                            onChange={(e) => e.target.value && setCurrentMonth(e.target.value)}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        />
                    </div>
                    <button onClick={() => changeMonth(1)} className="p-2 hover:bg-slate-800 dark:hover:bg-slate-700 rounded-lg transition text-slate-400 hover:text-white">
                        <ChevronRight size={20} />
                    </button>
                </div>
                <button
                    onClick={() => setShowSettingsModal(true)}
                    className="p-2 bg-slate-800 dark:bg-slate-700 hover:bg-slate-700 dark:hover:bg-slate-600 text-slate-400 hover:text-white rounded-lg transition-colors"
                >
                    <Settings size={20} />
                </button>
            </div>

            {/* Settlement Card */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-2 bg-gradient-to-br from-pink-900 to-purple-900 dark:from-pink-800 dark:to-purple-800 rounded-2xl shadow-xl border border-pink-800/50 dark:border-pink-700/50 text-white p-6 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <ArrowLeftRight size={140} />
                    </div>
                    <div className="flex justify-between items-start relative z-10">
                        <h2 className="text-pink-200 dark:text-pink-100 font-medium mb-1 text-sm uppercase tracking-wider">Resultado do Mês</h2>
                        <button onClick={() => setShowExportModal(true)} className="p-2 bg-white/10 hover:bg-white/20 rounded-lg backdrop-blur-sm transition">
                            <Share2 size={18} />
                        </button>
                    </div>
                    <div className="flex flex-col gap-1 mb-6 relative z-0">
                        <span className="text-4xl font-bold tracking-tight text-white drop-shadow-sm">
                            {!monthlyBalance.settlement ? 'Zerado!' : formatCurrency(monthlyBalance.settlement.amount)}
                        </span>
                        {monthlyBalance.settlement && (
                            <span className="text-sm font-medium bg-white/10 self-start px-3 py-1 rounded-full backdrop-blur-sm border border-white/10">
                                {settlementTextShort}
                            </span>
                        )}
                    </div>
                    <div className="grid grid-cols-2 gap-4 pt-4 border-t border-pink-500/30 relative z-0">
                        <div className="cursor-pointer" onClick={() => setShowSettingsModal(true)}>
                            <div className="flex items-center gap-1 mb-1">
                                <div className="flex items-center gap-2 w-full border-b border-pink-300/30 pb-0.5 hover:border-pink-300 transition-colors">
                                    <span className="text-[10px] text-pink-300 uppercase font-bold tracking-wider">{userSettings.user1Name}</span>
                                    <Pencil size={10} className="text-pink-300 opacity-70" />
                                </div>
                            </div>
                            <p className="text-xs text-pink-300/80">Pagou: <span className="text-white font-semibold">{formatCurrency(monthlyBalance.user1Paid)}</span></p>
                            <p className="text-xs text-pink-300/80">Parte Justa: {formatCurrency(monthlyBalance.user1Share)}</p>
                        </div>
                        <div className="cursor-pointer" onClick={() => setShowSettingsModal(true)}>
                            <div className="flex items-center gap-1 mb-1">
                                <div className="flex items-center gap-2 w-full border-b border-pink-300/30 pb-0.5 hover:border-pink-300 transition-colors">
                                    <span className="text-[10px] text-pink-300 uppercase font-bold tracking-wider">{userSettings.user2Name}</span>
                                    <Pencil size={10} className="text-pink-300 opacity-70" />
                                </div>
                            </div>
                            <p className="text-xs text-pink-300/80">Pagou: <span className="text-white font-semibold">{formatCurrency(monthlyBalance.user2Paid)}</span></p>
                            <p className="text-xs text-pink-300/80">Parte Justa: {formatCurrency(monthlyBalance.user2Share)}</p>
                        </div>
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="bg-slate-900 dark:bg-slate-800 rounded-2xl shadow-lg border border-slate-800 dark:border-slate-700 p-6 flex flex-col justify-between">
                    <div>
                        <h3 className="text-slate-400 dark:text-slate-300 text-xs font-bold uppercase tracking-wider mb-4">Resumo</h3>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center p-3 bg-slate-950/50 dark:bg-slate-900/50 rounded-lg border border-slate-800/50 dark:border-slate-700/50">
                                <span className="text-slate-400 dark:text-slate-300 text-sm">Total Gastos</span>
                                <span className="font-bold text-slate-200 dark:text-white">{formatCurrency(monthlyBalance.total)}</span>
                            </div>
                            <div className="flex justify-between items-center p-3 bg-slate-950/50 dark:bg-slate-900/50 rounded-lg border border-slate-800/50 dark:border-slate-700/50">
                                <span className="text-slate-400 dark:text-slate-300 text-sm">Itens</span>
                                <span className="font-bold text-slate-200 dark:text-white">{monthlyBalance.items.length}</span>
                            </div>
                        </div>
                    </div>
                    <button
                        onClick={() => setShowAddModal(true)}
                        className="w-full mt-6 py-3 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white font-bold rounded-lg shadow-lg shadow-pink-500/30 transition-all hover:scale-105 active:scale-95 flex items-center justify-center gap-2"
                    >
                        <Plus size={18} /> Nova Despesa
                    </button>
                </div>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-slate-900 dark:bg-slate-800 p-6 rounded-2xl shadow-lg border border-slate-800 dark:border-slate-700">
                    <h3 className="text-lg font-semibold text-slate-100 dark:text-white mb-6 flex items-center gap-2">
                        <Calendar size={18} className="text-pink-400" /> Projeção de Gastos
                    </h3>
                    <div className="h-64 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={projectionData} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
                                <XAxis dataKey="month" fontSize={12} tickLine={false} axisLine={false} tick={{ fill: '#94a3b8' }} />
                                <YAxis fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => `R$${v}`} tick={{ fill: '#94a3b8' }} />
                                <Tooltip cursor={{ fill: '#1e293b' }} formatter={(value: number) => [formatCurrency(value), '']} contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', border: '1px solid #1e293b', color: '#f8fafc' }} />
                                <Legend iconType="circle" wrapperStyle={{ color: '#94a3b8', fontSize: '12px', paddingTop: '10px' }} />
                                <Bar dataKey="user1Spend" name={userSettings.user1Name} stackId="a" fill="#ec4899" radius={[0, 0, 0, 0]} />
                                <Bar dataKey="user2Spend" name={userSettings.user2Name} stackId="a" fill="#a855f7" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="bg-slate-900 dark:bg-slate-800 p-6 rounded-2xl shadow-lg border border-slate-800 dark:border-slate-700">
                    <h3 className="text-lg font-semibold text-slate-100 dark:text-white mb-6 flex items-center gap-2">
                        <TrendingUp size={18} className="text-sky-400" /> Histórico Detalhado
                    </h3>
                    <div className="h-64 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={projectionData} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
                                <XAxis dataKey="month" fontSize={12} tickLine={false} axisLine={false} tick={{ fill: '#94a3b8' }} />
                                <YAxis fontSize={12} tickLine={false} axisLine={false} tick={{ fill: '#94a3b8' }} />
                                <Tooltip formatter={(value: number) => formatCurrency(value)} contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', border: '1px solid #1e293b', color: '#f8fafc' }} />
                                <Legend iconType="plainline" wrapperStyle={{ color: '#94a3b8', fontSize: '12px', paddingTop: '10px' }} />
                                <Line type="monotone" dataKey="total" name="Total" stroke="#0ea5e9" strokeWidth={3} dot={{ r: 3 }} activeDot={{ r: 5 }} />
                                <Line type="monotone" dataKey="user1Spend" name={userSettings.user1Name} stroke="#ec4899" strokeWidth={2} strokeDasharray="5 5" dot={{ r: 2 }} />
                                <Line type="monotone" dataKey="user2Spend" name={userSettings.user2Name} stroke="#a855f7" strokeWidth={2} strokeDasharray="5 5" dot={{ r: 2 }} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Expense List */}
            <div className="bg-slate-900 dark:bg-slate-800 rounded-2xl shadow-lg border border-slate-800 dark:border-slate-700 overflow-hidden">
                <div className="p-6 border-b border-slate-800 dark:border-slate-700 flex justify-between items-center">
                    <h3 className="text-lg font-semibold text-slate-100 dark:text-white">Detalhamento do Mês</h3>
                    <span className="text-xs text-slate-500 dark:text-slate-400 bg-slate-950 dark:bg-slate-900 px-3 py-1 rounded-full border border-slate-800 dark:border-slate-700">{sortedExpenses.length} registros</span>
                </div>

                {sortedExpenses.length === 0 ? (
                    <div className="px-6 py-12 text-center text-slate-600 dark:text-slate-400">
                        <div className="flex flex-col items-center justify-center">
                            <div className="p-4 rounded-full bg-slate-800 dark:bg-slate-700 mb-3">
                                <Calendar className="text-slate-600 dark:text-slate-400" size={24} />
                            </div>
                            <p>Nenhuma despesa registrada neste mês.</p>
                            <button onClick={() => setShowAddModal(true)} className="mt-2 text-pink-400 hover:text-pink-300 hover:bg-pink-950/30 dark:hover:bg-pink-900/20 px-4 py-2 rounded-lg transition-colors">
                                Adicionar primeira despesa
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="divide-y divide-slate-800 dark:divide-slate-700">
                        {sortedExpenses.map((expense) => {
                            const categoryInfo = getCategoryInfo(expense.category);
                            const [y, m, d] = expense.date.split('-').map(Number);
                            const displayDate = new Date(y, m - 1, d, 12, 0, 0);
                            const dateStr = isNaN(displayDate.getTime()) ? '--' : displayDate.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });

                        
    // Helper para calcular qual parcela está sendo exibida
    const getCurrentInstallment = (expense: DomesticExpense, currentMonthKey: string): number | null => {
        if (expense.frequency !== 'PARCELADA' || !expense.installmentsCount) return null;
        
        const [expenseYear, expenseMonth] = expense.date.split('-').map(Number);
        const [currentYear, currentMonth] = currentMonthKey.split('-').map(Number);
        
        const monthsDiff = (currentYear - expenseYear) * 12 + (currentMonth - expenseMonth);
        
        if (monthsDiff < 0 || monthsDiff >= expense.installmentsCount) return null;
        
        return monthsDiff + 1; // Parcela atual (1-indexed)
    };


    const handleExportExcel = () => {
        const monthName = new Date(currentMonth + '-01T12:00:00').toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
        
        // Preparar dados para o Excel
        const data = monthlyBalance.items.map(item => ({
            Data: new Date(item.date).toLocaleDateString('pt-BR'),
            Descrição: item.description,
            Categoria: item.category,
            Valor: item.amount,
            'Quem Pagou': item.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name,
            'Responsabilidade': item.ownershipPercentage !== 50 
                ? `${userSettings.user1Name} ${item.ownershipPercentage}% / ${userSettings.user2Name} ${100 - item.ownershipPercentage}%`
                : 'Meio a Meio',
            'Recorrência': item.frequency === 'UNICA' ? 'Única' : item.frequency === 'MENSAL' ? 'Mensal' : `Parcelada (${item.installmentsCount}x)`
        }));

        // Adicionar resumo no final
        data.push({} as any); // Linha em branco
        data.push({
            Data: 'RESUMO',
            Descrição: 'Total Gastos',
            Valor: monthlyBalance.total
        } as any);
        data.push({
            Data: '',
            Descrição: `${userSettings.user1Name} Pagou`,
            Valor: monthlyBalance.user1Paid
        } as any);
        data.push({
            Data: '',
            Descrição: `${userSettings.user2Name} Pagou`,
            Valor: monthlyBalance.user2Paid
        } as any);
        
        if (monthlyBalance.settlement) {
            data.push({
                Data: 'RESULTADO',
                Descrição: `${monthlyBalance.settlement.from} deve a ${monthlyBalance.settlement.to}`,
                Valor: monthlyBalance.settlement.amount
            } as any);
        }

        const ws = XLSX.utils.json_to_sheet(data);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Despesas");
        
        // Ajustar largura das colunas
        const wscols = [
            {wch: 12}, // Data
            {wch: 30}, // Descrição
            {wch: 15}, // Categoria
            {wch: 12}, // Valor
            {wch: 15}, // Quem Pagou
            {wch: 30}, // Responsabilidade
            {wch: 20}  // Recorrência
        ];
        ws['!cols'] = wscols;

        XLSX.writeFile(wb, `BoraDividir_${monthName.replace(' ', '_')}.xlsx`);
        setShowExportModal(false);
    };
    return (
                                <div key={expense.id} className="p-4 hover:bg-slate-800/50 dark:hover:bg-slate-700/50 transition-colors group flex items-center justify-between">
                                    <div className="flex items-center gap-4 flex-1">
                                        <div className={`p-3 rounded-xl ${categoryInfo.bgColor}`}>
                                            <span className="text-2xl">{categoryInfo.icon}</span>
                                        </div>
                                        <div className="flex-1">
                                            <p className="font-semibold text-slate-200 dark:text-white text-lg">{expense.description}</p>
                                            <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 mt-1">
                                                <span className="font-mono">{dateStr}</span>
                                                <span>•</span>
                                                <span>
                                                    Pago por <span className="font-medium">{expense.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name}</span>
                                                    {expense.ownershipPercentage !== 50 && (
                                                        <span className="ml-1 text-slate-400">
                                                            ({userSettings.user1Name} {expense.ownershipPercentage}% / {100 - expense.ownershipPercentage}% {userSettings.user2Name})
                                                        </span>
                                                    )}
                                                </span>
                                                {expense.frequency === 'MENSAL' && (
                                                    <>
                                                        <span>•</span>
                                                        <span className="px-2 py-0.5 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded text-xs font-medium">
                                                            Mensal
                                                        </span>
                                                    </>
                                                )}
                                                {expense.frequency === 'PARCELADA' && expense.installmentsCount && (
                                                    <>
                                                        <span>•</span>
                                                        <span className="px-2 py-0.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded text-xs font-medium">
                                                            {(() => {
                                                                const current = getCurrentInstallment(expense, currentMonth);
                                                                return current ? `${current}/${expense.installmentsCount}` : `${expense.installmentsCount}x`;
                                                            })()}
                                                        </span>
                                                    </>
                                                )}
                                            </div>
                                        </div>
                                        <div className="text-right mr-4">
                                            <p className="font-bold text-xl text-slate-900 dark:text-white">{formatCurrency(expense.amount)}</p>
                                            <p className="text-xs text-slate-500 dark:text-slate-400">{categoryInfo.label}</p>
                                        </div>
                                        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button onClick={() => handleEditExpense(expense)} className="p-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors">
                                                <Pencil size={18} />
                                            </button>
                                            <button onClick={() => confirm('Deseja excluir esta despesa?') && onUpdateExpenses(expenses.filter(e => e.id !== expense.id))} className="p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors">
                                                <Trash2 size={18} />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>

            {/* Modal Add/Edit */}
            {showAddModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
                    <div className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-md animate-scale-in bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                        <h3 className="text-xl font-bold mb-6 text-slate-900 dark:text-white">{editingExpense ? 'Editar Despesa' : 'Nova Despesa'}</h3>
                        <form onSubmit={handleAddExpense} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Descrição</label>
                                <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Ex: Mercado, Aluguel, Luz..." className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500" required autoFocus />
                            </div>
                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Valor</label>
                                    <input type="number" step="0.01" value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="0,00" className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500" required />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Data</label>
                                    <input type="date" value={date} onChange={(e) => setDate(e.target.value)} className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500 [color-scheme:dark]" required />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Categoria</label>
                                <select value={category} onChange={(e) => setCategory(e.target.value as any)} className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500">
                                    <option value="CASA">🏠 Casa</option>
                                    <option value="MERCADO">🛒 Mercado</option>
                                    <option value="TRANSPORTE">🚗 Transporte</option>
                                    <option value="LAZER">🎉 Lazer</option>
                                    <option value="SAUDE">💊 Saúde</option>
                                    <option value="OUTROS">📦 Outros</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Quem pagou?</label>
                                <div className="grid grid-cols-2 gap-3">
                                    <button type="button" onClick={() => setPayer('USER1')} className={`py-3 px-4 rounded-lg font-semibold transition-all ${payer === 'USER1' ? 'bg-gradient-to-r from-pink-600 to-purple-600 text-white shadow-lg' : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-300 dark:hover:bg-slate-600'}`}>
                                        {userSettings.user1Name}
                                    </button>
                                    <button type="button" onClick={() => setPayer('USER2')} className={`py-3 px-4 rounded-lg font-semibold transition-all ${payer === 'USER2' ? 'bg-gradient-to-r from-pink-600 to-purple-600 text-white shadow-lg' : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-300 dark:hover:bg-slate-600'}`}>
                                        {userSettings.user2Name}
                                    </button>
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Recorrência</label>
                                <select value={frequency} onChange={(e) => setFrequency(e.target.value as any)} className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500">
                                    <option value="UNICA">Única</option>
                                    <option value="MENSAL">Mensal (Fixo)</option>
                                    <option value="PARCELADA">Parcelado</option>
                                </select>
                            </div>
                            {frequency === 'PARCELADA' && (
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Número de Parcelas</label>
                                    <input type="number" min="2" max="120" value={installmentsCount} onChange={(e) => setInstallmentsCount(e.target.value)} className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500" />
                                </div>
                            )}
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                    Responsabilidade pelo pagamento:
                                    <div className="flex justify-between mt-1">
                                        <span className="font-bold text-pink-600 dark:text-pink-400">{userSettings.user1Name}: {ownershipPercentage}%</span>
                                        <span className="font-bold text-purple-600 dark:text-purple-400">{userSettings.user2Name}: {100 - ownershipPercentage}%</span>
                                    </div>
                                </label>
                                <input type="range" min="0" max="100" value={100 - ownershipPercentage} onChange={(e) => setOwnershipPercentage(100 - parseInt(e.target.value))} className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-pink-600" />
                                <div className="flex justify-between text-xs text-slate-500 dark:text-slate-400 mt-1">
                                    <span>{userSettings.user1Name}</span>
                                    <span>{userSettings.user2Name}</span>
                                </div>
                            </div>
                            <div className="flex gap-3 mt-6 pt-4 border-t border-slate-200 dark:border-slate-700">
                                <button type="button" onClick={resetForm} className="flex-1 px-4 py-3 bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg font-semibold hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors">
                                    Cancelar
                                </button>
                                <button type="submit" className="flex-1 px-4 py-3 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-lg font-bold shadow-lg shadow-pink-500/30 transition-all hover:scale-105 active:scale-95">
                                    {editingExpense ? 'Salvar' : 'Adicionar'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Modal Settings */}
            {showSettingsModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
                    <div className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-md animate-scale-in bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                        <h3 className="text-xl font-bold mb-6 text-slate-900 dark:text-white">⚙️ Configurações</h3>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Nome Participante 1</label>
                                <input type="text" value={userSettings.user1Name} onChange={(e) => onUpdateSettings({ ...userSettings, user1Name: e.target.value })} className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Nome Participante 2</label>
                                <input type="text" value={userSettings.user2Name} onChange={(e) => onUpdateSettings({ ...userSettings, user2Name: e.target.value })} className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500" />
                            </div>
                            <button onClick={() => setShowSettingsModal(false)} className="w-full px-4 py-3 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-lg font-bold shadow-lg shadow-pink-500/30 transition-all hover:scale-105 active:scale-95 mt-6">
                                Salvar
                            </button>
                        </div>
                    </div>
                </div>
            )}
            
            {/* Export Modal */}
            {showExportModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
                    <div className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-sm animate-scale-in bg-white dark:bg-slate-900">
                        <h3 className="text-xl font-bold mb-6 text-slate-900 dark:text-white text-center">Compartilhar / Exportar</h3>
                        
                        <div className="space-y-3">
                            <button 
                                onClick={() => {
                                    handleShareSummary();
                                    setShowExportModal(false);
                                }}
                                className="w-full p-4 bg-[#25D366] hover:bg-[#128C7E] text-white rounded-xl font-bold flex items-center justify-center gap-3 transition-colors shadow-lg"
                            >
                                <Share2 size={20} />
                                Compartilhar no WhatsApp
                            </button>
                            
                            <button 
                                onClick={handleExportExcel}
                                className="w-full p-4 bg-[#1D6F42] hover:bg-[#155230] text-white rounded-xl font-bold flex items-center justify-center gap-3 transition-colors shadow-lg"
                            >
                                <TrendingUp size={20} />
                                Baixar Excel (.xlsx)
                            </button>
                        </div>

                        <button 
                            onClick={() => setShowExportModal(false)}
                            className="w-full mt-6 py-3 text-slate-500 dark:text-slate-400 font-medium hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
                        >
                            Cancelar
                        </button>
                    </div>
                </div>
            )}
    
        </div>
    );
};