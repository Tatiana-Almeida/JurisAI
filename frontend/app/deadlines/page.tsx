import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ModuleStateCard } from "@/components/shared/module-state-card";

export default function DeadlinesPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Prazos"
          description="Foundation para prazos processuais com foco em clareza operacional e estados vazios seguros."
        />
        <ModuleStateCard
          title="Deadlines"
          status="active"
          description="O backend já expõe deadlines; a tela final ligará filtros, calendário e estados de urgência."
          bullets={["Endpoint real confirmado.", "Componentização final entra no próximo prompt."]}
        />
      </div>
    </AppShell>
  );
}
