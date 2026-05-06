"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { DeadlinesTable } from "@/components/deadlines/deadlines-table";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useDeadlines } from "@/hooks/use-jurisai-queries";

export default function DeadlinesPage() {
  const deadlinesQuery = useDeadlines();

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Prazos"
          description="Tabela de prazos com risco visual, datas próximas e alinhamento ao endpoint real `/api/v1/deadlines/`."
        />
        {deadlinesQuery.isLoading ? <LoadingSkeleton /> : null}
        {deadlinesQuery.isError ? (
          <ErrorState
            title="Não foi possível carregar prazos"
            description="Confirme autenticação e disponibilidade do endpoint de prazos."
          />
        ) : null}
        {deadlinesQuery.data ? <DeadlinesTable deadlines={deadlinesQuery.data} /> : null}
      </div>
    </AppShell>
  );
}
