import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar e substituir o fluxo de criação de eventos
# Vamos modificar para mostrar o modal de tipo PRIMEIRO, depois pedir nome e data

# 1. Modificar o estado para incluir o tipo selecionado
old_state = """  const [newEventName, setNewEventName] = useState('');
  const [newEventDate, setNewEventDate] = useState(new Date().toISOString().split('T')[0]);
  const [pendingEvent, setPendingEvent] = useState<{name: string, date: string} | null>(null);
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [showBillSetupModal, setShowBillSetupModal] = useState(false);"""

new_state = """  const [newEventName, setNewEventName] = useState('');
  const [newEventDate, setNewEventDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedType, setSelectedType] = useState<'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES' | null>(null);
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [showNameModal, setShowNameModal] = useState(false);
  const [showBillSetupModal, setShowBillSetupModal] = useState(false);"""

content = content.replace(old_state, new_state)

# 2. Modificar handleInitiateAddEvent para mostrar o modal de tipo primeiro
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

# 3. Modificar handleSelectEventType para mostrar o modal de nome/data
old_select_type = """  const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => {
    if (!pendingEvent) return;
    setShowTypeModal(false);
    if (type === 'SHARED_EXPENSES' || type === 'DOMESTIC_EXPENSES') {
        onAddEvent(pendingEvent.name, pendingEvent.date, type);
        cleanup();
    } else {
        setShowBillSetupModal(true);
    }
  }"""

new_select_type = """  const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => {
    setSelectedType(type);
    setShowTypeModal(false);
    if (type === 'ITEMIZED_BILL') {
        setShowBillSetupModal(true);
    } else {
        setShowNameModal(true);
    }
  }"""

content = content.replace(old_select_type, new_select_type)

# 4. Adicionar handleConfirmName
insert_pos = content.find("  const handleConfirmBillSetup")
if insert_pos != -1:
    new_handler = """  const handleConfirmName = (e: React.FormEvent) => {
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
    content = content[:insert_pos] + new_handler + content[insert_pos:]

# 5. Modificar handleConfirmBillSetup
old_bill_setup = """  const handleConfirmBillSetup = (details: { billSubtotal: number; tip: { value: number; type: 'PERCENT' | 'FIXED'}; tax: number; }) => {
    if (!pendingEvent) return;
    onAddEvent(pendingEvent.name, pendingEvent.date, 'ITEMIZED_BILL', details);
    cleanup();
  }"""

new_bill_setup = """  const handleConfirmBillSetup = (details: { billSubtotal: number; tip: { value: number; type: 'PERCENT' | 'FIXED'}; tax: number; }) => {
    setShowBillSetupModal(false);
    setShowNameModal(true);
  }
  
  const handleConfirmNameAfterBillSetup = (e: React.FormEvent, billDetails: { billSubtotal: number; tip: { value: number; type: 'PERCENT' | 'FIXED'}; tax: number; }) => {
    e.preventDefault();
    if (!newEventName.trim()) {
        onShowAlert("Atenção", "Por favor, dê um nome ao seu evento.");
        return;
    }
    if (!newEventDate) {
        onShowAlert("Atenção", "Por favor, selecione a data do evento.");
        return;
    }
    
    onAddEvent(newEventName.trim(), newEventDate, 'ITEMIZED_BILL', billDetails);
    cleanup();
  }"""

content = content.replace(old_bill_setup, new_bill_setup)

# 6. Modificar cleanup
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

# 7. Modificar o formulário de criação para ser um botão simples
old_form = """                    <form onSubmit={handleInitiateAddEvent} className="flex flex-col sm:flex-row gap-3 max-w-xl mx-auto bg-white dark:bg-slate-800/50 p-2 rounded-xl sm:rounded-full shadow-lg ring-1 ring-slate-200 dark:ring-slate-700">
                        <input
                            type="text"
                            value={newEventName}
                            onChange={(e) => setNewEventName(e.target.value)}
                            placeholder="Nome do evento (ex: Pizza de Sexta)"
                            className="flex-grow px-4 py-3 bg-transparent border-none focus:ring-0 text-slate-900 dark:text-white placeholder-slate-400"
                        />
                         <div className="w-px bg-slate-200 dark:bg-slate-700 hidden sm:block"></div>
                         <input
                            type="date"
                            value={newEventDate}
                            onChange={(e) => setNewEventDate(e.target.value)}
                            className="px-4 py-3 bg-transparent border-none focus:ring-0 text-slate-600 dark:text-slate-300 w-full sm:w-auto"
                        />
                        <button
                            type="submit"
                            className="px-8 py-3 rounded-lg sm:rounded-full bg-violet-600 hover:bg-violet-700 text-white font-semibold shadow-md shadow-violet-500/30 transition-all hover:scale-105 active:scale-95"
                        >
                            Criar
                        </button>
                    </form>"""

new_form = """                    <button
                        onClick={handleInitiateAddEvent}
                        className="px-8 py-4 rounded-full bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 text-white font-bold shadow-lg shadow-violet-500/30 transition-all hover:scale-105 active:scale-95 text-lg"
                    >
                        + Criar Novo Evento
                    </button>"""

content = content.replace(old_form, new_form)

# Salvar o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("EventSelector.tsx atualizado - fluxo invertido!")
