# AJUSTE 1: Mensagem simplificada no header do card Consumo

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ItemizedBillManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir a seção do header para adicionar mensagem quando expandido
old_header_section = """                <div className="flex items-center gap-3">
                    {/* Always show summary when collapsed */}
                    {!isExpanded && items.length > 0 && (
                        <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 animate-fade-in">
                             <span className="hidden sm:inline font-medium">{items.length} itens</span>
                             <span className="hidden sm:inline h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-600"></span>
                             <span className="font-bold text-violet-600 dark:text-violet-400 bg-violet-50 dark:bg-violet-900/20 px-2 py-1 rounded-md">
                                {formatCurrency(itemsSubtotal)}
                             </span>
                        </div>
                    )}
                    <ChevronDownIcon className={`h-5 w-5 text-slate-400 transition-transform duration-300 flex-shrink-0 ${isExpanded ? 'rotate-180' : ''}`} />
                </div>"""

new_header_section = """                <div className="flex items-center gap-3">
                    {/* Show summary when collapsed */}
                    {!isExpanded && items.length > 0 && (
                        <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 animate-fade-in">
                             <span className="hidden sm:inline font-medium">{items.length} itens</span>
                             <span className="hidden sm:inline h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-600"></span>
                             <span className="font-bold text-violet-600 dark:text-violet-400 bg-violet-50 dark:bg-violet-900/20 px-2 py-1 rounded-md">
                                {formatCurrency(itemsSubtotal)}
                             </span>
                        </div>
                    )}
                    {/* Show difference message when expanded */}
                    {isExpanded && !isSubtotalValid && (
                        <span className={`text-sm font-medium ${
                            difference > 0 
                                ? 'text-amber-600 dark:text-amber-400' 
                                : 'text-blue-600 dark:text-blue-400'
                        }`}>
                            {difference > 0 
                                ? `Falta incluir ${formatCurrency(difference)}` 
                                : `Passou ${formatCurrency(Math.abs(difference))}`}
                        </span>
                    )}
                    {isExpanded && isSubtotalValid && items.length > 0 && (
                        <span className="text-sm font-medium text-emerald-600 dark:text-emerald-400">
                            Subtotal correto ✓
                        </span>
                    )}
                    <ChevronDownIcon className={`h-5 w-5 text-slate-400 transition-transform duration-300 flex-shrink-0 ${isExpanded ? 'rotate-180' : ''}`} />
                </div>"""

content = content.replace(old_header_section, new_header_section)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ItemizedBillManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ AJUSTE 1 COMPLETO: Mensagem simplificada no header do card Consumo!")
