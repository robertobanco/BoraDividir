# Adicionar APENAS Export/Import, sem mexer em nada mais

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar useRef ao import
if ", useRef" not in content:
    content = content.replace(
        "import React, { useState, useCallback, useMemo, useEffect } from 'react';",
        "import React, { useState, useCallback, useMemo, useEffect, useRef } from 'react';"
    )
    print("✅ useRef adicionado ao import")

# 2. Adicionar funções ANTES do "return ("
# Procurar um ponto seguro - logo antes do return
insert_before = "  return (\n    <>\n      <EventSelector"

export_import_code = """  // Export/Import functionality
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
          showAlert('Erro', 'Arquivo inválido.');
        }
      } catch (error) {
        showAlert('Erro', 'Não foi possível ler o arquivo.');
      }
    };
    reader.readAsText(file);
    event.target.value = '';
  };

  """

if insert_before in content:
    content = content.replace(insert_before, export_import_code + insert_before)
    print("✅ Funções de export/import adicionadas")
else:
    print("❌ Ponto de inserção não encontrado")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ App.tsx atualizado com export/import!")
