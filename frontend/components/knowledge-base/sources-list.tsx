import type { SourceItem } from "@/types/knowledge-base";
import { EmptyState } from "@/components/shared/empty-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type SourcesListProps = {
  sources: SourceItem[];
  confidence?: string | number | null;
  retrievalMethod?: string;
  fallbackUsed?: boolean;
  fallbackReason?: string;
};

export function SourcesList({
  sources,
  confidence,
  retrievalMethod,
  fallbackUsed,
  fallbackReason,
}: SourcesListProps) {
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
        <CardTitle>Fontes e confianca</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="rounded-2xl border border-border/60 p-3 text-xs text-muted-foreground">
          confidence={String(confidence ?? "n/d")} · retrieval_method={retrievalMethod ?? "n/d"} · fallback_used={String(
            fallbackUsed ?? false,
          )} {fallbackReason ? `· fallback_reason=${fallbackReason}` : ""}
        </div>
        {sources.map((source, index) => (
          <div
            key={`${source.document_id ?? source.title ?? "source"}-${index}`}
            className="rounded-2xl border border-border/60 p-4 text-sm"
          >
            <div className="font-medium">{source.title ?? `Fonte ${index + 1}`}</div>
            <div className="mt-1 text-muted-foreground">{source.excerpt ?? "Sem excerto."}</div>
            <div className="mt-2 text-xs text-muted-foreground">
              documento={source.document_id ?? "n/d"} · final_score={String(source.final_score ?? "n/d")} ·
              text_score={String(source.text_score ?? "n/d")} · embedding_score={String(
                source.embedding_score ?? "n/d",
              )} · retrieval_method={source.retrieval_method ?? retrievalMethod ?? "n/d"}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
