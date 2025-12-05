# REFACTOR LAYOUT MOBILE E AJUSTES FINAIS

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Vamos substituir o bloco inteiro do render do item da lista (map)
# Precisamos identificar onde começa o map das despesas

# Padrão para encontrar o início do map
start_map_pattern = "{sortedExpenses.map((expense) => {"

# Padrão para encontrar o fim do map (o fechamento do return do map)
# É difícil achar o fim exato com regex simples dado o aninhamento.
# Vamos substituir o conteúdo do return do map.

# Vamos construir o novo JSX para o item da lista
new_item_jsx = """                        {sortedExpenses.map((expense) => {
                            const categoryInfo = getCategoryInfo(expense.category);
                            const [y, m, d] = expense.date.split('-').map(Number);
                            const displayDate = new Date(y, m - 1, d, 12, 0, 0);
                            const dateStr = isNaN(displayDate.getTime()) ? '--' : displayDate.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });

                            // Helper para calcular qual parcela está sendo exibida
                            const getCurrentInstallment = (expense: DomesticExpense, currentMonthKey: string): number | null => {
                                if (expense.frequency !== 'PARCELADA' || !expense.installmentsCount) return null;
                                const [expenseYear, expenseMonth] = expense.date.split('-').map(Number);
                                const [currentYear, currentMonth] = currentMonthKey.split('-').map(Number);
                                const monthsDiff = (currentYear - expenseYear) * 12 + (currentMonth - expenseMonth);
                                if (monthsDiff < 0 || monthsDiff >= expense.installmentsCount) return null;
                                return monthsDiff + 1;
                            };

                            return (
                                <div key={expense.id} className="relative p-4 hover:bg-slate-800/50 dark:hover:bg-slate-700/50 transition-colors group border-b border-slate-800/50 dark:border-slate-700/50 last:border-0">
                                    <div className="flex items-start gap-3">
                                        {/* Icon */}
                                        <div className={`p-2.5 rounded-xl ${categoryInfo.bgColor} flex-shrink-0 mt-0.5`}>
                                            <span className="text-xl">{categoryInfo.icon}</span>
                                        </div>

                                        {/* Main Content */}
                                        <div className="flex-1 min-w-0">
                                            {/* Top Row: Description & Amount */}
                                            <div className="flex justify-between items-start gap-3">
                                                <p className="font-semibold text-slate-200 dark:text-white text-base leading-tight break-words pr-8">
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
                                            
                                            {/* Category Label (Mobile optimized) */}
                                            <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-wider font-medium">
                                                {categoryInfo.label}
                                            </p>
                                        </div>
                                    </div>

                                    {/* Action Buttons - Absolute Positioned */}
                                    <div className="absolute right-2 top-1/2 -translate-y-1/2 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity bg-slate-900/90 dark:bg-slate-800/90 p-1 rounded-lg backdrop-blur-sm border border-slate-700 shadow-xl z-10">
                                        <button 
                                            onClick={(e) => { e.stopPropagation(); handleEditExpense(expense); }}
                                            className="p-2 text-blue-400 hover:text-blue-300 hover:bg-blue-500/20 rounded-md transition-colors"
                                            title="Editar"
                                        >
                                            <Pencil size={16} />
                                        </button>
                                        <button 
                                            onClick={(e) => { e.stopPropagation(); handleDeleteExpense(expense.id); }}
                                            className="p-2 text-red-400 hover:text-red-300 hover:bg-red-500/20 rounded-md transition-colors"
                                            title="Excluir"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>
                            );
                        })}"""

# Precisamos substituir o bloco antigo pelo novo.
# Vamos usar regex para capturar do sortedExpenses.map até o fechamento dele.
import re

# Regex para capturar o bloco do map. 
# Assume que começa com {sortedExpenses.map e termina com })} antes do </div> que fecha a lista
# Isso é arriscado com regex simples.
# Vamos tentar localizar pelo início e fim conhecidos do código anterior.

start_marker = "{sortedExpenses.map((expense) => {"
end_marker = "                        })}\n                    </div>"

# O código anterior terminava com:
#                                 </div>
#                             );
#                         })}
#                     </div>

# Vamos ler o arquivo e tentar localizar o bloco.
if start_marker in content:
    # Encontrar o índice de início
    start_idx = content.find(start_marker)
    
    # Encontrar o índice do fim (procurar o fechamento da div da lista)
    # A div da lista é: <div className="divide-y divide-slate-800 dark:divide-slate-700">
    # O map está dentro dela.
    
    # Vamos procurar a string que fecha o map no código ATUAL
    # No código atual, o map termina com:
    #                             );
    #                         })}
    #                     </div>
    
    # Vamos pegar tudo entre start_marker e o fechamento da div pai
    # Mas é mais seguro substituir o bloco inteiro da lista se possível.
    
    list_container_start = '<div className="divide-y divide-slate-800 dark:divide-slate-700">'
    if list_container_start in content:
        container_start_idx = content.find(list_container_start)
        # Achar o fechamento dessa div. É o primeiro </div> após o map.
        # Vamos assumir que o map é o único filho direto relevante.
        
        # Vamos substituir o conteúdo interno da div
        # Conteúdo antigo:
        # {sortedExpenses.map...
        # ...
        # })}
        
        # Vamos usar o start_marker e tentar achar o final do map
        # O final do map é "})}" seguido de "</div>" (fechamento do container)
        
        # Vamos tentar uma substituição direta do trecho conhecido do map antigo
        # O problema é que o map antigo é grande.
        
        # Vamos usar uma estratégia de "âncoras".
        # Âncora inicial: {sortedExpenses.map((expense) => {
        # Âncora final: })} (antes do </div>)
        
        # Vamos reconstruir o arquivo
        pre_map = content[:start_idx]
        
        # Achar onde termina o map antigo.
        # Vamos procurar "})}" a partir do start_idx
        # Mas cuidado com maps aninhados (não tem aqui).
        
        # Vamos procurar o fechamento da div container
        div_close_idx = content.find("</div>", start_idx)
        
        # O map deve fechar antes disso.
        # Vamos procurar "})}" de trás pra frente a partir do div_close_idx
        map_close_idx = content.rfind("})}", start_idx, div_close_idx + 6) # +6 margem
        
        if map_close_idx != -1:
             post_map = content[map_close_idx + 3:] # +3 para pular "})}"
             
             # Montar novo conteúdo
             new_content = pre_map + new_item_jsx + post_map
             
             # Salvar
             with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
                 f.write(new_content)
                 print("✅ Layout Mobile e Lógica 50/50 atualizados com sucesso!")
        else:
            print("❌ Erro: Não foi possível encontrar o fim do map antigo.")
    else:
        print("❌ Erro: Container da lista não encontrado.")
else:
    print("❌ Erro: Início do map não encontrado.")
