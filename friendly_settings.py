# AJUSTE: Botão Cancelar e Mensagem Amigável

import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Mudar a mensagem de alerta
old_alert = 'alert("Por favor, altere os nomes padrão para os nomes reais.");'
new_alert = 'alert("Que tal personalizar os nomes para deixar o app com a sua cara? 😊");'

content = content.replace(old_alert, new_alert)

# 2. Adicionar botão Cancelar no modal de Settings
# O botão Salvar atual é:
# <button onClick={() => { ... }} className="...">Salvar</button>

# Vamos procurar o bloco dos botões. Atualmente só tem o Salvar.
# Vamos substituir o botão Salvar por um container flex com Cancelar e Salvar.

# Padrão para encontrar o botão Salvar (com a lógica de validação inserida anteriormente)
save_button_pattern = r'<button \s+onClick=\{\(\) => \{[\s\S]+?Salvar\s+</button>'

# Vamos localizar manualmente para ser mais preciso
start_save = """<button 
                                onClick={() => {
                                    if (!userSettings.user1Name.trim() || !userSettings.user2Name.trim()) {
                                        alert("Por favor, preencha o nome dos dois participantes.");
                                        return;
                                    }
                                    if (userSettings.user1Name === 'Participante 1' || userSettings.user2Name === 'Participante 2') {
                                        alert("Que tal personalizar os nomes para deixar o app com a sua cara? 😊");
                                        return;
                                    }
                                    setShowSettingsModal(false);
                                }} 
                                className="w-full px-4 py-3 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-lg font-bold shadow-lg shadow-pink-500/30 transition-all hover:scale-105 active:scale-95 mt-6"
                            >
                                Salvar
                            </button>"""

# Novo bloco com Cancelar e Salvar lado a lado
new_buttons = """                            <div className="flex gap-3 mt-6">
                                <button 
                                    onClick={() => setShowSettingsModal(false)}
                                    className="flex-1 px-4 py-3 bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg font-semibold hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors"
                                >
                                    Cancelar
                                </button>
                                <button 
                                    onClick={() => {
                                        if (!userSettings.user1Name.trim() || !userSettings.user2Name.trim()) {
                                            alert("Ops! Os nomes não podem ficar vazios.");
                                            return;
                                        }
                                        if (userSettings.user1Name === 'Participante 1' || userSettings.user2Name === 'Participante 2') {
                                            if(!confirm("Deseja manter os nomes padrão? Personalizar ajuda a identificar quem pagou o quê!")) {
                                                return;
                                            }
                                        }
                                        setShowSettingsModal(false);
                                    }} 
                                    className="flex-1 px-4 py-3 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-lg font-bold shadow-lg shadow-pink-500/30 transition-all hover:scale-105 active:scale-95"
                                >
                                    Salvar
                                </button>
                            </div>"""

# Como eu já fiz o replace do alert no passo 1, o texto no start_save mudou na memória do python script?
# Sim, se eu usar o content já modificado.
# O start_save acima tem o alert ANTIGO.
# Preciso usar o alert NOVO no start_save para encontrar o bloco no content modificado.

start_save_updated = start_save.replace('alert("Por favor, altere os nomes padrão para os nomes reais.");', new_alert)

# Tentar substituir
if start_save_updated in content:
    content = content.replace(start_save_updated, new_buttons)
    print("Botões atualizados com sucesso!")
else:
    # Se falhar, tentar achar pelo trecho sem o alert (pois pode ter espaços diferentes)
    print("Aviso: Não encontrei o bloco exato do botão Salvar. Tentando abordagem alternativa...")
    
    # Vamos procurar pelo início do onClick
    partial_start = 'onClick={() => {'
    # E o final
    partial_end = 'Salvar\n                            </button>'
    
    # Isso é arriscado. Vamos tentar localizar o botão Salvar do modal de Settings especificamente.
    # Ele está dentro de <div className="space-y-4"> ... </div>
    
    # Vamos usar o replace do passo 1 apenas, e depois tentar inserir o botão cancelar.
    # Mas o usuário quer "não prender". Então o botão cancelar é essencial.
    
    # Vamos tentar substituir o bloco inteiro do modal de settings
    settings_modal_start = '{showSettingsModal && ('
    
    # ... (muito código) ...
    
    # Vamos tentar achar o botão Salvar antigo pelo className, que é bem específico
    class_name = 'className="w-full px-4 py-3 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-lg font-bold shadow-lg shadow-pink-500/30 transition-all hover:scale-105 active:scale-95 mt-6"'
    
    if class_name in content:
        # Achamos o botão! Agora precisamos pegar o bloco inteiro dele.
        # Ele começa com <button e termina com </button>
        
        # Vamos achar o início do botão
        btn_start_idx = content.rfind('<button', 0, content.find(class_name))
        # Vamos achar o fim
        btn_end_idx = content.find('</button>', content.find(class_name)) + 9
        
        if btn_start_idx != -1 and btn_end_idx != -1:
            content = content[:btn_start_idx] + new_buttons + content[btn_end_idx:]
            print("Botões substituídos via className!")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Ajuste amigável aplicado!")
