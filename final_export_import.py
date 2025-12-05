# Script FINAL para adicionar Export/Import ao EventSelector

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Atualizar interface para incluir DOMESTIC_EXPENSES e props de export/import
old_interface = """interface EventSelectorProps {
  events: BillSplitEvent[];
  currentEventId: string | null;
  onSelectEvent: (id: string) => void;
  onAddEvent: (name: string, date: string, type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL', options?: { billSubtotal?: number; tip?: { value: number; type: 'PERCENT' | 'FIXED' }; tax?: number; }) => void;
  onEditEvent: (id: string, name: string, date: string) => void;
  onDeleteEvent: (id: string) => void;
  onBack: () => void;
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  onShowAlert: (title: string, message: string) => void;
}"""

new_interface = """interface EventSelectorProps {
  events: BillSplitEvent[];
  currentEventId: string | null;
  onSelectEvent: (id: string) => void;
  onAddEvent: (name: string, date: string, type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES', options?: { billSubtotal?: number; tip?: { value: number; type: 'PERCENT' | 'FIXED' }; tax?: number; }) => void;
  onEditEvent: (id: string, name: string, date: string) => void;
  onDeleteEvent: (id: string) => void;
  onBack: () => void;
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  onShowAlert: (title: string, message: string) => void;
  onExportData?: () => void;
  onImportData?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  fileInputRef?: React.RefObject<HTMLInputElement>;
}"""

content = content.replace(old_interface, new_interface)
print("✅ Interface atualizada")

# 2. Atualizar assinatura do componente
old_signature = "export const EventSelector: React.FC<EventSelectorProps> = ({ events, currentEventId, onSelectEvent, onAddEvent, onEditEvent, onDeleteEvent, onBack, theme, setTheme, onShowAlert }) => {"

new_signature = "export const EventSelector: React.FC<EventSelectorProps> = ({ events, currentEventId, onSelectEvent, onAddEvent, onEditEvent, onDeleteEvent, onBack, theme, setTheme, onShowAlert, onExportData, onImportData, fileInputRef }) => {"

content = content.replace(old_signature, new_signature)
print("✅ Assinatura atualizada")

# 3. Adicionar botões no header (antes do botão de tema)
old_header = """                    <button
                        onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
                        className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                        aria-label="Alternar tema"
                    >
                        {theme === 'light' ? <MoonIcon className="h-5 w-5" /> : <SunIcon className="h-5 w-5" />}
                    </button>"""

new_header = """                    {onExportData && events.length > 0 && (
                        <button
                            onClick={onExportData}
                            className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                            title="Exportar dados"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                        </button>
                    )}
                    {onImportData && fileInputRef && (
                        <>
                            <button
                                onClick={() => fileInputRef.current?.click()}
                                className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                                title="Importar dados"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L9 8m4-4v12" />
                                </svg>
                            </button>
                            <input
                                ref={fileInputRef}
                                type="file"
                                accept=".json"
                                onChange={onImportData}
                                className="hidden"
                            />
                        </>
                    )}
                    <button
                        onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
                        className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                        aria-label="Alternar tema"
                    >
                        {theme === 'light' ? <MoonIcon className="h-5 w-5" /> : <SunIcon className="h-5 w-5" />}
                    </button>"""

content = content.replace(old_header, new_header)
print("✅ Botões adicionados")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ EXPORT/IMPORT COMPLETO NO EVENTSELECTOR!")
