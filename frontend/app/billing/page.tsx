import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { BillingStatusCard } from "@/components/billing/billing-status-card";
import { PlanCard } from "@/components/billing/plan-card";

const billingPlans = [
  { id: "foundation", name: "Billing foundation", status: "pending", priceLabel: "Checkout não ativo." },
  { id: "subscription", name: "Subscription status", status: "partial", priceLabel: "Leitura real antes de venda." },
] as const;

export default function BillingPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Billing"
          description="Foundation honesta do billing: sem fingir checkout ou cobrança prontos enquanto o backend não provar esses fluxos."
        />
        <BillingStatusCard />
        <div className="grid gap-4 md:grid-cols-2">
          {billingPlans.map((plan) => (
            <PlanCard key={plan.id} plan={plan} />
          ))}
        </div>
      </div>
    </AppShell>
  );
}
