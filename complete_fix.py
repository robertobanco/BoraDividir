import re

# Ler o arquivo backup original
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx.backup', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar selectedType e showNameModal ao estado
old_state = """  const [newEventName, setNewEventName] = useState('');
  const [newEventDate, setNewEventDate] = useState(new Date().toISOString().split('T')[0]);
  const [pendingEvent, setPendingEvent] = useState<{ name: string, date: string } | null>(null);
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [showBillSetupModal, setShowBillSetupModal] = useState(false);"""

new_state = """  const [newEventName, setNewEventName] = useState('');
  const [newEventDate, setNewEventDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedType, setSelectedType] = useState<'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES' | null>(null);
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [showNameModal, setShowNameModal] = useState(false);
  const [showBillSetupModal, setShowBillSetupModal] = useState(false);"""

content = content.replace(old_state, new_state)

# 2. Simplificar handleInitiateAddEvent
old_initiate = """  const handleInitiateAddEvent = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEventName.trim()) {
        onShowAlert("Atenção", "Por favor, dê um nome ao seu evento antes de continuar.");
        return;
    }
    if (!newEventDate) {
        onShowAlert("Atenção", "Por favor, selecione a data do evento.");
        return;
    }
    setPendingEvent({ name: newEventName.trim(), date: newEventDate });
    setShowTypeModal(true);
  };"""

new_initiate = """  const handleInitiateAddEvent = () => {
    setShowTypeModal(true);
  };"""

content = content.replace(old_initiate, new_initiate)

# 3. Atualizar handleSelectEventType
old_select = """  const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => {
    if (!pendingEvent) return;
    setShowTypeModal(false);
    if (type === 'SHARED_EXPENSES' || type === 'DOMESTIC_EXPENSES') {
        onAddEvent(pendingEvent.name, pendingEvent.date, type);
        cleanup();
    } else {
        setShowBillSetupModal(true);
    }
  }"""

new_select = """  const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => {
    setSelectedType(type);
    setShowTypeModal(false);
    if (type === 'ITEMIZED_BILL') {
        setShowBillSetupModal(true);
    } else {
        setShowNameModal(true);
    }
  }"""

content = content.replace(old_select, new_select)

# 4. Adicionar handleConfirmName ANTES de handleConfirmBillSetup
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

# 5. Atualizar handleConfirmBillSetup
old_bill = """  const handleConfirmBillSetup = (details: { billSubtotal: number; tip: { value: number; type: 'PERCENT' | 'FIXED'}; tax: number; }) => {
    if (!pendingEvent) return;
    onAddEvent(pendingEvent.name, pendingEvent.date, 'ITEMIZED_BILL', details);
    cleanup();
  }"""

new_bill = """  const handleConfirmBillSetup = (details: { billSubtotal: number; tip: { value: number; type: 'PERCENT' | 'FIXED'}; tax: number; }) => {
    setShowBillSetupModal(false);
    setShowNameModal(true);
  }"""

content = content.replace(old_bill, new_bill)

# 6. Atualizar cleanup
old_cleanup = """  const cleanup = () => {
    setNewEventName('');
    setNewEventDate(new Date().toISOString().split('T')[0]);
    setPendingEvent(null);
    setShowTypeModal(false);
    setShowBillSetupModal(false);
  }"""

new_cleanup = """  const cleanup = () => {
    setNewEventName('');
    setNewEventDate(new Date().toISOString().split('T')[0]);
    setSelectedType(null);
    setShowTypeModal(false);
    setShowNameModal(false);
    setShowBillSetupModal(false);
  }"""

content = content.replace(old_cleanup, new_cleanup)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("EventSelector.tsx completamente corrigido!")
