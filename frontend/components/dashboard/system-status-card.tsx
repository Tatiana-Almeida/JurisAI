import type { HealthStatusResponse } from "@/types/api";
import type { Organization } from "@/types/organization";
import { ModuleStateCard } from "@/components/shared/module-state-card";

type SystemStatusCardProps = {
  health?: HealthStatusResponse;
  organization?: Organization | null;
  apiUrl: string;
  environment: string;
  reachable: boolean;
};

export function SystemStatusCard({
  health,
  organization,
  apiUrl,
  environment,
  reachable,
}: SystemStatusCardProps) {
  return (
    <ModuleStateCard
      title="Estado do sistema"
      status={reachable && health?.status === "ok" ? "active" : "partial"}
      description="O frontend consome healthcheck real, contexto multi-tenant e módulos jurídicos confirmados no backend."
      bullets={[
        `Environment: ${environment}`,
        `API URL: ${apiUrl}`,
        `Healthcheck backend: ${health?.status ?? "indisponível"}`,
        `Backend reachable: ${reachable ? "sim" : "não"}`,
        `Organização ativa: ${organization?.name ?? "não selecionada"}`,
        "Worker Celery no staging público continua pendente no plano atual.",
        "Checkout, webhook comercial e subscription enforcement continuam pendentes.",
      ]}
    />
  );
}
