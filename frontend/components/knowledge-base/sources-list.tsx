import type { RetrievalSource } from "@/types/knowledge-base";
import { EmptyState } from "@/components/shared/empty-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type SourcesListProps = {
  sources: RetrievalSource[];
};

export function SourcesList({ sources }: SourcesListProps) {
  if (sources.length === 0) {
    return (
      <EmptyState
        title="Sem fontes ainda"
        description="As fontes RAG aparecem aqui quando houver uma pergunta respondida pela Knowledge Base."
      />
    );
  }

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Fontes e confiança</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {sources.map((source, index) => (
          <div key={`${source.title}-${index}`} className="rounded-2xl border border-border/60 p-4 text-sm">
            <div className="font-medium">{source.title ?? `Fonte ${index + 1}`}</div>
            <div className="mt-1 text-muted-foreground">{source.excerpt ?? "Sem excerto."}</div>
            <div className="mt-2 text-xs text-muted-foreground">
              final_score={source.final_score ?? "n/a"} · text_score={source.text_score ?? "n/a"} · embedding_score={source.embedding_score ?? "n/a"} · retrieval_method={source.retrieval_method ?? "n/a"} · confidence={source.confidence ?? "n/a"} · fallback_used={String(source.fallback_used ?? false)}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
