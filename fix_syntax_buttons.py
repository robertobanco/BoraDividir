# CORREÇÃO: Adicionar ); faltante

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# O problema está aqui:
# 514:                                 </div>
# 515:                         })}

# Deveria ser:
# 514:                                 </div>
# 515:                             );
# 516:                         })}

# Vamos procurar o padrão errado
wrong_pattern = """                                </div>
                        })}"""

correct_pattern = """                                </div>
                            );
                        })}"""

if wrong_pattern in content:
    content = content.replace(wrong_pattern, correct_pattern)
else:
    # Tentar com regex para flexibilidade de espaços
    import re
    content = re.sub(r'</div>\s*\}\)\}', '</div>\n                            );\n                        })}', content)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Sintaxe corrigida (adicionado ); faltante)!")
