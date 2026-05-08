"use client";

import { useMemo, useState } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { OCRAuditLogTable } from "@/components/ocr/ocr-audit-log-table";
import { OCRJobTable } from "@/components/ocr/ocr-job-table";
import { OCRPipelineCard } from "@/components/ocr/ocr-pipeline-card";
import { OCRResultCard } from "@/components/ocr/ocr-result-card";
import { OCRSettingsPanel } from "@/components/ocr/ocr-settings-panel";
import { PageResultsTable } from "@/components/ocr/page-results-table";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import {
  useApplyOCRResult,
  useOCRAuditLogs,
  useOCRJobs,
  useOCRPageResults,
  useOCRPipelines,
  useOCRResultPages,
  useOCRResults,
  useOCRSettings,
} from "@/hooks/use-ocr";

type OCRPageClientProps = {
  documentId?: string;
};

export function OCRPageClient({ documentId }: OCRPageClientProps) {
  const { activeOrganizationId } = useActiveOrganization();
  const [activeTab, setActiveTab] = useState("jobs");
  const [selectedResultId, setSelectedResultId] = useState<string | undefined>();
  const jobsQuery = useOCRJobs(documentId ? { document_id: documentId } : undefined);
  const resultsQuery = useOCRResults(documentId ? { document_id: documentId } : undefined);
  const settingsQuery = useOCRSettings();
  const logsQuery = useOCRAuditLogs(documentId ? { document_id: documentId } : undefined);
  const pageResultsQuery = useOCRPageResults(documentId ? { document_id: documentId } : undefined);
  const pipelinesQuery = useOCRPipelines(documentId ? { document_id: documentId } : undefined);
  const applyResult = useApplyOCRResult();

  const focusedResultId = selectedResultId ?? resultsQuery.data?.[0]?.id;
  const resultPagesQuery = useOCRResultPages(focusedResultId);
  const focusedResult = useMemo(
    () => resultsQuery.data?.find((item) => item.id === focusedResultId) ?? resultsQuery.data?.[0],
    [focusedResultId, resultsQuery.data],
  );

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para visualizar jobs, resultados, logs e pipelines de OCR."
        />
      </AppShell>
    );
  }

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
          description="Verifique permissoes, organizacao ativa, worker Celery e configuracao do backend."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="OCR"
          description="Fluxos reais de jobs, resultados, OCR por pagina, audit trail, settings e pipeline OCR para Knowledge Base."
        />
        <div className="rounded-2xl border border-primary/20 bg-primary/5 p-4 text-sm text-muted-foreground">
          Em staging publico no Render Free, o worker Celery pode continuar indisponivel. Se os
          jobs nao avancarem de `pending` ou falharem, confirme primeiro a infraestrutura do worker.
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList variant="line" className="flex flex-wrap">
            <TabsTrigger value="jobs">Jobs</TabsTrigger>
            <TabsTrigger value="results">Results</TabsTrigger>
            <TabsTrigger value="page-results">Page Results</TabsTrigger>
            <TabsTrigger value="audit-logs">Audit Logs</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
            <TabsTrigger value="pipelines">Pipelines</TabsTrigger>
          </TabsList>

          <TabsContent value="jobs">
            <OCRJobTable jobs={jobsQuery.data ?? []} />
          </TabsContent>

          <TabsContent value="results" className="space-y-6">
            {resultsQuery.data?.length ? (
              <div className="grid gap-4 xl:grid-cols-[0.35fr_0.65fr]">
                <div className="space-y-3">
                  {resultsQuery.data.map((result) => (
                    <button
                      key={result.id}
                      type="button"
                      onClick={() => setSelectedResultId(result.id)}
                      className={`w-full rounded-2xl border p-4 text-left text-sm transition-colors ${
                        focusedResult?.id === result.id
                          ? "border-primary/50 bg-primary/5"
                          : "border-border/60 hover:border-primary/30"
                      }`}
                    >
                      <div className="font-medium">Resultado {result.id.slice(0, 8)}</div>
                      <div className="mt-1 text-muted-foreground">
                        documento={result.document_id ?? result.document ?? "n/d"} · chars={result.char_count ?? 0}
                      </div>
                    </button>
                  ))}
                </div>
                {focusedResult ? (
                  <OCRResultCard
                    result={focusedResult}
                    isApplying={applyResult.isPending}
                    onApply={() => applyResult.mutate(focusedResult.id)}
                    onViewPages={() => {
                      setSelectedResultId(focusedResult.id);
                      setActiveTab("page-results");
                    }}
                    onSendToKnowledgeBase={() => setActiveTab("pipelines")}
                  />
                ) : null}
              </div>
            ) : (
              <EmptyState
                title="Sem resultados de OCR"
                description="Execute OCR sobre um documento para ver texto extraido e aplicacao ao documento."
              />
            )}
          </TabsContent>

          <TabsContent value="page-results" className="space-y-6">
            {focusedResultId ? (
              <div className="rounded-2xl border border-border/60 p-4 text-sm text-muted-foreground">
                A mostrar paginas do resultado {focusedResultId.slice(0, 8)}.
              </div>
            ) : null}
            <PageResultsTable pages={focusedResultId ? resultPagesQuery.data ?? [] : pageResultsQuery.data ?? []} />
          </TabsContent>

          <TabsContent value="audit-logs">
            <OCRAuditLogTable logs={logsQuery.data ?? []} />
          </TabsContent>

          <TabsContent value="settings">
            <OCRSettingsPanel settings={settingsQuery.data} />
          </TabsContent>

          <TabsContent value="pipelines">
            <OCRPipelineCard initialDocumentId={documentId} latestRun={pipelinesQuery.data?.[0]} />
          </TabsContent>
        </Tabs>
      </div>
    </AppShell>
  );
}
