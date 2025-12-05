# Script consolidado para aplicar todas as mudanças ao EventSelector

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar DOMESTIC_EXPENSES ao tipo do EventTypeModal
content = content.replace(
    "const EventTypeModal: React.FC<{ onSelect: (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL') => void, onCancel: () => void }> = ({ onSelect, onCancel }) => {",
    "const EventTypeModal: React.FC<{ onSelect: (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => void, onCancel: () => void }> = ({ onSelect, onCancel }) => {"
)

# 2. Adicionar botão de Contas Domésticas (usando insert_button.py já testado)
lines = content.split('\n')
insert_after = None
for i, line in enumerate(lines):
    if '</button>' in line and i + 1 < len(lines) and '</div>' in lines[i+1] and i + 2 < len(lines) and 'mt-8 text-center' in lines[i+2]:
        insert_after = i + 1
        break

if insert_after:
    domestic_button = '''                    <button onClick={() => onSelect('DOMESTIC_EXPENSES')} className="group w-full text-left p-5 border border-slate-200 dark:border-slate-700 rounded-xl hover:bg-violet-50 dark:hover:bg-violet-900/20 hover:border-violet-300 dark:hover:border-violet-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-violet-500">
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
'''
    lines.insert(insert_after, domestic_button)
    content = '\n'.join(lines)

# 3. Atualizar handleSelectEventType
content = content.replace(
    "const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL') =>",
    "const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') =>"
)

content = content.replace(
    """if (type === 'SHARED_EXPENSES') {
            onAddEvent(pendingEvent.name, pendingEvent.date, type);
            cleanup();
        } else {
            setShowBillSetupModal(true);
        }""",
    """if (type === 'SHARED_EXPENSES' || type === 'DOMESTIC_EXPENSES') {
            onAddEvent(pendingEvent.name, pendingEvent.date, type);
            cleanup();
        } else {
            setShowBillSetupModal(true);
        }"""
)

# 4. Corrigir badge para mostrar "Doméstico"
# Usar regex para encontrar e substituir
import re
badge_pattern = r'event\.type === \'SHARED_EXPENSES\' \? \'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300\' : \'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300\''
badge_replacement = "event.type === 'SHARED_EXPENSES' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' : event.type === 'DOMESTIC_EXPENSES' ? 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'"
content = re.sub(badge_pattern, badge_replacement, content)

label_pattern = r"\{event\.type === 'SHARED_EXPENSES' \? 'Compartilhado' : 'Detalhado'\}"
label_replacement = "{event.type === 'SHARED_EXPENSES' ? 'Compartilhado' : event.type === 'DOMESTIC_EXPENSES' ? 'Doméstico' : 'Detalhado'}"
content = re.sub(label_pattern, label_replacement, content)

# 5. Corrigir participantes do card doméstico
content = content.replace(
    "{event.participants.length === 0 && <span className=\"text-xs text-slate-400 italic py-2\">Sem participantes</span>}",
    """{event.type === 'DOMESTIC_EXPENSES' ? (
                                                            <>
                                                                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-slate-800 bg-gradient-to-br from-pink-400 to-rose-400 flex items-center justify-center text-xs font-bold text-white">
                                                                    {event.userSettings.user1Name.charAt(0).toUpperCase()}
                                                                </div>
                                                                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-slate-800 bg-gradient-to-br from-violet-400 to-indigo-400 flex items-center justify-center text-xs font-bold text-white">
                                                                    {event.userSettings.user2Name.charAt(0).toUpperCase()}
                                                                </div>
                                                            </>
                                                        ) : event.participants.length === 0 && <span className="text-xs text-slate-400 italic py-2">Sem participantes</span>}"""
)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Todas as mudanças aplicadas ao EventSelector!")
print("  - DOMESTIC_EXPENSES adicionado")
print("  - Botão de Contas Domésticas adicionado")
print("  - Handler atualizado")
print("  - Badge corrigido")
print("  - Participantes domésticos corrigidos")
