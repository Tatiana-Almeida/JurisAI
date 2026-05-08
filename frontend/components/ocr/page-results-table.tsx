import type { OCRPageResult } from "@/types/ocr";
import { EmptyState } from "@/components/shared/empty-state";
import { OCRStatusBadge } from "@/components/ocr/ocr-status-badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type PageResultsTableProps = {
  pages: OCRPageResult[];
};

export function PageResultsTable({ pages }: PageResultsTableProps) {
  if (pages.length === 0) {
    return (
      <EmptyState
        title="Sem resultados por pagina"
        description="Os resultados page-level de OCR aparecem aqui quando o tenant tiver store_page_level_ocr ativo."
      />
    );
  }

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Resultados por pagina</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {pages.map((page) => (
          <details key={page.id} className="rounded-2xl border border-border/60 p-4 text-sm">
            <summary className="flex cursor-pointer list-none flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <span className="font-medium">Pagina {page.page_number}</span>
                <OCRStatusBadge status={page.status ?? "pending"} />
              </div>
              <div className="text-xs text-muted-foreground">
                confidence: {String(page.metadata?.confidence ?? "n/d")} · {page.created_at ?? "sem data"}
              </div>
            </summary>
            <div className="mt-3 space-y-3">
              {page.error_message ? (
                <p className="rounded-xl border border-destructive/20 bg-destructive/10 p-3 text-destructive">
                  {page.error_message}
                </p>
              ) : null}
              <div className="rounded-xl border border-border/60 p-3 text-muted-foreground">
                {page.extracted_text?.trim() || "Sem texto extraido para esta pagina."}
              </div>
            </div>
          </details>
        ))}
      </CardContent>
    </Card>
  );
}
