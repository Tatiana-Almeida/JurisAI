import { ModuleStateCard } from "@/components/shared/module-state-card";
import type { BillingInvoice, BillingSubscription } from "@/types/billing";

type BillingStatusCardProps = {
  subscriptions?: BillingSubscription[];
  invoices?: BillingInvoice[];
};

export function BillingStatusCard({
  subscriptions = [],
  invoices = [],
}: BillingStatusCardProps) {
  return (
    <ModuleStateCard
      title="Billing integration pending"
      status="pending"
      description="Billing ainda esta em preparacao para cobranca real. O backend atual tem pagamentos, subscriptions, invoices e webhook, mas nao expoe checkout, cancelamento nem portal comercial de faturacao."
      bullets={[
        `Subscriptions reais visiveis: ${subscriptions.length}.`,
        `Invoices reais visiveis: ${invoices.length}.`,
        "Checkout pending.",
        "Webhook existe, mas o enforcement comercial completo continua pendente.",
        "Subscription enforcement pending.",
      ]}
    />
  );
}
