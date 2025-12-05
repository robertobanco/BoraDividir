# Adicionar props de export/import ao EventSelector no App.tsx

# Ler App.tsx
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar as props ao EventSelector
old_event_selector = """      <EventSelector
        events={events}
        currentEventId={currentEventId}
        onSelectEvent={selectEvent}
        onAddEvent={addEvent}
        onEditEvent={editEvent}
        onDeleteEvent={deleteEvent}
        onBack={() => {
          console.log('🔙 Voltando para lista de eventos...');
          setCurrentEventId(null);
        }}
        theme={theme}
        setTheme={setTheme}
        onShowAlert={showAlert}"""

new_event_selector = """      <EventSelector
        events={events}
        currentEventId={currentEventId}
        onSelectEvent={selectEvent}
        onAddEvent={addEvent}
        onEditEvent={editEvent}
        onDeleteEvent={deleteEvent}
        onBack={() => {
          console.log('🔙 Voltando para lista de eventos...');
          setCurrentEventId(null);
        }}
        theme={theme}
        setTheme={setTheme}
        onShowAlert={showAlert}
        onExportData={handleExportData}
        onImportData={handleImportData}
        fileInputRef={fileInputRef}"""

content = content.replace(old_event_selector, new_event_selector)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Props de export/import passadas para EventSelector!")
print("✅ Funcionalidade de Exportar/Importar COMPLETA!")
