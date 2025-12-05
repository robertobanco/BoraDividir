# Corrigir a posição das funções de export/import no App.tsx

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remover as funções que foram inseridas no lugar errado
# Procurar e remover o bloco que está dentro do useState
wrong_position = """    const savedTheme = localStorage.getItem('theme');
    // Exportar/Importar dados
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

  return ("""

correct_position = """    const savedTheme = localStorage.getItem('theme');
    return (savedTheme === 'dark' || savedTheme === 'light') ? savedTheme : 'light';
  });"""

# Substituir
content = content.replace(wrong_position, correct_position)

# Agora adicionar as funções no lugar correto (antes do return final do App)
# Procurar onde adicionar (logo antes do "return (")
# Vou procurar por uma linha característica que vem antes do return
insert_before = "  return (\n    <>\n      <EventSelector"

functions_block = """  // Ref para input de arquivo
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Exportar/Importar dados
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

  """

content = content.replace(insert_before, functions_block + insert_before)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Funções de export/import movidas para o lugar correto!")
print("✅ Erro de Hooks corrigido!")
