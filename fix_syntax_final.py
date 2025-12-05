# CORREÇÃO FINAL: Remover div extra

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remover o penúltimo </div>
# O arquivo termina com:
#         </div>
#     
#         </div>);
# };

# Vamos substituir esse final pelo correto
wrong_ending = """        </div>
    
        </div>);
};"""

correct_ending = """        </div>
    );
};"""

if wrong_ending in content:
    content = content.replace(wrong_ending, correct_ending)
else:
    # Tentar outra variação se a indentação estiver diferente
    # Vamos usar regex para pegar os últimos caracteres
    import re
    content = re.sub(r'</div>\s*</div>\);\s*};$', '</div>\n    );\n};', content)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Sintaxe corrigida definitivamente!")
