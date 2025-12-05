# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar scroll após setShowSettlement(true)
old_calculate = """  setSettlements(newSettlements);
  setShowSettlement(true);
  // When calculating, we can optionally close the expenses section or leave it open.
  // If you want to auto-collapse expenses to show settlement better:
  // setActiveSection(null);
};"""

new_calculate = """  setSettlements(newSettlements);
  setShowSettlement(true);
  // Scroll suave para baixo para mostrar o resultado
  setTimeout(() => {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  }, 100);
  // When calculating, we can optionally close the expenses section or leave it open.
  // If you want to auto-collapse expenses to show settlement better:
  // setActiveSection(null);
};"""

content = content.replace(old_calculate, new_calculate)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Problema 2 (parte 2) corrigido: Scroll automático após 'Calcular Divisão'!")
