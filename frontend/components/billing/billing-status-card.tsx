import { ModuleStateCard } from "@/components/shared/module-state-card";

export function BillingStatusCard() {
  return (
    <ModuleStateCard
      title="Billing integration pending"
      status="pending"
      description="Billing ainda está em preparação para cobrança real. O backend atual tem pagamentos, subscriptions, invoices e webhook, mas não expõe checkout nem cancelamento comercial."
      bullets={[
        "Checkout pending.",
        "Webhook pending para enforcement comercial completo.",
        "Subscription enforcement pending.",
        "UI deve permanecer honesta enquanto checkout não existir.",
      ]}
    />
  );
}
