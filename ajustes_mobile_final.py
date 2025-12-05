# AJUSTES MOBILE, 50/50 e VALIDAÇÃO

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# ---------------------------------------------------------
# 1. AJUSTE MOBILE: Layout da lista de despesas
# ---------------------------------------------------------
# Procurar a div da lista de despesas
# Vamos adicionar flex-wrap e ajustar o layout para mobile

old_item_layout = """                                <div key={expense.id} className="p-4 hover:bg-slate-800/50 dark:hover:bg-slate-700/50 transition-colors group flex items-center justify-between">
                                    <div className="flex items-center gap-4 flex-1">
                                        <div className={`p-3 rounded-xl ${categoryInfo.bgColor}`}>
                                            <span className="text-2xl">{categoryInfo.icon}</span>
                                        </div>
                                        <div className="flex-1">
                                            <p className="font-semibold text-slate-200 dark:text-white text-lg">{expense.description}</p>
                                            <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 mt-1">"""

# Novo layout: 
# - flex-wrap na div de detalhes
# - min-width no container
new_item_layout = """                                <div key={expense.id} className="p-4 hover:bg-slate-800/50 dark:hover:bg-slate-700/50 transition-colors group flex items-center justify-between">
                                    <div className="flex items-center gap-3 sm:gap-4 flex-1 min-w-0">
                                        <div className={`p-2 sm:p-3 rounded-xl ${categoryInfo.bgColor} flex-shrink-0`}>
                                            <span className="text-xl sm:text-2xl">{categoryInfo.icon}</span>
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className="font-semibold text-slate-200 dark:text-white text-base sm:text-lg truncate pr-2">{expense.description}</p>
                                            <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">"""

content = content.replace(old_item_layout, new_item_layout)


# ---------------------------------------------------------
# 2. AJUSTE 50/50: Mostrar sempre
# ---------------------------------------------------------
# Remover a condição {expense.ownershipPercentage !== 50 && (...)}

# O código atual (do último patch) tem:
# {expense.ownershipPercentage !== 50 && (
#     <span className="ml-1 text-slate-400">
#         ({userSettings.user1Name} {expense.ownershipPercentage}% / {100 - expense.ownershipPercentage}% {userSettings.user2Name})
#     </span>
# )}

# Vamos substituir para mostrar sempre, mas com estilo diferente se for 50/50 para não poluir tanto, ou igual.
# O usuário pediu: "mostre os 50% / 50% como já faz quando a divisao é desproprocional"

old_50_50_logic = """                                                {expense.ownershipPercentage !== 50 && (
                                                    <span className="ml-1 text-slate-400">
                                                        ({userSettings.user1Name} {expense.ownershipPercentage}% / {100 - expense.ownershipPercentage}% {userSettings.user2Name})
                                                    </span>
                                                )}"""

new_50_50_logic = """                                                <span className="ml-1 text-slate-400">
                                                    ({userSettings.user1Name} {expense.ownershipPercentage}% / {100 - expense.ownershipPercentage}% {userSettings.user2Name})
                                                </span>"""

content = content.replace(old_50_50_logic, new_50_50_logic)

# Também precisamos ajustar no WhatsApp (handleShareSummary)
# Código atual:
# const responsibility = e.ownershipPercentage !== 50 
#    ? ` (${userSettings.user1Name} ${e.ownershipPercentage}% / ${100 - e.ownershipPercentage}% ${userSettings.user2Name})` 
#    : '';

old_whatsapp_logic = """                const responsibility = e.ownershipPercentage !== 50 
                    ? ` (${userSettings.user1Name} ${e.ownershipPercentage}% / ${100 - e.ownershipPercentage}% ${userSettings.user2Name})` 
                    : '';"""

new_whatsapp_logic = """                const responsibility = ` (${userSettings.user1Name} ${e.ownershipPercentage}% / ${100 - e.ownershipPercentage}% ${userSettings.user2Name})`;"""

content = content.replace(old_whatsapp_logic, new_whatsapp_logic)

# E no Excel também (handleExportExcel)
# 'Responsabilidade': item.ownershipPercentage !== 50 
#     ? `${userSettings.user1Name} ${item.ownershipPercentage}% / ${userSettings.user2Name} ${100 - item.ownershipPercentage}%`
#     : 'Meio a Meio',

old_excel_logic = """            'Responsabilidade': item.ownershipPercentage !== 50 
                ? `${userSettings.user1Name} ${item.ownershipPercentage}% / ${userSettings.user2Name} ${100 - item.ownershipPercentage}%`
                : 'Meio a Meio',"""

new_excel_logic = """            'Responsabilidade': `${userSettings.user1Name} ${item.ownershipPercentage}% / ${userSettings.user2Name} ${100 - item.ownershipPercentage}%`,"""

content = content.replace(old_excel_logic, new_excel_logic)


# ---------------------------------------------------------
# 3. AJUSTE NOMES: Validação
# ---------------------------------------------------------
# No modal de settings, vamos alterar o botão de salvar para validar antes

old_settings_save = """                            <button onClick={() => setShowSettingsModal(false)} className="w-full px-4 py-3 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-lg font-bold shadow-lg shadow-pink-500/30 transition-all hover:scale-105 active:scale-95 mt-6">
                                Salvar
                            </button>"""

new_settings_save = """                            <button 
                                onClick={() => {
                                    if (!userSettings.user1Name.trim() || !userSettings.user2Name.trim()) {
                                        alert("Por favor, preencha o nome dos dois participantes.");
                                        return;
                                    }
                                    setShowSettingsModal(false);
                                }} 
                                className="w-full px-4 py-3 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-lg font-bold shadow-lg shadow-pink-500/30 transition-all hover:scale-105 active:scale-95 mt-6"
                            >
                                Salvar
                            </button>"""

content = content.replace(old_settings_save, new_settings_save)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Ajustes Mobile, 50/50 e Validação aplicados!")
