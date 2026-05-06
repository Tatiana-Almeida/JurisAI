import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ModuleStateCard } from "@/components/shared/module-state-card";

export default function ClientsPage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Clientes"
          description="Foundation da área de clientes sem inventar endpoints dedicados que o backend ainda não prova."
        />
        <ModuleStateCard
          title="Clientes / utilizadores"
          status="partial"
          description="A camada comercial de clientes precisa de definição mais fina; a base atual parte do módulo de utilizadores."
          bullets={[
            "Sem endpoint dedicado de clients confirmado nesta fase.",
            "A UI final deverá alinhar com os contratos reais do backend.",
          ]}
        />
      </div>
    </AppShell>
  );
}
