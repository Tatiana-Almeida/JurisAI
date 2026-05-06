export interface Invoice {
  id: string;
  amount: number;
  status: string;
  dueDate?: string;
}

export interface Expense {
  id: string;
  amount: number;
  category?: string;
  createdAt?: string;
}
