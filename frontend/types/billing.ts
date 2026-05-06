export type SubscriptionStatus =
  | "active"
  | "past_due"
  | "canceled"
  | "incomplete"
  | "pending";

export interface BillingPlan {
  id: string;
  name: string;
  status?: "implemented" | "partial" | "pending" | "missing" | "roadmap";
  priceLabel?: string;
}

export interface BillingSubscription {
  id: string;
  plan?: string;
  status?: SubscriptionStatus | string;
  stripe_subscription_id?: string;
  current_period_start?: string | null;
  current_period_end?: string | null;
  trial_end?: string | null;
}

export interface BillingInvoice {
  id: string;
  stripe_invoice_id?: string;
  amount?: number | string;
  status?: string;
  due_date?: string | null;
  paid_at?: string | null;
}
