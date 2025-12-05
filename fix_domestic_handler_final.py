# CORREÇÃO FINAL DO MODO DOMÉSTICO - handleSelectEventType

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Corrigir o handleSelectEventType
old_handler = """  const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => {
    if (!pendingEvent) return;
    setShowTypeModal(false);
    if (type === 'SHARED_EXPENSES') {
        onAddEvent(pendingEvent.name, pendingEvent.date, type);
        cleanup();
    } else {
        setShowBillSetupModal(true);
    }
  }"""

new_handler = """  const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => {
    if (!pendingEvent) return;
    setShowTypeModal(false);
    if (type === 'SHARED_EXPENSES' || type === 'DOMESTIC_EXPENSES') {
        // SHARED_EXPENSES e DOMESTIC_EXPENSES não precisam de setup adicional
        onAddEvent(pendingEvent.name, pendingEvent.date, type);
        cleanup();
    } else {
        // ITEMIZED_BILL precisa do modal de setup (subtotal, taxa, etc)
        setShowBillSetupModal(true);
    }
  }"""

content = content.replace(old_handler, new_handler)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CORREÇÃO FINAL APLICADA!")
print("✅ Agora DOMESTIC_EXPENSES não abre mais o modal de Conta Detalhada!")
