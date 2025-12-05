# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Texto antigo
old_text = '''<div className="mb-4">
                                                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${event.type === 'SHARED_EXPENSES' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'}`}>
                                                        {event.type === 'SHARED_EXPENSES' ? 'Compartilhado' : 'Detalhado'}
                                                    </span>
                                                </div>'''

# Novo texto
new_text = '''<div className="mb-4">
                                                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                                        event.type === 'SHARED_EXPENSES' 
                                                            ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' 
                                                            : event.type === 'DOMESTIC_EXPENSES'
                                                                ? 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300'
                                                                : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                                                    }`}>
                                                        {event.type === 'SHARED_EXPENSES' 
                                                            ? 'Compartilhado' 
                                                            : event.type === 'DOMESTIC_EXPENSES'
                                                                ? 'Doméstico'
                                                                : 'Detalhado'}
                                                    </span>
                                                </div>'''

# Normalizar espaços para busca (opcional, mas ajuda se tiver tabs vs spaces)
# Vou tentar replace direto primeiro, copiando exatamente o que vi no view_file
# O view_file mostrou muitos espaços antes do <div...

# Vou usar uma regex para ser mais flexível com a indentação
import re

pattern = r'<div className="mb-4">\s*<span className=\{`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium \$\{event\.type === \'SHARED_EXPENSES\' \? \'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300\' : \'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300\'\}`\}>\s*\{event\.type === \'SHARED_EXPENSES\' \? \'Compartilhado\' : \'Detalhado\'\}\s*</span>\s*</div>'

match = re.search(pattern, content, re.DOTALL)

if match:
    print("Encontrado!")
    content = content.replace(match.group(0), new_text)
    
    with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Substituído com sucesso!")
else:
    print("Não encontrado via regex. Tentando string exata...")
    # Tentativa com string exata baseada no view_file, ajustando indentação visualmente
    # Linha 311 tem indentação grande.
    
    # Vou tentar localizar pelo contexto
    part1 = '{event.type === \'SHARED_EXPENSES\' ? \'Compartilhado\' : \'Detalhado\'}'
    if part1 in content:
        print("Parte encontrada. Substituindo bloco manualmente...")
        # Vou substituir o bloco inteiro de lógica
        content = content.replace(
            "event.type === 'SHARED_EXPENSES' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'",
            "event.type === 'SHARED_EXPENSES' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300' : event.type === 'DOMESTIC_EXPENSES' ? 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'"
        )
        content = content.replace(
            "{event.type === 'SHARED_EXPENSES' ? 'Compartilhado' : 'Detalhado'}",
            "{event.type === 'SHARED_EXPENSES' ? 'Compartilhado' : event.type === 'DOMESTIC_EXPENSES' ? 'Doméstico' : 'Detalhado'}"
        )
        
        with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Substituição manual realizada!")
    else:
        print("Nada encontrado.")

