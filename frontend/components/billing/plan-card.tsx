import type { BillingPlan } from "@/types/billing";
import { StatusBadge } from "@/components/shared/status-badge";

type PlanCardProps = {
  plan: BillingPlan;
};

export function PlanCard({ plan }: PlanCardProps) {
  return (
    <div className="jurisai-panel rounded-3xl p-5">
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-lg font-semibold">{plan.name}</h3>
        <StatusBadge status={plan.status === "implemented" ? "implemented" : "pending"} />
      </div>
      <p className="mt-2 text-sm text-muted-foreground">
        {plan.priceLabel ?? "Preço e automação comercial pendentes."}
      </p>
    </div>
  );
}
