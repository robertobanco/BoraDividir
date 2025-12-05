# AJUSTE BOTÕES: Horizontal, Bottom-Right, Toggle

import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar o estado activeExpenseId
# Vamos adicionar logo após o estado editingExpense
if "const [editingExpense, setEditingExpense] = useState<DomesticExpense | null>(null);" in content:
    content = content.replace(
        "const [editingExpense, setEditingExpense] = useState<DomesticExpense | null>(null);",
        "const [editingExpense, setEditingExpense] = useState<DomesticExpense | null>(null);\n    const [activeExpenseId, setActiveExpenseId] = useState<string | null>(null);"
    )

# 2. Substituir o render do item da lista
# Vamos usar um padrão que pegue o início do return do map até o fim
# O padrão anterior que usamos para inserir o layout mobile deve servir de base.

# Vamos procurar o trecho do return dentro do map
# O trecho começa com: return ( <div key={expense.id}
# E termina com o fechamento dos botões e da div.

# Vamos substituir o bloco inteiro do return do map para garantir que tudo fique certo.
# O bloco atual é:
old_return_block_start = 'return (\n                                <div key={expense.id} className="relative p-4 hover:bg-slate-800/50 dark:hover:bg-slate-700/50 transition-colors group border-b border-slate-800/50 dark:border-slate-700/50 last:border-0">'

# Novo bloco com a lógica de toggle e novo posicionamento
new_return_block = """return (
                                <div 
                                    key={expense.id} 
                                    onClick={() => setActiveExpenseId(activeExpenseId === expense.id ? null : expense.id)}
                                    className={`relative p-4 transition-all border-b border-slate-800/50 dark:border-slate-700/50 last:border-0 cursor-pointer
                                        ${activeExpenseId === expense.id ? 'bg-slate-800/80 dark:bg-slate-700/80' : 'hover:bg-slate-800/50 dark:hover:bg-slate-700/50'}
                                    `}
                                >
                                    <div className="flex items-start gap-3">
                                        {/* Icon */}
                                        <div className={`p-2.5 rounded-xl ${categoryInfo.bgColor} flex-shrink-0 mt-0.5`}>
                                            <span className="text-xl">{categoryInfo.icon}</span>
                                        </div>

                                        {/* Main Content */}
                                        <div className="flex-1 min-w-0">
                                            {/* Top Row: Description & Amount */}
                                            <div className="flex justify-between items-start gap-3">
                                                <p className="font-semibold text-slate-200 dark:text-white text-base leading-tight break-words pr-2">
                                                    {expense.description}
                                                </p>
                                                <div className="text-right flex-shrink-0">
                                                    <p className="font-bold text-slate-900 dark:text-white text-lg whitespace-nowrap">
                                                        {formatCurrency(expense.amount)}
                                                    </p>
                                                </div>
                                            </div>

                                            {/* Bottom Row: Metadata */}
                                            <div className="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs sm:text-sm text-slate-500 dark:text-slate-400">
                                                <span className="font-mono text-slate-400">{dateStr}</span>
                                                <span className="text-slate-600 dark:text-slate-500">•</span>
                                                
                                                <span>
                                                    Pago por <span className="font-medium text-slate-300 dark:text-slate-200">{expense.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name}</span>
                                                    <span className="ml-1 text-slate-500 dark:text-slate-500">
                                                        {expense.ownershipPercentage === 50 
                                                            ? '(50% / 50%)'
                                                            : `(${userSettings.user1Name} ${expense.ownershipPercentage}% / ${100 - expense.ownershipPercentage}% ${userSettings.user2Name})`
                                                        }
                                                    </span>
                                                </span>

                                                {(expense.frequency === 'MENSAL' || expense.frequency === 'PARCELADA') && (
                                                    <span className="text-slate-600 dark:text-slate-500 hidden sm:inline">•</span>
                                                )}

                                                {expense.frequency === 'MENSAL' && (
                                                    <span className="px-1.5 py-0.5 bg-blue-500/10 text-blue-400 rounded text-[10px] font-medium uppercase tracking-wide border border-blue-500/20">
                                                        Mensal
                                                    </span>
                                                )}

                                                {expense.frequency === 'PARCELADA' && expense.installmentsCount && (
                                                    <span className="px-1.5 py-0.5 bg-purple-500/10 text-purple-400 rounded text-[10px] font-medium uppercase tracking-wide border border-purple-500/20">
                                                        {(() => {
                                                            const current = getCurrentInstallment(expense, currentMonth);
                                                            return current ? `${current}/${expense.installmentsCount}` : `${expense.installmentsCount}x`;
                                                        })()}
                                                    </span>
                                                )}
                                            </div>
                                            
                                            {/* Category Label & Actions Row */}
                                            <div className="flex justify-between items-end mt-1 h-8">
                                                <p className="text-[10px] text-slate-500 uppercase tracking-wider font-medium self-center">
                                                    {categoryInfo.label}
                                                </p>

                                                {/* Action Buttons - Horizontal Bottom Right */}
                                                {activeExpenseId === expense.id && (
                                                    <div className="flex items-center gap-2 animate-scale-in">
                                                        <button 
                                                            onClick={(e) => { e.stopPropagation(); handleEditExpense(expense); }}
                                                            className="p-2 bg-blue-500/20 text-blue-400 hover:bg-blue-500/30 hover:text-blue-300 rounded-lg transition-colors shadow-sm"
                                                            title="Editar"
                                                        >
                                                            <Pencil size={18} />
                                                        </button>
                                                        <button 
                                                            onClick={(e) => { e.stopPropagation(); handleDeleteExpense(expense.id); }}
                                                            className="p-2 bg-red-500/20 text-red-400 hover:bg-red-500/30 hover:text-red-300 rounded-lg transition-colors shadow-sm"
                                                            title="Excluir"
                                                        >
                                                            <Trash2 size={18} />
                                                        </button>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                </div>"""

# Precisamos substituir o bloco antigo pelo novo.
# Vamos usar o start_marker e tentar achar o fim do bloco antigo.
# O bloco antigo termina com </div> );

if old_return_block_start in content:
    # Achar onde começa
    start_idx = content.find(old_return_block_start)
    
    # Achar onde termina o bloco antigo.
    # Ele termina com:
    #                                     </div>
    #                                 </div>
    #                             );
    
    # Vamos procurar o fechamento ");" após o start_idx
    # Mas cuidado, tem outros fechamentos dentro.
    
    # Vamos procurar o fechamento da div principal do item
    # <div key={expense.id} ...> ... </div> );
    
    # Vamos usar uma string única do final do bloco antigo para localizar o fim
    unique_end_string = '<Trash2 size={16} />\n                                        </button>\n                                    </div>\n                                </div>\n                            );'
    
    end_idx = content.find(unique_end_string, start_idx)
    
    if end_idx != -1:
        end_idx += len(unique_end_string)
        
        # Substituir
        content = content[:start_idx] + new_return_block + content[end_idx:]
        
        # Salvar
        with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Botões ajustados: Horizontal, Bottom-Right e Toggle!")
    else:
        print("❌ Erro: Não encontrei o final do bloco antigo.")
else:
    print("❌ Erro: Não encontrei o início do bloco antigo.")
