import type { OCRPageResult } from "@/types/ocr";
import { EmptyState } from "@/components/shared/empty-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type PageResultsTableProps = {
  pages: OCRPageResult[];
};

export function PageResultsTable({ pages }: PageResultsTableProps) {
  if (pages.length === 0) {
    return (
      <EmptyState
        title="Sem resultados por página"
        description="Os resultados page-level de OCR aparecem aqui quando o tenant tiver store_page_level_ocr ativo."
      />
    );
  }

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Resultados por página</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {pages.map((page) => (
          <div key={page.id} className="rounded-2xl border border-border/60 p-4 text-sm">
            <div className="font-medium">Página {page.page_number}</div>
            <div className="mt-2 text-muted-foreground">{page.extracted_text?.slice(0, 400) || "Sem texto"}</div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
