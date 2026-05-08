"use client";

import { useMemo, useState } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { DeadlinesTable } from "@/components/deadlines/deadlines-table";
import { EmptyState } from "@/components/shared/empty-state";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useDeadlines } from "@/hooks/use-deadlines";
import type { DeadlineFilterStatus } from "@/types/deadlines";

export default function DeadlinesPage() {
  const { activeOrganizationId } = useActiveOrganization();
  const [statusFilter, setStatusFilter] = useState<DeadlineFilterStatus>("all");
  const [upcomingDays, setUpcomingDays] = useState("30");
  const deadlinesQuery = useDeadlines(
    upcomingDays ? { upcoming_days: upcomingDays, ordering: "due_date" } : { ordering: "due_date" },
  );

  const filteredDeadlines = useMemo(() => {
    const rows = deadlinesQuery.data ?? [];
    if (statusFilter === "all") {
      return rows;
    }
    if (statusFilter === "completed") {
      return rows.filter((item) => item.completed);
    }
    if (statusFilter === "overdue") {
      return rows.filter((item) => item.is_overdue && !item.completed);
    }
    if (statusFilter === "critical") {
      return rows.filter(
        (item) =>
          !item.completed &&
          !item.is_overdue &&
          typeof item.days_remaining === "number" &&
          item.days_remaining <= 3,
      );
    }
    return rows.filter((item) => !item.completed && !item.is_overdue);
  }, [deadlinesQuery.data, statusFilter]);

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para visualizar os prazos juridicos deste modulo."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Prazos"
          description="Listagem real de prazos com filtros por estado, janela de proximidade e destaque visual para itens criticos."
        />
        <div className="flex flex-wrap gap-3 rounded-3xl border border-border/60 p-4">
          <select
            className="rounded-lg border border-input bg-transparent px-3 py-2 text-sm"
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value as DeadlineFilterStatus)}
          >
            <option value="all">Todos</option>
            <option value="pending">Pendentes</option>
            <option value="critical">Criticos</option>
            <option value="overdue">Em atraso</option>
            <option value="completed">Concluidos</option>
          </select>
          <input
            type="number"
            min="1"
            className="w-36 rounded-lg border border-input bg-transparent px-3 py-2 text-sm"
            value={upcomingDays}
            onChange={(event) => setUpcomingDays(event.target.value)}
            placeholder="Próximos dias"
          />
        </div>
        {deadlinesQuery.isLoading ? <LoadingSkeleton /> : null}
        {deadlinesQuery.isError ? (
          <ErrorState
            title="Nao foi possivel carregar prazos"
            description="Confirme autenticacao, organizacao ativa e disponibilidade do endpoint `/api/v1/deadlines/`."
          />
        ) : null}
        {!deadlinesQuery.isLoading && !deadlinesQuery.isError ? (
          <DeadlinesTable deadlines={filteredDeadlines} />
        ) : null}
      </div>
    </AppShell>
  );
}
