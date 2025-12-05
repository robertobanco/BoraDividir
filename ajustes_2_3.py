# AJUSTES 2 e 3: Responsabilidade e Detalhamento

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. AJUSTE 2: Mudar "Divisão" para "Responsabilidade pelo pagamento"
old_label = """                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                    Divisão: <span className="font-bold text-pink-600 dark:text-pink-400">{ownershipPercentage}%</span> / <span className="font-bold text-purple-600 dark:text-purple-400">{100 - ownershipPercentage}%</span>
                                </label>"""

new_label = """                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                    Responsabilidade pelo pagamento:
                                    <div className="flex justify-between mt-1">
                                        <span className="font-bold text-pink-600 dark:text-pink-400">{userSettings.user1Name}: {ownershipPercentage}%</span>
                                        <span className="font-bold text-purple-600 dark:text-purple-400">{userSettings.user2Name}: {100 - ownershipPercentage}%</span>
                                    </div>
                                </label>"""

content = content.replace(old_label, new_label)

# 2. AJUSTE 3: Atualizar lista de despesas
old_list_display = """                                                <span>Pago por <span className="font-medium">{expense.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name}</span></span>
                                                {expense.ownershipPercentage !== 50 && (
                                                    <>
                                                        <span>•</span>
                                                        <span className="px-2 py-0.5 bg-pink-100 dark:bg-pink-900/30 text-pink-700 dark:text-pink-300 rounded text-xs font-medium">
                                                            {expense.ownershipPercentage}% / {100 - expense.ownershipPercentage}%
                                                        </span>
                                                    </>
                                                )}"""

new_list_display = """                                                <span>
                                                    Pago por <span className="font-medium">{expense.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name}</span>
                                                    {expense.ownershipPercentage !== 50 && (
                                                        <span className="ml-1 text-slate-400">
                                                            ({userSettings.user1Name} {expense.ownershipPercentage}% / {100 - expense.ownershipPercentage}% {userSettings.user2Name})
                                                        </span>
                                                    )}
                                                </span>"""

content = content.replace(old_list_display, new_list_display)

# 3. AJUSTE 3 (WhatsApp): Atualizar handleShareSummary
old_whatsapp_logic = """            ...monthlyBalance.items.map(e => {
                const payer = e.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name;
                const responsibility = e.ownershipPercentage !== 50 ? ` [${e.ownershipPercentage}% / ${100 - e.ownershipPercentage}%]` : '';
                return `- ${e.description}: ${formatCurrency(e.amount)} (${payer})${responsibility}`;
            })"""

new_whatsapp_logic = """            ...monthlyBalance.items.map(e => {
                const payer = e.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name;
                const responsibility = e.ownershipPercentage !== 50 
                    ? ` (${userSettings.user1Name} ${e.ownershipPercentage}% / ${100 - e.ownershipPercentage}% ${userSettings.user2Name})` 
                    : '';
                return `- ${e.description}: ${formatCurrency(e.amount)} (Pago por ${payer}${responsibility})`;
            })"""

content = content.replace(old_whatsapp_logic, new_whatsapp_logic)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ AJUSTES 2 e 3 COMPLETOS: Responsabilidade e Detalhamento atualizados!")
