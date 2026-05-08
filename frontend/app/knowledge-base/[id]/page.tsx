"use client";

import { useParams } from "next/navigation";
import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { IndexingJobsTable } from "@/components/knowledge-base/indexing-jobs-table";
import { KBAsk } from "@/components/knowledge-base/kb-ask";
import { KBSearch } from "@/components/knowledge-base/kb-search";
import { KBStats } from "@/components/knowledge-base/kb-stats";
import { RAGSettingsPanel } from "@/components/knowledge-base/rag-settings-panel";
import { SourcesList } from "@/components/knowledge-base/sources-list";
import { EmptyState } from "@/components/shared/empty-state";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import {
  useEmbeddingAuditLogs,
  useIndexingJobs,
  useKnowledgeBase,
  useKnowledgeBaseStats,
  useKnowledgeDocuments,
  useRAGSettings,
  useRetrievalQueries,
} from "@/hooks/use-knowledge-base";

export default function KnowledgeBaseDetailPage() {
  const params = useParams<{ id: string }>();
  const { activeOrganizationId } = useActiveOrganization();
  const knowledgeBaseQuery = useKnowledgeBase(params.id);
  const statsQuery = useKnowledgeBaseStats(params.id);
  const indexingJobsQuery = useIndexingJobs({ knowledge_base_id: params.id });
  const retrievalQueriesQuery = useRetrievalQueries({ knowledge_base_id: params.id });
  const knowledgeDocumentsQuery = useKnowledgeDocuments({ knowledge_base_id: params.id });
  const ragSettingsQuery = useRAGSettings();
  const embeddingAuditLogsQuery = useEmbeddingAuditLogs();
  const latestQuery = retrievalQueriesQuery.data?.[0];

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para visualizar esta Knowledge Base."
        />
      </AppShell>
    );
  }

  if (knowledgeBaseQuery.isLoading) {
    return (
      <AppShell>
        <LoadingSkeleton />
      </AppShell>
    );
  }

  if (knowledgeBaseQuery.isError || !knowledgeBaseQuery.data) {
    return (
      <AppShell>
        <ErrorState
          title="Knowledge Base nao encontrada"
          description="Confirme o identificador e a disponibilidade do backend."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title={knowledgeBaseQuery.data.name}
          description={
            knowledgeBaseQuery.data.description ||
            "Base de conhecimento juridica da organizacao ativa."
          }
        />

        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList variant="line" className="flex flex-wrap">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="search">Search</TabsTrigger>
            <TabsTrigger value="ask">Ask</TabsTrigger>
            <TabsTrigger value="documents">Documents</TabsTrigger>
            <TabsTrigger value="indexing-jobs">Indexing Jobs</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
            <TabsTrigger value="audit-logs">Audit Logs</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="grid gap-6 xl:grid-cols-[1fr_1fr]">
            <KBStats stats={statsQuery.data} />
            <SourcesList
              sources={latestQuery?.sources_payload?.sources ?? []}
              confidence={latestQuery?.sources_payload?.confidence}
              retrievalMethod={latestQuery?.sources_payload?.retrieval_method}
              fallbackUsed={latestQuery?.sources_payload?.fallback_used}
              fallbackReason={latestQuery?.sources_payload?.fallback_reason}
            />
          </TabsContent>

          <TabsContent value="search">
            <KBSearch knowledgeBaseId={params.id} />
          </TabsContent>

          <TabsContent value="ask">
            <KBAsk knowledgeBaseId={params.id} />
          </TabsContent>

          <TabsContent value="documents">
            {knowledgeDocumentsQuery.data?.length ? (
              <div className="grid gap-4">
                {knowledgeDocumentsQuery.data.map((document) => (
                  <div key={document.id} className="rounded-2xl border border-border/60 p-4 text-sm">
                    <div className="font-medium">{document.title}</div>
                    <div className="mt-1 text-muted-foreground">
                      status={document.status ?? "n/d"} · source_type={document.source_type ?? "n/d"} ·
                      document_id={document.document_id ?? "n/d"}
                    </div>
                    {document.error_message ? (
                      <p className="mt-2 text-destructive">{document.error_message}</p>
                    ) : null}
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                title="Sem documentos indexados"
                description="Assim que os documentos forem ligados a esta Knowledge Base, eles aparecem aqui."
              />
            )}
          </TabsContent>

          <TabsContent value="indexing-jobs">
            <IndexingJobsTable jobs={indexingJobsQuery.data ?? []} />
          </TabsContent>

          <TabsContent value="settings">
            <RAGSettingsPanel settings={ragSettingsQuery.data} />
          </TabsContent>

          <TabsContent value="audit-logs">
            {embeddingAuditLogsQuery.data?.length ? (
              <div className="space-y-4">
                {embeddingAuditLogsQuery.data.map((log) => (
                  <div key={log.id} className="rounded-2xl border border-border/60 p-4 text-sm">
                    <div className="font-medium">
                      {log.action ?? "embedding"} · {log.status ?? "n/d"}
                    </div>
                    <div className="mt-1 text-muted-foreground">
                      provider={log.provider ?? "n/d"} · model={log.model ?? "n/d"} ·
                      knowledge_document={log.knowledge_document ?? "n/d"}
                    </div>
                    {log.reason ? <p className="mt-2 text-destructive">{log.reason}</p> : null}
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                title="Sem audit logs de embeddings"
                description="Os logs de embeddings aparecem aqui quando houver indexacao ou reprocessamento."
              />
            )}
          </TabsContent>
        </Tabs>
      </div>
    </AppShell>
  );
}
