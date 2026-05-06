import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { CaseForm } from "@/components/cases/case-form";

export default function NewCasePage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Novo processo"
          description="Criação de processo respeitando cliente, advogado, organização ativa e validações DRF."
        />
        <CaseForm />
      </div>
    </AppShell>
  );
}
