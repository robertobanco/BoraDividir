# Script para adicionar funcionalidade de Exportar/Importar dados

# Ler o arquivo App.tsx
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar funções de exportar/importar antes do return
# Procurar onde adicionar (antes do return final do componente App)
insert_point = "return ("

export_import_functions = """  // Exportar/Importar dados
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
    // Limpar o input para permitir importar o mesmo arquivo novamente
    event.target.value = '';
  };

  const fileInputRef = useRef<HTMLInputElement>(null);

  """

# Inserir as funções antes do return
content = content.replace("  return (", export_import_functions + "return (")

# 2. Adicionar import do useRef no topo
old_import = "import React, { useState, useCallback, useMemo, useEffect } from 'react';"
new_import = "import React, { useState, useCallback, useMemo, useEffect, useRef } from 'react';"
content = content.replace(old_import, new_import)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Funções de Exportar/Importar adicionadas ao App.tsx!")
print("Agora vou adicionar os botões na interface...")
