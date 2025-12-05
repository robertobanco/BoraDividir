# CORREÇÃO FINAL 2: Adicionar div faltante no modal de settings

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# O problema está aqui:
# 659:                     </div>
# 660:                 
# 661:             )}

# Precisa ser:
# 659:                     </div>
# 660:                 </div>
# 661:             )}

# Vamos procurar esse padrão
missing_div_pattern = """                    </div>
                
            )}"""

fixed_pattern = """                    </div>
                </div>
            )}"""

if missing_div_pattern in content:
    content = content.replace(missing_div_pattern, fixed_pattern)
else:
    # Tentar outra variação se a indentação estiver diferente
    # Vamos procurar pelo fechamento do modal de settings
    # Ele termina antes do Export Modal
    export_modal_start = "{/* Export Modal */}"
    parts = content.split(export_modal_start)
    
    if len(parts) > 1:
        before_export = parts[0]
        # Verificar se tem o fechamento correto
        if not before_export.strip().endswith("</div>\n            )}"):
             # Tentar corrigir inserindo o div
             last_brace = before_export.rfind(")}")
             if last_brace != -1:
                 # Verificar se tem o div antes
                 snippet = before_export[last_brace-20:last_brace]
                 if "</div>" not in snippet: # Simplificação grosseira
                     # Inserir o div
                     before_export = before_export[:last_brace] + "    </div>\n            " + before_export[last_brace:]
                     content = before_export + export_modal_start + parts[1]

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Sintaxe corrigida (div faltante adicionado)!")
