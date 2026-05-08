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
      description="O frontend consome healthcheck real, contexto multi-tenant e modulos juridicos confirmados no backend."
      bullets={[
        `Environment: ${environment}`,
        `API URL: ${apiUrl}`,
        `Healthcheck backend: ${health?.status ?? "indisponivel"}`,
        `Backend reachable: ${reachable ? "sim" : "nao"}`,
        `Organizacao ativa: ${organization?.name ?? "nao selecionada"}`,
        "Worker Celery pendente no Render Free para jobs assincronos reais.",
        "Checkout, webhooks comerciais e bloqueio por plano continuam pendentes.",
      ]}
    />
  );
}
