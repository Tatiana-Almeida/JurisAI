import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ModuleStateCard } from "@/components/shared/module-state-card";

export default function SettingsPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Configurações"
          description="Settings UI preparada para tenant, tema, OCR e RAG sem acoplar promessas não confirmadas."
        />
        <ModuleStateCard
          title="Tenant settings"
          status="partial"
          description="A base do frontend já está pronta para settings por organização."
          bullets={["Dark mode e theme provider ativos.", "RAG/OCR settings entram na fase de integração."]}
        />
      </div>
    </AppShell>
  );
}
