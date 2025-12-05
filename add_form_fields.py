import re

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar a seção do formulário de valor e adicionar data ao lado
old_valor_section = """              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Valor</label>
                <input
                  type="number"
step ="0.01"
value = { amount }
onChange = {(e) => setAmount(e.target.value)}
placeholder ="0,00"
className ="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
required
    />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Categoria</label>"""

new_valor_section = """              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Valor</label>
                  <input
                    type="number"
                    step="0.01"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="0,00"
                    className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Data</label>
                  <input
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500 [color-scheme:dark]"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Categoria</label>"""

content = content.replace(old_valor_section, new_valor_section)

# Adicionar campo de recorrência antes da divisão
old_before_division = """              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  Divisão: <span className="font-bold text-pink-600 dark:text-pink-400">{ownershipPercentage}%</span> / <span className="font-bold text-purple-600 dark:text-purple-400">{100 - ownershipPercentage}%</span>
                </label>"""

new_before_division = """              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Recorrência</label>
                <select
                  value={frequency}
                  onChange={(e) => setFrequency(e.target.value as any)}
                  className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
                >
                  <option value="UNICA">Única</option>
                  <option value="MENSAL">Mensal (Fixo)</option>
                  <option value="PARCELADA">Parcelado</option>
                </select>
              </div>
              {frequency === 'PARCELADA' && (
                <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Número de Parcelas</label>
                  <input
                    type="number"
                    min="2"
                    max="120"
                    value={installmentsCount}
                    onChange={(e) => setInstallmentsCount(e.target.value)}
                    className="w-full px-4 py-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
                  />
                </div>
              )}
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  Divisão: <span className="font-bold text-pink-600 dark:text-pink-400">{ownershipPercentage}%</span> / <span className="font-bold text-purple-600 dark:text-purple-400">{100 - ownershipPercentage}%</span>
                </label>"""

content = content.replace(old_before_division, new_before_division)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Campos de data e recorrência adicionados ao formulário!")
