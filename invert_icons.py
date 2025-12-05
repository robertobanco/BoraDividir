# CORREÇÃO: Inverter ícones de Exportar e Importar

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Ícones atuais
icon_down = 'd="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"'
icon_up = 'd="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L9 8m4-4v12"'

# Substituir usando placeholders para não confundir
content = content.replace(icon_down, "ICON_PLACEHOLDER_DOWN")
content = content.replace(icon_up, "ICON_PLACEHOLDER_UP")

# Agora inverter
content = content.replace("ICON_PLACEHOLDER_DOWN", icon_up) # Onde era down (export), agora é up
content = content.replace("ICON_PLACEHOLDER_UP", icon_down) # Onde era up (import), agora é down

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Ícones invertidos com sucesso!")
