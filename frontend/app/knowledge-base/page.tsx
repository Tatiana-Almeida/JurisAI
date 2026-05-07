"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { IndexingJobsTable } from "@/components/knowledge-base/indexing-jobs-table";
import { KBList } from "@/components/knowledge-base/kb-list";
import { KBStats } from "@/components/knowledge-base/kb-stats";
import { RAGSettingsPanel } from "@/components/knowledge-base/rag-settings-panel";
import { EmptyState } from "@/components/shared/empty-state";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import { useActiveOrganization } from "@/hooks/use-active-organization";
import { useIndexingJobs, useKnowledgeBases, useKnowledgeBaseStats, useRAGSettings } from "@/hooks/use-knowledge-base";

export default function KnowledgeBasePage() {
  const { activeOrganizationId } = useActiveOrganization();
  const knowledgeBasesQuery = useKnowledgeBases();
  const firstBase = knowledgeBasesQuery.data?.[0];
  const statsQuery = useKnowledgeBaseStats(firstBase?.id);
  const settingsQuery = useRAGSettings();
  const indexingJobsQuery = useIndexingJobs(firstBase?.id ? { knowledge_base_id: firstBase.id } : undefined);

  if (!activeOrganizationId) {
    return (
      <AppShell>
        <EmptyState
          title="Selecione uma organizacao"
          description="Selecione uma organizacao para consultar a Knowledge Base do tenant ativo."
        />
      </AppShell>
    );
  }

  if (knowledgeBasesQuery.isLoading || settingsQuery.isLoading) {
    return (
      <AppShell>
        <LoadingSkeleton />
      </AppShell>
    );
  }

  if (knowledgeBasesQuery.isError || settingsQuery.isError) {
    return (
      <AppShell>
        <ModuleErrorState
          moduleName="knowledge base"
          description="Confirme autenticacao, organizacao ativa e endpoints de RAG."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Knowledge Base"
          description="Busca e perguntas com fontes, confianca, retrieval method e alerta honesto sobre a limitacao do local-hash-v1."
        />
        <div className="rounded-2xl border border-primary/20 bg-primary/5 p-4 text-sm text-muted-foreground">
          Sem provider semantico externo, o tenant pode operar em modo local-hash-v1. Isso valida o pipeline, mas nao substitui embeddings semanticos avancados.
        </div>
        <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
          <KBList knowledgeBases={knowledgeBasesQuery.data ?? []} />
          <RAGSettingsPanel settings={settingsQuery.data} />
        </div>
        {firstBase ? (
          <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
            <KBStats stats={statsQuery.data} />
            <IndexingJobsTable jobs={indexingJobsQuery.data ?? []} />
          </div>
        ) : (
          <EmptyState
            title="Sem Knowledge Bases"
            description="Crie a primeira base quando a organizacao estiver pronta para indexar documentos juridicos."
          />
        )}
      </div>
    </AppShell>
  );
}
