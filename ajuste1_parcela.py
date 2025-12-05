# AJUSTE 1: Mostrar parcela atual (ex: 2/6)

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar função helper para calcular parcela atual
# Procurar onde adicionar (antes do return principal)
helper_function = """
    // Helper para calcular qual parcela está sendo exibida
    const getCurrentInstallment = (expense: DomesticExpense, currentMonthKey: string): number | null => {
        if (expense.frequency !== 'PARCELADA' || !expense.installmentsCount) return null;
        
        const [expenseYear, expenseMonth] = expense.date.split('-').map(Number);
        const [currentYear, currentMonth] = currentMonthKey.split('-').map(Number);
        
        const monthsDiff = (currentYear - expenseYear) * 12 + (currentMonth - expenseMonth);
        
        if (monthsDiff < 0 || monthsDiff >= expense.installmentsCount) return null;
        
        return monthsDiff + 1; // Parcela atual (1-indexed)
    };

"""

# Inserir antes do return
insert_before = "    return ("
content = content.replace(insert_before, helper_function + insert_before)

# Atualizar a exibição da parcela (linha 372)
old_installment_display = """                                                        <span className="px-2 py-0.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded text-xs font-medium">
                                                            {expense.installmentsCount}x
                                                        </span>"""

new_installment_display = """                                                        <span className="px-2 py-0.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded text-xs font-medium">
                                                            {(() => {
                                                                const current = getCurrentInstallment(expense, currentMonth);
                                                                return current ? `${current}/${expense.installmentsCount}` : `${expense.installmentsCount}x`;
                                                            })()}
                                                        </span>"""

content = content.replace(old_installment_display, new_installment_display)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ AJUSTE 1 COMPLETO: Parcela atual sendo exibida (ex: 2/6)")
