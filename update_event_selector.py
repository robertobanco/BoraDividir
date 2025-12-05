import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Atualizar calculateEventTotal
old_calc = """const calculateEventTotal = (event: BillSplitEvent): number => {
    if (event.type === 'SHARED_EXPENSES') {
        return event.expenses.reduce((sum, exp) => sum + exp.amount, 0);
    } else { // ITEMIZED_BILL
        const itemsSubtotal = event.items.reduce((sum, item) => sum + item.amount, 0);
        const tipAmount = event.tip.type === 'PERCENT'
            ? itemsSubtotal * (event.tip.value / 100)
            : event.tip.value;
        return itemsSubtotal + tipAmount + event.tax;
    }
};"""

new_calc = """const calculateEventTotal = (event: BillSplitEvent): number => {
    if (event.type === 'SHARED_EXPENSES') {
        return event.expenses.reduce((sum, exp) => sum + exp.amount, 0);
    } else if (event.type === 'ITEMIZED_BILL') {
        const itemsSubtotal = event.items.reduce((sum, item) => sum + item.amount, 0);
        const tipAmount = event.tip.type === 'PERCENT'
            ? itemsSubtotal * (event.tip.value / 100)
            : event.tip.value;
        return itemsSubtotal + tipAmount + event.tax;
    } else { // DOMESTIC_EXPENSES
        return event.domesticExpenses.reduce((sum, exp) => sum + exp.amount, 0);
    }
};"""

content = content.replace(old_calc, new_calc)

# 2. Adicionar botão de Contas Domésticas no modal
# Encontrar o final do botão de SHARED_EXPENSES
search_text = """                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para viagens. Registre quem pagou o quê e acerte as diferenças.</p>
                    </button>
                </div>"""

domestic_button = """                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para viagens. Registre quem pagou o quê e acerte as diferenças.</p>
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
                </div>"""

content = content.replace(search_text, domestic_button)

# 3. Atualizar badge na lista de eventos
old_event_badge = """<span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${event.type === 'SHARED_EXPENSES' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'}`}>
                                            {event.type === 'SHARED_EXPENSES' ? 'Compartilhado' : 'Detalhado'}
                                        </span>"""

new_event_badge = """<span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                            event.type === 'SHARED_EXPENSES' 
                                                ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' 
                                                : event.type === 'ITEMIZED_BILL'
                                                ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                                                : 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300'
                                        }`}>
                                            {event.type === 'SHARED_EXPENSES' 
                                                ? 'Compartilhado' 
                                                : event.type === 'ITEMIZED_BILL'
                                                ? 'Detalhado'
                                                : 'Doméstico'}
                                        </span>"""

content = content.replace(old_event_badge, new_event_badge)

# Salvar o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("EventSelector.tsx atualizado com sucesso!")
