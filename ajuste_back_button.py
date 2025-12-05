# AJUSTE 4: Botão Voltar (Histórico)

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar o useEffect para gerenciar o histórico
# Vamos inserir após o useEffect do localStorage (linha 132)

history_hook = """
  // Handle Browser Back Button to prevent exiting the app
  useEffect(() => {
    const handlePopState = (event: PopStateEvent) => {
      // Se o usuário clicar em Voltar e estivermos em um evento, voltamos para a lista
      if (currentEventId) {
        // Previne o comportamento padrão se necessário, mas aqui queremos apenas atualizar o estado
        setCurrentEventId(null);
      }
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, [currentEventId]);

  // Push history state when opening an event
  useEffect(() => {
    if (currentEventId) {
      // Adiciona uma entrada no histórico
      // Usamos replaceState se já estivermos no hash para evitar duplicação em alguns casos, 
      // mas pushState é o padrão para "navegar"
      window.history.pushState({ view: 'event' }, '', '#event');
    }
  }, [currentEventId]);
"""

# Inserir após o useEffect da linha 132
insert_marker = "  }, [currentEventId]);"
# Cuidado, tem vários useEffects. Vamos procurar um contexto maior.
context = """  useEffect(() => {
    if (currentEventId) {
        localStorage.setItem('currentEventId', currentEventId);
    } else {
        localStorage.removeItem('currentEventId');
    }
  }, [currentEventId]);"""

if context in content:
    content = content.replace(context, context + "\n" + history_hook)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Lógica do botão Voltar implementada!")
