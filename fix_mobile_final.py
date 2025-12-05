# AJUSTES FINAIS: Modal Scroll e Layout Lista

import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Corrigir Scroll do Modal
# Procurar o container do modal de Add/Edit
# Ele tem className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-md animate-scale-in bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700"
# Vamos adicionar max-h-[90vh] overflow-y-auto

modal_class_old = 'className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-md animate-scale-in bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700"'
modal_class_new = 'className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-md animate-scale-in bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 max-h-[90vh] overflow-y-auto"'

if modal_class_old in content:
    content = content.replace(modal_class_old, modal_class_new)
    print("✅ Scroll do modal corrigido!")
else:
    print("⚠️ Aviso: Não encontrei a classe exata do modal para adicionar scroll.")

# 2. Ajustar Layout da Lista (Categoria embaixo do ícone e quebra de linha no Pago Por)
# Vamos substituir o bloco do render do item novamente.

# Bloco antigo (simplificado para busca)
# Começa com <div className="flex items-start gap-3">
# Termina antes dos botões de ação

# Vamos construir o novo JSX para o item
new_item_inner = """                                    <div className="flex items-start gap-3">
                                        {/* Left Column: Icon + Category Name */}
                                        <div className="flex flex-col items-center gap-1 min-w-[3.5rem]">
                                            <div className={`p-2.5 rounded-xl ${categoryInfo.bgColor} flex-shrink-0`}>
                                                <span className="text-xl">{categoryInfo.icon}</span>
                                            </div>
                                            <span className="text-[9px] font-bold uppercase tracking-wider text-slate-500 text-center leading-tight">
                                                {categoryInfo.label}
                                            </span>
                                        </div>

                                        {/* Main Content */}
                                        <div className="flex-1 min-w-0">
                                            {/* Top Row: Description & Amount */}
                                            <div className="flex justify-between items-start gap-2">
                                                <p className="font-semibold text-slate-200 dark:text-white text-base leading-tight break-words pt-1">
                                                    {expense.description}
                                                </p>
                                                <div className="text-right flex-shrink-0 pt-1">
                                                    <p className="font-bold text-slate-900 dark:text-white text-lg whitespace-nowrap">
                                                        {formatCurrency(expense.amount)}
                                                    </p>
                                                </div>
                                            </div>

                                            {/* Metadata Column */}
                                            <div className="mt-2 flex flex-col gap-1 text-xs sm:text-sm text-slate-500 dark:text-slate-400">
                                                {/* Date & Tags Row */}
                                                <div className="flex flex-wrap items-center gap-2">
                                                    <span className="font-mono text-slate-400">{dateStr}</span>
                                                    
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

                                                {/* Payer & Responsibility (Stacked) */}
                                                <div className="flex flex-col">
                                                    <span>
                                                        Pago por <span className="font-medium text-slate-300 dark:text-slate-200">{expense.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name}</span>
                                                    </span>
                                                    <span className="text-slate-500 dark:text-slate-500 text-[11px]">
                                                        {expense.ownershipPercentage === 50 
                                                            ? '(50% / 50%)'
                                                            : `(${userSettings.user1Name} ${expense.ownershipPercentage}% / ${100 - expense.ownershipPercentage}% ${userSettings.user2Name})`
                                                        }
                                                    </span>
                                                </div>
                                            </div>
                                            
                                            {/* Action Buttons - Horizontal Bottom Right */}
                                            <div className="flex justify-end mt-2 h-8">
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
                                    </div>"""

# Precisamos substituir o conteúdo interno da div principal do item.
# A div principal começa com: <div key={expense.id} ... onClick={...} className={...}>
# E termina com </div>

# Vamos localizar o início do conteúdo interno
start_marker = '<div className="flex items-start gap-3">'

# Vamos localizar o fim do conteúdo interno
# O conteúdo interno termina antes do fechamento da div principal.
# No código atual, ele termina com:
#                                             </div>
#                                         </div>
#                                     </div>
#                                 </div>

# Vamos substituir tudo entre start_marker e o fechamento da div principal.
# Mas como o código atual está um pouco diferente do que eu imagino (por causa das edições anteriores),
# vamos ser cirúrgicos.

# Vamos substituir o bloco inteiro do item novamente para garantir.
# Mas precisamos pegar o onClick e className corretos que já estão lá (com a lógica de toggle).

# Vamos ler o bloco atual do item
if start_marker in content:
    start_idx = content.find(start_marker)
    
    # Achar o fim do item.
    # O item termina com:
    #                                 </div>
    #                             );
    #                         })}
    
    end_marker = '                                </div>\n                            );\n                        })}'
    end_idx = content.find(end_marker)
    
    if end_idx != -1:
        # Substituir o miolo
        content = content[:start_idx] + new_item_inner + content[end_idx:]
        print("✅ Layout da lista atualizado!")
    else:
        print("❌ Erro: Não encontrei o fim do item da lista.")
else:
    print("❌ Erro: Não encontrei o início do item da lista.")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
