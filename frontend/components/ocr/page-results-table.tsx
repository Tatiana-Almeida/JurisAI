import { ModuleStateCard } from "@/components/shared/module-state-card";

export function PageResultsTable() {
  return (
    <ModuleStateCard
      title="Page results"
      status="partial"
      description="Foundation para OCR página a página e observabilidade por tenant."
      bullets={[
        "Suporta pageNumber e output truncation no modelo.",
        "Ligação real ao backend fica para a próxima fase.",
      ]}
    />
  );
}
