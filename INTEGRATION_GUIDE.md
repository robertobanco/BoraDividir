# Integração de Contas Domésticas - Passos Finais

## Status Atual
A maior parte da integração está completa. Falta apenas atualizar o App.tsx principal e corrigir alguns detalhes.

## Passos Restantes:

### 1. Atualizar calculateEventTotal em EventSelector.tsx

Localizar a função `calculateEventTotal` (linha 24) e substituir por:

```typescript
const calculateEventTotal = (event: BillSplitEvent): number => {
    if (event.type === 'SHARED_EXPENSES') {
        return event.expenses.reduce((sum, exp) => sum + exp.amount, 0);
    } else if (event.type === 'ITEMIZED_BILL') {
        const itemsSubtotal = event.items.reduce((sum, item) => sum + item.amount, 0);
        const tipAmount = event.tip.type === 'PERCENT'
            ? itemsSubtotal * (event.tip.value / 100)
            : event.tip.value;
        return itemsSubtotal + tipAmount + event.tax;
    } else { // DOMESTIC_EXPENSES
        return event.domesticExpenses.reduce((sum, exp) => sum + exp.amount, 0);
    }
};
```

### 2. Adicionar botão de Contas Domésticas no modal EventTypeModal

Adicionar após o botão de "Despesas Compartilhadas" (linha ~73):

```typescript
<button onClick={() => onSelect('DOMESTIC_EXPENSES')} className="group w-full text-left p-5 border border-slate-200 dark:border-slate-700 rounded-xl hover:bg-violet-50 dark:hover:bg-violet-900/20 hover:border-violet-300 dark:hover:border-violet-700 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-violet-500">
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
```

### 3. Atualizar App.tsx

#### 3.1 Adicionar import do DomesticExpensesManager:
```typescript
import { DomesticExpensesManager } from './components/DomesticExpensesManager';
import { UserSettings } from './types';
```

#### 3.2 Atualizar a função addEvent (linha ~132):
```typescript
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
    } else { // DOMESTIC_EXPENSES
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
    setActiveSection('participants');
  };
```

#### 3.3 Adicionar funções para gerenciar despesas domésticas:
```typescript
// Domestic Expenses Logic
const updateDomesticExpenses = (expenses: DomesticExpense[]) => {
    if (!currentEvent || currentEvent.type !== 'DOMESTIC_EXPENSES') return;
    updateCurrentEvent(event => {
        if (event.type !== 'DOMESTIC_EXPENSES') return event;
        return { ...event, domesticExpenses: expenses };
    });
};

const updateDomesticSettings = (settings: UserSettings) => {
    if (!currentEvent || currentEvent.type !== 'DOMESTIC_EXPENSES') return;
    updateCurrentEvent(event => {
        if (event.type !== 'DOMESTIC_EXPENSES') return event;
        return { ...event, userSettings: settings };
    });
};
```

#### 3.4 Adicionar renderização condicional no JSX (após linha ~428):
```typescript
{currentEvent.type === 'DOMESTIC_EXPENSES' && (
    <DomesticExpensesManager 
        expenses={currentEvent.domesticExpenses}
        userSettings={currentEvent.userSettings}
        onUpdateExpenses={updateDomesticExpenses}
        onUpdateSettings={updateDomesticSettings}
        isExpanded={activeSection === 'expenses'}
        onToggle={toggleExpenses}
    />
)}
```

#### 3.5 Atualizar o badge de tipo de evento (linha ~353):
```typescript
<span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
    currentEvent.type === 'SHARED_EXPENSES' 
        ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' 
        : currentEvent.type === 'ITEMIZED_BILL'
        ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
        : 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300'
}`}>
    {currentEvent.type === 'SHARED_EXPENSES' 
        ? 'Despesas Compartilhadas' 
        : currentEvent.type === 'ITEMIZED_BILL'
        ? 'Conta Detalhada'
        : 'Contas Domésticas'}
</span>
```

#### 3.6 Atualizar o badge na lista de eventos (EventSelector.tsx linha ~300):
```typescript
<span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
    event.type === 'SHARED_EXPENSES' 
        ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' 
        : event.type === 'ITEMIZED_BILL'
        ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
        : 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300'
}`}>
    {event.type === 'SHARED_EXPENSES' 
        ? 'Compartilhado' 
        : event.type === 'ITEMIZED_BILL'
        ? 'Detalhado'
        : 'Doméstico'}
</span>
```

### 4. Instalar dependências e testar

```bash
cd c:\Antigravity\QuemPagou\BoraDividir
npm install
npm run dev
```

## Arquivos Criados/Modificados:

✅ `types.ts` - Atualizado com novos tipos
✅ `domesticUtils.ts` - Criado
✅ `components/DomesticExpensesManager.tsx` - Criado
✅ `components/EventSelector.tsx` - Parcialmente atualizado
⏳ `App.tsx` - Precisa ser atualizado

## Notas Importantes:

1. O componente DomesticExpensesManager é completamente autônomo e gerencia seu próprio estado
2. Ele usa os mesmos padrões de design do BoraDividir (dark mode, glassmorphism, etc.)
3. Todos os cálculos de balanço e projeções estão implementados
4. O componente suporta:
   - Navegação por meses
   - Categorias de despesas
   - Recorrência (única, mensal, parcelada)
   - Divisão personalizada (não apenas 50/50)
   - Gráficos de projeção
   - Compartilhamento de resumo

## Teste Final:

1. Criar um novo evento do tipo "Contas Domésticas"
2. Configurar os nomes dos participantes
3. Adicionar algumas despesas
4. Verificar os cálculos de acerto de contas
5. Testar navegação entre meses
6. Verificar os gráficos de projeção
