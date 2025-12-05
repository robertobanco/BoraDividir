# CORREÇÃO: Inverter lógica do slider de responsabilidade

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir o input range
old_input = """<input type="range" min="0" max="100" value={ownershipPercentage} onChange={(e) => setOwnershipPercentage(parseInt(e.target.value))} className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-pink-600" />"""

new_input = """<input type="range" min="0" max="100" value={100 - ownershipPercentage} onChange={(e) => setOwnershipPercentage(100 - parseInt(e.target.value))} className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-pink-600" />"""

content = content.replace(old_input, new_input)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Lógica do slider invertida com sucesso!")
