import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ModuleStateCard } from "@/components/shared/module-state-card";

export default function CasesPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Processos"
          description="Base da gestão de processos jurídicos, preparada para filtros, listagem e criação orientada por tenant."
        />
        <ModuleStateCard
          title="Casos jurídicos"
          status="active"
          description="O backend expõe `/api/v1/cases/`; a UI final será construída sobre esta foundation."
          bullets={["Estados loading/empty/error preparados.", "Formulários Zod já iniciados."]}
        />
      </div>
    </AppShell>
  );
}
