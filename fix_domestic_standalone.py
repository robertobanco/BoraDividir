import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar e substituir o ParticipantManager para ser condicional
old_participant = '''            <ParticipantManager
              participants={currentEvent.participants}
              onAddParticipant={addParticipant}
              onRemoveParticipant={removeParticipant}
              onUpdateParticipant={updateParticipant}
              isExpanded={activeSection === 'participants'}
              onToggle={toggleParticipants}
            />'''

new_participant = '''            {/* ParticipantManager only for SHARED_EXPENSES and ITEMIZED_BILL */}
            {(currentEvent.type === 'SHARED_EXPENSES' || currentEvent.type === 'ITEMIZED_BILL') && (
              <ParticipantManager
                participants={currentEvent.participants}
                onAddParticipant={addParticipant}
                onRemoveParticipant={removeParticipant}
                onUpdateParticipant={updateParticipant}
                isExpanded={activeSection === 'participants'}
                onToggle={toggleParticipants}
              />
            )}'''

content = content.replace(old_participant, new_participant)

# Atualizar o DomesticExpensesManager para ser sempre expandido
old_domestic = '''            {currentEvent.type === 'DOMESTIC_EXPENSES' && (
              <DomesticExpensesManager 
                expenses={currentEvent.domesticExpenses}
                userSettings={currentEvent.userSettings}
                onUpdateExpenses={updateDomesticExpenses}
                onUpdateSettings={updateDomesticSettings}
                isExpanded={activeSection === 'expenses'}
                onToggle={toggleExpenses}
              />
            )}'''

new_domestic = '''            {currentEvent.type === 'DOMESTIC_EXPENSES' && (
              <DomesticExpensesManager 
                expenses={currentEvent.domesticExpenses}
                userSettings={currentEvent.userSettings}
                onUpdateExpenses={updateDomesticExpenses}
                onUpdateSettings={updateDomesticSettings}
                isExpanded={true}
                onToggle={() => {}}
              />
            )}'''

content = content.replace(old_domestic, new_domestic)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("App.tsx atualizado - modo doméstico agora é standalone!")
