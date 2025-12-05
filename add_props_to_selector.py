# Adicionar props ao EventSelector de forma precisa

# Ler App.tsx
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir o EventSelector
old_selector = """      <EventSelector 
        events={events}
        currentEventId={currentEventId}
        onSelectEvent={selectEvent}
        onAddEvent={addEvent}
        onEditEvent={editEvent}
        onDeleteEvent={deleteEvent}
        onBack={() => setCurrentEventId(null)}
        theme={theme}
        setTheme={setTheme}
        onShowAlert={showAlert}
      />"""

new_selector = """      <EventSelector 
        events={events}
        currentEventId={currentEventId}
        onSelectEvent={selectEvent}
        onAddEvent={addEvent}
        onEditEvent={editEvent}
        onDeleteEvent={deleteEvent}
        onBack={() => setCurrentEventId(null)}
        theme={theme}
        setTheme={setTheme}
        onShowAlert={showAlert}
        onExportData={handleExportData}
        onImportData={handleImportData}
        fileInputRef={fileInputRef}
      />"""

if old_selector in content:
    content = content.replace(old_selector, new_selector)
    print("✅ Props adicionadas ao EventSelector!")
else:
    print("❌ Não encontrado")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
