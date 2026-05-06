"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { BillingStatusCard } from "@/components/billing/billing-status-card";
import { PlanCard } from "@/components/billing/plan-card";
import { useBillingSummary } from "@/hooks/use-jurisai-queries";

const plans = [
  {
    id: "starter",
    name: "Starter",
    status: "pending" as const,
    priceLabel: "Checkout ainda não ativo.",
  },
  {
    id: "growth",
    name: "Growth",
    status: "pending" as const,
    priceLabel: "Integração comercial depende de checkout e webhooks.",
  },
];

export default function BillingPage() {
  const billingQuery = useBillingSummary();

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Billing"
          description="UI honesta: leitura de subscriptions e invoices quando existirem, sem fingir checkout, cancelamento ou portal comercial prontos."
        />
        <BillingStatusCard />
        <div className="grid gap-4 md:grid-cols-2">
          {plans.map((plan) => (
            <PlanCard key={plan.id} plan={plan} />
          ))}
        </div>
        <div className="jurisai-panel rounded-3xl p-6 text-sm text-muted-foreground">
          subscriptions={billingQuery.data?.subscriptions.length ?? 0} · invoices=
          {billingQuery.data?.invoices.length ?? 0}
        </div>
      </div>
    </AppShell>
  );
}
