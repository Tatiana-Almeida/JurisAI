import { ModuleStateCard } from "@/components/shared/module-state-card";

export function KBList() {
  return (
    <ModuleStateCard
      title="Knowledge bases"
      status="active"
      description="O backend já expõe bases, documentos, chunks e jobs; a UI base já está pronta."
      bullets={[
        "Listagem multi-tenant será ligada via TanStack Query.",
        "Estados loading/empty/error já previstos na fundação.",
      ]}
    />
  );
}
