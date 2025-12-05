# AJUSTE 4: Exportação Excel e Modal de Escolha

# Ler o arquivo
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar import do XLSX
if "import * as XLSX" not in content:
    content = content.replace(
        "import React, { useState, useMemo } from 'react';",
        "import React, { useState, useMemo } from 'react';\nimport * as XLSX from 'xlsx';"
    )

# 2. Adicionar estado para o modal de exportação
if "const [showExportModal, setShowExportModal]" not in content:
    content = content.replace(
        "const [showSettingsModal, setShowSettingsModal] = useState(false);",
        "const [showSettingsModal, setShowSettingsModal] = useState(false);\n    const [showExportModal, setShowExportModal] = useState(false);"
    )

# 3. Adicionar função handleExportExcel
export_function = """
    const handleExportExcel = () => {
        const monthName = new Date(currentMonth + '-01T12:00:00').toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
        
        // Preparar dados para o Excel
        const data = monthlyBalance.items.map(item => ({
            Data: new Date(item.date).toLocaleDateString('pt-BR'),
            Descrição: item.description,
            Categoria: item.category,
            Valor: item.amount,
            'Quem Pagou': item.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name,
            'Responsabilidade': item.ownershipPercentage !== 50 
                ? `${userSettings.user1Name} ${item.ownershipPercentage}% / ${userSettings.user2Name} ${100 - item.ownershipPercentage}%`
                : 'Meio a Meio',
            'Recorrência': item.frequency === 'UNICA' ? 'Única' : item.frequency === 'MENSAL' ? 'Mensal' : `Parcelada (${item.installmentsCount}x)`
        }));

        // Adicionar resumo no final
        data.push({} as any); // Linha em branco
        data.push({
            Data: 'RESUMO',
            Descrição: 'Total Gastos',
            Valor: monthlyBalance.total
        } as any);
        data.push({
            Data: '',
            Descrição: `${userSettings.user1Name} Pagou`,
            Valor: monthlyBalance.user1Paid
        } as any);
        data.push({
            Data: '',
            Descrição: `${userSettings.user2Name} Pagou`,
            Valor: monthlyBalance.user2Paid
        } as any);
        
        if (monthlyBalance.settlement) {
            data.push({
                Data: 'RESULTADO',
                Descrição: `${monthlyBalance.settlement.from} deve a ${monthlyBalance.settlement.to}`,
                Valor: monthlyBalance.settlement.amount
            } as any);
        }

        const ws = XLSX.utils.json_to_sheet(data);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Despesas");
        
        // Ajustar largura das colunas
        const wscols = [
            {wch: 12}, // Data
            {wch: 30}, // Descrição
            {wch: 15}, // Categoria
            {wch: 12}, // Valor
            {wch: 15}, // Quem Pagou
            {wch: 30}, // Responsabilidade
            {wch: 20}  // Recorrência
        ];
        ws['!cols'] = wscols;

        XLSX.writeFile(wb, `BoraDividir_${monthName.replace(' ', '_')}.xlsx`);
        setShowExportModal(false);
    };
"""

# Inserir a função antes do return
insert_before = "    return ("
content = content.replace(insert_before, export_function + insert_before)

# 4. Modificar botão de compartilhar para abrir modal
old_share_button = """                        <button onClick={handleShareSummary} className="p-2 bg-white/10 hover:bg-white/20 rounded-lg backdrop-blur-sm transition">
                            {navigator.share ? <Share2 size={18} /> : <Copy size={18} />}
                        </button>"""

new_share_button = """                        <button onClick={() => setShowExportModal(true)} className="p-2 bg-white/10 hover:bg-white/20 rounded-lg backdrop-blur-sm transition">
                            <Share2 size={18} />
                        </button>"""

content = content.replace(old_share_button, new_share_button)

# 5. Adicionar o Modal de Exportação no final do JSX
# Procurar o fechamento do modal de configurações ou adicionar no final
modal_code = """
            {/* Export Modal */}
            {showExportModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
                    <div className="glass-card p-6 rounded-2xl shadow-2xl w-full max-w-sm animate-scale-in bg-white dark:bg-slate-900">
                        <h3 className="text-xl font-bold mb-6 text-slate-900 dark:text-white text-center">Compartilhar / Exportar</h3>
                        
                        <div className="space-y-3">
                            <button 
                                onClick={() => {
                                    handleShareSummary();
                                    setShowExportModal(false);
                                }}
                                className="w-full p-4 bg-[#25D366] hover:bg-[#128C7E] text-white rounded-xl font-bold flex items-center justify-center gap-3 transition-colors shadow-lg"
                            >
                                <Share2 size={20} />
                                Compartilhar no WhatsApp
                            </button>
                            
                            <button 
                                onClick={handleExportExcel}
                                className="w-full p-4 bg-[#1D6F42] hover:bg-[#155230] text-white rounded-xl font-bold flex items-center justify-center gap-3 transition-colors shadow-lg"
                            >
                                <TrendingUp size={20} />
                                Baixar Excel (.xlsx)
                            </button>
                        </div>

                        <button 
                            onClick={() => setShowExportModal(false)}
                            className="w-full mt-6 py-3 text-slate-500 dark:text-slate-400 font-medium hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
                        >
                            Cancelar
                        </button>
                    </div>
                </div>
            )}
"""

# Inserir antes do último fechamento
if "{/* Export Modal */}" not in content:
    last_closing = "    );\n};"
    content = content.replace(last_closing, modal_code + last_closing)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ AJUSTE 4 COMPLETO: Exportação Excel e Modal de Escolha implementados!")
