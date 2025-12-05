# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ExpenseManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar ref para o campo "O que foi?"
# Adicionar após a linha 41 (depois de cameraInputRef)
old_refs = """  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);"""

new_refs = """  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const descriptionInputRef = useRef<HTMLInputElement>(null);"""

content = content.replace(old_refs, new_refs)

# 2. Adicionar foco no campo após resetForm
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
    // Dar foco ao campo "O que foi?" após limpar
    setTimeout(() => {
      if(descriptionInputRef.current) descriptionInputRef.current.focus();
    }, 100);
  }"""

content = content.replace(old_reset, new_reset)

# 3. Adicionar ref ao input "O que foi?"
old_input = '<input type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Ex: Supermercado" className="w-full px-3 py-2 bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg text-sm focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-slate-900 dark:text-white" />'

new_input = '<input ref={descriptionInputRef} type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Ex: Supermercado" className="w-full px-3 py-2 bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg text-sm focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all text-slate-900 dark:text-white" />'

content = content.replace(old_input, new_input)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\ExpenseManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Problema 2 (parte 1) corrigido: Foco automático no campo 'O que foi?' após adicionar despesa!")
