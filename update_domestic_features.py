import re

# Ler o arquivo atual
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar estado para data, frequency e installmentsCount
old_state = """    const [description, setDescription] = useState('');
    const [amount, setAmount] = useState('');
    const [category, setCategory] = useState<'CASA' | 'MERCADO' | 'TRANSPORTE' | 'LAZER' | 'SAUDE' | 'OUTROS'>('MERCADO');
    const [payer, setPayer] = useState<Payer>('USER1');
    const [ownershipPercentage, setOwnershipPercentage] = useState(50);"""

new_state = """    const [description, setDescription] = useState('');
    const [amount, setAmount] = useState('');
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [category, setCategory] = useState<'CASA' | 'MERCADO' | 'TRANSPORTE' | 'LAZER' | 'SAUDE' | 'OUTROS'>('MERCADO');
    const [payer, setPayer] = useState<Payer>('USER1');
    const [ownershipPercentage, setOwnershipPercentage] = useState(50);
    const [frequency, setFrequency] = useState<'UNICA' | 'MENSAL' | 'PARCELADA'>('UNICA');
    const [installmentsCount, setInstallmentsCount] = useState('2');"""

content = content.replace(old_state, new_state)

# 2. Atualizar handleAddExpense para incluir date, frequency e installmentsCount
old_expense_data = """        const expenseData: DomesticExpense = {
            id: crypto.randomUUID(),
            description: description.trim(),
            amount: parseFloat(amount),
            category,
            payer,
            date: new Date().toISOString().split('T')[0],
            ownershipPercentage,
            frequency: 'UNICA'
        };"""

new_expense_data = """        const expenseData: DomesticExpense = {
            id: crypto.randomUUID(),
            description: description.trim(),
            amount: parseFloat(amount),
            category,
            payer,
            date,
            ownershipPercentage,
            frequency,
            installmentsCount: frequency === 'PARCELADA' ? parseInt(installmentsCount) : undefined
        };"""

content = content.replace(old_expense_data, new_expense_data)

# 3. Atualizar reset form
old_reset = """        // Reset form
        setDescription('');
        setAmount('');
        setCategory('MERCADO');
        setPayer('USER1');
        setOwnershipPercentage(50);
        setShowAddModal(false);"""

new_reset = """        // Reset form
        setDescription('');
        setAmount('');
        setDate(new Date().toISOString().split('T')[0]);
        setCategory('MERCADO');
        setPayer('USER1');
        setOwnershipPercentage(50);
        setFrequency('UNICA');
        setInstallmentsCount('2');
        setShowAddModal(false);"""

content = content.replace(old_reset, new_reset)

# 4. Atualizar handleEditExpense
old_edit = """    const handleEditExpense = (expense: DomesticExpense) => {
        setEditingExpense(expense);
        setDescription(expense.description);
        setAmount(expense.amount.toString());
        setCategory(expense.category as any);
        setPayer(expense.payer);
        setOwnershipPercentage(expense.ownershipPercentage);
        setShowAddModal(true);
    };"""

new_edit = """    const handleEditExpense = (expense: DomesticExpense) => {
        setEditingExpense(expense);
        setDescription(expense.description);
        setAmount(expense.amount.toString());
        setDate(expense.date);
        setCategory(expense.category as any);
        setPayer(expense.payer);
        setOwnershipPercentage(expense.ownershipPercentage);
        setFrequency(expense.frequency);
        setInstallmentsCount(expense.installmentsCount?.toString() || '2');
        setShowAddModal(true);
    };"""

content = content.replace(old_edit, new_edit)

# 5. Atualizar handleShareSummary para incluir responsabilidade
old_share_map = """            ...monthlyBalance.items.map(e => {
                const payer = e.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name;
                return `- ${e.description}: ${formatCurrency(e.amount)} (${payer})`;
            })"""

new_share_map = """            ...monthlyBalance.items.map(e => {
                const payer = e.payer === 'USER1' ? userSettings.user1Name : userSettings.user2Name;
                const responsibility = e.ownershipPercentage !== 50 ? ` [${e.ownershipPercentage}% / ${100 - e.ownershipPercentage}%]` : '';
                return `- ${e.description}: ${formatCurrency(e.amount)} (${payer})${responsibility}`;
            })"""

content = content.replace(old_share_map, new_share_map)

# 6. Adicionar ordenação por data no monthlyBalance
# Encontrar onde monthlyBalance.items é usado na lista e adicionar sort
old_map_start = """            {monthlyBalance.items.map((expense) => {"""
new_map_start = """            {monthlyBalance.items.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()).map((expense) => {"""

content = content.replace(old_map_start, new_map_start)

# 7. Atualizar o cleanup do modal
old_modal_cleanup = """                    setShowAddModal(false);
                    setEditingExpense(null);
                    setDescription('');
                    setAmount('');
                    setCategory('MERCADO');
                    setPayer('USER1');
                    setOwnershipPercentage(50);"""

new_modal_cleanup = """                    setShowAddModal(false);
                    setEditingExpense(null);
                    setDescription('');
                    setAmount('');
                    setDate(new Date().toISOString().split('T')[0]);
                    setCategory('MERCADO');
                    setPayer('USER1');
                    setOwnershipPercentage(50);
                    setFrequency('UNICA');
                    setInstallmentsCount('2');"""

content = content.replace(old_modal_cleanup, new_modal_cleanup)

# Salvar
with open(r'c:\Antigravity\QuemPagou\BoraDividir\components\DomesticExpensesManager.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("DomesticExpensesManager.tsx atualizado com recorrência e melhorias!")
