# Script simples e seguro para adicionar foco automático

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ExpenseManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar useRef para descriptionInput (já existe fileInputRef e cameraInputRef)
# Procurar a linha com cameraInputRef e adicionar depois
old_refs = "  const cameraInputRef = useRef<HTMLInputElement>(null);"
new_refs = """  const cameraInputRef = useRef<HTMLInputElement>(null);
  const descriptionInputRef = useRef<HTMLInputElement>(null);"""

if old_refs in content:
    content = content.replace(old_refs, new_refs)
    print("✅ Ref adicionado")
else:
    print("❌ Ref não encontrado")

# 2. Adicionar foco no resetForm
old_reset = """  const resetForm = () => {
    setDescription('');
    setAmount('');
    setPaidById('');
    setReceiptImage(null);
    if(fileInputRef.current) fileInputRef.current.value = "";
    if(cameraInputRef.current) cameraInputRef.current.value = "";
  }"""

new_reset = """  const resetForm = () => {
    setDescription('');
    setAmount('');
    setPaidById('');
    setReceiptImage(null);
    if(fileInputRef.current) fileInputRef.current.value = "";
    if(cameraInputRef.current) cameraInputRef.current.value = "";
    setTimeout(() => descriptionInputRef.current?.focus(), 100);
  }"""

if old_reset in content:
    content = content.replace(old_reset, new_reset)
    print("✅ Foco adicionado ao resetForm")
else:
    print("❌ resetForm não encontrado")

# 3. Adicionar ref ao input
# Procurar o input de description
old_input = 'type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Ex: Supermercado"'
new_input = 'ref={descriptionInputRef} type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Ex: Supermercado"'

if old_input in content:
    content = content.replace(old_input, new_input)
    print("✅ Ref adicionado ao input")
else:
    print("❌ Input não encontrado")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ExpenseManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ExpenseManager atualizado com segurança!")
