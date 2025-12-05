# CORREÇÃO DEFINITIVA - addEvent com suporte a DOMESTIC_EXPENSES

import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Procurar e substituir a função addEvent completa
# Usar regex para encontrar a função
pattern = r"const addEvent = \(name: string, date: string, type: 'SHARED_EXPENSES' \| 'ITEMIZED_BILL'.*?\n  \};"

replacement = """const addEvent = (name: string, date: string, type: 'SHARED_EXPENSES' | 'ITEMIZED_BILL' | 'DOMESTIC_EXPENSES', options: { billSubtotal?: number; tip?: { value: number; type: 'PERCENT' | 'FIXED'}; tax?: number } = {}) => {
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

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ addEvent corrigido com suporte a DOMESTIC_EXPENSES!")
print("✅ Agora eventos domésticos serão criados corretamente!")
