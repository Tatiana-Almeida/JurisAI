"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { BillingStatusCard } from "@/components/billing/billing-status-card";
import { PlanCard } from "@/components/billing/plan-card";
import { EmptyState } from "@/components/shared/empty-state";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useBillingSummary } from "@/hooks/use-billing";

const plans = [
  {
    id: "solo",
    name: "Solo",
    status: "pending" as const,
    priceLabel: "Checkout ainda nao ativo.",
    description:
      "Preview apenas. Este plano ainda depende da ativacao de checkout e enforcement comercial.",
  },
  {
    id: "growth",
    name: "Growth",
    status: "partial" as const,
    priceLabel: "Webhook e registos existem, mas a cobranca real ainda nao esta pronta.",
    description:
      "Subscriptions e invoices reais podem ser lidas, mas o backend ainda nao expoe checkout nem cancelamento self-serve.",
  },
];

export default function BillingPage() {
  const { activeOrganizationId } = useActiveOrganization();
  const billingQuery = useBillingSummary();

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para avaliar o estado de billing deste tenant."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Billing"
          description="UI honesta: leitura de subscriptions e invoices reais quando existirem, sem fingir checkout, cancelamento ou portal comercial prontos."
        />
        {billingQuery.isLoading ? <LoadingSkeleton /> : null}
        {billingQuery.isError ? (
          <ErrorState
            title="Nao foi possivel carregar billing"
            description="Confirme autenticacao, organizacao ativa e disponibilidade dos endpoints de subscriptions e invoices."
          />
        ) : null}
        {!billingQuery.isLoading && !billingQuery.isError ? (
          <>
            <BillingStatusCard
              subscriptions={billingQuery.data?.subscriptions ?? []}
              invoices={billingQuery.data?.invoices ?? []}
            />
            <div className="grid gap-4 md:grid-cols-2">
              {plans.map((plan) => (
                <PlanCard key={plan.id} plan={plan} />
              ))}
            </div>
            <div className="jurisai-panel rounded-3xl p-6 text-sm text-muted-foreground">
              subscriptions={billingQuery.data?.subscriptions.length ?? 0} · invoices=
              {billingQuery.data?.invoices.length ?? 0} · checkout pending · webhook ready only
              for backend-side foundation.
            </div>
          </>
        ) : null}
      </div>
    </AppShell>
  );
}
