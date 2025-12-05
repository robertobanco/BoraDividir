# CORREÇÃO: Remover funções duplicadas

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remover handleExportExcel duplicado (o que está dentro do map/return, ou próximo dele)
# Vamos identificar pelo contexto. O duplicado está logo antes do "return (" do componente?
# Não, o duplicado foi inserido na linha 251.
# O correto está no topo (linha 100+ no arquivo anterior, mas agora deve estar no topo também se o script anterior funcionou em parte).

# Vamos verificar quantas vezes aparece "const handleExportExcel ="
count = content.count("const handleExportExcel =")
print(f"Encontradas {count} declarações de handleExportExcel")

if count > 1:
    # Vamos remover a segunda ocorrência (a que está mais abaixo).
    # A primeira deve ser a que inserimos no topo (perto de monthlyBalance).
    
    parts = content.split("const handleExportExcel =")
    
    # parts[0] = código antes da primeira declaração
    # parts[1] = corpo da primeira declaração + código entre
    # parts[2] = corpo da segunda declaração + resto
    
    # Vamos reconstruir mantendo apenas a primeira.
    # Mas precisamos saber onde termina a segunda declaração para cortar corretamente.
    
    # A segunda declaração termina com "setShowExportModal(false);\n    };"
    
    second_decl_start = content.rfind("const handleExportExcel =")
    second_decl_end = content.find("setShowExportModal(false);\n    };", second_decl_start)
    
    if second_decl_end != -1:
        # Remover do start até o end + tamanho do end marker
        end_marker_len = len("setShowExportModal(false);\n    };")
        content = content[:second_decl_start] + content[second_decl_end + end_marker_len:]
        print("Removida declaração duplicada de handleExportExcel")

# 2. Remover getCurrentInstallment duplicado (dentro do map)
# O correto está no topo. O duplicado está dentro do map.
count_install = content.count("const getCurrentInstallment =")
print(f"Encontradas {count_install} declarações de getCurrentInstallment")

if count_install > 1:
    # Remover a última ocorrência
    last_install_start = content.rfind("const getCurrentInstallment =")
    # Achar o fim da função. Termina com "return monthsDiff + 1;\n                            };" ou algo assim.
    # Vamos procurar o fechamento "};" mais próximo.
    
    last_install_end = content.find("};", last_install_start)
    if last_install_end != -1:
        # Remover
        content = content[:last_install_start] + content[last_install_end + 2:]
        print("Removida declaração duplicada de getCurrentInstallment")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Limpeza de duplicatas concluída!")
