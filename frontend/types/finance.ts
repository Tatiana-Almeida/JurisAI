export interface Invoice {
  id: string;
  invoice_number?: string;
  amount: number | string;
  status?: string;
  due_date?: string | null;
  paid_at?: string | null;
  created_at?: string;
}

export interface Expense {
  id: string;
  amount: number | string;
  description?: string;
  expense_date?: string;
  created_at?: string;
}

export interface FinanceSummary {
  total_invoices: number;
  paid_invoices: number;
  pending_invoices: number;
  total_fees_amount: number | string;
  total_expenses_amount: number | string;
  total_payments_amount: number | string;
}
