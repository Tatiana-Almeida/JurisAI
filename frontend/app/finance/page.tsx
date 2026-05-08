"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { FinanceSummaryCard } from "@/components/finance/finance-summary";
import { EmptyState } from "@/components/shared/empty-state";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleStateCard } from "@/components/shared/module-state-card";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useFinanceExpenses, useFinanceInvoices, useFinanceSummary } from "@/hooks/use-finance";

export default function FinancePage() {
  const { activeOrganizationId } = useActiveOrganization();
  const summaryQuery = useFinanceSummary();
  const invoicesQuery = useFinanceInvoices({ ordering: "-created_at" });
  const expensesQuery = useFinanceExpenses({ ordering: "-created_at" });

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para visualizar o financeiro juridico."
        />
      </AppShell>
    );
  }

  const hasData = Boolean((invoicesQuery.data?.length ?? 0) > 0 || (expensesQuery.data?.length ?? 0) > 0);

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Financeiro"
          description="Resumo financeiro ligado ao backend legal-finance. Onde faltar fluxo operacional, a UI mantem estado de preparacao."
        />
        {summaryQuery.isLoading || invoicesQuery.isLoading || expensesQuery.isLoading ? (
          <LoadingSkeleton />
        ) : null}
        {summaryQuery.isError || invoicesQuery.isError || expensesQuery.isError ? (
          <ErrorState
            title="Nao foi possivel carregar o financeiro"
            description="Confirme autenticacao, organizacao ativa e disponibilidade dos endpoints de legal finance."
          />
        ) : null}
        {!summaryQuery.isLoading && !summaryQuery.isError && !hasData ? (
          <ModuleStateCard
            title="Financeiro em preparacao operacional"
            status="partial"
            description="Os endpoints reais existem, mas esta organizacao ainda pode nao ter faturas ou despesas suficientes para uma operacao financeira completa."
            bullets={[
              "Resumo financeiro real ja usa /api/v1/legal-finance/summary/.",
              "Faturas e despesas continuam dependentes dos dados do tenant ativo.",
            ]}
          />
        ) : null}
        {!summaryQuery.isLoading && !summaryQuery.isError && hasData ? (
          <FinanceSummaryCard
            summary={summaryQuery.data}
            invoices={invoicesQuery.data ?? []}
            expenses={expensesQuery.data ?? []}
          />
        ) : null}
      </div>
    </AppShell>
  );
}
