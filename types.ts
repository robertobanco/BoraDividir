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
);
