import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";

export default function NewCasePage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Novo processo"
          description="A fundação do formulário está pronta, mas a experiência final de criação entra no próximo ciclo."
        />
        <EmptyState
          title="Formulário de caso em preparação"
          description="Schemas, stores e infraestrutura estão prontos para receber a implementação final."
        />
      </div>
    </AppShell>
  );
}
