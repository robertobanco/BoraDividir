# REVERT: Cores de volta para Roxo (Purple) onde apropriado

import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Vamos fazer substituições cirúrgicas para não afetar o que deve ser azul (Mensal, Editar)

# 1. Gradients (Botões principais, Header, Settlement)
# from-pink-600 to-blue-600 -> to-purple-600
content = content.replace('to-blue-600', 'to-purple-600')
content = content.replace('to-blue-700', 'to-purple-700') # Hover
content = content.replace('to-blue-800', 'to-purple-800') # Dark mode gradients?
content = content.replace('to-blue-900', 'to-purple-900') # Settlement card

# 2. Texto do Participante 2 (Settings, Modal)
# text-blue-600 dark:text-blue-400 -> text-purple-600 dark:text-purple-400
content = content.replace('text-blue-600 dark:text-blue-400', 'text-purple-600 dark:text-purple-400')

# 3. Botões de Recorrência (Active state)
# bg-blue-600 text-white border-blue-600 -> bg-purple-600 ...
# O padrão é: frequency === opt.value ? 'bg-blue-600 text-white border-blue-600
content = content.replace("frequency === opt.value\n                                                    ? 'bg-blue-600 text-white border-blue-600", 
                          "frequency === opt.value\n                                                    ? 'bg-purple-600 text-white border-purple-600")
# Tentar versão em uma linha caso a formatação tenha mudado
content = content.replace("frequency === opt.value ? 'bg-blue-600 text-white border-blue-600", 
                          "frequency === opt.value ? 'bg-purple-600 text-white border-purple-600")

# 4. Sombras
content = content.replace('shadow-blue-500', 'shadow-purple-500')

# 5. Tag Parcelada (bg-blue-500/10 text-blue-400)
# Precisamos diferenciar da tag Mensal (que é igual).
# Vamos usar o contexto: expense.frequency === 'PARCELADA'
# O bloco é:
# {expense.frequency === 'PARCELADA' && expense.installmentsCount && (
#     <span className="px-1.5 py-0.5 bg-blue-500/10 text-blue-400 ...">

# Vamos usar regex para pegar esse bloco específico
parcelada_pattern = r"(expense\.frequency === 'PARCELADA'[\s\S]+?bg-)blue(-500/10 text-)blue(-400)"
# Substituir por purple
content = re.sub(parcelada_pattern, r"\1purple\2purple\3", content)

# 6. Borda do Settlement Card (border-blue-700/50)
# Era border-pink-700/50 ou border-purple?
# No original era border-pink-700/50.
# Se eu mudei purple pra blue, talvez não tenha afetado pink.
# Mas vamos checar se tem border-blue-700 que deveria ser purple.
# O settlement card usa from-pink-900 to-purple-900.
# A borda era border-pink.
# Vamos deixar quieto se não tiver certeza, mas gradients já foram corrigidos.

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Cores revertidas para Roxo (Purple) com sucesso!")
