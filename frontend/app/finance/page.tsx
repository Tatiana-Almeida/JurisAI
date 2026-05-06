"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { FinanceSummaryCard } from "@/components/finance/finance-summary";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useFinanceExpenses, useFinanceInvoices, useFinanceSummary } from "@/hooks/use-jurisai-queries";

export default function FinancePage() {
  const summaryQuery = useFinanceSummary();
  const invoicesQuery = useFinanceInvoices();
  const expensesQuery = useFinanceExpenses();

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Financeiro"
          description="Resumo financeiro ligado ao backend legal-finance. Onde faltar fluxo operacional, a UI mantém estado de preparação."
        />
        {summaryQuery.isLoading || invoicesQuery.isLoading || expensesQuery.isLoading ? (
          <LoadingSkeleton />
        ) : null}
        {summaryQuery.isError || invoicesQuery.isError || expensesQuery.isError ? (
          <ErrorState
            title="Não foi possível carregar o financeiro"
            description="Confirme autenticação e disponibilidade dos endpoints de legal finance."
          />
        ) : null}
        {invoicesQuery.data && expensesQuery.data ? (
          <FinanceSummaryCard
            summary={summaryQuery.data}
            invoices={invoicesQuery.data}
            expenses={expensesQuery.data}
          />
        ) : null}
      </div>
    </AppShell>
  );
}
