# CORREÇÃO: Mover modal para dentro do componente

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# O problema é que temos:
#       )}
#   </div>
#
#   {/* Export Modal */}
#   {showExportModal && ...

# Precisamos mover o </div> para o final

# 1. Remover o </div> que está antes do modal
wrong_div_position = """            )}
        </div>

            {/* Export Modal */}"""

# 2. Adicionar o </div> no final do arquivo (antes do último ); )
# Mas primeiro vamos remover o div errado
if wrong_div_position in content:
    content = content.replace(wrong_div_position, """            )}
            
            {/* Export Modal */}""")
    
    # Agora adicionar o </div> no final
    # Procurar o final do componente
    content = content.strip()
    if content.endswith(");"):
        content = content[:-2] + "\n        </div>\n    );\n};"
    elif content.endswith("};"):
        # Tentar achar onde fecha o return
        last_brace = content.rfind("}")
        before_last_brace = content[:last_brace].rstrip()
        if before_last_brace.endswith(");"):
             content = before_last_brace[:-2] + "\n        </div>\n    );\n};"

# Essa abordagem de string replace no final é arriscada. Vamos tentar algo mais seguro.
# Vamos substituir o bloco inteiro do final.

# Ler as últimas linhas para confirmar
lines = content.split('\n')
# Encontrar a linha 662 (que era </div>)
# No arquivo lido, deve estar por volta dessa posição.

# Vamos usar uma abordagem mais simples:
# Encontrar "            {/* Export Modal */}" e olhar o que tem antes.
modal_marker = "            {/* Export Modal */}"
parts = content.split(modal_marker)

if len(parts) > 1:
    before_modal = parts[0]
    after_modal = parts[1]
    
    # Remover o último </div> de before_modal
    last_div_index = before_modal.rfind("</div>")
    if last_div_index != -1:
        before_modal = before_modal[:last_div_index] + before_modal[last_div_index+6:]
    
    # Reconstruir
    new_content = before_modal + modal_marker + after_modal
    
    # Agora precisamos garantir que o </div> esteja no final do after_modal, antes do );
    # O after_modal termina com );\n};
    # Vamos inserir o </div> antes do );
    
    last_paren_semi = new_content.rfind(");")
    if last_paren_semi != -1:
        new_content = new_content[:last_paren_semi] + "\n        </div>" + new_content[last_paren_semi:]
        
    content = new_content

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Correção de sintaxe aplicada!")
