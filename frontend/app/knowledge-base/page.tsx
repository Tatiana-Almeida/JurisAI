"use client";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { KBAsk } from "@/components/knowledge-base/kb-ask";
import { KBList } from "@/components/knowledge-base/kb-list";
import { RAGSettingsPanel } from "@/components/knowledge-base/rag-settings-panel";
import { SourcesList } from "@/components/knowledge-base/sources-list";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { ModuleErrorState } from "@/components/shared/module-error-state";
import {
  useKnowledgeBases,
  useRAGSettings,
  useRetrievalQueries,
} from "@/hooks/use-jurisai-queries";

export default function KnowledgeBasePage() {
  const knowledgeBasesQuery = useKnowledgeBases();
  const settingsQuery = useRAGSettings();
  const queriesQuery = useRetrievalQueries();
  const firstBase = knowledgeBasesQuery.data?.[0];
  const latestQuery = queriesQuery.data?.[0];

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
          description="Confirme autenticação, organização ativa e endpoints de RAG."
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Knowledge Base"
          description="Busca e perguntas com fontes, confiança, retrieval method e alerta honesto sobre local-hash-v1."
        />
        <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
          <KBList knowledgeBases={knowledgeBasesQuery.data ?? []} />
          <RAGSettingsPanel settings={settingsQuery.data} />
        </div>
        <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
          <KBAsk knowledgeBaseId={firstBase?.id} />
          <SourcesList sources={latestQuery?.sources_payload ?? []} />
        </div>
      </div>
    </AppShell>
  );
}
