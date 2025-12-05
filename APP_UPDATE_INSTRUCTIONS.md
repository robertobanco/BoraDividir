// INSTRUÇÕES PARA ATUALIZAR App.tsx

// 1. Adicionar após a linha 336 (após updateActualPayments):

  // Domestic Expenses Logic
  const updateDomesticExpenses = (expenses: DomesticExpense[]) => {
      if (!currentEvent || currentEvent.type !== 'DOMESTIC_EXPENSES') return;
      updateCurrentEvent(event => {
          if (event.type !== 'DOMESTIC_EXPENSES') return event;
          return { ...event, domesticExpenses: expenses };
      });
  };

  const updateDomesticSettings = (settings: UserSettings) => {
      if (!currentEvent || currentEvent.type !== 'DOMESTIC_EXPENSES') return;
      updateCurrentEvent(event => {
          if (event.type !== 'DOMESTIC_EXPENSES') return event;
          return { ...event, userSettings: settings };
      });
  };

// 2. Atualizar o badge de tipo de evento (procurar por "Despesas Compartilhadas" ou "Conta Detalhada" na linha ~363):

<span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
    currentEvent.type === 'SHARED_EXPENSES' 
        ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' 
        : currentEvent.type === 'ITEMIZED_BILL'
        ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
        : 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300'
}`}>
    {currentEvent.type === 'SHARED_EXPENSES' 
        ? 'Despesas Compartilhadas' 
        : currentEvent.type === 'ITEMIZED_BILL'
        ? 'Conta Detalhada'
        : 'Contas Domésticas'}
</span>

// 3. Adicionar após o bloco ItemizedBillManager (procurar por "currentEvent.type === 'ITEMIZED_BILL'" na linha ~424):

{currentEvent.type === 'DOMESTIC_EXPENSES' && (
    <DomesticExpensesManager 
        expenses={currentEvent.domesticExpenses}
        userSettings={currentEvent.userSettings}
        onUpdateExpenses={updateDomesticExpenses}
        onUpdateSettings={updateDomesticSettings}
        isExpanded={activeSection === 'expenses'}
        onToggle={toggleExpenses}
    />
)}
