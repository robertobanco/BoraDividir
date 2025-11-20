
import React, { useState, useCallback, useMemo, useEffect } from 'react';
import type { Participant, Expense, Transaction, Balance, BillSplitEvent, BillItem, ActualPayment } from './types';
import { ParticipantManager } from './components/ParticipantManager';
import { ExpenseManager } from './components/ExpenseManager';
import { SettlementDisplay } from './components/SettlementDisplay';
import { EventSelector } from './components/EventSelector';
import { ItemizedBillManager } from './components/ItemizedBillManager';
import { ShareSummaryModal } from './components/ShareSummaryModal';
import { SunIcon } from './components/icons/SunIcon';
import { MoonIcon } from './components/icons/MoonIcon';
import { ArrowLeftIcon } from './components/icons/ArrowLeftIcon';
import { AlertModal } from './components/AlertModal';
import { LiveReceipt } from './components/LiveReceipt';
import { BillSetupModal } from './components/BillSetupModal';

const App: React.FC = () => {
  const [events, setEvents] = useState<BillSplitEvent[]>(() => {
    const saved = localStorage.getItem('billSplitEvents');
    if (!saved) return [];
    const parsedEvents: BillSplitEvent[] = JSON.parse(saved);
    return parsedEvents.map(event => {
      if (!(event as any).date) {
        return { ...event, date: event.createdAt };
      }
      return event;
    });
  });

  // Restore currentEventId from localStorage to persist session state
  const [currentEventId, setCurrentEventId] = useState<string | null>(() => {
    return localStorage.getItem('currentEventId') || null;
  });

  const [isSummaryVisible, setSummaryVisible] = useState(false);
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const savedTheme = localStorage.getItem('theme');
    return (savedTheme as 'light' | 'dark') || 'dark'; 
  });

  // Accordion State
  const [activeSection, setActiveSection] = useState<'participants' | 'expenses' | null>('participants');

  // Modal State
  const [alertState, setAlertState] = useState<{
    isOpen: boolean;
    type: 'alert' | 'confirm';
    title: string;
    message: string;
    onConfirm?: () => void;
  }>({
    isOpen: false,
    type: 'alert',
    title: '',
    message: ''
  });

  const [isBillSetupModalOpen, setIsBillSetupModalOpen] = useState(false);

  const showAlert = (title: string, message: string) => {
    setAlertState({
      isOpen: true,
      type: 'alert',
      title,
      message
    });
  };

  const showConfirm = (title: string, message: string, onConfirm: () => void) => {
    setAlertState({
      isOpen: true,
      type: 'confirm',
      title,
      message,
      onConfirm
    });
  };

  const closeAlert = () => {
    setAlertState(prev => ({ ...prev, isOpen: false }));
  };

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    localStorage.setItem('billSplitEvents', JSON.stringify(events));
  }, [events]);

  // Save currentEventId to localStorage whenever it changes
  useEffect(() => {
    if (currentEventId) {
        localStorage.setItem('currentEventId', currentEventId);
    } else {
        localStorage.removeItem('currentEventId');
    }
  }, [currentEventId]);

  const currentEvent = useMemo(() => events.find(e => e.id === currentEventId), [events, currentEventId]);

  // If stored event ID doesn't exist in events array anymore (deleted), reset it
  useEffect(() => {
      if (currentEventId && !currentEvent && events.length > 0) {
         const exists = events.some(e => e.id === currentEventId);
         if (!exists) {
             setCurrentEventId(null);
         }
      }
  }, [events, currentEventId, currentEvent]);

  const [settlements, setSettlements] = useState<Transaction[]>([]);
  const [showSettlement, setShowSettlement] = useState(false);
  
  const [editingExpense, setEditingExpense] = useState<Expense | null>(null);

  const updateCurrentEvent = (updater: (event: BillSplitEvent) => BillSplitEvent) => {
    setEvents(prevEvents => prevEvents.map(event => 
      event.id === currentEventId ? updater(event) : event
    ));
    setShowSettlement(false);
    setSettlements([]);
  };

  // Event Management
  const addEvent = (name: string, date: string, type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL', options: { billSubtotal?: number; tip?: { value: number; type: 'PERCENT' | 'FIXED'}; tax?: number } = {}) => {
    const baseEvent = {
      id: crypto.randomUUID(),
      name,
      date,
      participants: [],
      createdAt: new Date().toISOString(),
    };

    let newEvent: BillSplitEvent;
    if (type === 'SHARED_EXPENSES') {
      newEvent = { ...baseEvent, type, expenses: [] };
    } else {
      newEvent = { 
          ...baseEvent, 
          type, 
          items: [], 
          tip: options.tip || { value: 0, type: 'PERCENT' }, 
          tax: options.tax || 0, 
          billSubtotal: options.billSubtotal || 0,
          actualPayments: [],
      };
    }

    setEvents(prev => [...prev, newEvent]);
    setCurrentEventId(newEvent.id);
    setActiveSection('participants'); // Reset accordion to start
  };

  const editEvent = (id: string, name: string, date: string) => {
    setEvents(prev => prev.map(event => 
        event.id === id ? { ...event, name, date } : event
    ));
  };

  const deleteEvent = (id: string) => {
    showConfirm(
        'Excluir Evento', 
        'Tem certeza que deseja excluir este evento e todos os seus dados? Esta ação não pode ser desfeita.', 
        () => {
            setEvents(prev => prev.filter(e => e.id !== id));
            if (currentEventId === id) {
                setCurrentEventId(null);
            }
        }
    );
  };
  
  const selectEvent = (id: string) => {
    setCurrentEventId(id);
    setShowSettlement(false);
    setEditingExpense(null);
    setActiveSection('participants'); // Reset accordion
  };

  // Participant Management
  const addParticipant = (name: string) => {
    if (!currentEvent) return;
    const newParticipant: Participant = { id: crypto.randomUUID(), name };
    updateCurrentEvent(event => ({ ...event, participants: [...event.participants, newParticipant] }));
  };

  const removeParticipant = (id: string) => {
    if (!currentEvent) return;
    
    const proceedToRemove = () => {
        updateCurrentEvent(event => ({
            ...event,
            participants: event.participants.filter(p => p.id !== id)
        }));
    };

    if (currentEvent.type === 'SHARED_EXPENSES') {
        const hasExpenses = currentEvent.expenses.some(e => e.paidById === id);
        if (hasExpenses) {
            showAlert('Ação Bloqueada', 'Não é possível remover este participante pois ele possui despesas registradas.');
            return;
        }
    } else {
        const hasItems = currentEvent.items.some(i => i.consumedByIds.includes(id));
        const hasPayments = currentEvent.actualPayments.some(p => p.participantId === id);
        if(hasItems || hasPayments) {
            showAlert('Ação Bloqueada', 'Não é possível remover este participante pois ele possui itens ou pagamentos vinculados.');
            return;
        }
    }
    proceedToRemove();
  };

  const updateParticipant = (id: string, name: string) => {
    if (!currentEvent) return;
    updateCurrentEvent(event => ({
      ...event,
      participants: event.participants.map(p => p.id === id ? { ...p, name } : p)
    }));
  };

  // Shared Expenses Logic
  const addExpense = (expenseData: Omit<Expense, 'id'>) => {
    if (!currentEvent || currentEvent.type !== 'SHARED_EXPENSES') return;
    const newExpense = { ...expenseData, id: crypto.randomUUID() };
    updateCurrentEvent(event => {
        if (event.type !== 'SHARED_EXPENSES') return event;
        return { ...event, expenses: [...event.expenses, newExpense] };
    });
  };

  const removeExpense = (id: string) => {
    if (!currentEvent || currentEvent.type !== 'SHARED_EXPENSES') return;
    updateCurrentEvent(event => {
        if (event.type !== 'SHARED_EXPENSES') return event;
        return { ...event, expenses: event.expenses.filter(e => e.id !== id) };
    });
  };

  const updateExpense = (id: string, expenseData: Omit<Expense, 'id'>) => {
    if (!currentEvent || currentEvent.type !== 'SHARED_EXPENSES') return;
    updateCurrentEvent(event => {
        if (event.type !== 'SHARED_EXPENSES') return event;
        return { ...event, expenses: event.expenses.map(e => e.id === id ? { ...expenseData, id } : e) };
    });
    setEditingExpense(null);
  };

  const calculateSettlements = () => {
    if (!currentEvent || currentEvent.type !== 'SHARED_EXPENSES' || currentEvent.participants.length === 0) return;

    const totalExpenses = currentEvent.expenses.reduce((sum, e) => sum + e.amount, 0);
    const splitAmount = totalExpenses / currentEvent.participants.length;

    const balances: Balance[] = currentEvent.participants.map(p => {
      const paid = currentEvent.expenses.filter(e => e.paidById === p.id).reduce((sum, e) => sum + e.amount, 0);
      return { participantId: p.id, name: p.name, balance: paid - splitAmount };
    });

    const sortedBalances = [...balances].sort((a, b) => a.balance - b.balance);
    const newSettlements: Transaction[] = [];
    
    let i = 0;
    let j = sortedBalances.length - 1;

    while (i < j) {
      const debtor = sortedBalances[i];
      const creditor = sortedBalances[j];

      const amount = Math.min(Math.abs(debtor.balance), creditor.balance);

      if (amount > 0.01) {
        newSettlements.push({
          from: debtor.name,
          to: creditor.name,
          amount: amount
        });
      }

      debtor.balance += amount;
      creditor.balance -= amount;

      if (Math.abs(debtor.balance) < 0.01) i++;
      if (Math.abs(creditor.balance) < 0.01) j--;
    }

    setSettlements(newSettlements);
    setShowSettlement(true);
    // When calculating, we can optionally close the expenses section or leave it open.
    // If you want to auto-collapse expenses to show settlement better:
    // setActiveSection(null);
  };

  // Itemized Bill Logic
  const updateItems = (items: BillItem[]) => {
      if (!currentEvent || currentEvent.type !== 'ITEMIZED_BILL') return;
      updateCurrentEvent(event => {
        if (event.type !== 'ITEMIZED_BILL') return event;
        return { ...event, items };
      });
  }

  const updateDetails = (details: { billSubtotal: number; tip: { value: number; type: 'PERCENT' | 'FIXED'}; tax: number }) => {
       if (!currentEvent || currentEvent.type !== 'ITEMIZED_BILL') return;
      updateCurrentEvent(event => {
        if (event.type !== 'ITEMIZED_BILL') return event;
        return { ...event, billSubtotal: details.billSubtotal, tip: details.tip, tax: details.tax };
      });
      setIsBillSetupModalOpen(false);
  }

  const updateActualPayments = (payments: ActualPayment[]) => {
      if (!currentEvent || currentEvent.type !== 'ITEMIZED_BILL') return;
      updateCurrentEvent(event => {
        if (event.type !== 'ITEMIZED_BILL') return event;
        return { ...event, actualPayments: payments };
      });
  }

  // Toggle Helpers
  const toggleParticipants = () => setActiveSection(prev => prev === 'participants' ? null : 'participants');
  const toggleExpenses = () => setActiveSection(prev => prev === 'expenses' ? null : 'expenses');

  return (
    <>
      <EventSelector 
        events={events}
        currentEventId={currentEventId}
        onSelectEvent={selectEvent}
        onAddEvent={addEvent}
        onEditEvent={editEvent}
        onDeleteEvent={deleteEvent}
        onBack={() => setCurrentEventId(null)}
        theme={theme}
        setTheme={setTheme}
        onShowAlert={showAlert}
      />

      <main className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 pb-24">
        {currentEvent && (
          <div className="space-y-8 animate-slide-up">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">{currentEvent.name}</h1>
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${currentEvent.type === 'SHARED_EXPENSES' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'}`}>
                        {currentEvent.type === 'SHARED_EXPENSES' ? 'Despesas Compartilhadas' : 'Conta Detalhada'}
                    </span>
                </div>
            </div>

            {/* Render LiveReceipt at the top only for Itemized Bill */}
            {currentEvent.type === 'ITEMIZED_BILL' && (
                <LiveReceipt 
                    items={currentEvent.items}
                    tip={currentEvent.tip}
                    tax={currentEvent.tax}
                    billSubtotal={currentEvent.billSubtotal}
                    onEditDetails={() => setIsBillSetupModalOpen(true)}
                />
            )}

            <ParticipantManager 
              participants={currentEvent.participants}
              onAddParticipant={addParticipant}
              onRemoveParticipant={removeParticipant}
              onUpdateParticipant={updateParticipant}
              isExpanded={activeSection === 'participants'}
              onToggle={toggleParticipants}
            />
            
            {currentEvent.type === 'SHARED_EXPENSES' && (
                <>
                    <ExpenseManager 
                        participants={currentEvent.participants}
                        expenses={currentEvent.expenses}
                        onAddExpense={addExpense}
                        onRemoveExpense={removeExpense}
                        editingExpense={editingExpense}
                        onUpdateExpense={updateExpense}
                        onStartEdit={setEditingExpense}
                        onCancelEdit={() => setEditingExpense(null)}
                        isExpanded={activeSection === 'expenses'}
                        onToggle={toggleExpenses}
                    />

                    <div className="flex justify-center pt-8">
                        <button 
                            onClick={calculateSettlements}
                            disabled={currentEvent.participants.length < 2 || currentEvent.expenses.length === 0}
                            className="px-8 py-4 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 text-white font-bold rounded-full shadow-lg shadow-violet-500/30 transform transition-all hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Calcular Divisão
                        </button>
                    </div>

                    {showSettlement && (
                        <SettlementDisplay 
                            settlements={settlements} 
                            totalExpenses={currentEvent.expenses.reduce((sum, e) => sum + e.amount, 0)}
                            numParticipants={currentEvent.participants.length}
                            onOpenSummary={() => setSummaryVisible(true)}
                        />
                    )}
                </>
            )}

            {currentEvent.type === 'ITEMIZED_BILL' && (
                <ItemizedBillManager 
                    participants={currentEvent.participants}
                    items={currentEvent.items}
                    tip={currentEvent.tip}
                    tax={currentEvent.tax}
                    billSubtotal={currentEvent.billSubtotal}
                    actualPayments={currentEvent.actualPayments}
                    onUpdateItems={updateItems}
                    onUpdateActualPayments={updateActualPayments}
                    onOpenSummary={() => setSummaryVisible(true)}
                    isExpanded={activeSection === 'expenses'}
                    onToggle={toggleExpenses}
                />
            )}
          </div>
        )}
      </main>

      {isSummaryVisible && currentEvent && (
        <ShareSummaryModal 
            event={currentEvent} 
            settlements={settlements} 
            onClose={() => setSummaryVisible(false)} 
            onShowAlert={showAlert}
        />
      )}

      <AlertModal 
        isOpen={alertState.isOpen}
        type={alertState.type}
        title={alertState.title}
        message={alertState.message}
        onClose={closeAlert}
        onConfirm={alertState.onConfirm}
      />
      
      {isBillSetupModalOpen && currentEvent && currentEvent.type === 'ITEMIZED_BILL' && (
         <BillSetupModal 
            onConfirm={updateDetails}
            onCancel={() => setIsBillSetupModalOpen(false)}
            initialData={{ billSubtotal: currentEvent.billSubtotal, tip: currentEvent.tip, tax: currentEvent.tax }}
         />
      )}
    </>
  );
};

export default App;