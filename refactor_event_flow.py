import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar opção DOMESTIC_EXPENSES ao EventTypeModal
content = content.replace(
    "const EventTypeModal: React.FC<{ onSelect: (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL') => void, onCancel: () => void }> = ({ onSelect, onCancel }) => {",
    "const EventTypeModal: React.FC<{ onSelect: (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => void, onCancel: () => void }> = ({ onSelect, onCancel }) => {"
)

# 2. Mudar título do modal
content = content.replace(
    '<h3 className="text-xl font-bold mb-6 text-slate-900 dark:text-white text-center">Como vamos dividir?</h3>',
    '<h3 className="text-xl font-bold mb-6 text-slate-900 dark:text-white text-center">Que tipo de conta vamos dividir?</h3>'
)

# 3. Adicionar botão de Contas Domésticas no modal (antes do </div> que fecha os botões)
domestic_button = '''                    <button onClick={() => onSelect('DOMESTIC_EXPENSES')} className="group w-full text-left p-5 border border-slate-200 dark:border-slate-700 rounded-xl hover:bg-violet-50 dark:hover:bg-violet-900/20 hover:border-violet-300 dark:hover:border-violet-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-violet-500">
                        <div className="flex items-center gap-3 mb-1">
                             <div className="p-2 bg-pink-100 dark:bg-pink-900/30 text-pink-600 dark:text-pink-400 rounded-lg group-hover:scale-110 transition-transform">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                                </svg>
                            </div>
                            <p className="font-bold text-slate-800 dark:text-slate-100 text-lg group-hover:text-violet-700 dark:group-hover:text-violet-300">Contas Domésticas</p>
                        </div>
                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para casais. Gerencie despesas mensais da casa com divisão personalizada.</p>
                    </button>
                </div>'''

content = content.replace(
    '                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para viagens ou casa. Registre quem pagou o quê e acerte as diferenças.</p>\r\n                    </button>\r\n                </div>',
    '                        <p className="text-sm text-slate-500 dark:text-slate-400 pl-[52px]">Ideal para viagens. Registre quem pagou o quê e acerte as diferenças.</p>\r\n                    </button>\r\n' + domestic_button
)

# 4. Adicionar novo modal EventDetailsModal antes do export
event_details_modal = '''
const EventDetailsModal: React.FC<{ eventType: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES', onConfirm: (name: string, date: string) => void, onCancel: () => void }> = ({ eventType, onConfirm, onCancel }) => {
    const [name, setName] = useState('');
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);

    const getTypeLabel = () => {
        if (eventType === 'ITEMIZED_BILL') return 'Conta Detalhada';
        if (eventType === 'SHARED_EXPENSES') return 'Despesas Compartilhadas';
        return 'Contas Domésticas';
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (name.trim() && date) {
            onConfirm(name.trim(), date);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
            <div className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-md animate-scale-in">
                <h3 className="text-xl font-bold mb-2 text-slate-900 dark:text-white text-center">{getTypeLabel()}</h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 text-center mb-6">Preencha os detalhes do evento</p>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Nome do Evento</label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Ex: Pizza de Sexta, Viagem SP, Contas de Março"
                            className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
                            required
                            autoFocus
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Data</label>
                        <input
                            type="date"
                            value={date}
                            onChange={(e) => setDate(e.target.value)}
                            className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-violet-500 focus:border-violet-500 [color-scheme:dark]"
                            required
                        />
                    </div>
                    <div className="flex gap-3 mt-6 pt-4 border-t border-slate-200 dark:border-slate-700">
                        <button
                            type="button"
                            onClick={onCancel}
                            className="flex-1 px-4 py-3 bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg font-semibold hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors"
                        >
                            Voltar
                        </button>
                        <button
                            type="submit"
                            className="flex-1 px-4 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 text-white rounded-lg font-bold shadow-lg shadow-violet-500/30 transition-all hover:scale-105 active:scale-95"
                        >
                            Criar Evento
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

'''

content = content.replace(
    '\r\nexport const EventSelector: React.FC<EventSelectorProps> = ({ events, currentEventId, onSelectEvent, onAddEvent, onEditEvent, onDeleteEvent, onBack, theme, setTheme, onShowAlert }) => {',
    event_details_modal + '\r\nexport const EventSelector: React.FC<EventSelectorProps> = ({ events, currentEventId, onSelectEvent, onAddEvent, onEditEvent, onDeleteEvent, onBack, theme, setTheme, onShowAlert }) => {'
)

# 5. Atualizar estados do componente
old_states = '''  const [newEventName, setNewEventName] = useState('');
  const [newEventDate, setNewEventDate] = useState(new Date().toISOString().split('T')[0]);
  const [pendingEvent, setPendingEvent] = useState<{name: string, date: string} | null>(null);
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [showBillSetupModal, setShowBillSetupModal] = useState(false);'''

new_states = '''  const [selectedEventType, setSelectedEventType] = useState<'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES' | null>(null);
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [showBillSetupModal, setShowBillSetupModal] = useState(false);
  const [pendingEventDetails, setPendingEventDetails] = useState<{name: string, date: string} | null>(null);'''

content = content.replace(old_states, new_states)

# 6. Substituir handleInitiateAddEvent por handleStartNewEvent
old_handler = '''  const handleInitiateAddEvent = (e: React.FormEvent) => {
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
  };'''

new_handler = '''  const handleStartNewEvent = () => {
    setShowTypeModal(true);
  };'''

content = content.replace(old_handler, new_handler)

# 7. Atualizar handleSelectEventType
old_select = '''  const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL') => {
    if (!pendingEvent) return;
    setShowTypeModal(false);
    if (type === 'SHARED_EXPENSES') {
        onAddEvent(pendingEvent.name, pendingEvent.date, type);
        cleanup();
    } else {
        setShowBillSetupModal(true);
    }
  }'''

new_select = '''  const handleSelectEventType = (type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES') => {
    setSelectedEventType(type);
    setShowTypeModal(false);
    setShowDetailsModal(true);
  };

  const handleConfirmEventDetails = (name: string, date: string) => {
    if (!selectedEventType) return;
    setPendingEventDetails({ name, date });
    setShowDetailsModal(false);
    
    if (selectedEventType === 'ITEMIZED_BILL') {
        setShowBillSetupModal(true);
    } else {
        onAddEvent(name, date, selectedEventType);
        cleanup();
    }
  };'''

content = content.replace(old_select, new_select)

# 8. Atualizar handleConfirmBillSetup
content = content.replace(
    'if (!pendingEvent) return;\r\n    onAddEvent(pendingEvent.name, pendingEvent.date, \'ITEMIZED_BILL\', details);',
    'if (!pendingEventDetails) return;\r\n    onAddEvent(pendingEventDetails.name, pendingEventDetails.date, \'ITEMIZED_BILL\', details);'
)

# 9. Atualizar cleanup
old_cleanup = '''  const cleanup = () => {
    setNewEventName('');
    setNewEventDate(new Date().toISOString().split('T')[0]);
    setPendingEvent(null);
    setShowTypeModal(false);
    setShowBillSetupModal(false);
  }'''

new_cleanup = '''  const cleanup = () => {
    setSelectedEventType(null);
    setPendingEventDetails(null);
    setShowTypeModal(false);
    setShowDetailsModal(false);
    setShowBillSetupModal(false);
  };'''

content = content.replace(old_cleanup, new_cleanup)

# 10. Substituir o formulário por um botão grande
# Encontrar e substituir todo o form
form_pattern = r'<form onSubmit=\{handleInitiateAddEvent\}.*?</form>'
new_button = '''<button
                        onClick={handleStartNewEvent}
                        className="px-8 py-4 rounded-full bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 text-white text-lg font-bold shadow-lg shadow-violet-500/30 transition-all hover:scale-105 active:scale-95 flex items-center gap-3 mx-auto"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                        </svg>
                        Criar Novo Evento
                    </button>'''

content = re.sub(form_pattern, new_button, content, flags=re.DOTALL)

# 11. Atualizar os modais no final
old_modals = '''    {showTypeModal && <EventTypeModal onSelect={handleSelectEventType} onCancel={cleanup} />}
    {showBillSetupModal && <BillSetupModal onConfirm={handleConfirmBillSetup} onCancel={cleanup} />}'''

new_modals = '''    {showTypeModal && <EventTypeModal onSelect={handleSelectEventType} onCancel={cleanup} />}
    {showDetailsModal && selectedEventType && <EventDetailsModal eventType={selectedEventType} onConfirm={handleConfirmEventDetails} onCancel={() => { setShowDetailsModal(false); setShowTypeModal(true); }} />}
    {showBillSetupModal && <BillSetupModal onConfirm={handleConfirmBillSetup} onCancel={cleanup} />}'''

content = content.replace(old_modals, new_modals)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ EventSelector.tsx atualizado com sucesso!")
print("📋 Mudanças aplicadas:")
print("  - Adicionada opção 'Contas Domésticas' no modal de tipo")
print("  - Criado novo modal EventDetailsModal para nome e data")
print("  - Substituído formulário por botão 'Criar Novo Evento'")
print("  - Fluxo invertido: tipo → nome/data")
