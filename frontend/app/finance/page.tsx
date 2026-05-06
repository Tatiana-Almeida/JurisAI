import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ModuleStateCard } from "@/components/shared/module-state-card";

export default function FinancePage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Financeiro"
          description="Área preparada para resumir invoices, payments e indicadores do módulo legal-finance."
        />
        <ModuleStateCard
          title="Legal finance"
          status="active"
          description="O backend já expõe summary, invoices e payments em legal-finance."
          bullets={["Pronto para Recharts e tabelas TanStack.", "Sem misturar com billing comercial."]}
        />
      </div>
    </AppShell>
  );
}
