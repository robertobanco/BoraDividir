export interface Participant {
  id: string;
  name: string;
}

export interface Expense {
  id: string;
  description: string;
  amount: number;
  paidById: string;
  receiptImage?: string | null; // Base64 string of the image
}

export interface BillItem {
  id: string;
  description: string;
  amount: number;
  consumedByIds: string[];
}

export interface ActualPayment {
  participantId: string;
  amount: number;
}

export interface Transaction {
  from: string;
  to: string;
  amount: number;
}

export interface Balance {
  participantId: string;
  name: string;
  balance: number;
}

// Domestic Expenses Types
export enum Payer {
  USER1 = 'USER1',
  USER2 = 'USER2'
}

export enum CategoryType {
  HOME = 'HOME',
  FOOD = 'FOOD',
  TRANSPORT = 'TRANSPORT',
  LEISURE = 'LEISURE',
  HEALTH = 'HEALTH',
  OTHER = 'OTHER'
}

export enum Frequency {
  ONE_TIME = 'ONE_TIME',
  MONTHLY = 'MONTHLY',
  INSTALLMENTS = 'INSTALLMENTS'
}

export interface DomesticExpense {
  id: string;
  title: string;
  amount: number;
  date: string;
  payer: Payer;
  category: CategoryType;
  ownershipPercentage: number;
  frequency: Frequency;
  installmentsCount?: number;
}

export interface UserSettings {
  user1Name: string;
  user2Name: string;
}

interface BaseEvent {
  id: string;
  name: string;
  participants: Participant[];
  createdAt: string;
  date: string;
}

export type BillSplitEvent = BaseEvent & (
  | {
      type: 'SHARED_EXPENSES';
      expenses: Expense[];
    }
  | {
      type: 'ITEMIZED_BILL';
      items: BillItem[];
      tip: {
        value: number;
        type: 'PERCENT' | 'FIXED';
      };
      tax: number; // Outras taxas (couvert, etc)
      billSubtotal: number; // Subtotal dos produtos para validação
      actualPayments: ActualPayment[];
    }
  | {
      type: 'DOMESTIC_EXPENSES';
      domesticExpenses: DomesticExpense[];
      userSettings: UserSettings;
    }
);
