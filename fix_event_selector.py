import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Corrigir o tipo do EventTypeModal
old_type_modal_sig = "const EventTypeModal: React.FC<{ onSelect: (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL') => void, onCancel: () => void }>"
new_type_modal_sig = "const EventTypeModal: React.FC<{ onSelect: (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => void, onCancel: () => void }>"
content = content.replace(old_type_modal_sig, new_type_modal_sig)

# Adicionar handleConfirmName se não existir
if "const handleConfirmName" not in content:
    # Encontrar onde adicionar (antes de handleConfirmBillSetup)
    insert_pos = content.find("  const handleConfirmBillSetup")
    if insert_pos != -1:
        handler = """  const handleConfirmName = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEventName.trim()) {
        onShowAlert("Atenção", "Por favor, dê um nome ao seu evento.");
        return;
    }
    if (!newEventDate) {
        onShowAlert("Atenção", "Por favor, selecione a data do evento.");
        return;
    }
    if (!selectedType) return;
    
    onAddEvent(newEventName.trim(), newEventDate, selectedType);
    cleanup();
  };

  """
        content = content[:insert_pos] + handler + content[insert_pos:]

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("EventSelector.tsx corrigido!")
