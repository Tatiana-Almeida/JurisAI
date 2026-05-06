"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { OCRAuditLogTable } from "@/components/ocr/ocr-audit-log-table";
import { OCRJobTable } from "@/components/ocr/ocr-job-table";
import { OCRResultCard } from "@/components/ocr/ocr-result-card";
import { OCRSettingsPanel } from "@/components/ocr/ocr-settings-panel";
import { PageResultsTable } from "@/components/ocr/page-results-table";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import {
  useApplyOCRResult,
  useOCRAuditLogs,
  useOCRJobs,
  useOCRPageResults,
  useOCRResults,
  useOCRSettings,
} from "@/hooks/use-jurisai-queries";

export default function OCRPage() {
  const jobsQuery = useOCRJobs();
  const resultsQuery = useOCRResults();
  const settingsQuery = useOCRSettings();
  const logsQuery = useOCRAuditLogs();
  const firstResult = resultsQuery.data?.[0];
  const pageResultsQuery = useOCRPageResults(firstResult?.id);
  const applyResult = useApplyOCRResult();

  if (jobsQuery.isLoading || resultsQuery.isLoading || settingsQuery.isLoading) {
    return (
      <AppShell>
        <LoadingSkeleton />
      </AppShell>
    );
  }

  if (jobsQuery.isError || resultsQuery.isError || settingsQuery.isError) {
    return (
      <AppShell>
        <ModuleErrorState
          moduleName="OCR"
          description="Verifique permissões, organização ativa e configuração do backend."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="OCR"
          description="Jobs, resultados, page-level OCR, audit trail e limites por tenant com polling para execuções em curso."
        />
        <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <OCRJobTable jobs={jobsQuery.data ?? []} />
          <OCRSettingsPanel settings={settingsQuery.data} />
        </div>
        <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
          {firstResult ? (
            <OCRResultCard
              result={firstResult}
              onApply={() => applyResult.mutate(firstResult.id)}
            />
          ) : (
            <ModuleErrorState
              moduleName="resultado OCR"
              title="Sem resultados de OCR"
              description="Execute OCR sobre um documento para ver texto extraído e aplicação ao documento."
            />
          )}
          <PageResultsTable pages={pageResultsQuery.data ?? []} />
        </div>
        <OCRAuditLogTable logs={logsQuery.data ?? []} />
      </div>
    </AppShell>
  );
}
