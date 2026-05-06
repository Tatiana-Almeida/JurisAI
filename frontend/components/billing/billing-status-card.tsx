import { ModuleStateCard } from "@/components/shared/module-state-card";

export function BillingStatusCard() {
  return (
    <ModuleStateCard
      title="Billing integration pending"
      status="pending"
      description="O backend atual tem pagamentos, subscriptions, invoices e webhook, mas ainda não expõe checkout nem cancelamento comercial."
      bullets={[
        "Não fingir cobrança pronta nesta fase.",
        "UI deve permanecer honesta enquanto checkout não existir.",
      ]}
    />
  );
}
