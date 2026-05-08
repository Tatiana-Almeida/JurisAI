import type { OCRResult } from "@/types/ocr";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type OCRResultCardProps = {
  result: OCRResult;
  isApplying?: boolean;
  onApply?: () => void;
  onViewPages?: () => void;
  onSendToKnowledgeBase?: () => void;
};

function getConfidence(result: OCRResult) {
  return result.metadata?.confidence ?? "n/d";
}

export function OCRResultCard({
  result,
  isApplying = false,
  onApply,
  onViewPages,
  onSendToKnowledgeBase,
}: OCRResultCardProps) {
  const pagesProcessed = result.metadata?.pages_processed;
  const pagesFailed = result.metadata?.pages_failed;
  const totalPages = result.metadata?.total_pages_detected;
  const pagesLimitApplied = Boolean(result.metadata?.pages_limit_applied);
  const outputTruncated = Boolean(result.metadata?.output_truncated);

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Resultado OCR {result.id.slice(0, 8)}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid gap-3 text-sm text-muted-foreground md:grid-cols-2">
          <div>Caracteres extraidos: {result.char_count ?? 0}</div>
          <div>Confianca: {String(getConfidence(result))}</div>
          <div>Paginas processadas: {pagesProcessed ?? "n/d"}</div>
          <div>Paginas falhadas: {pagesFailed ?? "n/d"}</div>
          <div>Total de paginas detetadas: {totalPages ?? "n/d"}</div>
          <div>Documento: {result.document_id ?? result.document ?? "n/d"}</div>
        </div>

        {pagesLimitApplied ? (
          <div className="rounded-2xl border border-amber-300/40 bg-amber-500/10 p-3 text-sm text-amber-900 dark:text-amber-200">
            O limite de paginas do tenant foi aplicado neste OCR.
          </div>
        ) : null}
        {outputTruncated ? (
          <div className="rounded-2xl border border-amber-300/40 bg-amber-500/10 p-3 text-sm text-amber-900 dark:text-amber-200">
            O output foi truncado para respeitar o maximo de caracteres permitido pelo tenant.
          </div>
        ) : null}

        <details className="rounded-2xl border border-border/60 p-4 text-sm">
          <summary className="cursor-pointer font-medium">Ver texto extraido</summary>
          <div className="mt-3 max-h-72 overflow-auto whitespace-pre-wrap text-muted-foreground">
            {result.extracted_text?.trim() || "Sem texto extraido."}
          </div>
        </details>

        <div className="flex flex-wrap gap-3">
          <Button type="button" variant="outline" onClick={onApply} disabled={isApplying}>
            {isApplying ? "A aplicar..." : "Aplicar ao documento"}
          </Button>
          <Button type="button" variant="outline" onClick={onViewPages}>
            Ver paginas
          </Button>
          {onSendToKnowledgeBase ? (
            <Button type="button" variant="secondary" onClick={onSendToKnowledgeBase}>
              Enviar para Knowledge Base
            </Button>
          ) : null}
        </div>
      </CardContent>
    </Card>
  );
}
