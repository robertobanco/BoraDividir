import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar o NameDateModal antes do EventTypeModal
insert_pos = content.find("const EventTypeModal:")
if insert_pos != -1:
    name_modal = """const NameDateModal: React.FC<{ 
    eventType: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES',
    onConfirm: (e: React.FormEvent) => void, 
    onCancel: () => void,
    newEventName: string,
    setNewEventName: (name: string) => void,
    newEventDate: string,
    setNewEventDate: (date: string) => void
}> = ({ eventType, onConfirm, onCancel, newEventName, setNewEventName, newEventDate, setNewEventDate }) => {
    const typeLabels = {
        'SHARED_EXPENSES': 'Despesas Compartilhadas',
        'ITEMIZED_BILL': 'Conta Detalhada',
        'DOMESTIC_EXPENSES': 'Contas Domésticas'
    };
    
    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
            <div className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-md animate-scale-in">
                <h3 className="text-xl font-bold mb-2 text-slate-900 dark:text-white">Novo Evento</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">
                    Tipo: <span className="font-semibold text-violet-600 dark:text-violet-400">{typeLabels[eventType]}</span>
                </p>
                <form onSubmit={onConfirm} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                            Nome do Evento
                        </label>
                        <input
                            type="text"
                            value={newEventName}
                            onChange={(e) => setNewEventName(e.target.value)}
                            placeholder="Ex: Pizza de Sexta, Viagem SP, Contas de Janeiro"
                            className="w-full px-4 py-3 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white placeholder-slate-400 focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
                            autoFocus
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                            Data
                        </label>
                        <input
                            type="date"
                            value={newEventDate}
                            onChange={(e) => setNewEventDate(e.target.value)}
                            className="w-full px-4 py-3 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
                        />
                    </div>
                    <div className="flex gap-3 mt-6">
                        <button
                            type="button"
                            onClick={onCancel}
                            className="flex-1 px-4 py-3 bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg font-medium hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            className="flex-1 px-4 py-3 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 text-white rounded-lg font-semibold shadow-md shadow-violet-500/30 transition-all hover:scale-105 active:scale-95"
                        >
                            Criar Evento
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

"""
    content = content[:insert_pos] + name_modal + content[insert_pos:]

# Adicionar a renderização do NameDateModal
old_modals = """            {showTypeModal && <EventTypeModal onSelect={handleSelectEventType} onCancel={cleanup} />}
            {showBillSetupModal && <BillSetupModal onConfirm={handleConfirmBillSetup} onCancel={cleanup} />}"""

new_modals = """            {showTypeModal && <EventTypeModal onSelect={handleSelectEventType} onCancel={cleanup} />}
            {showNameModal && selectedType && (
                <NameDateModal 
                    eventType={selectedType}
                    onConfirm={handleConfirmName}
                    onCancel={cleanup}
                    newEventName={newEventName}
                    setNewEventName={setNewEventName}
                    newEventDate={newEventDate}
                    setNewEventDate={setNewEventDate}
                />
            )}
            {showBillSetupModal && <BillSetupModal onConfirm={handleConfirmBillSetup} onCancel={cleanup} />}"""

content = content.replace(old_modals, new_modals)

# Salvar o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modal de nome/data adicionado!")
