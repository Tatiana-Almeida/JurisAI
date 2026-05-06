"use client";

import { useParams } from "next/navigation";
import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { IndexingJobsTable } from "@/components/knowledge-base/indexing-jobs-table";
import { KBAsk } from "@/components/knowledge-base/kb-ask";
import { KBStats } from "@/components/knowledge-base/kb-stats";
import { SourcesList } from "@/components/knowledge-base/sources-list";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { useIndexingJobs, useKnowledgeBase, useRetrievalQueries } from "@/hooks/use-jurisai-queries";

export default function KnowledgeBaseDetailPage() {
  const params = useParams<{ id: string }>();
  const knowledgeBaseQuery = useKnowledgeBase(params.id);
  const indexingJobsQuery = useIndexingJobs({ knowledge_base_id: params.id });
  const retrievalQueriesQuery = useRetrievalQueries({ knowledge_base_id: params.id });
  const latestQuery = retrievalQueriesQuery.data?.[0];

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
          title="Knowledge Base não encontrada"
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
          description={knowledgeBaseQuery.data.description || "Base de conhecimento jurídica da organização ativa."}
        />
        <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
          <KBStats />
          <KBAsk knowledgeBaseId={params.id} />
        </div>
        <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
          <IndexingJobsTable jobs={indexingJobsQuery.data ?? []} />
          <SourcesList sources={latestQuery?.sources_payload ?? []} />
        </div>
      </div>
    </AppShell>
  );
}
