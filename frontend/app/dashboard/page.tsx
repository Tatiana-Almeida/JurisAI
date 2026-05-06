"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ActivityFeed } from "@/components/dashboard/activity-feed";
import { MetricCard } from "@/components/dashboard/metric-card";
import { RecentCases } from "@/components/dashboard/recent-cases";
import { SystemStatusCard } from "@/components/dashboard/system-status-card";
import { UpcomingDeadlines } from "@/components/dashboard/upcoming-deadlines";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { OfflineApiState } from "@/components/shared/offline-api-state";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import {
  useCases,
  useDashboardDeadlines,
  useDashboardDocuments,
  useDashboardFinancial,
  useDashboardSummary,
  useHealthStatus,
  useOCRJobs,
} from "@/hooks/use-jurisai-queries";
import { getApiBaseUrl } from "@/lib/api/client";

export default function DashboardPage() {
  const { activeOrganization } = useActiveOrganization();
  const apiUrl = getApiBaseUrl();
  const environment = process.env.NEXT_PUBLIC_ENVIRONMENT || "development";
  const healthQuery = useHealthStatus();
  const summaryQuery = useDashboardSummary();
  const deadlinesQuery = useDashboardDeadlines();
  const documentsQuery = useDashboardDocuments();
  const financialQuery = useDashboardFinancial();
  const casesQuery = useCases();
  const ocrJobsQuery = useOCRJobs({ status: "pending" });

  const isLoading =
    summaryQuery.isLoading || deadlinesQuery.isLoading || documentsQuery.isLoading;

  if (isLoading) {
    return (
      <AppShell>
        <LoadingSkeleton />
      </AppShell>
    );
  }

  if (summaryQuery.isError) {
    return (
      <AppShell>
        {healthQuery.isError ? (
          <OfflineApiState apiUrl={apiUrl} />
        ) : (
          <ModuleErrorState
            moduleName="dashboard"
            description="Verifique autenticação, organização ativa e disponibilidade dos endpoints de dashboard."
          />
        )}
      </AppShell>
    );
  }

  const summary = summaryQuery.data;

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Dashboard"
          description="Visão operacional inicial do JurisAI com healthcheck, multi-tenancy e módulos jurídicos ligados aos endpoints reais do backend."
        />
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard
            title="Processos"
            value={summary?.total_cases ?? 0}
            hint={`${summary?.active_cases ?? 0} ativos`}
          />
          <MetricCard
            title="Documentos"
            value={summary?.total_documents ?? 0}
            hint="Documentos da organização ativa"
          />
          <MetricCard
            title="Prazos próximos"
            value={summary?.upcoming_deadlines ?? 0}
            hint={`${summary?.overdue_deadlines ?? 0} em atraso`}
          />
          <MetricCard
            title="Faturas pendentes"
            value={summary?.pending_invoices ?? 0}
            hint={`${financialQuery.data?.paid_invoices ?? 0} pagas`}
          />
        </div>
        <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
          <RecentCases cases={casesQuery.data ?? []} />
          <SystemStatusCard
            health={healthQuery.data}
            organization={activeOrganization}
            apiUrl={apiUrl}
            environment={environment}
            reachable={!healthQuery.isError}
          />
        </div>
        <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
          <UpcomingDeadlines deadlines={deadlinesQuery.data ?? []} />
          <ActivityFeed documents={documentsQuery.data ?? []} jobs={ocrJobsQuery.data ?? []} />
        </div>
      </div>
    </AppShell>
  );
}
