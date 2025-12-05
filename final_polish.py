# AJUSTES FINAIS: Cores e Layout Compacto

import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Substituir Cores (Purple -> Blue)
# Vamos substituir todas as ocorrências de 'purple' por 'blue'
# Isso cuida de text-purple-*, bg-purple-*, border-purple-*, from-purple-*, to-purple-*
content = content.replace('purple', 'blue')
print("✅ Cores atualizadas: Roxo -> Azul")

# 2. Ajustar Layout da Lista para remover espaço vazio
# Vamos reestruturar o final do item da lista para que os botões fiquem na mesma linha da info de responsabilidade.

# Bloco antigo (baseado no último patch)
# Começa com {/* Metadata Column */}
# Termina com o fechamento da div principal do item

# Vamos localizar o início da coluna de metadados
start_marker = '{/* Metadata Column */}'

# Vamos construir o novo bloco de metadados + ações
new_metadata_block = """{/* Metadata Column */}
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
                                                        <span className="px-1.5 py-0.5 bg-blue-500/10 text-blue-400 rounded text-[10px] font-medium uppercase tracking-wide border border-blue-500/20">
                                                            {(() => {
                                                                const current = getCurrentInstallment(expense, currentMonth);
                                                                return current ? `${current}/${expense.installmentsCount}` : `${expense.installmentsCount}x`;
                                                            })()}
                                                        </span>
                                                    )}
                                                </div>

                                                {/* Bottom Row: Payer Info + Actions */}
                                                <div className="flex justify-between items-end mt-0.5 min-h-[2.5rem]">
                                                    {/* Payer & Responsibility */}
                                                    <div className="flex flex-col justify-center">
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

                                                    {/* Action Buttons - Inline Right */}
                                                    {activeExpenseId === expense.id && (
                                                        <div className="flex items-center gap-2 animate-scale-in ml-2 mb-0.5">
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

# Precisamos substituir o trecho antigo.
# O trecho antigo começa em {/* Metadata Column */} e vai até o fechamento das divs.
# No último patch, adicionamos:
# {/* Action Buttons - Horizontal Bottom Right */}
# <div className="flex justify-end mt-2 h-8"> ... </div>

# Vamos localizar o início e o fim desse bloco maior.
if start_marker in content:
    start_idx = content.find(start_marker)
    
    # O fim é antes do fechamento do item.
    # O item termina com:
    #                                 </div>
    #                             );
    #                         })}
    
    end_marker = '                                </div>\n                            );\n                        })}'
    end_idx = content.find(end_marker)
    
    if end_idx != -1:
        # Substituir
        content = content[:start_idx] + new_metadata_block + content[end_idx:]
        print("✅ Layout compactado com sucesso!")
    else:
        print("❌ Erro: Não encontrei o fim do bloco do item.")
else:
    print("❌ Erro: Não encontrei o início do bloco de metadados.")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
