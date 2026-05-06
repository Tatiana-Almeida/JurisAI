import type { RetrievalSource } from "@/types/knowledge-base";

type SourcesListProps = {
  sources?: RetrievalSource[];
  retrievalMethod?: string;
  confidence?: string | null;
  fallbackUsed?: boolean;
  fallbackReason?: string | null;
};

export function SourcesList({
  sources = [],
  retrievalMethod,
  confidence,
  fallbackUsed,
  fallbackReason,
}: SourcesListProps) {
  return (
    <div className="space-y-4 rounded-[1.75rem] border border-border/60 bg-background/75 p-5">
      <div className="flex flex-wrap gap-3 text-xs text-muted-foreground">
        <span>retrieval_method: {retrievalMethod ?? "n/a"}</span>
        <span>confidence: {confidence ?? "n/a"}</span>
        <span>fallback_used: {String(Boolean(fallbackUsed))}</span>
        <span>fallback_reason: {fallbackReason ?? "n/a"}</span>
      </div>
      <div className="space-y-3">
        {sources.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Sources list preparada. Os resultados reais entram na próxima fase.
          </p>
        ) : (
          sources.map((source, index) => (
            <div key={`${source.title}-${index}`} className="rounded-2xl border border-border/60 p-4">
              <h4 className="font-medium">{source.title}</h4>
              <p className="mt-2 text-sm text-muted-foreground">{source.excerpt}</p>
              <div className="mt-3 flex flex-wrap gap-3 text-xs text-muted-foreground">
                <span>final_score: {source.final_score ?? "n/a"}</span>
                <span>text_score: {source.text_score ?? "n/a"}</span>
                <span>embedding_score: {source.embedding_score ?? "n/a"}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
