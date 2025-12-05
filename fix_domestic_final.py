# CORREÇÃO DEFINITIVA DO MODO DOMÉSTICO

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Corrigir o badge do header para mostrar "Contas Domésticas"
old_badge = """                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${currentEvent.type === 'SHARED_EXPENSES' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'}`}>
                        {currentEvent.type === 'SHARED_EXPENSES' ? 'Despesas Compartilhadas' : 'Conta Detalhada'}
                    </span>"""

new_badge = """                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                        currentEvent.type === 'SHARED_EXPENSES' 
                            ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' 
                            : currentEvent.type === 'DOMESTIC_EXPENSES'
                                ? 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300'
                                : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                    }`}>
                        {currentEvent.type === 'SHARED_EXPENSES' 
                            ? 'Despesas Compartilhadas' 
                            : currentEvent.type === 'DOMESTIC_EXPENSES'
                                ? 'Contas Domésticas'
                                : 'Conta Detalhada'}
                    </span>"""

content = content.replace(old_badge, new_badge)
print("✅ Badge do header corrigido")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ MODO DOMÉSTICO CORRIGIDO DEFINITIVAMENTE!")
