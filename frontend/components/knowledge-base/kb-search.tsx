import { SourcesList } from "@/components/knowledge-base/sources-list";
import { ModuleStateCard } from "@/components/shared/module-state-card";

export function KBSearch() {
  return (
    <div className="space-y-4">
      <ModuleStateCard
        title="KB search"
        status="active"
        description="Pesquisa com fontes e scores já prevista para a camada real."
        bullets={[
          "Search e ask partilham contratos de retrieval.",
          "A UI mostrará fontes e confiança sem inventar respostas.",
        ]}
      />
      <SourcesList retrievalMethod="textual_fallback" confidence="low" fallbackUsed fallbackReason="embeddings_not_prepared" />
    </div>
  );
}
