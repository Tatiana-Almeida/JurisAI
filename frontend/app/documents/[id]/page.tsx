"use client";

import { useMemo } from "react";
import { useParams, useRouter } from "next/navigation";
import { toast } from "sonner";
import { AppShell } from "@/components/layout/app-shell";
import { DocumentDetail } from "@/components/documents/document-detail";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useDocument } from "@/hooks/use-documents";
import {
  useApplyOCRResult,
  useOCRJobs,
  useOCRPipelines,
  useOCRResults,
  useRunAdvancedOCR,
  useRunOCR,
  useRunOCRToKnowledgeBasePipeline,
} from "@/hooks/use-ocr";
import { useKnowledgeBases } from "@/hooks/use-knowledge-base";
import { getDRFErrorMessage } from "@/lib/errors/drf";

export default function DocumentDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const { activeOrganizationId } = useActiveOrganization();
  const documentQuery = useDocument(params.id);
  const knowledgeBasesQuery = useKnowledgeBases();
  const jobsQuery = useOCRJobs({ document_id: params.id });
  const resultsQuery = useOCRResults({ document_id: params.id });
  const pipelinesQuery = useOCRPipelines({ document_id: params.id });
  const runOCR = useRunOCR();
  const runAdvancedOCR = useRunAdvancedOCR();
  const applyResult = useApplyOCRResult();
  const runPipeline = useRunOCRToKnowledgeBasePipeline();

  const latestJob = useMemo(() => jobsQuery.data?.[0], [jobsQuery.data]);
  const latestResult = useMemo(() => resultsQuery.data?.[0], [resultsQuery.data]);
  const latestPipeline = useMemo(() => pipelinesQuery.data?.[0], [pipelinesQuery.data]);
  const firstKnowledgeBase = knowledgeBasesQuery.data?.[0];

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para visualizar este documento."
        />
      </AppShell>
    );
  }

  if (documentQuery.isLoading) {
    return (
      <AppShell>
        <LoadingSkeleton />
      </AppShell>
    );
  }

  if (documentQuery.isError || !documentQuery.data) {
    return (
      <AppShell>
        <ModuleErrorState
          moduleName="documento"
          title="Documento nao encontrado"
          description="Confirme o identificador do documento e a disponibilidade do backend."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Detalhe do documento"
          description="Fluxo real documento → OCR → resultado → Document.content → Knowledge Base."
        />
        <DocumentDetail
          document={documentQuery.data}
          latestJob={latestJob}
          latestResult={latestResult}
          latestPipeline={latestPipeline}
          isRunningOCR={runOCR.isPending}
          isRunningAdvancedOCR={runAdvancedOCR.isPending}
          isApplyingOCR={applyResult.isPending}
          isRunningPipeline={runPipeline.isPending}
          onRunOCR={async () => {
            try {
              await runOCR.mutateAsync(documentQuery.data!.id);
              router.push(`/ocr?document=${documentQuery.data!.id}`);
            } catch (error) {
              toast.error("Nao foi possivel iniciar OCR para este documento.", {
                description: getDRFErrorMessage(error),
              });
            }
          }}
          onRunAdvancedOCR={async () => {
            try {
              await runAdvancedOCR.mutateAsync(documentQuery.data!.id);
              router.push(`/ocr?document=${documentQuery.data!.id}`);
            } catch (error) {
              toast.error("Nao foi possivel iniciar OCR avancado para este documento.", {
                description: getDRFErrorMessage(error),
              });
            }
          }}
          onApplyOCRResult={async () => {
            if (!latestResult) {
              toast.error("Ainda nao existe resultado OCR para aplicar.");
              return;
            }

            try {
              await applyResult.mutateAsync(latestResult.id);
              await documentQuery.refetch();
            } catch (error) {
              toast.error("Nao foi possivel aplicar o resultado OCR ao documento.", {
                description: getDRFErrorMessage(error),
              });
            }
          }}
          onRunPipeline={async () => {
            if (!firstKnowledgeBase) {
              toast.error("Nenhuma Knowledge Base disponivel para este tenant.");
              return;
            }

            try {
              await runPipeline.mutateAsync({
                document_id: documentQuery.data!.id,
                knowledge_base_id: firstKnowledgeBase.id,
                update_document_content: true,
              });
              router.push(`/knowledge-base/${firstKnowledgeBase.id}`);
            } catch (error) {
              toast.error("Nao foi possivel iniciar o pipeline OCR para Knowledge Base.", {
                description: getDRFErrorMessage(error),
              });
            }
          }}
        />
      </div>
    </AppShell>
  );
}
