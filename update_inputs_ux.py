# AJUSTE: Menus de Categoria e Recorrência em Grade/Botões

import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Substituir Categoria
old_category_block = """                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Categoria</label>
                                <select value={category} onChange={(e) => setCategory(e.target.value as any)} className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500">
                                    <option value="CASA">🏠 Casa</option>
                                    <option value="MERCADO">🛒 Mercado</option>
                                    <option value="TRANSPORTE">🚗 Transporte</option>
                                    <option value="LAZER">🎉 Lazer</option>
                                    <option value="SAUDE">💊 Saúde</option>
                                    <option value="OUTROS">📦 Outros</option>
                                </select>
                            </div>"""

new_category_block = """                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Categoria</label>
                                <div className="grid grid-cols-3 gap-2">
                                    {(['CASA', 'MERCADO', 'TRANSPORTE', 'LAZER', 'SAUDE', 'OUTROS'] as const).map((cat) => {
                                        const info = getCategoryInfo(cat);
                                        const isSelected = category === cat;
                                        return (
                                            <button
                                                key={cat}
                                                type="button"
                                                onClick={() => setCategory(cat)}
                                                className={`flex flex-col items-center justify-center p-3 rounded-xl border transition-all ${
                                                    isSelected
                                                        ? 'bg-pink-600 text-white border-pink-600 shadow-lg shadow-pink-500/20 scale-105'
                                                        : 'bg-slate-50 dark:bg-slate-900/50 text-slate-500 dark:text-slate-400 border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800'
                                                }`}
                                            >
                                                <span className="text-2xl mb-1">{info.icon}</span>
                                                <span className="text-[10px] font-bold uppercase tracking-wide">{info.label}</span>
                                            </button>
                                        );
                                    })}
                                </div>
                            </div>"""

# 2. Substituir Recorrência
old_recurrence_block = """                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Recorrência</label>
                                <select value={frequency} onChange={(e) => setFrequency(e.target.value as any)} className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500">
                                    <option value="UNICA">Única</option>
                                    <option value="MENSAL">Mensal (Fixo)</option>
                                    <option value="PARCELADA">Parcelado</option>
                                </select>
                            </div>"""

new_recurrence_block = """                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Recorrência</label>
                                <div className="grid grid-cols-3 gap-2">
                                    {[
                                        { value: 'UNICA', label: 'Única' },
                                        { value: 'MENSAL', label: 'Mensal' },
                                        { value: 'PARCELADA', label: 'Parcelada' }
                                    ].map((opt) => (
                                        <button
                                            key={opt.value}
                                            type="button"
                                            onClick={() => setFrequency(opt.value as any)}
                                            className={`py-3 rounded-xl text-sm font-bold transition-all border ${
                                                frequency === opt.value
                                                    ? 'bg-purple-600 text-white border-purple-600 shadow-lg shadow-purple-500/20'
                                                    : 'bg-slate-50 dark:bg-slate-900/50 text-slate-500 dark:text-slate-400 border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800'
                                            }`}
                                        >
                                            {opt.label}
                                        </button>
                                    ))}
                                </div>
                            </div>"""

# Substituir
if old_category_block in content:
    content = content.replace(old_category_block, new_category_block)
    print("Categoria atualizada!")
else:
    print("Erro: Bloco de categoria não encontrado.")

if old_recurrence_block in content:
    content = content.replace(old_recurrence_block, new_recurrence_block)
    print("Recorrência atualizada!")
else:
    print("Erro: Bloco de recorrência não encontrado.")

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Menus transformados em botões!")
