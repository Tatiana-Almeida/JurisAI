import { ModuleStateCard } from "@/components/shared/module-state-card";

export function RAGSettingsPanel() {
  return (
    <ModuleStateCard
      title="RAG settings"
      status="active"
      description="Painel base para retrieval_mode, provider, governança e limites por tenant."
      bullets={[
        "local-hash-v1 será exposto como fundação, não como semântica avançada.",
        "Opt-in para embeddings externos continua explícito.",
      ]}
    />
  );
}
