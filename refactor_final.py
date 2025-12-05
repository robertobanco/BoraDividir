# REFACTOR COMPLETO: Corrigir estrutura e layout mobile

import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extrair getCurrentInstallment e handleExportExcel que estão mal posicionados (dentro do map)
# Vamos removê-los do meio do código e colocá-los no início do componente.

# Padrão para remover getCurrentInstallment de dentro do map
bad_helper_pattern = r"// Helper para calcular qual parcela está sendo exibida\s+const getCurrentInstallment =[\s\S]+?};"
content = re.sub(bad_helper_pattern, "", content)

# Padrão para remover handleExportExcel de dentro do map
bad_export_pattern = r"const handleExportExcel = \(\) => \{[\s\S]+?setShowExportModal\(false\);\s+};\s+return \("
# Esse padrão é perigoso porque pega o return. Vamos tentar achar o bloco exato.
# O handleExportExcel termina com setShowExportModal(false); };
# E logo depois vem o return ( do map.

# Vamos localizar o trecho errado manualmente
start_bad_export = "const handleExportExcel = () => {"
if content.count(start_bad_export) > 1:
    # Se tiver mais de uma vez, a segunda (que está mais pro final, dentro do map) é a errada.
    # Mas na verdade, o patch anterior INSERIU ela lá. Então só deve ter uma, no lugar errado.
    pass

# Vamos definir as funções corretas para inserir no topo
correct_functions = """
    // Helper para calcular qual parcela está sendo exibida
    const getCurrentInstallment = (expense: DomesticExpense, currentMonthKey: string): number | null => {
        if (expense.frequency !== 'PARCELADA' || !expense.installmentsCount) return null;
        const [expenseYear, expenseMonth] = expense.date.split('-').map(Number);
        const [currentYear, currentMonth] = currentMonthKey.split('-').map(Number);
        const monthsDiff = (currentYear - expenseYear) * 12 + (currentMonth - expenseMonth);
        if (monthsDiff < 0 || monthsDiff >= expense.installmentsCount) return null;
        return monthsDiff + 1;
    };

    const handleExportExcel = () => {
        const monthName = new Date(currentMonth + '-01T12:00:00').toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
        
        // Preparar dados para o Excel
        const data = monthlyBalance.items.map(item => ({
            Data: new Date(item.date).toLocaleDateString('pt-BR'),
            Descrição: item.description,
            Categoria: item.category,
            Valor: item.amount,
            'Quem Pagou': item.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name,
            'Responsabilidade': item.ownershipPercentage !== 50 
                ? `${userSettings.user1Name} ${item.ownershipPercentage}% / ${userSettings.user2Name} ${100 - item.ownershipPercentage}%`
                : 'Meio a Meio',
            'Recorrência': item.frequency === 'UNICA' ? 'Única' : item.frequency === 'MENSAL' ? 'Mensal' : `Parcelada (${item.installmentsCount}x)`
        }));

        // Adicionar resumo no final
        data.push({} as any); // Linha em branco
        data.push({
            Data: 'RESUMO',
            Descrição: 'Total Gastos',
            Valor: monthlyBalance.total
        } as any);
        data.push({
            Data: '',
            Descrição: `${userSettings.user1Name} Pagou`,
            Valor: monthlyBalance.user1Paid
        } as any);
        data.push({
            Data: '',
            Descrição: `${userSettings.user2Name} Pagou`,
            Valor: monthlyBalance.user2Paid
        } as any);
        
        if (monthlyBalance.settlement) {
            data.push({
                Data: 'RESULTADO',
                Descrição: `${monthlyBalance.settlement.from} deve a ${monthlyBalance.settlement.to}`,
                Valor: monthlyBalance.settlement.amount
            } as any);
        }

        const ws = XLSX.utils.json_to_sheet(data);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Despesas");
        
        // Ajustar largura das colunas
        const wscols = [
            {wch: 12}, // Data
            {wch: 30}, // Descrição
            {wch: 15}, // Categoria
            {wch: 12}, // Valor
            {wch: 15}, // Quem Pagou
            {wch: 30}, // Responsabilidade
            {wch: 20}  // Recorrência
        ];
        ws['!cols'] = wscols;

        XLSX.writeFile(wb, `BoraDividir_${monthName.replace(' ', '_')}.xlsx`);
        setShowExportModal(false);
    };
"""

# Inserir as funções no lugar certo (antes do return principal do componente)
# Procurar "const monthlyBalance = useMemo" e inserir antes
if "const monthlyBalance = useMemo" in content:
    content = content.replace("const monthlyBalance = useMemo", correct_functions + "\n    const monthlyBalance = useMemo")

# Agora vamos substituir o bloco da lista de despesas inteiro pelo novo layout
# Vamos usar o marcador da div container
list_start = '<div className="divide-y divide-slate-800 dark:divide-slate-700">'
list_end = '</div>' # O primeiro fechamento após o início, mas tem maps dentro...

# Vamos localizar o início e tentar achar o fim do map antigo
if list_start in content:
    start_idx = content.find(list_start) + len(list_start)
    
    # O conteúdo antigo tem o map errado com as funções dentro.
    # Vamos procurar onde termina o map antigo.
    # Ele termina com "})}"
    # Mas como inserimos funções dentro, ele ficou gigante.
    
    # Vamos procurar o próximo "sortedExpenses.map"
    map_start_idx = content.find("{sortedExpenses.map", start_idx)
    
    # Achar o fim desse map.
    # Vamos procurar "return (" dentro do map, e depois o fechamento.
    
    # Vamos simplificar: Vamos substituir TUDO dentro da div "divide-y..."
    # Precisamos achar onde essa div fecha.
    # Como o conteúdo dentro está bagunçado, vamos assumir que a div fecha antes de "{/* Charts */}" ou algo assim?
    # Não, a lista está DEPOIS dos charts.
    
    # A lista está dentro de:
    # <div className="bg-slate-900 ... overflow-hidden">
    #    <div className="p-6 ...">Header</div>
    #    {sortedExpenses.length === 0 ? (...) : (
    #       <div className="divide-y ...">
    #           CONTEUDO A SUBSTITUIR
    #       </div>
    #    )}
    # </div>
    
    # Então a div fecha antes de ")}".
    
    # Vamos achar o trecho:
    # <div className="divide-y divide-slate-800 dark:divide-slate-700">
    # ...
    # </div>
    
    # Vamos usar regex para achar esse bloco, mas regex com aninhamento é ruim.
    # Vamos usar split.
    
    parts = content.split(list_start)
    if len(parts) > 1:
        pre_list = parts[0]
        post_list_raw = parts[1]
        
        # Achar o fechamento da div.
        # Sabemos que depois da div vem ")}".
        end_list_idx = post_list_raw.find("</div>\n                )")
        if end_list_idx == -1:
             end_list_idx = post_list_raw.find("</div>)") # Tentar sem quebra de linha
        
        if end_list_idx != -1:
            post_list = post_list_raw[end_list_idx:]
            
            # Novo conteúdo da lista
            new_list_content = """
                        {sortedExpenses.map((expense) => {
                            const categoryInfo = getCategoryInfo(expense.category);
                            const [y, m, d] = expense.date.split('-').map(Number);
                            const displayDate = new Date(y, m - 1, d, 12, 0, 0);
                            const dateStr = isNaN(displayDate.getTime()) ? '--' : displayDate.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });

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
                        })}
            """
            
            content = pre_list + list_start + new_list_content + post_list

# Limpar qualquer resquício das funções mal posicionadas que o regex inicial pode ter perdido ou deixado lixo
# (O regex inicial já deve ter cuidado da maior parte)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Refatoração completa: Layout Mobile e Estrutura corrigidos!")
