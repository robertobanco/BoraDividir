# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar a linha onde inserir (depois do botão de Despesas Compartilhadas)
insert_after = None
for i, line in enumerate(lines):
    if '</button>' in line and i + 1 < len(lines) and '</div>' in lines[i+1] and i + 2 < len(lines) and 'mt-8 text-center' in lines[i+2]:
        insert_after = i + 1
        break

if insert_after:
    # Criar o novo botão
    new_button = '''                    <button onClick={() => onSelect('DOMESTIC_EXPENSES')} className="group w-full text-left p-5 border border-slate-200 dark:border-slate-700 rounded-xl hover:bg-violet-50 dark:hover:bg-violet-900/20 hover:border-violet-300 dark:hover:border-violet-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-violet-500">
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
    
    # Inserir o botão
    lines.insert(insert_after, new_button)
    
    # Salvar
    with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✅ Botão adicionado na linha {insert_after + 1}")
else:
    print("❌ Posição não encontrada")
