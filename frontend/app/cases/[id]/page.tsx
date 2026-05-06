"use client";

import { useParams } from "next/navigation";
import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { CaseStatusBadge } from "@/components/cases/case-status-badge";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useCase } from "@/hooks/use-jurisai-queries";

export default function CaseDetailPage() {
  const params = useParams<{ id: string }>();
  const caseQuery = useCase(params.id);

  if (caseQuery.isLoading) {
    return (
      <AppShell>
        <LoadingSkeleton />
      </AppShell>
    );
  }

  if (caseQuery.isError || !caseQuery.data) {
    return (
      <AppShell>
        <ErrorState
          title="Processo não encontrado"
          description="Confirme o identificador do processo e a disponibilidade do backend."
        />
      </AppShell>
    );
  }

  const lawCase = caseQuery.data;

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title={lawCase.title}
          description={lawCase.description || "Sem descrição detalhada para este processo."}
          actions={<CaseStatusBadge status={lawCase.status} />}
        />
        <div className="jurisai-panel rounded-3xl p-6 text-sm text-muted-foreground">
          Cliente: {lawCase.client?.name ?? "N/D"} · Advogado: {lawCase.lawyer?.name ?? "N/D"} · Organização: {lawCase.organization_id ?? "N/D"}
        </div>
      </div>
    </AppShell>
  );
}
