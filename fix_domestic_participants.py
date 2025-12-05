# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir a lógica de exibição de participantes para eventos domésticos
old_participants_logic = "{event.participants.length === 0 && <span className=\"text-xs text-slate-400 italic py-2\">Sem participantes</span>}"

new_participants_logic = """{event.type === 'DOMESTIC_EXPENSES' ? (
                                                            <>
                                                                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-slate-800 bg-gradient-to-br from-pink-400 to-rose-400 flex items-center justify-center text-xs font-bold text-white">
                                                                    {event.userSettings.user1Name.charAt(0).toUpperCase()}
                                                                </div>
                                                                <div className="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-slate-800 bg-gradient-to-br from-violet-400 to-indigo-400 flex items-center justify-center text-xs font-bold text-white">
                                                                    {event.userSettings.user2Name.charAt(0).toUpperCase()}
                                                                </div>
                                                            </>
                                                        ) : event.participants.length === 0 && <span className="text-xs text-slate-400 italic py-2">Sem participantes</span>}"""

content = content.replace(old_participants_logic, new_participants_logic)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Problema 1 corrigido: Participantes do modo doméstico agora aparecem corretamente!")
