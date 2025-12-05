# PASSO 2: Passar props de export/import para EventSelector

# Ler App.tsx
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar as props ao EventSelector
old_selector = """      <EventSelector
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

new_selector = """      <EventSelector
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

if old_selector in content:
    content = content.replace(old_selector, new_selector)
    print("✅ Props passadas para EventSelector")
else:
    print("❌ EventSelector não encontrado")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ PASSO 2 COMPLETO!")
