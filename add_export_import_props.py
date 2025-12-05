# Adicionar botões de Exportar/Importar na interface do EventSelector

# Ler EventSelector.tsx
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar props para as funções de export/import
old_props = """interface EventSelectorProps {
  events: BillSplitEvent[];
  currentEventId: string | null;
  onSelectEvent: (id: string) => void;
  onAddEvent: (name: string, date: string, type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES', options?: { billSubtotal?: number; tip?: { value: number; type: 'PERCENT' | 'FIXED' }; tax?: number }) => void;
  onEditEvent: (id: string, name: string, date: string) => void;
  onDeleteEvent: (id: string) => void;
  onBack: () => void;
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  onShowAlert: (title: string, message: string) => void;
}"""

new_props = """interface EventSelectorProps {
  events: BillSplitEvent[];
  currentEventId: string | null;
  onSelectEvent: (id: string) => void;
  onAddEvent: (name: string, date: string, type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES', options?: { billSubtotal?: number; tip?: { value: number; type: 'PERCENT' | 'FIXED' }; tax?: number }) => void;
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

content = content.replace(old_props, new_props)

# Adicionar os parâmetros na assinatura do componente
old_signature = "export const EventSelector: React.FC<EventSelectorProps> = ({ events, currentEventId, onSelectEvent, onAddEvent, onEditEvent, onDeleteEvent, onBack, theme, setTheme, onShowAlert }) => {"

new_signature = "export const EventSelector: React.FC<EventSelectorProps> = ({ events, currentEventId, onSelectEvent, onAddEvent, onEditEvent, onDeleteEvent, onBack, theme, setTheme, onShowAlert, onExportData, onImportData, fileInputRef }) => {"

content = content.replace(old_signature, new_signature)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Props de export/import adicionadas ao EventSelector!")
