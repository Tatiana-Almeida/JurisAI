import { ModuleStateCard } from "@/components/shared/module-state-card";

export function IndexingJobsTable() {
  return (
    <ModuleStateCard
      title="Indexing jobs"
      status="active"
      description="Observabilidade do knowledge base já modelada no backend."
      bullets={[
        "Tabela preparada para status, chunks_created e chunks_deleted.",
        "Ligação real entra no prompt seguinte.",
      ]}
    />
  );
}
