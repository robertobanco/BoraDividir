
import React, { useState } from 'react';
import type { BillSplitEvent } from '../types';
import { TrashIcon } from './icons/TrashIcon';
import { PencilIcon } from './icons/PencilIcon';
import { BillSetupModal } from './BillSetupModal';
import { SunIcon } from './icons/SunIcon';
import { MoonIcon } from './icons/MoonIcon';
import { ArrowLeftIcon } from './icons/ArrowLeftIcon';

interface EventSelectorProps {
  events: BillSplitEvent[];
  currentEventId: string | null;
  onSelectEvent: (id: string) => void;
  onAddEvent: (name: string, date: string, type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES', options?: { billSubtotal?: number; tip?: { value: number; type: 'PERCENT' | 'FIXED' }; tax?: number; }) => void;
  onEditEvent: (id: string, name: string, date: string) => void;
  onDeleteEvent: (id: string) => void;
  onBack: () => void;
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  onShowAlert: (title: string, message: string) => void;
  onExportData?: () => void;
  onImportData?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  fileInputRef?: React.RefObject<HTMLInputElement>;
}

const calculateEventTotal = (event: BillSplitEvent): number => {
    if (event.type === 'SHARED_EXPENSES') {
        return event.expenses.reduce((sum, exp) => sum + exp.amount, 0);
    } else if (event.type === 'DOMESTIC_EXPENSES') {
        return event.domesticExpenses.reduce((sum, exp) => sum + exp.amount, 0);
    } else { // ITEMIZED_BILL
        const itemsSubtotal = event.items.reduce((sum, item) => sum + item.amount, 0);
        const tipAmount = event.tip.type === 'PERCENT'
            ? itemsSubtotal * (event.tip.value / 100)
            : event.tip.value;
        return itemsSubtotal + tipAmount + event.tax;
    }
};

const formatDate = (dateString: string) => {
    try {
        const date = new Date(dateString);
        const userTimezoneOffset = date.getTimezoneOffset() * 60000;
        return new Date(date.getTime() + userTimezoneOffset).toLocaleDateString('pt-BR');
    } catch (e) {
        return "Data inválida";
    }
};

const EventTypeModal: React.FC<{ onSelect: (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL') => void, onCancel: () => void }> = ({ onSelect, onCancel }) => {
    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
            <div className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-md animate-scale-in">
                <h3 className="text-xl font-bold mb-6 text-slate-900 dark:text-white text-center">Como vamos dividir?</h3>
                <div className="space-y-4">
                     <button onClick={() => onSelect('ITEMIZED_BILL')} className="group w-full text-left p-5 border border-slate-200 dark:border-slate-700 rounded-xl hover:bg-violet-50 dark:hover:bg-violet-900/20 hover:border-violet-300 dark:hover:border-violet-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-violet-500">
                        <div className="flex items-center gap-3 mb-1">
                            <div className="p-2 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg group-hover:scale-110 transition-transform">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                                </svg>
                            </div>
                            <p className="font-bold text-slate-800 dark:text-slate-100 text-lg group-hover:text-violet-700 dark:group-hover:text-violet-300">Conta Detalhada</p>
                        </div>
                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para restaurantes. Divida item por item, calcule gorjeta e taxas.</p>
                    </button>
                    <button onClick={() => onSelect('SHARED_EXPENSES')} className="group w-full text-left p-5 border border-slate-200 dark:border-slate-700 rounded-xl hover:bg-violet-50 dark:hover:bg-violet-900/20 hover:border-violet-300 dark:hover:border-violet-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-violet-500">
                        <div className="flex items-center gap-3 mb-1">
                             <div className="p-2 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 rounded-lg group-hover:scale-110 transition-transform">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                                </svg>
                            </div>
                            <p className="font-bold text-slate-800 dark:text-slate-100 text-lg group-hover:text-violet-700 dark:group-hover:text-violet-300">Despesas Compartilhadas</p>
                        </div>
                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para viagens ou casa. Registre quem pagou o quê e acerte as diferenças.</p>
                    </button>
                    <button onClick={() => onSelect('DOMESTIC_EXPENSES')} className="group w-full text-left p-5 border border-slate-200 dark:border-slate-700 rounded-xl hover:bg-violet-50 dark:hover:bg-violet-900/20 hover:border-violet-300 dark:hover:border-violet-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-violet-500">
                        <div className="flex items-center gap-3 mb-1">
                             <div className="p-2 bg-pink-100 dark:bg-pink-900/30 text-pink-600 dark:text-pink-400 rounded-lg group-hover:scale-110 transition-transform">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                                </svg>
                            </div>
                            <p className="font-bold text-slate-800 dark:text-slate-100 text-lg group-hover:text-violet-700 dark:group-hover:text-violet-300">Contas Domésticas</p>
                        </div>
                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para casais. Gerencie despesas mensais da casa com divisão personalizada.</p>
                    </button>
                </div>
                <div className="mt-8 text-center">
                    <button onClick={onCancel} className="text-sm font-medium text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 transition-colors">Cancelar</button>
                </div>
            </div>
        </div>
    )
}

export const EventSelector: React.FC<EventSelectorProps> = ({ events, currentEventId, onSelectEvent, onAddEvent, onEditEvent, onDeleteEvent, onBack, theme, setTheme, onShowAlert, onExportData, onImportData, fileInputRef }) => {
  const [newEventName, setNewEventName] = useState('');
  const [newEventDate, setNewEventDate] = useState(new Date().toISOString().split('T')[0]);
  const [pendingEvent, setPendingEvent] = useState<{name: string, date: string} | null>(null);
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [showBillSetupModal, setShowBillSetupModal] = useState(false);
  
  // Edit Event State
  const [editingEventId, setEditingEventId] = useState<string | null>(null);
  const [editName, setEditName] = useState('');
  const [editDate, setEditDate] = useState('');

  const handleInitiateAddEvent = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEventName.trim()) {
        onShowAlert("Atenção", "Por favor, dê um nome ao seu evento antes de continuar.");
        return;
    }
    if (!newEventDate) {
        onShowAlert("Atenção", "Por favor, selecione a data do evento.");
        return;
    }
    setPendingEvent({ name: newEventName.trim(), date: newEventDate });
    setShowTypeModal(true);
  };

  const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => {
    if (!pendingEvent) return;
    setShowTypeModal(false);
    if (type === 'SHARED_EXPENSES' || type === 'DOMESTIC_EXPENSES') {
        // SHARED_EXPENSES e DOMESTIC_EXPENSES não precisam de setup adicional
        onAddEvent(pendingEvent.name, pendingEvent.date, type);
        cleanup();
    } else {
        // ITEMIZED_BILL precisa do modal de setup (subtotal, taxa, etc)
        setShowBillSetupModal(true);
    }
  }

  const handleConfirmBillSetup = (details: { billSubtotal: number; tip: { value: number; type: 'PERCENT' | 'FIXED'}; tax: number; }) => {
    if (!pendingEvent) return;
    onAddEvent(pendingEvent.name, pendingEvent.date, 'ITEMIZED_BILL', details);
    cleanup();
  }
  
  const cleanup = () => {
    setNewEventName('');
    setNewEventDate(new Date().toISOString().split('T')[0]);
    setPendingEvent(null);
    setShowTypeModal(false);
    setShowBillSetupModal(false);
  }

  const handleDelete = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    onDeleteEvent(id);
  };

  const handleStartEdit = (e: React.MouseEvent, event: BillSplitEvent) => {
    e.stopPropagation();
    setEditingEventId(event.id);
    setEditName(event.name);
    setEditDate(event.date || event.createdAt.split('T')[0]);
  };

  const handleSaveEdit = (e: React.MouseEvent) => {
      e.stopPropagation();
      if(editingEventId && editName.trim() && editDate) {
          onEditEvent(editingEventId, editName, editDate);
          setEditingEventId(null);
      }
  };
  
  const handleCancelEdit = (e: React.MouseEvent) => {
      e.stopPropagation();
      setEditingEventId(null);
  }
  
  const sortedEvents = [...events].sort((a, b) => new Date(b.date || b.createdAt).getTime() - new Date(a.date || a.createdAt).getTime());

  return (
    <>
      <header className={`sticky top-0 z-30 glass border-b border-white/20 dark:border-white/5 transition-all duration-300 ${currentEventId ? 'shadow-sm' : ''}`}>
        <div className="max-w-7xl mx-auto py-3 px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
             <div className="flex items-center gap-3">
                {currentEventId && (
                   <button 
                        onClick={onBack}
                        className="flex items-center justify-center text-slate-600 dark:text-slate-300 hover:text-violet-600 dark:hover:text-violet-400 transition-colors bg-slate-100 dark:bg-slate-800/50 hover:bg-violet-50 dark:hover:bg-violet-900/20 p-2 rounded-xl"
                        aria-label="Voltar"
                   >
                       <ArrowLeftIcon className="h-5 w-5" />
                   </button>
                )}
                
                <div className="flex items-center gap-2 animate-fade-in">
                    <div className="bg-gradient-to-br from-violet-500 to-fuchsia-500 text-white p-1.5 rounded-lg shadow-lg shadow-violet-500/20">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                        </svg>
                    </div>
                    <span className="font-bold text-lg bg-clip-text text-transparent bg-gradient-to-r from-violet-600 to-indigo-600 dark:from-violet-300 dark:to-indigo-300">Bora Dividir</span>
                </div>
             </div>
            <div className="flex items-center gap-2">
                {/* Export button */}
                {onExportData && events.length > 0 && (
                    <button
                        onClick={onExportData}
                        className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                        title="Exportar dados"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L9 8m4-4v12" />
                        </svg>
                    </button>
                )}
                {/* Import button */}
                {onImportData && fileInputRef && (
                    <>
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                            title="Importar dados"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                        </button>
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept=".json"
                            onChange={onImportData}
                            className="hidden"
                        />
                    </>
                )}
                {/* Theme button */}
                <button 
                  onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} 
                  className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                >
                    {theme === 'light' ? <MoonIcon className="h-6 w-6" /> : <SunIcon className="h-6 w-6" />}
                </button>
            </div>
        </div>
      </header>

      {!currentEventId && (
          <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 animate-fade-in">
            
            {/* Hero Create Section */}
            <div className="mb-12 relative overflow-hidden rounded-3xl glass-card p-8 sm:p-10">
                 <div className="absolute top-0 right-0 -mt-10 -mr-10 w-64 h-64 bg-violet-500/10 rounded-full blur-3xl pointer-events-none"></div>
                 <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
                 
                 <div className="relative z-10 max-w-3xl mx-auto text-center">
                    <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white mb-4 tracking-tight">
                        Dividir contas nunca foi tão <span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-fuchsia-600 dark:from-violet-400 dark:to-fuchsia-400">fácil</span>.
                    </h2>
                    <p className="text-lg text-slate-600 dark:text-slate-300 mb-8">Crie um evento, adicione amigos e deixe a matemática com a gente.</p>
                    
                    <form onSubmit={handleInitiateAddEvent} className="flex flex-col sm:flex-row gap-3 max-w-xl mx-auto bg-white dark:bg-slate-800/50 p-2 rounded-xl sm:rounded-full shadow-lg ring-1 ring-slate-200 dark:ring-slate-700">
                        <input
                            type="text"
                            value={newEventName}
                            onChange={(e) => setNewEventName(e.target.value)}
                            placeholder="Nome do evento (ex: Pizza de Sexta)"
                            className="flex-grow px-4 py-3 bg-transparent border-none focus:ring-0 text-slate-900 dark:text-white placeholder-slate-400"
                        />
                         <div className="w-px bg-slate-200 dark:bg-slate-700 hidden sm:block"></div>
                         <input
                            type="date"
                            value={newEventDate}
                            onChange={(e) => setNewEventDate(e.target.value)}
                            className="px-4 py-3 bg-transparent border-none focus:ring-0 text-slate-600 dark:text-slate-300 w-full sm:w-auto"
                        />
                        <button
                            type="submit"
                            className="px-8 py-3 rounded-lg sm:rounded-full bg-violet-600 hover:bg-violet-700 text-white font-semibold shadow-md shadow-violet-500/30 transition-all hover:scale-105 active:scale-95"
                        >
                            Criar
                        </button>
                    </form>
                 </div>
            </div>

            {/* Grid of Events */}
            <div>
                <h2 className="text-xl font-bold mb-6 text-slate-900 dark:text-slate-100 px-2 flex items-center gap-2">
                    <span className="w-2 h-8 bg-violet-500 rounded-full"></span>
                    Seus Eventos
                </h2>
                
                {sortedEvents.length === 0 ? (
                     <div className="text-center py-12 rounded-2xl border-2 border-dashed border-slate-300 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/30">
                        <p className="text-slate-500 dark:text-slate-400 text-lg">Nenhum evento encontrado.</p>
                        <p className="text-sm text-slate-400 dark:text-slate-500">Use o formulário acima para começar!</p>
                     </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {sortedEvents.map(event => (
                            <div 
                                key={event.id} 
                                onClick={() => editingEventId !== event.id && onSelectEvent(event.id)}
                                className={`group relative glass-card rounded-2xl p-6 transition-all duration-300 hover:shadow-xl hover:shadow-violet-500/10 border-l-4 border-l-transparent hover:border-l-violet-500 overflow-hidden ${editingEventId === event.id ? '' : 'cursor-pointer hover:-translate-y-1'}`}
                            >
                               {editingEventId === event.id ? (
                                   <div className="animate-fade-in" onClick={e => e.stopPropagation()}>
                                        <div className="mb-3">
                                            <label className="block text-xs font-medium text-slate-500 mb-1">Nome</label>
                                            <input 
                                                type="text" 
                                                value={editName} 
                                                onChange={e => setEditName(e.target.value)}
                                                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-violet-500 rounded-lg text-sm"
                                                autoFocus
                                            />
                                        </div>
                                        <div className="mb-4">
                                            <label className="block text-xs font-medium text-slate-500 mb-1">Data</label>
                                            <input 
                                                type="date" 
                                                value={editDate} 
                                                onChange={e => setEditDate(e.target.value)}
                                                className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-violet-500 rounded-lg text-sm"
                                            />
                                        </div>
                                        <div className="flex gap-2">
                                            <button onClick={handleSaveEdit} className="flex-1 py-2 bg-violet-600 text-white rounded-lg text-xs font-bold">Salvar</button>
                                            <button onClick={handleCancelEdit} className="flex-1 py-2 bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg text-xs font-bold">Cancelar</button>
                                        </div>
                                   </div>
                               ) : (
                                   <>
                                    <div className="absolute top-2 right-2 flex gap-1">
                                        <button 
                                            onClick={(e) => handleStartEdit(e, event)}
                                            className="p-2 bg-white/80 dark:bg-slate-800/80 backdrop-blur rounded-full text-slate-400 hover:text-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/30 transition-colors shadow-sm z-10"
                                            aria-label="Editar"
                                        >
                                            <PencilIcon className="h-4 w-4" />
                                        </button>
                                        <button 
                                            onClick={(e) => handleDelete(e, event.id)}
                                            className="p-2 bg-white/80 dark:bg-slate-800/80 backdrop-blur rounded-full text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 transition-colors shadow-sm z-10"
                                            aria-label="Excluir"
                                        >
                                            <TrashIcon className="h-4 w-4" />
                                        </button>
                                   </div>

                                   <div className="mb-4">
                                                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                                        event.type === 'SHARED_EXPENSES' 
                                                            ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' 
                                                            : event.type === 'DOMESTIC_EXPENSES'
                                                                ? 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300'
                                                                : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                                                    }`}>
                                                        {event.type === 'SHARED_EXPENSES' 
                                                            ? 'Compartilhado' 
                                                            : event.type === 'DOMESTIC_EXPENSES'
                                                                ? 'Doméstico'
                                                                : 'Detalhado'}
                                                    </span>
                                                </div>

                                    <h3 className="text-lg font-bold text-slate-900 dark:text-white truncate mb-1 pr-16">{event.name}</h3>
                                    <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">{formatDate(event.date || event.createdAt)}</p>
                                    
                                    <div className="flex items-end justify-between mt-4 pt-4 border-t border-slate-200/50 dark:border-slate-700/50">
                                        <div className="flex -space-x-2 overflow-hidden">
                                            {event.participants.slice(0, 4).map((p, i) => (
                                                <div key={p.id} className="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-slate-800 bg-gradient-to-br from-violet-400 to-indigo-400 flex items-center justify-center text-xs font-bold text-white">
                                                    {p.name.charAt(0).toUpperCase()}
                                                </div>
                                            ))}
                                            {event.participants.length > 4 && (
                                                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-slate-800 bg-slate-200 dark:bg-slate-700 flex items-center justify-center text-xs font-medium text-slate-600 dark:text-slate-300">
                                                    +{event.participants.length - 4}
                                                </div>
                                            )}
                                            {event.type === 'DOMESTIC_EXPENSES' ? (
                                                            <>
                                                                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-slate-800 bg-gradient-to-br from-pink-400 to-rose-400 flex items-center justify-center text-xs font-bold text-white">
                                                                    {event.userSettings.user1Name.charAt(0).toUpperCase()}
                                                                </div>
                                                                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-slate-800 bg-gradient-to-br from-violet-400 to-indigo-400 flex items-center justify-center text-xs font-bold text-white">
                                                                    {event.userSettings.user2Name.charAt(0).toUpperCase()}
                                                                </div>
                                                            </>
                                                        ) : event.participants.length === 0 && <span className="text-xs text-slate-400 italic py-2">Sem participantes</span>}
                                        </div>
                                        <div className="text-right">
                                            <p className="text-xs text-slate-500 dark:text-slate-400">Total</p>
                                            <p className="text-lg font-bold text-slate-800 dark:text-white">
                                                {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(calculateEventTotal(event))}
                                            </p>
                                        </div>
                                    </div>
                                   </>
                               )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
          </main>
      )}
    {showTypeModal && <EventTypeModal onSelect={handleSelectEventType} onCancel={cleanup} />}
    {showBillSetupModal && <BillSetupModal onConfirm={handleConfirmBillSetup} onCancel={cleanup} />}
    </>
  );
};