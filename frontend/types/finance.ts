export interface Invoice {
  id: string;
  organization_id?: string;
  law_case_id?: string | null;
  client_id?: string | null;
  invoice_number?: string;
  description?: string;
  amount: number | string;
  status?: "draft" | "open" | "paid" | "overdue" | "cancelled" | string;
  issued_at?: string | null;
  due_date?: string | null;
  paid_at?: string | null;
  created_at?: string;
}

export interface Expense {
  id: string;
  organization_id?: string;
  law_case_id?: string | null;
  description?: string;
  amount: number | string;
  currency?: string;
  expense_date?: string;
  reimbursable?: boolean;
  created_by_id?: string;
  created_at?: string;
}

export interface FinanceSummary {
  total_invoices: number;
  open_invoices: number;
  paid_invoices: number;
  total_payments: number;
  payments_amount: number | string;
  expenses_amount: number | string;
}
