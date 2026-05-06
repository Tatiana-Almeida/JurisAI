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
