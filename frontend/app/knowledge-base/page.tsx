import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { KBAsk } from "@/components/knowledge-base/kb-ask";
import { KBList } from "@/components/knowledge-base/kb-list";
import { KBSearch } from "@/components/knowledge-base/kb-search";
import { KBStats } from "@/components/knowledge-base/kb-stats";
import { IndexingJobsTable } from "@/components/knowledge-base/indexing-jobs-table";
import { RAGSettingsPanel } from "@/components/knowledge-base/rag-settings-panel";

export default function KnowledgeBasePage() {
  return (
    <AppShell>
      <div className="space-y-8">
        <PageHeader
          title="Knowledge Base"
          description="Área preparada para ask com fontes, retrieval transparency, indexing jobs e settings de RAG por tenant."
        />
        <div className="grid gap-4 xl:grid-cols-2">
          <KBList />
          <KBStats />
          <KBSearch />
          <KBAsk />
          <IndexingJobsTable />
          <RAGSettingsPanel />
        </div>
      </div>
    </AppShell>
  );
}
