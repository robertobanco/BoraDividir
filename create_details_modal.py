import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Criar o EventDetailsModal
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

# Inserir antes do export
content = content.replace(
    '\r\nexport const EventSelector: React.FC<EventSelectorProps> = ({ events, currentEventId, onSelectEvent, onAddEvent, onEditEvent, onDeleteEvent, onBack, theme, setTheme, onShowAlert }) => {',
    event_details_modal + '\r\nexport const EventSelector: React.FC<EventSelectorProps> = ({ events, currentEventId, onSelectEvent, onAddEvent, onEditEvent, onDeleteEvent, onBack, theme, setTheme, onShowAlert }) => {'
)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ EventDetailsModal criado com sucesso!")
