# AJUSTE: Forçar nomes de participantes

import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar useEffect para checar nomes na inicialização
# Vamos adicionar logo após os estados iniciais.

check_names_effect = """
    // Forçar preenchimento de nomes se estiverem com o padrão
    React.useEffect(() => {
        if (userSettings.user1Name === 'Participante 1' || userSettings.user2Name === 'Participante 2') {
            setShowSettingsModal(true);
        }
    }, []); // Executa apenas na montagem
"""

# Inserir após a declaração dos estados
# Procurar por "const [installmentsCount, setInstallmentsCount] = useState('2');"
insert_point = "const [installmentsCount, setInstallmentsCount] = useState('2');"

if insert_point in content:
    content = content.replace(insert_point, insert_point + "\n" + check_names_effect)

# 2. Melhorar a validação no botão Salvar para também checar os nomes padrão
# O código atual é:
# if (!userSettings.user1Name.trim() || !userSettings.user2Name.trim()) {
#     alert("Por favor, preencha o nome dos dois participantes.");
#     return;
# }

old_validation = """                                    if (!userSettings.user1Name.trim() || !userSettings.user2Name.trim()) {
                                        alert("Por favor, preencha o nome dos dois participantes.");
                                        return;
                                    }"""

new_validation = """                                    if (!userSettings.user1Name.trim() || !userSettings.user2Name.trim()) {
                                        alert("Por favor, preencha o nome dos dois participantes.");
                                        return;
                                    }
                                    if (userSettings.user1Name === 'Participante 1' || userSettings.user2Name === 'Participante 2') {
                                        alert("Por favor, altere os nomes padrão para os nomes reais.");
                                        return;
                                    }"""

if old_validation in content:
    content = content.replace(old_validation, new_validation)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Validação de nomes reforçada!")
