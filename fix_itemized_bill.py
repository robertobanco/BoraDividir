# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ItemizedBillManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Mudar botão de ícone $ para texto "Incluir"
old_button = """                            <button type="submit" disabled={!itemDescription.trim() || !itemAmount} className="bg-violet-600 hover:bg-violet-700 text-white p-2 rounded-lg transition-colors disabled:opacity-50 flex-shrink-0">
                                <CurrencyDollarIcon className="h-5 w-5"/>
                            </button>"""

new_button = """                            <button type="submit" disabled={!itemDescription.trim() || !itemAmount} className="bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg transition-colors disabled:opacity-50 flex-shrink-0 text-sm font-semibold">
                                Incluir
                            </button>"""

content = content.replace(old_button, new_button)

# 2. Adicionar mensagem de diferença no header do card quando expandido
# Vou adicionar após a linha do ChevronDownIcon, dentro do header
old_header_end = """                    <ChevronDownIcon className={`h-5 w-5 text-slate-400 transition-transform duration-300 flex-shrink-0 ${isExpanded ? 'rotate-180' : ''}`} />
                </div>
            </div>"""

new_header_end = """                    <ChevronDownIcon className={`h-5 w-5 text-slate-400 transition-transform duration-300 flex-shrink-0 ${isExpanded ? 'rotate-180' : ''}`} />
                </div>
            </div>
            
            {/* Mensagem de diferença quando expandido */}
            {isExpanded && !isSubtotalValid && (
                <div className="px-4 pb-3 animate-fade-in">
                    <div className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium ${
                        difference > 0 
                            ? 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300' 
                            : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                    }`}>
                        <ExclamationTriangleIcon className="h-4 w-4 flex-shrink-0" />
                        <span>
                            {difference > 0 
                                ? `Faltam ${formatCurrency(difference)} para atingir o subtotal` 
                                : `Você passou ${formatCurrency(Math.abs(difference))} do subtotal`}
                        </span>
                    </div>
                </div>
            )}
            {isExpanded && isSubtotalValid && items.length > 0 && (
                <div className="px-4 pb-3 animate-fade-in">
                    <div className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300">
                        <CheckCircleIcon className="h-4 w-4 flex-shrink-0" />
                        <span>Subtotal correto! ✓</span>
                    </div>
                </div>
            )}"""

content = content.replace(old_header_end, new_header_end)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ItemizedBillManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Problema 3 corrigido:")
print("  - Botão mudado de ícone '$' para texto 'Incluir'")
print("  - Mensagem de diferença adicionada no card Consumo")
print("  - Foco automático já estava implementado!")
