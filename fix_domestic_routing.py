import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Corrigir a assinatura do handleSelectEventType
content = content.replace(
    "const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL') =>",
    "const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') =>"
)

# Corrigir a lógica para incluir DOMESTIC_EXPENSES
old_logic = """    if (type === 'SHARED_EXPENSES') {
        onAddEvent(pendingEvent.name, pendingEvent.date, type);
        cleanup();
    } else {
        setShowBillSetupModal(true);
    }"""

new_logic = """    if (type === 'SHARED_EXPENSES' || type === 'DOMESTIC_EXPENSES') {
        onAddEvent(pendingEvent.name, pendingEvent.date, type);
        cleanup();
    } else {
        setShowBillSetupModal(true);
    }"""

content = content.replace(old_logic, new_logic)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("EventSelector.tsx corrigido - DOMESTIC_EXPENSES agora funciona!")
