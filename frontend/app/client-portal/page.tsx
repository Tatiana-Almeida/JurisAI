import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ModuleStateCard } from "@/components/shared/module-state-card";

export default function ClientPortalPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Portal do Cliente"
          description="Foundation do portal do cliente com posicionamento cuidadoso para casos, documentos e mensagens."
        />
        <ModuleStateCard
          title="Client portal"
          status="partial"
          description="Casos e documentos já têm endpoints confirmados. Mensagens precisam de validação adicional antes de UX final."
          bullets={[
            "Base visual preparada.",
            "Sem prometer onboarding final ainda.",
          ]}
        />
      </div>
    </AppShell>
  );
}
