import { DomesticExpense, UserSettings } from './types';

export const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
};

export const getCategoryInfo = (type: string) => {
    const categories: Record<string, { label: string; icon: string; bgColor: string }> = {
        'CASA': { label: 'Casa', icon: '🏠', bgColor: 'bg-blue-100 dark:bg-blue-900/30' },
        'MERCADO': { label: 'Mercado', icon: '🛒', bgColor: 'bg-orange-100 dark:bg-orange-900/30' },
        'TRANSPORTE': { label: 'Transporte', icon: '🚗', bgColor: 'bg-gray-100 dark:bg-gray-900/30' },
        'LAZER': { label: 'Lazer', icon: '🎉', bgColor: 'bg-pink-100 dark:bg-pink-900/30' },
        'SAUDE': { label: 'Saúde', icon: '💊', bgColor: 'bg-red-100 dark:bg-red-900/30' },
        'OUTROS': { label: 'Outros', icon: '📦', bgColor: 'bg-slate-100 dark:bg-slate-900/30' }
    };
    return categories[type] || categories['OUTROS'];
};

export const getMonthKey = (date: Date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    return `${year}-${month}`;
};

export const addMonths = (date: Date, months: number) => {
    const d = new Date(date);
    d.setMonth(d.getMonth() + months);
    return d;
};

const parseDateSafe = (dateStr: string): Date => {
    const [y, m, d] = dateStr.split('-').map(Number);
    return new Date(y, m - 1, d, 12, 0, 0);
};

export const isExpenseInMonth = (expense: DomesticExpense, targetMonthStr: string): boolean => {
    const expenseDate = parseDateSafe(expense.date);
    const [tYear, tMonth] = targetMonthStr.split('-').map(Number);
    const targetDate = new Date(tYear, tMonth - 1, 1, 12, 0, 0);

    const expenseMonthStart = new Date(expenseDate.getFullYear(), expenseDate.getMonth(), 1, 12, 0, 0);
    const targetMonthStart = new Date(targetDate.getFullYear(), targetDate.getMonth(), 1, 12, 0, 0);

    if (expense.frequency === 'UNICA') {
        return expenseMonthStart.getTime() === targetMonthStart.getTime();
    }

    if (expense.frequency === 'MENSAL') {
        return targetMonthStart.getTime() >= expenseMonthStart.getTime();
    }

    if (expense.frequency === 'PARCELADA' && expense.installmentsCount) {
        const endDate = addMonths(expenseMonthStart, expense.installmentsCount);
        return targetMonthStart.getTime() >= expenseMonthStart.getTime() && targetMonthStart.getTime() < endDate.getTime();
    }

    return false;
};

export interface MonthlyBalance {
    month: string;
    total: number;
    user1Paid: number;
    user2Paid: number;
    user1Share: number;
    user2Share: number;
    settlement: {
        from: string;
        to: string;
        amount: number;
    } | null;
    items: DomesticExpense[];
}

export const calculateMonthlyBalance = (
    expenses: DomesticExpense[],
    userSettings: UserSettings,
    monthStr: string
): MonthlyBalance => {
    const activeExpenses = expenses.filter(e => isExpenseInMonth(e, monthStr));

    let total = 0;
    let user1Paid = 0;
    let user2Paid = 0;
    let user1Share = 0;
    let user2Share = 0;

    activeExpenses.forEach(expense => {
        total += expense.amount;

        if (expense.payer === 'USER1') {
            user1Paid += expense.amount;
        } else {
            user2Paid += expense.amount;
        }

        const user1ShareAmount = expense.amount * (expense.ownershipPercentage / 100);
        const user2ShareAmount = expense.amount - user1ShareAmount;

        user1Share += user1ShareAmount;
        user2Share += user2ShareAmount;
    });

    const user1Balance = user1Paid - user1Share;
    const user2Balance = user2Paid - user2Share;

    let settlement: { from: string; to: string; amount: number } | null = null;

    if (Math.abs(user1Balance) > 0.01) {
        if (user1Balance > 0) {
            // User1 pagou mais, User2 deve pagar
            settlement = {
                from: userSettings.user2Name,
                to: userSettings.user1Name,
                amount: Math.abs(user1Balance)
            };
        } else {
            // User2 pagou mais, User1 deve pagar
            settlement = {
                from: userSettings.user1Name,
                to: userSettings.user2Name,
                amount: Math.abs(user1Balance)
            };
        }
    }

    return {
        month: monthStr,
        total,
        user1Paid,
        user2Paid,
        user1Share,
        user2Share,
        settlement,
        items: activeExpenses
    };
};
