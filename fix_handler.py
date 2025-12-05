# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir a assinatura do handleSelectEventType
old_signature = "const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL') =>"
new_signature = "const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') =>"

content = content.replace(old_signature, new_signature)

# Substituir a lógica para incluir DOMESTIC_EXPENSES
old_logic = """if (type === 'SHARED_EXPENSES') {
            onAddEvent(pendingEvent.name, pendingEvent.date, type);
            cleanup();
        } else {
            setShowBillSetupModal(true);
        }"""

new_logic = """if (type === 'SHARED_EXPENSES' || type === 'DOMESTIC_EXPENSES') {
            onAddEvent(pendingEvent.name, pendingEvent.date, type);
            cleanup();
        } else {
            setShowBillSetupModal(true);
        }"""

content = content.replace(old_logic, new_logic)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ handleSelectEventType atualizado para suportar DOMESTIC_EXPENSES!")
