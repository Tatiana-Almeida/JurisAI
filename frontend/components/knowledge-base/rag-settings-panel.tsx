import type { RAGSettings } from "@/types/knowledge-base";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type RAGSettingsPanelProps = {
  settings?: RAGSettings;
};

export function RAGSettingsPanel({ settings }: RAGSettingsPanelProps) {
  const usesLocalHash = !settings?.embedding_provider || settings.embedding_provider === "local";

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>RAG settings</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 text-sm text-muted-foreground">
        <div>retrieval_mode: {settings?.retrieval_mode ?? "textual"}</div>
        <div>embedding_provider: {settings?.embedding_provider ?? "local"}</div>
        <div>embedding_model: {settings?.embedding_model ?? "local-hash-v1"}</div>
        <div>max_sources_per_answer: {settings?.max_sources_per_answer ?? 5}</div>
        <div>min_confidence_threshold: {settings?.min_confidence_threshold ?? "low"}</div>
        {usesLocalHash ? (
          <div className="rounded-2xl border border-amber-300/40 bg-amber-500/10 p-3 text-amber-900 dark:text-amber-200">
            O modo local-hash-v1 valida o pipeline de retrieval sem enviar dados para fora, mas não é embedding semântico avançado.
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
