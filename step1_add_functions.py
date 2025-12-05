# Script SUPER CUIDADOSO para adicionar Export/Import

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Primeiro, corrigir o useState do theme que está quebrado
# Remover o código que está dentro do useState
broken_theme = """  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const savedTheme = localStorage.getItem('theme');
    // Domestic Expenses Logic
  const updateDomesticExpenses = (expenses: DomesticExpense[]) => {
    if (!currentEvent || currentEvent.type !== 'DOMESTIC_EXPENSES') return;
    updateCurrentEvent(event => {
      if (event.type !== 'DOMESTIC_EXPENSES') return event;
      return { ...event, domesticExpenses: expenses };
    });
  };

  const updateDomesticSettings = (settings: UserSettings) => {
    if (!currentEvent || currentEvent.type !== 'DOMESTIC_EXPENSES') return;
    updateCurrentEvent(event => {
      if (event.type !== 'DOMESTIC_EXPENSES') return event;
      return { ...event, userSettings: settings };
    });
  };

  return ("""

fixed_theme = """  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const savedTheme = localStorage.getItem('theme');
    return (savedTheme === 'dark' || savedTheme === 'light') ? savedTheme : 'light';
  });"""

content = content.replace(broken_theme, fixed_theme)

# 2. Adicionar import do useRef
old_import = "import React, { useState, useCallback, useMemo, useEffect } from 'react';"
new_import = "import React, { useState, useCallback, useMemo, useEffect, useRef } from 'react';"
content = content.replace(old_import, new_import)

# 3. Adicionar as funções de Domestic Expenses e Export/Import ANTES do return
# Procurar onde está o "// Toggle Helpers" que é um bom ponto de referência
insert_point = "  // Toggle Helpers"

functions_to_add = """  // Domestic Expenses Logic
  const updateDomesticExpenses = (expenses: DomesticExpense[]) => {
    if (!currentEvent || currentEvent.type !== 'DOMESTIC_EXPENSES') return;
    updateCurrentEvent(event => {
      if (event.type !== 'DOMESTIC_EXPENSES') return event;
      return { ...event, domesticExpenses: expenses };
    });
  };

  const updateDomesticSettings = (settings: UserSettings) => {
    if (!currentEvent || currentEvent.type !== 'DOMESTIC_EXPENSES') return;
    updateCurrentEvent(event => {
      if (event.type !== 'DOMESTIC_EXPENSES') return event;
      return { ...event, userSettings: settings };
    });
  };

  // Export/Import Data
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleExportData = () => {
    const dataStr = JSON.stringify(events, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `bora-dividir-backup-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
    showAlert('Sucesso', 'Dados exportados com sucesso!');
  };

  const handleImportData = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const importedEvents = JSON.parse(e.target?.result as string);
        if (Array.isArray(importedEvents)) {
          setEvents(importedEvents);
          showAlert('Sucesso', `${importedEvents.length} evento(s) importado(s) com sucesso!`);
        } else {
          showAlert('Erro', 'Arquivo inválido. Certifique-se de que é um backup válido.');
        }
      } catch (error) {
        showAlert('Erro', 'Não foi possível ler o arquivo. Verifique se é um backup válido.');
      }
    };
    reader.readAsText(file);
    event.target.value = '';
  };

  """

content = content.replace(insert_point, functions_to_add + insert_point)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ PASSO 1 COMPLETO: Funções adicionadas ao App.tsx")
