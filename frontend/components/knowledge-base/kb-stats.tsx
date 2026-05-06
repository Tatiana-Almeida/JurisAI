import { ModuleStateCard } from "@/components/shared/module-state-card";

export function KBStats() {
  return (
    <ModuleStateCard
      title="Knowledge base stats"
      status="active"
      description="Foundation preparada para métricas como total de documentos, chunks e queries."
      bullets={[
        "Consumo esperado do endpoint /stats/ por base.",
        "Cards prontos para combinação com Recharts.",
      ]}
    />
  );
}
