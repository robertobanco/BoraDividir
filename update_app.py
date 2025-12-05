import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar funções de domestic expenses após updateActualPayments
insert_pos = content.find("  // Toggle Helpers")
if insert_pos != -1:
    domestic_functions = """  // Domestic Expenses Logic
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

  """
    content = content[:insert_pos] + domestic_functions + content[insert_pos:]

# 2. Atualizar o badge de tipo de evento
old_badge = """<span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${currentEvent.type === 'SHARED_EXPENSES' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'}`}>
                  {currentEvent.type === 'SHARED_EXPENSES' ? 'Despesas Compartilhadas' : 'Conta Detalhada'}
                </span>"""

new_badge = """<span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
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
                </span>"""

content = content.replace(old_badge, new_badge)

# 3. Adicionar renderização do DomesticExpensesManager
insert_pos = content.find("            {currentEvent.type === 'ITEMIZED_BILL' && (")
if insert_pos != -1:
    # Encontrar o final do bloco ITEMIZED_BILL
    end_pos = content.find("            )}\n          </div>", insert_pos)
    if end_pos != -1:
        domestic_render = """

            {currentEvent.type === 'DOMESTIC_EXPENSES' && (
              <DomesticExpensesManager 
                expenses={currentEvent.domesticExpenses}
                userSettings={currentEvent.userSettings}
                onUpdateExpenses={updateDomesticExpenses}
                onUpdateSettings={updateDomesticSettings}
                isExpanded={activeSection === 'expenses'}
                onToggle={toggleExpenses}
              />
            )}"""
        content = content[:end_pos] + "            )}" + domestic_render + "\n          </div>" + content[end_pos+len("            )}\n          </div>"):]

# Salvar o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("App.tsx atualizado com sucesso!")
