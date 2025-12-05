# Adicionar suporte completo para DOMESTIC_EXPENSES no App.tsx

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar imports necessários
old_imports = "import type { Participant, Expense, Transaction, Balance, BillSplitEvent, BillItem, ActualPayment } from './types';"
new_imports = "import type { Participant, Expense, Transaction, Balance, BillSplitEvent, BillItem, ActualPayment, DomesticExpense, UserSettings } from './types';"
content = content.replace(old_imports, new_imports)

# 2. Adicionar import do DomesticExpensesManager
old_import_line = "import { ShareSummaryModal } from './components/ShareSummaryModal';"
new_import_line = """import { ShareSummaryModal } from './components/ShareSummaryModal';
import { DomesticExpensesManager } from './components/DomesticExpensesManager';"""
content = content.replace(old_import_line, new_import_line)

# 3. Adicionar funções para gerenciar despesas domésticas (antes do return)
# Procurar onde adicionar (antes do return)
insert_before = "  return ("

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

content = content.replace(insert_before, domestic_functions + insert_before)

# 4. Adicionar renderização do DomesticExpensesManager
# Procurar onde adicionar (depois do ItemizedBillManager)
# Vou procurar pelo final do ItemizedBillManager e adicionar depois
search_text = """            )}
          </main>
        )}
      </>"""

replacement_text = """            )}

            {/* Domestic Expenses Manager */}
            {currentEvent.type === 'DOMESTIC_EXPENSES' && (
              <DomesticExpensesManager
                expenses={currentEvent.domesticExpenses}
                userSettings={currentEvent.userSettings}
                onUpdateExpenses={updateDomesticExpenses}
                onUpdateSettings={updateDomesticSettings}
              />
            )}
          </main>
        )}
      </>"""

content = content.replace(search_text, replacement_text)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Suporte para DOMESTIC_EXPENSES adicionado ao App.tsx!")
print("  - Imports adicionados")
print("  - Funções de gerenciamento adicionadas")
print("  - DomesticExpensesManager renderizado")
