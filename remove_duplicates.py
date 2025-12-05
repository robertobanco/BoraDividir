# Remover mensagens duplicadas abaixo do header

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ItemizedBillManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remover o primeiro bloco duplicado (linhas 420-436)
duplicate1 = """            
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

content = content.replace(duplicate1, "")

# Verificar se há mais duplicatas e remover
# Procurar por qualquer outro bloco similar
import re
# Remover qualquer outro bloco de mensagem de diferença que possa existir
pattern = r'\s*{/\* Mensagem de diferença quando expandido \*/}\s*{isExpanded && !isSubtotalValid &&[^}]+}</div>\s*</div>\s*\)}'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ItemizedBillManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Mensagens duplicadas removidas!")
print("✅ Agora só aparece a mensagem no header do card")
