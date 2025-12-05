# Corrigir renderização dos componentes no App.tsx

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar condição ao ParticipantManager para não aparecer em DOMESTIC_EXPENSES
old_participant = """            <ParticipantManager 
              participants={currentEvent.participants}
              onAddParticipant={addParticipant}
              onRemoveParticipant={removeParticipant}
              onUpdateParticipant={updateParticipant}
              isExpanded={activeSection === 'participants'}
              onToggle={toggleParticipants}
            />"""

new_participant = """            {(currentEvent.type === 'SHARED_EXPENSES' || currentEvent.type === 'ITEMIZED_BILL') && (
              <ParticipantManager 
                participants={currentEvent.participants}
                onAddParticipant={addParticipant}
                onRemoveParticipant={removeParticipant}
                onUpdateParticipant={updateParticipant}
                isExpanded={activeSection === 'participants'}
                onToggle={toggleParticipants}
              />
            )}"""

content = content.replace(old_participant, new_participant)

# 2. Adicionar DomesticExpensesManager antes do fechamento do </div>
old_closing = """            )}
          </div>
        )}
      </main>"""

new_closing = """            )}

            {/* Domestic Expenses Manager */}
            {currentEvent.type === 'DOMESTIC_EXPENSES' && (
              <DomesticExpensesManager
                expenses={currentEvent.domesticExpenses}
                userSettings={currentEvent.userSettings}
                onUpdateExpenses={updateDomesticExpenses}
                onUpdateSettings={updateDomesticSettings}
              />
            )}
          </div>
        )}
      </main>"""

content = content.replace(old_closing, new_closing)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Renderização corrigida!")
print("  - ParticipantManager agora só aparece em SHARED_EXPENSES e ITEMIZED_BILL")
print("  - DomesticExpensesManager adicionado para DOMESTIC_EXPENSES")
