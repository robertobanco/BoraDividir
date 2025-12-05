import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Atualizar a assinatura do EventTypeModal
content = content.replace(
    "const EventTypeModal: React.FC<{ onSelect: (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL') => void",
    "const EventTypeModal: React.FC<{ onSelect: (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => void"
)

# 2. Encontrar onde adicionar o botão (após o botão de SHARED_EXPENSES e antes do </div> de fechamento)
# Procurar por "Ideal para viagens ou casa" e adicionar o novo botão depois
search_text = '''                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para viagens ou casa. Registre quem pagou o quê e acerte as diferenças.</p>
                    </button>
                </div>'''

replacement_text = '''                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para viagens. Registre quem pagou o quê e acerte as diferenças.</p>
                    </button>
                    <button onClick={() => onSelect('DOMESTIC_EXPENSES')} className="group w-full text-left p-5 border border-slate-200 dark:border-slate-700 rounded-xl hover:bg-violet-50 dark:hover:bg-violet-900/20 hover:border-violet-300 dark:hover:border-violet-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-violet-500">
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
                </div>'''

content = content.replace(search_text, replacement_text)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Botão de Contas Domésticas adicionado com sucesso!")
