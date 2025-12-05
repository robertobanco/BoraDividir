# AJUSTE 2: Garantir que eventos domésticos sejam criados corretamente

# Ler App.tsx
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar validação no useState de events para migrar eventos antigos
old_events_init = """  const [events, setEvents] = useState<BillSplitEvent[]>(() => {
    const saved = localStorage.getItem('billSplitEvents');
    if (!saved) return [];
    const parsedEvents: BillSplitEvent[] = JSON.parse(saved);
    return parsedEvents.map(event => {
      if (!(event as any).date) {
        return { ...event, date: event.createdAt };
      }
      return event;
    });
  });"""

new_events_init = """  const [events, setEvents] = useState<BillSplitEvent[]>(() => {
    const saved = localStorage.getItem('billSplitEvents');
    if (!saved) return [];
    const parsedEvents: BillSplitEvent[] = JSON.parse(saved);
    return parsedEvents.map(event => {
      // Adicionar date se não existir
      if (!(event as any).date) {
        event = { ...event, date: event.createdAt };
      }
      // Validar eventos domésticos antigos
      if (event.type === 'DOMESTIC_EXPENSES') {
        if (!(event as any).domesticExpenses) {
          event = { ...event, domesticExpenses: [] };
        }
        if (!(event as any).userSettings) {
          event = { ...event, userSettings: { user1Name: 'Participante 1', user2Name: 'Participante 2' } };
        }
      }
      return event;
    });
  });"""

content = content.replace(old_events_init, new_events_init)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ AJUSTE 2 COMPLETO: Validação de eventos domésticos adicionada!")
print("⚠️  IMPORTANTE: Limpe o cache do navegador ou use Ctrl+Shift+R para recarregar!")
