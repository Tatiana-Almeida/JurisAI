import type { HealthStatusResponse } from "@/types/api";
import type { Organization } from "@/types/organization";
import { ModuleStateCard } from "@/components/shared/module-state-card";

type SystemStatusCardProps = {
  health?: HealthStatusResponse;
  organization?: Organization | null;
};

export function SystemStatusCard({ health, organization }: SystemStatusCardProps) {
  return (
    <ModuleStateCard
      title="Estado do sistema"
      status={health?.status === "ok" ? "active" : "partial"}
      description="O frontend inicial consome healthcheck real, contexto multi-tenant e módulos jurídicos já expostos pelo backend."
      bullets={[
        `Healthcheck backend: ${health?.status ?? "indisponível"}`,
        `Organização ativa: ${organization?.name ?? "não selecionada"}`,
        "Billing permanece em modo honesto enquanto checkout e cancelamento não forem confirmados.",
      ]}
    />
  );
}
