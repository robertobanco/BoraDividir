# CORREÇÃO DEFINITIVA - addEvent para suportar DOMESTIC_EXPENSES

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir a função addEvent completa
old_add_event = """// Event Management
const addEvent = (name: string, date: string, type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL', options: { billSubtotal?: number; tip?: { value: number; type: 'PERCENT' | 'FIXED'}; tax?: number } = {}) => {
  const baseEvent = {
    id: crypto.randomUUID(),
    name,
    date,
    participants: [],
    createdAt: new Date().toISOString(),
  };

  let newEvent: BillSplitEvent;
  if (type === 'SHARED_EXPENSES') {
    newEvent = { ...baseEvent, type, expenses: [] };
  } else {
    newEvent = { 
        ...baseEvent, 
        type, 
        items: [], 
        tip: options.tip || { value: 0, type: 'PERCENT' }, 
        tax: options.tax || 0, 
        billSubtotal: options.billSubtotal || 0,
        actualPayments: [],
    };
  }

  setEvents(prev => [...prev, newEvent]);
  setCurrentEventId(newEvent.id);
  setActiveSection('participants'); // Reset accordion to start
};"""

new_add_event = """// Event Management
const addEvent = (name: string, date: string, type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES', options: { billSubtotal?: number; tip?: { value: number; type: 'PERCENT' | 'FIXED'}; tax?: number } = {}) => {
  const baseEvent = {
    id: crypto.randomUUID(),
    name,
    date,
    participants: [],
    createdAt: new Date().toISOString(),
  };

  let newEvent: BillSplitEvent;
  if (type === 'SHARED_EXPENSES') {
    newEvent = { ...baseEvent, type, expenses: [] };
  } else if (type === 'ITEMIZED_BILL') {
    newEvent = { 
        ...baseEvent, 
        type, 
        items: [], 
        tip: options.tip || { value: 0, type: 'PERCENT' }, 
        tax: options.tax || 0, 
        billSubtotal: options.billSubtotal || 0,
        actualPayments: [],
    };
  } else {
    // DOMESTIC_EXPENSES
    newEvent = {
        ...baseEvent,
        type,
        domesticExpenses: [],
        userSettings: {
          user1Name: 'Participante 1',
          user2Name: 'Participante 2'
        }
    };
  }

  setEvents(prev => [...prev, newEvent]);
  setCurrentEventId(newEvent.id);
  setActiveSection('participants'); // Reset accordion to start
};"""

content = content.replace(old_add_event, new_add_event)
print("✅ addEvent corrigido para suportar DOMESTIC_EXPENSES!")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ MODO DOMÉSTICO CORRIGIDO DE UMA VEZ POR TODAS!")
