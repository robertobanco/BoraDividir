# Adicionar botões de Export/Import no header do EventSelector

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir o botão de tema para adicionar os botões de export/import antes dele
old_theme_section = """             </div>
            <button 
              onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} 
              className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
                {theme === 'light' ? <MoonIcon className="h-6 w-6" /> : <SunIcon className="h-6 w-6" />}
            </button>"""

new_theme_section = """             </div>
            <div className="flex items-center gap-2">
                {/* Export button */}
                {onExportData && events.length > 0 && (
                    <button
                        onClick={onExportData}
                        className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                        title="Exportar dados"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                    </button>
                )}
                {/* Import button */}
                {onImportData && fileInputRef && (
                    <>
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                            title="Importar dados"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L9 8m4-4v12" />
                            </svg>
                        </button>
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept=".json"
                            onChange={onImportData}
                            className="hidden"
                        />
                    </>
                )}
                {/* Theme button */}
                <button 
                  onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} 
                  className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                >
                    {theme === 'light' ? <MoonIcon className="h-6 w-6" /> : <SunIcon className="h-6 w-6" />}
                </button>
            </div>"""

content = content.replace(old_theme_section, new_theme_section)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\EventSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Botões de Export/Import adicionados ao header!")
print("✅ Agora você verá os botões ao lado do tema!")
